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


def access_token():
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))["access_token"]


def report(token, **params):
    q = {"ids": "channel==MINE", "startDate": START, "endDate": dt.date.today().isoformat(), **params}
    req = urllib.request.Request("https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q),
                                 headers={"Authorization": "Bearer " + token})
    return json.load(urllib.request.urlopen(req)).get("rows") or []


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
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analytics.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    if {k: v for k, v in old.items() if k != "updated"} == {k: v for k, v in out.items() if k != "updated"} and old:
        print("No change")
        return
    json.dump(out, open(path, "w"), indent=1)
    print("Saved", path)


if __name__ == "__main__":
    main()
