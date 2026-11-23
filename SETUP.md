# Tibbo Stats: set-up

**Done:** a key is built into the page (Google Cloud project "Tibbo Stats" on the main account, key "Tibbo Stats website", locked to https://divtrader.github.io/* and YouTube Data API v3). There is no Settings section; the page always uses the built-in key and @tibboshow. Just open it and add it to your home screen (step 3). If the key ever stops working, a new one is made with step 1 and swapped into SITE_KEY in index.html.


Tibbo Stats reads your channel live from YouTube's official API every time you open it. It's free:
YouTube allows 10,000 "units" a day and one refresh uses about 3.

## 1. Get a free YouTube API key (on your computer)
1. Go to **console.cloud.google.com** and sign in with your Google account.
2. At the top, click the project picker → **New project** → name it `Tibbo Stats` → **Create**. Make sure it's selected.
3. Left menu: **APIs & Services → Library**. Search **YouTube Data API v3**, open it, click **Enable**.
4. Left menu: **APIs & Services → Credentials → + Create credentials → API key**. Copy the key (it starts with `AIza`).
5. Click **Edit API key** (or the key's name) to lock it down. This keeps it safe even though the page is public:
   - *Application restrictions*: **Websites** → **Add** → `https://divtrader.github.io/*`
   - *API restrictions*: **Restrict key** → tick **YouTube Data API v3**
   - **Save**. (It can take a few minutes to start working.)

## 2. Put the key into Tibbo Stats (on your iPhone)
1. Open **https://divtrader.github.io/tibbo-stats/** in **Safari**.
2. Tap **Settings**, paste the key, check the channel says `@tibboshow`, tap **Save and load**.
   The key is saved on your phone only.

## 3. Add it to your home screen with the Tibbo icon
1. Still in Safari, tap the **Share** button (square with an arrow pointing up).
2. Scroll down, tap **Add to Home Screen**.
3. The name is already **Tibbo Stats** and the icon is Tibbo's face. Tap **Add**.

Open it from the home screen any time: it loads the latest numbers straight from YouTube.
"+ since yesterday" figures and the trend line start the day after your first visit (the phone keeps a small history).

**Preview:** add `#demo` to the address to see the layout with labelled sample numbers.

## Who's watching (countries, watch time, sources)
Shown automatically, no sign-in. A GitHub Actions updater (.github/workflows/analytics.yml, every 3 hours, free,
no Claude involved) runs scripts/update_analytics.py, which reads the Tibbo channel's YouTube Analytics (read-only)
and saves the totals to analytics.json; the page reads that file.
- Permission: given once on 23 Nov 2026 by the channel owner for the Tibbo brand channel (Google sign-in app
  "Tibbo Stats", in production, desktop client "Tibbo Stats updater"). Keys live only in the repository secrets
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (and a private copy in ~/.config/tibbo-stats on the Mac).
- Remove access any time at myaccount.google.com/permissions (pick the Tibbo channel).
- Only channel totals are saved (countries, sources, devices, per-video watch %), never anything about a viewer.
- YouTube adds analytics about 2-3 days after the views.
