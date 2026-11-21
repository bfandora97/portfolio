"""Cek hasil build di _site/ sebelum tayang. Dijalankan otomatis di GitHub Actions.

Yang dicek:
  - setiap link/gambar/script lokal (href, src) menunjuk ke file yang ada
  - setiap link #anchor punya id tujuan
  - setiap halaman punya <title>, meta description, og:image yang filenya ada
  - setiap halaman ada di sitemap.xml
Gagal = exit code 1, dan daftar masalahnya dicetak.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE = Path(__file__).resolve().parent.parent / "_site"
DOMAIN = "kemangdata.my.id"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.meta, self.title = [], set(), {}, ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src"):
            if a.get(k) and not (tag == "link" and a.get("rel") in ("preconnect", "canonical", "alternate")):
                self.links.append(a[k])
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d


def resolve(page_path, link):
    u = urlparse(link)
    if u.scheme in ("mailto", "tel", "data", "javascript"):
        return None, None
    if u.scheme in ("http", "https"):
        if u.netloc != DOMAIN:
            return None, None
    path = unquote(u.path)
    if not path:
        target = page_path
    elif path.startswith("/"):
        target = SITE / path.lstrip("/")
    else:
        target = page_path.parent / path
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve(), u.fragment


def main():
    if not SITE.exists():
        sys.exit("_site/ belum ada. Jalankan: python build.py")
    # file verifikasi Google Search Console (googleXXXX.html) bukan halaman, dilewati
    pages = {p.resolve(): p for p in SITE.rglob("*.html") if not re.fullmatch(r"google[0-9a-f]+\.html", p.name)}
    parsed = {}
    for p in pages:
        pr = Page()
        pr.feed(p.read_text(encoding="utf-8"))
        parsed[p] = pr

    errors = []
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    for p, pr in parsed.items():
        rel = p.relative_to(SITE.resolve()).as_posix()
        if not pr.title.strip():
            errors.append(f"{rel}: <title> kosong")
        if not pr.meta.get("description"):
            errors.append(f"{rel}: meta description kosong")
        og = pr.meta.get("og:image", "")
        if not og:
            errors.append(f"{rel}: og:image kosong")
        else:
            t, _ = resolve(p, og)
            if t and not t.exists():
                errors.append(f"{rel}: og:image tidak ada -> {og}")
        url_path = "" if rel == "index.html" else re.sub(r"index\.html$", "", rel)
        if f"https://{DOMAIN}/{url_path}<" not in sitemap:
            errors.append(f"{rel}: tidak ada di sitemap.xml")
        for link in pr.links:
            target, frag = resolve(p, link)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{rel}: link rusak -> {link}")
            elif frag and target in parsed and frag not in parsed[target].ids:
                errors.append(f"{rel}: anchor #{frag} tidak ditemukan -> {link}")

    if errors:
        print("MASALAH DITEMUKAN:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(parsed)} halaman, semua link, gambar, dan anchor valid.")


if __name__ == "__main__":
    main()
