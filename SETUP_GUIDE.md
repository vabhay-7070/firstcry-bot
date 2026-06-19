# Setting Up Your Hot Wheels Alert Bot — Full Walkthrough

No coding involved. Just clicking through screens. Do these parts in
order. Takes about 15-20 minutes the first time.

---

## PART 1: Get a Discord Webhook

A "webhook" is just a private web address that, when something is
sent to it, posts a message into a specific Discord channel. You
need one so the bot has somewhere to send alerts.

1. Open the Discord app (or discord.com in a browser). If you don't
   have an account, sign up first — it's free, just needs an email.
2. On the left side, you'll see a list of servers (circular icons).
   Click the **+** icon at the bottom of that list → **Create My Own**
   → **For me and my friends** → give it any name, e.g. "Hot Wheels
   Alerts" → **Create**.
3. You'll land inside your new server. There's a channel called
   `#general` in the middle column. Hover over it, and a small gear
   icon (⚙️) will appear next to it — click that gear.
4. In the menu on the left of the screen that opens, click
   **Integrations**.
5. Click **Webhooks**, then click **New Webhook**.
6. A webhook named "Captain Hook" appears. Click on it.
7. You'll see a button labeled **Copy Webhook URL**. Click it.
8. Paste that URL somewhere safe for now (Notes app, anywhere) —
   it'll look like:
   `https://discord.com/api/webhooks/123456789/AbCdEfGhIjKlMnOpQrStUvWx`
9. That's it for Discord. Alerts will appear in that `#general`
   channel once everything's connected. Keep the Discord app on your
   phone so you get push notifications.

---

## PART 2: Get a GitHub Account

GitHub is where the bot's code will live, and where it'll run
automatically on a schedule — free, forever, no laptop needed.

1. Go to **github.com** in a browser (phone or computer, doesn't
   matter).
2. Click **Sign up**, enter an email, password, and username.
   Verify your email when it asks.

---

## PART 3: Create a New Repository (a project folder)

1. Once logged in, look for a **+** icon top-right (on desktop) or
   the menu (on mobile) → **New repository**.
   (Direct link: github.com/new)
2. **Repository name**: type `firstcry-bot`
3. Leave it set to **Public**.
4. Leave everything else as default.
5. Click the green **Create repository** button at the bottom.

---

## PART 4: Unzip the file I gave you

1. Find the `firstcry-bot.zip` file I sent (probably in your phone's
   Downloads or Files app).
2. Tap/click it.
   - **Phone (Android/iOS)**: tap it, your Files app should offer to
     "Extract" or "Unzip" it — tap that. It creates a folder called
     `firstcry-bot`.
   - **Windows**: right-click the zip → **Extract All** → Extract.
   - **Mac**: just double-click it.
3. Open that extracted `firstcry-bot` folder. You should see these
   items inside:
   - `scraper.py`
   - `requirements.txt`
   - `seen_products.json`
   - `README.md`
   - a folder called `.github` (it may be hidden by default — see
     note below)

> ⚠️ **Important about the `.github` folder**: folders starting with
> a dot are often hidden by your phone/computer's file browser. If
> you don't see it:
> - **Windows**: in File Explorer, go to View → tick "Hidden items"
> - **Mac**: in Finder, press `Cmd + Shift + .` (period) to reveal it
> - **Phone**: this step is genuinely easier to do on a laptop/desktop
>   if at all possible — phone file managers often can't show or
>   upload hidden folders properly. If you only have a phone, ask
>   someone to borrow a laptop for just this one step, or use a
>   library/cybercafe computer for 5 minutes.

---

## PART 5: Upload the Files to GitHub

1. On your new repository's page (from Part 3), click
   **Add file → Upload files**.
2. Open the extracted `firstcry-bot` folder from Part 4 in a separate
   window/file browser.
3. Select **everything inside** that folder (all files AND the
   `.github` folder) — not the outer `firstcry-bot` folder itself,
   just what's inside it.
4. Drag all of it into the gray upload box on the GitHub page (or
   click "choose your files" and select them all).
5. Scroll down, you'll see a box to describe the change — leave it as
   is.
6. Click the green **Commit changes** button.
7. Refresh the page — you should now see all your files listed,
   including a `.github` folder.

---

## PART 6: Add Your Webhook as a Secret

A "secret" is a hidden value GitHub stores safely — your code can use
it, but nobody browsing your repository can see it.

1. On your repository page, click the **Settings** tab (top menu,
   may need to tap the `...` menu on mobile to find it).
2. On the left sidebar, click **Secrets and variables** → **Actions**.
3. Click the green **New repository secret** button.
4. **Name**: type exactly `DISCORD_WEBHOOK_URL`
5. **Secret**: paste the webhook URL you copied in Part 1, step 8.
6. Click **Add secret**.

---

## PART 7: Run It for the First Time

1. Click the **Actions** tab on your repository (top menu).
2. On the left, click **FirstCry Hot Wheels Monitor**.
3. On the right, you'll see a button **Run workflow** (it may be
   inside a dropdown) → click it → click the green **Run workflow**
   button that appears.
4. Wait about 10-20 seconds, then refresh the page. You'll see a run
   appear with a yellow dot (running) that turns into either a green
   checkmark (success) or a red X (something failed).
5. Open Discord — you should see a wave of messages, one per product
   currently on the FirstCry page. This is expected and only happens
   on this first run, since the bot is "learning" what's already
   there.

---

## What Happens Next

You don't need to do anything else. The bot checks FirstCry every
**2 minutes**, continuously. Each run keeps polling for about
5 hours 45 minutes, then automatically hands off to a fresh run —
so there's only a small ~10-15 minute gap every 6 hours while that
handoff happens. You'll only get a Discord message when something
genuinely new shows up.

You'll also notice a lot of small automatic commits appearing in your
repository's history over time — that's normal, it's just the bot
saving its progress as it polls so it doesn't lose track or repeat
alerts.

## If Something Goes Wrong

- **Red X on the run**: click into that run → click the `check` step
  → it'll show an error message. Screenshot it and send it to me,
  I'll tell you the fix.
- **"0 products parsed" warning**: FirstCry changed their page
  layout. Send me that, I'll patch the script.
- **No messages at all in Discord**: double-check the secret name is
  exactly `DISCORD_WEBHOOK_URL` (capital letters, underscores) and
  that the webhook URL was pasted in full with no extra spaces.
