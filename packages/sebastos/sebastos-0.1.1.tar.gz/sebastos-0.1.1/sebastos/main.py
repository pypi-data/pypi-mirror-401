import argparse
import datetime
import fnmatch
import json
import os
import sys
import tomllib
import xml.etree.ElementTree as ET
from glob import glob

import requests
from tqdm import tqdm

SEBASTOS_DIR = ".sebastos"
METADATA_FILE = "metadata.json"
CONFIG_FILE = "config.toml"

NAMESPACES = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "se": "https://standardebooks.org/vocab/1.0",
}


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def ensure_configured():
    if not os.access(SEBASTOS_DIR, os.R_OK):
        print(
            "this is not a sebastos repository. to initialise, run: {} init".format(
                sys.argv[0]
            )
        )
        sys.exit(1)


def repository_names(org: str) -> list[str]:
    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/orgs/{org}/repos"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, params=params)
        response.raise_for_status()

        page_repos = response.json()
        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    return [t["name"] for t in repos]


class RateLimitException(Exception):
    pass


def get_if_200(url):
    resp = requests.get(url)
    if resp.status_code == 429:
        raise RateLimitException()
    if resp.status_code != 200:
        debug(f"HTTP {resp.status_code}: {url}")
        return None
    return resp.content


def get_meta_property(metadata: ET.Element, property_name: str) -> str | None:
    for meta in metadata.findall("opf:meta", NAMESPACES):
        if meta.get("property") == property_name:
            return meta.text
    return None


def get_refined_property(
    metadata: ET.Element, property_name: str, refines: str
) -> str | None:
    for meta in metadata.findall("opf:meta", NAMESPACES):
        if (
            meta.get("property") == property_name
            and meta.get("refines") == f"#{refines}"
        ):
            return meta.text
    return None


def parse_opf(opf_content: str) -> dict:
    root = ET.fromstring(opf_content)
    metadata = root.find("opf:metadata", NAMESPACES)
    if metadata is None:
        return {}

    collections = [
        m.text
        for m in metadata.findall("opf:meta", NAMESPACES)
        if m.get("property") == "belongs-to-collection"
    ]
    sources = [s.text for s in metadata.findall("dc:source", NAMESPACES) if s.text]
    authors = [s.text for s in metadata.findall("dc:creator", NAMESPACES) if s.text]
    subjects = [s.text for s in metadata.findall("dc:subject", NAMESPACES) if s.text]
    subjects += [
        m.text
        for m in metadata.findall("opf:meta", NAMESPACES)
        if m.get("property") == "se:subject"
    ]

    return {
        "identifier": metadata.findtext("dc:identifier", namespaces=NAMESPACES),
        "title": metadata.findtext("dc:title", namespaces=NAMESPACES),
        "author": authors,
        "subject": subjects,
        "collection": collections,
        "source": sources,
        "description": metadata.findtext("dc:description", namespaces=NAMESPACES),
        "long_description": get_meta_property(metadata, "se:long-description"),
        "language": metadata.findtext("dc:language", namespaces=NAMESPACES),
    }


FORMAT_EXTENSIONS = {
    "epub": ".epub",
    "azw3": ".azw3",
    "kepub": ".kepub.epub",
    "adv-epub": "_advanced.epub",
}


def load_config() -> dict:
    with open(SEBASTOS_DIR + "/" + CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def match_book(book: dict, query: dict) -> bool:
    for key, value in query.items():
        if key not in book:
            return False
        match_against = book.get(key)
        if not match_against:
            return False

        typ = type(match_against)
        if typ is str:
            if not fnmatch.fnmatch(match_against, value):
                return False
        elif typ is list:
            if not any(fnmatch.fnmatch(c, value) for c in match_against):
                return False
        else:
            debug(f"unexpected type for {key}: {typ} with value {match_against}")
            return False
    return True


def matching_metadata(opf, queries: list[dict]) -> list[dict]:
    """Find all books matching any of the queries (OR logic between queries)."""
    result = []
    for repo in opf:
        book = parse_opf(opf[repo])
        for query in queries:
            if match_book(book, query):
                result.append((repo, book))
    return result


def cmd_sync():
    ensure_configured()
    config = load_config()
    fmt = config.get("format", "epub")

    if fmt not in FORMAT_EXTENSIONS:
        print(f"unknown ebook format, aborting: {fmt}")
        return
    ext = FORMAT_EXTENSIONS[fmt]

    queries = config.get("query", [])

    with open(SEBASTOS_DIR + "/" + METADATA_FILE) as f:
        metadata = json.load(f)

    matches = matching_metadata(metadata["opf"], queries)

    if len(matches) == 0:
        print("No books match any queries: aborting.")
        return

    filepaths = set()

    # Determine what to download and remove
    to_download = []
    for repo, book in matches:
        filename = f"{repo}{ext}"
        filepaths.add(filename)
        if not os.access(filename, os.R_OK):
            to_download.append((repo, filename, book))

    extant_filepaths = set(glob(f"*{ext}"))
    to_remove = extant_filepaths - filepaths

    for repo, filename, book in to_download:
        if filename in extant_filepaths:
            continue
        url = get_download(parse_opf(metadata["opf"][repo])["identifier"], repo, ext)
        debug(f"Downloading {filename}")
        try:
            resp = get_if_200(url)
        except RateLimitException:
            debug(
                "Standard Ebooks rate limit exceeded - aborting sync. Try again later."
            )
            return
        if resp is None:
            debug(f"Failed downloading {filename}")
            return
        with open(filename + ".tmp", "wb") as f:
            f.write(resp)
        os.rename(filename + ".tmp", filename)

    # Remove books that no longer match
    if to_remove:
        print("The following books no longer match any queries:")
        for filepath in to_remove:
            print(f"  {filepath}")
        confirm = input("Remove them? [y/N] ")
        if confirm.lower() == "y":
            for filepath in to_remove:
                os.unlink(filepath)


def get_download(identifier, repo, ext):
    return f"{identifier}/downloads/{repo}{ext}?source=download"


def cmd_update():
    ensure_configured()
    metadata = None

    def write_metadata():
        tmpf = SEBASTOS_DIR + "/" + METADATA_FILE + ".tmp"
        outf = SEBASTOS_DIR + "/" + METADATA_FILE
        with open(tmpf, "w") as fd:
            json.dump(metadata, fd, indent=2)
        os.rename(tmpf, outf)

    metaf = SEBASTOS_DIR + METADATA_FILE
    if os.access(metaf, os.R_OK):
        with open(metaf) as fd:
            metadata = json.load(fd)
        if "version" not in metadata or metadata["version"] != 1:
            metadata = None

    if not metadata:
        metadata = {
            "version": 1,
            "opf": {},
        }

    metadata["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    debug("retrieving standard ebook metadata (this will take a few minutes)")
    repos = repository_names("standardebooks")
    opf = metadata["opf"]

    to_sync = [t for t in repos if "_" in t and t not in opf]
    for repo in tqdm(to_sync, desc="Fetching OPF metadata"):
        opf_data = get_if_200(
            f"https://raw.githubusercontent.com/standardebooks/{repo}/refs/heads/master/src/epub/content.opf"
        )
        if opf_data is None:
            debug(f"Failed to fetch content.opf for {repo}")
            continue
        opf[repo] = opf_data.decode("utf8")

    write_metadata()


def cmd_init():
    if os.access(SEBASTOS_DIR, os.R_OK):
        debug("sebastos is already configured in this directory. aborting.")
        return
    os.mkdir(SEBASTOS_DIR)
    with open(SEBASTOS_DIR + "/" + CONFIG_FILE, "w") as fd:
        fd.write("""\
# file format; options are: epub, azw3, kepub, adv-epub
format = 'epub'

# an example query. you can use glob-style patterns to match
# against the following fields:
#   - title
#   - author
#   - subject
#   - collection
#   - source
#   - description
#   - long_description
#   - language
# within a query, patterns are combined with AND
# if you have multiple queries, books which match any query are returned
[[query]]
author = "Jane Austen"
title = "Pride*"
""")
    cmd_update()
    print("your new sebastos repository is ready to go!")
    print("to configure queries, edit " + SEBASTOS_DIR + "/" + CONFIG_FILE)
    print("then run `sebastos sync` to download matching books")


def cmd_list():
    ensure_configured()
    with open(SEBASTOS_DIR + "/" + METADATA_FILE) as f:
        metadata = json.load(f)
    json.dump([parse_opf(t) for t in metadata["opf"].values()], sys.stdout, indent=2)


def cmd_links():
    ensure_configured()
    with open(SEBASTOS_DIR + "/" + METADATA_FILE) as f:
        metadata = json.load(f)
    for repo in metadata["opf"]:
        print(
            get_download(parse_opf(metadata["opf"][repo])["identifier"], repo, ".epub")
        )


def main():
    parser = argparse.ArgumentParser(description="Standard Ebooks CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "init", help="Start a new sebastos repository in current directory"
    )
    subparsers.add_parser("update", help="Update book metadata from GitHub")
    subparsers.add_parser("list", help="Print book metadata as JSON")
    subparsers.add_parser("links", help="Print download links for each book")
    subparsers.add_parser("sync", help="Sync books")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "update":
        cmd_update()
    elif args.command == "list":
        cmd_list()
    elif args.command == "links":
        cmd_links()
    elif args.command == "sync":
        cmd_sync()


if __name__ == "__main__":
    main()
