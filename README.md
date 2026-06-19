# FirstCry Hot Wheels New-Listing Bot

Checks the FirstCry Hot Wheels page every **2 minutes**, continuously.
When a product appears that wasn't there before, it sends you a
Discord message with the name, price, stock status, image, and a
link.

## 1. Create a Discord webhook (2 minutes)

1. Open Discord (or create a free account/server if you don't have one).
2. Go to the server/channel you want alerts in → click the gear icon
   next to the channel (or **Edit Channel**) → **Integrations** → **Webhooks**.
3. Click **New Webhook**, give it a name (e.g. "Hot Wheels Bot"), then
   click **Copy Webhook URL**. Save it — this is `DISCORD_WEBHOOK_URL`.
4. Install Discord on your phone and join that server if you haven't —
   that's where alerts will show up, with image previews.

## 2. Create the GitHub repo

1. Go to github.com → New repository → name it (e.g. `firstcry-bot`) →
   keep it **Public** (private also works, doesn't matter here) → Create.
2. Click **Add file → Upload files**, and drag in everything from this
   folder, including the `.github` folder — GitHub preserves the folder
   structure on upload. Commit.

## 3. Add your secret

1. In the repo: **Settings → Secrets and variables → Actions → New repository secret**.
2. Name: `DISCORD_WEBHOOK_URL`, Value: the URL from step 1.

## 4. Turn it on

1. Go to the **Actions** tab → you should see "FirstCry Hot Wheels Monitor".
2. Click it → **Run workflow** → Run. This tests it manually.
3. Check Discord — first run will likely message you for every product
   currently on the page (since nothing's "seen" yet). After that, it
   only messages you for genuinely new ones.
4. From here it checks every 2 minutes by itself, no laptop needed.
   Each run keeps polling for about 5h45m, then a fresh one
   automatically picks up — so there's only a small ~10-15 min gap
   every 6 hours while it hands off. Fully automatic either way.

## Notes

- You'll see a lot of small automatic commits in the repo's history
  (the bot checkpoints its progress as it polls). That's expected —
  it's how it remembers what it's already alerted you about.
- "Quantity" on the FirstCry listing page only shows up as an exact
  number when stock is low (e.g. "2 Left") — otherwise it just says
  "In stock". FirstCry doesn't publicly expose exact warehouse quantity
  for in-stock items, so the bot reports what's actually visible on the
  page.
- If a run ever reports "0 products parsed," FirstCry likely tweaked
  their page layout. Send me the Action's error log and I'll patch
  the scraper.
- Checking every 2 minutes nonstop is already fairly aggressive for a
  page that rarely changes. If FirstCry ever starts blocking the
  requests (you'll see errors in the Action logs, or it'll just stop
  finding new products), tell me and I'll back off the interval.
