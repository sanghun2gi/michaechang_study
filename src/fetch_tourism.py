#!/usr/bin/env python3
"""
전국관광지정보 수집기
공공데이터포털 tn_pubr_public_trrsrt_api 활용
Usage: python fetch_tourism.py
"""

import requests
import csv
import time

KEY = "f1e6ea23642989ef0eda1a98801e0ec360716cac6649b48713ccb09d1ad6ba3a"
URL = "http://api.data.go.kr/openapi/tn_pubr_public_trrsrt_api"

OUTPUT_FILE = "전국관광지정보.csv"


def fetch_all() -> list:
    all_data = []
    page = 1

    while True:
        r = requests.get(URL, params={
            "serviceKey": KEY,
            "pageNo": page,
            "numOfRows": 1000,
            "type": "json"
        }).json()

        items = r["response"]["body"]["items"]["item"]
        all_data.extend(items)
        total = r["response"]["body"]["totalCount"]
        print(f"수집: {len(all_data)}/{total}")

        if len(all_data) >= total:
            break
        page += 1
        time.sleep(0.3)

    return all_data


def save_csv(data: list, path: str):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"저장 완료: {path} ({len(data)}건)")


if __name__ == "__main__":
    data = fetch_all()
    save_csv(data, OUTPUT_FILE)
