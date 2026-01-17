import requests
import json
import time
import random

# ========== CONFIGURATION ==========
START_PAGE = 1
END_PAGE = 100
QUERY_NAMESERVER = "etienne.ns.cloudflare.com"
URL = f"https://securitytrails.com/_next/data/0afcffcf/list/ns/{QUERY_NAMESERVER}.json"
USER_AGENT = "XXXXX"
COOKIE = "XXXXX"
SLEEP_TIME_RANGE = (4, 8)  # seconds
# ===================================

for page_number in range(START_PAGE, END_PAGE + 1):

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": f"https://securitytrails.com/list/ns/{QUERY_NAMESERVER}?page={page_number}",
        "x-nextjs-data": "1",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Cookie": COOKIE
    }
    params = {
        "page": page_number,
        "ns": QUERY_NAMESERVER
    }

    _t = random.randint(*SLEEP_TIME_RANGE)
    print(f"+ Sleeping for {_t} seconds before requesting page {page_number}...")
    time.sleep(_t)

    # === Make the request ===
    response = requests.get(URL, headers=headers, params=params)

    # === Check if the response is JSON ===
    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"! Page {page_number} did not return JSON. Status code: {response.status_code}")
    else:
        filename = f"{QUERY_NAMESERVER}_{page_number}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"+ Successfully saved results from page {page_number} to {filename}.")
