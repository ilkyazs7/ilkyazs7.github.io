#!/usr/bin/env python3
"""
Download your images and videos from Cargo into this site.

Run from the top folder of the site, while the Cargo site is still online:

    python3 tools/download_cargo_images.py                 # everything
    python3 tools/download_cargo_images.py human-knitting  # one or more projects

Existing files are skipped. Large photos come down at 2000px wide; videos,
GIFs and smaller images as originals. The full list, with captions, is
tools/media.csv.
"""
import csv, os, sys, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
only = set(sys.argv[1:])

with open(os.path.join(HERE, "media.csv"), newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

done = skipped = failed = 0
for row in rows:
    if only and row["project"] not in only:
        continue
    dest = os.path.join(ROOT, row["file"])
    if os.path.exists(dest):
        skipped += 1
        continue
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    parts = urllib.parse.urlsplit(row["download_url"])
    url = urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(parts.path)))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(dest + ".part", "wb") as out:
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                out.write(chunk)
        os.replace(dest + ".part", dest)
        done += 1
        print("✓", row["file"])
    except Exception as e:
        failed += 1
        print("✗", row["file"], "-", e)
        if os.path.exists(dest + ".part"):
            os.remove(dest + ".part")

print(f"\n{done} downloaded, {skipped} already there, {failed} failed")
