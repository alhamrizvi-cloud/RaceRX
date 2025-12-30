#!/usr/bin/env python3
import requests
import argparse
import threading
import time
import sys

BANNER = r"""
 ______     ______     ______     ______     ______     __  __    
/\  == \   /\  __ \   /\  ___\   /\  ___\   /\  == \   /\_\_\_\   
\ \  __<   \ \  __ \  \ \ \____  \ \  __\   \ \  __<   \/_/\_\/_  
 \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_\ \_\   /\_\/\_\ 
  \/_/ /_/   \/_/\/_/   \/_____/   \/_____/   \/_/ /_/   \/_/\/_/ 
                                                                  
        RaceRx – Race Condition Testing Tool
        Bug Bounty | Security Research
        Tool By @alhamrizvii
"""

IMPORTANT_HEADERS = {
    "host",
    "cookie",
    "content-type",
    "authorization",
    "x-csrf-token",
    "csrf"
}

results = []

# ---------------- PARSING ---------------- #

def parse_raw_request(raw):
    headers = {}
    cookies = {}
    body = ""

    parts = raw.split("\n\n", 1)
    header_lines = parts[0].splitlines()

    for line in header_lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            if k.lower() == "cookie":
                for c in v.split(";"):
                    ck, cv = c.split("=", 1)
                    cookies[ck.strip()] = cv.strip()
            else:
                headers[k.strip()] = v.strip()

    if len(parts) == 2:
        body = parts[1].strip()

    return clean_headers(headers), cookies, body


def clean_headers(headers):
    return {
        k: v for k, v in headers.items()
        if k.lower() in IMPORTANT_HEADERS
    }

# ---------------- REQUEST ---------------- #

def send_request(session, args, req_id):
    try:
        r = session.request(
            method=args.method,
            url=args.url,
            headers=args.headers,
            cookies=args.cookies,
            data=args.data,
            timeout=8
        )
        print(f"[{req_id}] {r.status_code} | {len(r.content)} bytes")
        results.append(r.status_code)
    except Exception as e:
        print(f"[{req_id}] ERROR: {e}")

# ---------------- INPUT ---------------- #

def read_raw_request():
    print("[!] Paste RAW HTTP request (press Enter twice to finish):")
    lines = []
    empty = 0

    while True:
        line = input()
        if line == "":
            empty += 1
            if empty == 2:
                break
        else:
            empty = 0
        lines.append(line)

    return "\n".join(lines).strip()

def interactive_mode():
    print(BANNER)

    url = input("[?] Enter Target URL: ").strip()
    method = input("[?] HTTP Method (POST/GET) [POST]: ").strip() or "POST"

    raw = read_raw_request()

    headers, cookies, body = {}, {}, ""
    if raw:
        headers, cookies, body = parse_raw_request(raw)

    while True:
        try:
            threads = int(input("[?] Number of parallel requests [20]: ") or 20)
            break
        except ValueError:
            print("[!] Enter a valid number")

    return url, method, headers, cookies, body, threads

# ---------------- MAIN ---------------- #

def main():
    parser = argparse.ArgumentParser(
        description="RaceRx – Automated Race Condition Testing Tool"
    )

    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-X", "--method", default="POST", help="HTTP Method")
    parser.add_argument("-d", "--data", help="Request body")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Parallel requests")

    args = parser.parse_args()

    if not args.url:
        url, method, headers, cookies, body, threads = interactive_mode()
        args.url = url
        args.method = method
        args.headers = headers
        args.cookies = cookies
        args.data = body
        args.threads = threads
    else:
        args.headers = {}
        args.cookies = {}

    print("\n[+] Starting race condition test...\n")

    session = requests.Session()
    threads_list = []

    start = time.time()
    for i in range(args.threads):
        t = threading.Thread(target=send_request, args=(session, args, i + 1))
        threads_list.append(t)
        t.start()

    for t in threads_list:
        t.join()

    end = time.time()

    print(f"\n[✓] Completed in {round(end - start, 2)} seconds")

    if len(set(results)) > 1:
        print("[🔥] POSSIBLE RACE CONDITION DETECTED")
    else:
        print("[i] Responses consistent – likely safe")

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    main()
