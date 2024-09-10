#!/usr/bin/env python3

from argparse import ArgumentParser
from auttolib import get_id_and_name, download
from datetime import datetime
from os.path import expanduser as os_path_expanduser
from random import random, seed
from time import sleep, time_ns

DEFAULT_TIMEOUT = 6.9


def fetch_sequence(season, from_episode, to_episode, keywords, timeout, home):
    seed(time_ns())
    for i in range(from_episode, to_episode + 1):
        episode = f"S{season:02d}E{i:02d}"
        print(f"[{datetime.now()}] Trying to download \"{keywords} {episode}\"")
        try_again = True
        while try_again:
            try:
                ans = get_id_and_name(f"{keywords} {episode}")
                download(ans["id"], ans["full_name"], home)
                print(f"[{datetime.now()}] Downloaded to \"{home}\"")
                try_again = False
                if i != to_episode and timeout > 0:
                    print(f"[{datetime.now()}] Sleeping for {timeout:.1f} days")
                    sleep(60*60*24*timeout)
            except TypeError:
                print(f"[{datetime.now()}] No torrent found")
                r = (random() * 30 + 90) * 60
                print(f"[{datetime.now()}] Sleeping for {r/60:.1f} minutes")
                sleep(r)


def main():
    parser = ArgumentParser(description="File Fetching Automation")
    parser.add_argument("-s", "--season", required=True, type=int, help="select season to fetch")
    parser.add_argument("-f", "--from_episode", required=True, type=int, help="select episode range beginning to fetch")
    parser.add_argument("-t", "--to_episode", required=True, type=int, help="select episode range ending to fetch")
    parser.add_argument("-z", "--sleep", type=float,
                        help=f"number of days to sleep between each successfull fetch, defaults to {DEFAULT_TIMEOUT}")
    parser.add_argument("keywords", metavar="KEYWORDS",
                        help="downloads first file matching all space separated keywords")

    args = parser.parse_args()
    timeout = DEFAULT_TIMEOUT
    if args.sleep != None:
        timeout = args.sleep

    home = os_path_expanduser("~/Downloads")
    fetch_sequence(args.season, args.from_episode, args.to_episode, args.keywords, timeout, home)


if __name__ == "__main__":
    main()
