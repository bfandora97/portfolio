"""Cek hasil build di _site/ sebelum tayang. Dijalankan otomatis di GitHub Actions.

Yang dicek:
  - setiap link/gambar/script lokal (href, src) menunjuk ke file yang ada
  - setiap link #anchor punya id tujuan
  - setiap halaman punya <title>, meta description, og:image yang filenya ada
  - setiap halaman ada di sitemap.xml
  - setiap halaman punya menu (header) dan footer standar dari macro
  - aturan anti-kode-berulang di src/ (lihat cek_sumber):
      * style="..." hanya boleh variabel CSS (--d, --i, ...); tampilan lain lewat class di style.css
      * link WA / email / Upwork / LinkedIn tidak boleh ditulis manual di halaman: pakai site.yml ({{ wa() }}, {{ site.email }}, ...)
Gagal = exit code 1, dan daftar masalahnya dicetak.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
SRC = ROOT / "src"
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


def cek_sumber():
    """Aturan supaya kode tidak berulang. Mengembalikan daftar masalah."""
    errors = []
    css_var = re.compile(r"^(\s*--[\w-]+:[^;]+;?)+\s*$")
    kontak_manual = re.compile(r'href="[^"]*(wa\.me/|mailto:|upwork\.com|linkedin\.com)')  # hanya link, bukan teks contoh data
    for f in sorted(list((SRC / "pages").rglob("*.html")) + list((SRC / "layouts").glob("*.html"))):
        rel = f.relative_to(ROOT).as_posix()
        s = f.read_text(encoding="utf-8")
        for m in re.finditer(r'style="([^"]*)"', s):
            isi = re.sub(r"\{\{.*?\}\}", "x", m.group(1))
            if not css_var.match(isi):
                errors.append(f"{rel}: inline style selain variabel CSS -> style=\"{m.group(1)[:60]}\" (pakai class di style.css)")
        if f.parent.name != "layouts":
            for m in kontak_manual.finditer(s):
                errors.append(f"{rel}: link kontak ditulis manual ({m.group(1)}), ambil dari src/data/site.yml")
    return errors


def cek_karakter():
    """Penjaga gen_karakter.py: (1) blok karakter di macros.html/style.css = hasil generator (tidak diedit manual,
    generator sudah dijalankan); (2) tidak ada pose yang didefinisikan tapi tidak dipakai (kode mati)."""
    import importlib.util
    errors = []
    sumber = ROOT / "tools" / "gen_karakter.py"
    spec = importlib.util.spec_from_file_location("gen_karakter", sumber)
    gk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gk)
    m, c = gk.hasil()
    if m != gk.MACROS.read_text(encoding="utf-8") or c != gk.STYLE.read_text(encoding="utf-8"):
        errors.append("blok karakter di macros.html/style.css beda dengan generator -> jalankan python tools/gen_karakter.py (jangan edit blok KARAKTER manual)")
    teks = sumber.read_text(encoding="utf-8")
    for nama in re.findall(r'aksi == "(\w+)"', teks):
        if teks.count(f'"{nama}"') < 2:
            errors.append(f"gen_karakter.py: pose \"{nama}\" didefinisikan tapi tidak dipakai -> hapus")
    return errors


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

    errors = cek_sumber() + cek_karakter()
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
        html = p.read_text(encoding="utf-8")
        if html.count('<header class="top">') != 1 or html.count('<footer class="ft">') != 1:
            errors.append(f"{rel}: harus punya tepat 1 header() dan 1 footer() dari macro")
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
    print(f"OK: {len(parsed)} halaman, semua link, gambar, anchor, menu/footer, aturan anti-kode-berulang, dan karakter (sinkron, tanpa pose mati) valid.")


if __name__ == "__main__":
    main()
