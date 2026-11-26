"""Fetch Tibbo's YouTube Analytics (read-only) and save them as analytics.json for the dashboard.

Runs on GitHub Actions every few hours (no Claude involved). Needs three repository secrets:
YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (a one-time read-only permission from the channel owner,
for the Tibbo brand channel). Only channel totals are saved: no information about any individual viewer.
"""
import datetime as dt
import json
import os
import urllib.parse
import urllib.request

START = "2026-11-01"      # the channel's first month
CF_ZONE = "9afa901dadb047013f4aa571d15b8ab5"   # tibboshow.com on Cloudflare (a zone ID is not a secret)


def access_token():
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))["access_token"]


def report(token, **params):
    q = {"ids": "channel==MINE", "startDate": START, "endDate": dt.date.today().isoformat(), **params}
    req = urllib.request.Request("https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q),
                                 headers={"Authorization": "Bearer " + token})
    return json.load(urllib.request.urlopen(req)).get("rows") or []


def website():
    """Daily visitors, page views and countries for tibboshow.com, from Cloudflare's own counts (nothing runs on the
    website itself, so it stays cookie- and tracking-free). Needs the repository secret CF_API_TOKEN: a read-only
    Cloudflare token (Zone > Analytics > Read, for tibboshow.com only) made by the owner. None without it."""
    token = os.environ.get("CF_API_TOKEN")
    if not token:
        return None
    since = (dt.date.today() - dt.timedelta(days=29)).isoformat()
    q = """query($zone: String!, $since: Date!) { viewer { zones(filter: {zoneTag: $zone}) {
      httpRequests1dGroups(limit: 31, orderBy: [date_ASC], filter: {date_geq: $since}) {
        dimensions { date } uniq { uniques } sum { pageViews countryMap { clientCountryName requests } } } } } }"""
    body = json.dumps({"query": q, "variables": {"zone": CF_ZONE, "since": since}}).encode()
    req = urllib.request.Request("https://api.cloudflare.com/client/v4/graphql", body,
                                 headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req))
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    zones = data["data"]["viewer"]["zones"]
    groups = zones[0]["httpRequests1dGroups"] if zones else []
    countries = {}
    for g in groups:
        for c in g["sum"]["countryMap"]:
            countries[c["clientCountryName"]] = countries.get(c["clientCountryName"], 0) + c["requests"]
    daily = [[g["dimensions"]["date"], g["uniq"]["uniques"], g["sum"]["pageViews"]] for g in groups]
    return {"since": since, "visitors": sum(d[1] for d in daily), "pageviews": sum(d[2] for d in daily),
            "daily": daily, "countries": sorted(countries.items(), key=lambda kv: -kv[1])[:10]}


def main():
    tok = access_token()
    out = {
        "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "since": START,
        "totals": (report(tok, metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage") or [[0, 0, 0, 0]])[0],
        "countries": report(tok, dimensions="country", metrics="views", sort="-views", maxResults=10),
        "sources": report(tok, dimensions="insightTrafficSourceType", metrics="views", sort="-views"),
        "devices": report(tok, dimensions="deviceType", metrics="views", sort="-views"),
        "products": report(tok, dimensions="youtubeProduct", metrics="views", sort="-views"),
        "videos": report(tok, dimensions="video", metrics="views,averageViewPercentage,averageViewDuration", sort="-views", maxResults=25),
        "daily": report(tok, dimensions="day", metrics="views", sort="day"),
    }
    path0 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analytics.json")
    try:
        site = website()
    except Exception as e:                       # a website hiccup never stops the YouTube numbers
        print("Website stats skipped:", e)
        site = (json.load(open(path0)) if os.path.exists(path0) else {}).get("website")
    if site is not None:
        out["website"] = site
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analytics.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    if {k: v for k, v in old.items() if k != "updated"} == {k: v for k, v in out.items() if k != "updated"} and old:
        print("No change")
        return
    json.dump(out, open(path, "w"), indent=1)
    print("Saved", path)


if __name__ == "__main__":
    main()
