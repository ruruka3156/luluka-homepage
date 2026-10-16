import json, os, re, sys
from datetime import datetime, timezone
import requests

PLAYER_ID = "2364291522"
PROFILE_URL = f"https://www.streetfighter.com/6/buckler/ja-jp/profile/{PLAYER_ID}"
OUT = "mr.json"

cookie = os.environ.get("BUCKLER_ID", "").strip()
if not cookie:
    print("BUCKLER_ID is missing", file=sys.stderr)
    sys.exit(2)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/154 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja-JP,ja;q=0.9,en;q=0.8",
    "Referer": "https://www.streetfighter.com/6/buckler/ja-jp/",
}
cookies = {"buckler_id": cookie}

r = requests.get(PROFILE_URL, headers=headers, cookies=cookies, timeout=30)
r.raise_for_status()

m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
if not m:
    raise RuntimeError("__NEXT_DATA__ was not found; Buckler page structure may have changed.")

payload = json.loads(m.group(1))
pp = payload.get("props", {}).get("pageProps", {})
banner = pp.get("fighter_banner_info", {})
league = banner.get("favorite_character_league_info", {})
mr = league.get("master_rating")

if not isinstance(mr, int) or mr < 0:
    raise RuntimeError(f"Could not read a valid MR: {mr!r}")

old = {}
try:
    with open(OUT, encoding="utf-8") as f:
        old = json.load(f)
except FileNotFoundError:
    pass

best = max(mr, int(old.get("best", mr)))
data = {
    "mr": mr,
    "best": best,
    "goal": 2000,
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "source": "Capcom Buckler profile"
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False))
