#!/usr/bin/env python3

from argparse import ArgumentParser
from auttolib import get_id_and_name, download
from datetime import datetime
from os.path import expanduser as os_path_expanduser
from random import random, seed
from time import sleep, time_ns


def main():
    parser = ArgumentParser(description="TT Automation")
    parser.add_argument("-s", "--season", required=True, type=int, help="select season to fetch")
    parser.add_argument("-f", "--from_episode", required=True, type=int, help="select episode range beginning to fetch")
    parser.add_argument("-t", "--to_episode", required=True, type=int, help="select episode range ending to fetch")
    parser.add_argument("-z", "--sleep", type=float, help="number of days to sleep between each successfull fetch, defaults to 6.9")
    parser.add_argument("keywords", metavar="KEYWORDS", help="downloads first file matching all space separated keywords")

    args = parser.parse_args()
    timeout = 6.9
    if args.sleep != None:
        timeout = args.sleep

    home = os_path_expanduser("~/Downloads")

    seed(time_ns())
    for i in range(args.from_episode, args.to_episode + 1):
        episode = f"S{args.season:02d}E{i:02d}"
        print(f"[{datetime.now()}] Trying to download \"{args.keywords} {episode}\"")
        try:
            ans = get_id_and_name(f"{args.keywords} {episode}")
            download(ans["id"], ans["full_name"], home)
            print(f"[{datetime.now()}] Downloaded to \"{home}\"")
            if i != args.to_episode and timeout > 0:
                print(f"[{datetime.now()}] Sleeping for {timeout:.1f} days")
                sleep(60*60*24*timeout)
        except TypeError:
            print(f"[{datetime.now()}] No torrent found")
            r = (random() * 30 + 90) * 60
            print(f"[{datetime.now()}] Sleeping for {r/60:.1f} minutes")
            sleep(r)


if __name__ == "__main__":
    main()
