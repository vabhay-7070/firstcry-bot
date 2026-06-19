import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import subprocess

# ---- CONFIG ----
URL = "https://www.firstcry.com/hot-20wheels/0/0/113?q=as_hot%20wheel&asid=48299"
STATE_FILE = "seen_products.json"

POLL_SECONDS = 120          # check the page every 2 minutes
MAX_RUNTIME_SECONDS = 5 * 3600 + 45 * 60   # run for 5h45m, then hand off to the next scheduled run
CHECKPOINT_EVERY = 8        # commit state at least every ~16 min, even with nothing new

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def load_seen():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f).get("ids", []))
    return set()


def save_seen(ids):
    with open(STATE_FILE, "w") as f:
        json.dump({"ids": sorted(ids)}, f, indent=2)


def send_discord(product):
    embed = {
        "title": product["name"][:256],
        "url": product["url"],
        "description": f"Price: \u20B9{product['price']}\nStock: {product['stock']}",
        "color": 0x57F287,
    }
    if product["image"]:
        embed["image"] = {"url": product["image"]}

    payload = {
        "content": "\U0001F195 New Hot Wheels listing!",
        "embeds": [embed],
    }

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=20)
        if r.status_code not in (200, 204):
            print("Discord send failed:", r.status_code, r.text)
    except Exception as e:
        print("Discord send error:", e)


def git_commit_and_push(message):
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=False)
        subprocess.run(
            ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
            check=False,
        )
        subprocess.run(["git", "add", STATE_FILE], check=False)
        result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(["git", "pull", "--rebase"], check=False)
            push = subprocess.run(["git", "push"], capture_output=True, text=True)
            if push.returncode != 0:
                print("Git push failed:", push.stderr)
    except Exception as e:
        print("Git commit/push error:", e)


def scrape():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    products = {}
    handled_on_page = set()

    for a in soup.find_all("a", href=True):
        m = re.search(r"/(\d+)/product-detail", a["href"])
        if not m:
            continue
        pid = m.group(1)
        if pid in handled_on_page:
            continue
        handled_on_page.add(pid)

        # Walk up the DOM to find the enclosing product card
        card = a
        for _ in range(6):
            if card.parent is None:
                break
            card = card.parent
            text_so_far = card.get_text(" ", strip=True)
            if card.find("img") and re.search(r"\d{2,5}\.\d{1,2}", text_so_far):
                break

        img_tag = card.find("img")
        image = img_tag.get("src") if img_tag else None
        name = (img_tag.get("alt") or "").strip() if img_tag else ""
        if not name:
            name = a.get_text(strip=True) or f"Product {pid}"

        text_blob = card.get_text(" ", strip=True)

        price_match = re.search(r"(\d{2,5}\.\d{1,2})", text_blob)
        price = price_match.group(1) if price_match else "N/A"

        stock_match = re.search(r"(\d+)\s*Left", text_blob, re.IGNORECASE)
        stock = f"Only {stock_match.group(1)} left" if stock_match else "In stock"

        full_url = a["href"] if a["href"].startswith("http") else "https://www.firstcry.com" + a["href"]

        if pid not in products:
            products[pid] = {
                "name": name,
                "price": price,
                "stock": stock,
                "image": image,
                "url": full_url,
            }

    return products


def main():
    seen = load_seen()
    start = time.time()
    iteration = 0

    while time.time() - start < MAX_RUNTIME_SECONDS:
        iteration += 1
        try:
            products = scrape()
        except Exception as e:
            print(f"[{iteration}] Scrape error:", e)
            time.sleep(POLL_SECONDS)
            continue

        if not products:
            print(f"[{iteration}] WARNING: 0 products parsed. Page structure may have changed.")
        else:
            new_ids = [pid for pid in products if pid not in seen]

            for pid in new_ids:
                send_discord(products[pid])
                time.sleep(1)

            if new_ids:
                seen = seen.union(products.keys())
                save_seen(seen)
                git_commit_and_push(f"New listing(s) detected: {len(new_ids)}")
            elif iteration % CHECKPOINT_EVERY == 0:
                seen = seen.union(products.keys())
                save_seen(seen)
                git_commit_and_push("Checkpoint (no changes)")

            print(f"[{iteration}] Checked {len(products)} products, {len(new_ids)} new.")

        time.sleep(POLL_SECONDS)

    # Final safety flush before exiting so the next scheduled run picks up cleanly
    save_seen(seen)
    git_commit_and_push("Final checkpoint before run ends")
    print("Loop window ending — next scheduled run will pick up from here.")


if __name__ == "__main__":
    main()
