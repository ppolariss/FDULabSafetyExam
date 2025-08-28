#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
import requests

URL = "https://lsem.fudan.edu.cn/fd_aqks_new/examProgress/examOnline/addStudentStudy"

def parse_args():
    p = argparse.ArgumentParser(description="POST addStudentStudy with id & readTime")
    # p.add_argument("--id", default="2025072534212364", help="id 字段")
    p.add_argument("--readTime", default="-184000", help="readTime 字段（字符串即可）")
    p.add_argument(
        "--jsessionid",
        required=False,
        help="JSESSIONID 的值（不要带前缀），例如 FA4862...",
    )
    p.add_argument("--timeout", type=float, default=15.0, help="请求超时秒数")
    return p.parse_args()


def main():
    args = parse_args()
    ids = [
        2025072534212327,
        2025072534212329,
        2025072534212330,
        2025072534212334,
        2025072534212331,
        2025072534212328,
        2025072534212333,
        2025072534212326,
        2025072534212325,
        2025072434211478,
        2025052733664113,
        2025052733664112,
        2025052733664111,
        2025052733664108,
        2025072534212365,
        2025072534212364,
        2025072534212337,
        2025072434210265,
    ]
    ids = [str(i) for i in list(set(ids))]
    for id in ids:
        args.id = id
        # 构造会话与请求头
        sess = requests.Session()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://lsem.fudan.edu.cn",
            "Referer": "https://lsem.fudan.edu.cn/fd_aqks_new/examProgress/examOnline/examProgressOnlineIndex",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            # 下列头一般由浏览器自动带上，服务端通常不强校验，这里可选
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
        }
        sess.headers.update(headers)

        # 设置 Cookie（如果提供）
        if args.jsessionid:
            sess.cookies.set(
                "JSESSIONID", args.jsessionid, domain="lsem.fudan.edu.cn", path="/"
            )
        else:
            print(
                "⚠️ 未提供 --jsessionid，若接口需要有效登录态，请加上该参数。",
                file=sys.stderr,
            )

        # 表单数据
        data = {
            "id": args.id,
            "readTime": args.readTime,
        }

        try:
            resp = sess.post(URL, data=data, timeout=args.timeout)
        except requests.RequestException as e:
            print(f"请求失败：{e}", file=sys.stderr)
            sys.exit(2)

        print(f"HTTP {resp.status_code}")
        ctype = resp.headers.get("Content-Type", "")
        # 尝试以 JSON 打印
        if "application/json" in ctype.lower():
            try:
                obj = resp.json()
                print(json.dumps(obj, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print(resp.text)
        else:
            print(resp.text)

        # 根据常见后端返回判定简单成功/失败提示
        if resp.ok:
            print("✅ 请求已发送。")
        else:
            print("❌ 请求失败。")


if __name__ == "__main__":
    main()
