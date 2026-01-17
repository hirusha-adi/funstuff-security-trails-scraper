import requests
import json
import time
import random

# ========== CONFIGURATION ==========
START_PAGE = 1
END_PAGE = 100
DOMAIN = "etienne.ns.cloudflare.com"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
COOKIE = "cf_clearance=QPwYMsxKw.LnihJOi9W2H2.7NeEcrYutSx8P5T5l29s-1768681970-1.2.1.1-mSwZMCOlssRmJE3H_eio1o4xig2TNBSAAhZmZiKUir_KYGI90I0x3sRHJue01TrARfY4EII4lFauzsSFw0ulxsf16ZrHzeMdARFBG_cSgFYF85.dRRww9Vfq2bjMJ7.Ss2LRYZS27nRZNEomBKku6QCVngtxgoxNrgF1dNBTQKn9Ys.Y2Ntwexpn.6VKjbrjGyhtYkKt5RdTWkf4iE6K2x08bVV7K_a.dZZfDdKgK3zMFaixqhxLUfJ3IjDjmArL; _ga=GA1.2.174900909.1767520511; securitytrails_session=ogDXTjYEDPWeLyY8BzkrF8cHSYf1nVWp0rS2tepR; _gid=GA1.2.1141376254.1768679958; csrf=tn2_XMXO5Le41NzmKXIKkvtB; securitytrails_asn_preload=1; SecurityTrails=Fe26.2*1*850fc4cf9c9893eb8a609493bd55f0a3c3fc205f25406d59a2a241cf45fdd56f*3MNgJZpriKCNPLHhT2E5iw*SzUEKkWSHHVdILcRqxiWrNYZN0seg8rTaRjtpgGfywU16eXGWAylluVpE6ki7XmTq6vNO04dEVMxtooj2o1O3ANwivv3MJd2p_l2eXrfTGco6FfYcldhgps-G3gOvLYpZih3JOOylYqZnizunwLjV6mvCIPFne222HBBuHLh4-5tRGdBMa-0aYHZQ6QiaceTqKA_WMEHxzBlMHZx7L66-xcXvbiDNsoQSOq8-CpS-QR9HB74X0xbpt5Y7e9TcMIYL5-zpKRY5w8udRJeC9n86obz5X7Q7B1-q6NN6bnygH-R5Whv2kZoR9PPFxIsm78AOY6uS2kigC273J4rR37GWnOPHu5_S2aqNPUn_RM2AhPwUwI_NcrfyEUZYsCj0S6wEGSS_jkyXlvML3Isx-tKXey-KAdow5c6D1Rl3dblurxRUosX3WuB8w1EEaW9gkjtNPPue1MsP45omPI5WiTeewTbNUFNm6ivQR0sJjSaElqgay2fa8adwAsWY_nDe53XHR6KZn0CzL_-bWed2jQrVTDBJWuRVMElbxSNvCZfbs3i6wD2d2OfSkxHWnHAFnVt6s48Gc18tR4HwpypCXIgfoTukPiphgEINhDIZaVB9BrdD_7gJMswmXxaL1mBy4GjHzzx0A70kg-XUSv2QXjsarWCbmVkU2xlbcqZLOdjwdSWJWozf7euuCvbaMYLRCqdEQQo5iWJlnMUfV3d_tt7E8qDheEHt1Nois76mdr2Ez7AKK1bD_YDFyyenhAxXs8HBuI1CtK3lK6Owo3qeC1feImIZbt3_DIix15suBhVgIeSQcsgdvCz9el1_zFd59KlComJtgjf7BrMK34AY6rGtSQm4OYg1iq_fP5_WCxr_tKzDrj1EUp4JQOLIp68X-lpvxiyS7QJOopJUVAVzDRa3kHVXGJOk0nfCzh5DWj6kPi2Tner6F-VpquY96mXwQziF6iJqEgObEwHGmAcEeN0lGZjlFkTpbVmxIpbt14HDKx65jLK2rPSWvnOv4soT6-3*1769891616091*b9180f5ca3d3d04e71c1ba7a3d48a76bb8ad8c4c2180feb46a37e68539cc6a91*9c9WtysY-h-qXR8pX7cWyurKB5ohNH_j3fRkOxDx7pg~2"
SLEEP_TIME_RANGE = (4, 8)  # seconds
# ===================================

for page_number in range(START_PAGE, END_PAGE + 1):

    url = f"https://securitytrails.com/_next/data/0afcffcf/list/ns/{DOMAIN}.json"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": f"https://securitytrails.com/list/ns/{DOMAIN}?page={page_number}",
        "x-nextjs-data": "1",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Cookie": COOKIE
    }
    params = {
        "page": page_number,
        "ns": DOMAIN
    }

    _t = random.randint(*SLEEP_TIME_RANGE)
    print(f"+ Sleeping for {_t} seconds before requesting page {page_number}...")
    time.sleep(_t)

    # === Make the request ===
    response = requests.get(url, headers=headers, params=params)

    # === Check if the response is JSON ===
    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"! Page {page_number} did not return JSON. Status code: {response.status_code}")
    else:
        filename = f"{DOMAIN}_{page_number}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"+ Successfully saved results from page {page_number} to {filename}.")
