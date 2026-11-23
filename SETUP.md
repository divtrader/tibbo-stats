# Tibbo Stats: set-up (about 10 minutes, once)

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
