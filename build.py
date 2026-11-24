"""Merakit website ke folder _site/.

    python build.py            # hasil di _site/
    python -m http.server -d _site 8000   # lihat di http://localhost:8000

Struktur:
    src/pages/   isi tiap halaman (path file = path URL), diawali "front matter" YAML
    src/layouts/ base.html (kerangka) + macros.html (header, tombol WA, kartu paket, dll.)
    src/data/    site.yml (kontak, link) + paket.yml (harga) + alur.yml (isi animasi contoh) + produk.yml (template Etsy)
    assets/      css, js, gambar (disalin apa adanya)
    static/      file yang disalin ke root situs (CNAME, robots.txt)
"""
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "_site"
MACROS = ("header", "logo", "wa", "rupiah", "plan_card", "lightbox", "contact_buttons_en", "alur", "template_card")


def load_data():
    data = {}
    for f in sorted((SRC / "data").glob("*.yml")):
        data[f.stem] = yaml.safe_load(f.read_text(encoding="utf-8"))
    return data


def split_front_matter(text, path):
    if not text.startswith("---"):
        raise SystemExit(f"{path}: halaman harus diawali front matter '---'")
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body.lstrip("\n")


def page_url(site_url, rel):
    p = rel.as_posix()
    if p == "index.html":
        p = ""
    elif p.endswith("/index.html"):
        p = p[: -len("index.html")]
    return f"{site_url}/{p}"


def build():
    data = load_data()
    site = data["site"]
    env = Environment(loader=FileSystemLoader([str(SRC / "layouts"), str(SRC / "pages")]),
                      undefined=StrictUndefined, autoescape=False, keep_trailing_newline=True)
    produk = data["produk"]
    produk["tampil"] = [p for p in produk["produk"] if p.get("etsy")]  # hanya yang sudah ada link Etsy
    env.globals.update(site=site, paket=data["paket"]["paket"], alur_data=data["alur"], produk=produk)
    base = env.get_template("base.html")
    imports = "{% from 'macros.html' import " + ", ".join(MACROS) + " with context %}"

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for f in (ROOT / "static").iterdir():
        shutil.copy2(f, OUT / f.name)

    pages = []
    for src in sorted((SRC / "pages").rglob("*.html")):
        rel = src.relative_to(SRC / "pages")
        meta, body = split_front_matter(src.read_text(encoding="utf-8"), rel)
        for key in ("title", "description", "lang"):
            if not meta.get(key):
                raise SystemExit(f"{rel}: front matter wajib punya '{key}'")
        meta["url"] = page_url(site["url"], rel)
        content = env.from_string(imports + body).render(page=meta)
        html = base.render(page=meta, content=content.strip("\n"))
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8", newline="\n")
        if meta.get("sitemap", True):
            pages.append(meta["url"])
        print("  ", rel.as_posix())

    urls = "\n".join(f"  <url><loc>{u}</loc></url>" for u in pages)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8", newline="\n")
    print(f"OK: {len(pages)} halaman -> {OUT.name}/")


if __name__ == "__main__":
    build()
