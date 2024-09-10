#!/usr/bin/env python3

from argparse import ArgumentParser
from credentials import UID, PASS
from functools import reduce
from os import mkdir as os_mkdir
from os.path import exists as os_exists
from os.path import join as os_path_join
from re import match
from requests import get as requests_get
from requests.structures import CaseInsensitiveDict

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


ROOT_URL = ""
SEARCH_STEM = "browse.php?search="
DOWNLOAD_SCRIPT = "download.php"
DOWNLOAD_DIR = "downloads"

headers = CaseInsensitiveDict()
headers["Cookie"] = f"uid={UID}; pass={PASS}"


def get_id_and_name(query):
    q = query.replace(" ", "+")
    # print(q)
    response = requests_get(f"{ROOT_URL}/{SEARCH_STEM}{q}", headers=headers)

    # print(response.status_code)
    parsed_html = BeautifulSoup(response.content, features="lxml")
    # print(parsed_html.body)
    all_torrents = parsed_html.body.find_all("a", attrs={"class": "nameLink"})

    for t in all_torrents:
        # print(t)
        if reduce(lambda a, b: a and b, list(map(lambda kw: kw.lower() in t.text.lower(), query.split(" ")))):
            regex = r'.*href="details.php\?id=([0-9]+)".*'
            m = match(regex, str(t))
            # print(m[1])
            return {"full_name": t.text, "id": m[1]}

    return None


def download(tid, name, dldir):
    dotname = name.replace(" ", ".")
    torrent_file = f"{dotname}.torrent"
    response = requests_get(f"{ROOT_URL}/{DOWNLOAD_SCRIPT}/{tid}/{torrent_file}", headers=headers)
    # print(response.status_code)
    dl_location = os_path_join(dldir, torrent_file)
    if not os_exists(dldir):
        os_mkdir(dldir)
    with open(dl_location, "wb") as f:
        f.write(response.content)


def main():
    parser = ArgumentParser(description="File Fetching Automation")
    parser.add_argument("-q", "--quiet", action="store_true", help="do not output anything to the terminal")
    parser.add_argument("-d", "--download-dir", type=str,
                        help=f"where to put downloaded files, defaults to \"{DOWNLOAD_DIR}\"")
    parser.add_argument("keywords", nargs=1, help="downloads first file matching all keywords")

    args = parser.parse_args()
    quiet = args.quiet
    download_dir = DOWNLOAD_DIR
    if args.download_dir:
        download_dir = args.download_dir

    for keywords in args.keywords:
        try:
            ans = get_id_and_name(keywords)
            if not quiet:
                print(f"{ans['id']}: {ans['full_name']}")
            download(ans["id"], ans["full_name"], download_dir)
            if not quiet:
                print(f"Downloaded to \"{download_dir}\"")
        except TypeError:
            if not quiet:
                print(f"No torrent found for keywords: {keywords}")
            exit(1)


if __name__ == "__main__":
    main()
