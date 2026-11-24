"""Merakit website ke folder _site/.

    python build.py            # hasil di _site/
    python -m http.server -d _site 8000   # lihat di http://localhost:8000

Struktur:
    src/pages/   isi tiap halaman (path file = path URL), diawali "front matter" YAML
                 - `bahasa: [id, en]`  = SATU kerangka dibuat jadi 2 halaman: /<path> (id) dan /en/<path> (en),
                                         title/description/og_image dari i18n `utama.meta`
                 - `layout: kasus`     = halaman studi kasus (pembuka, kontak, footer otomatis)
    src/layouts/ base.html (kerangka <head>) + macros.html (semua komponen)
    src/data/    i18n/id.yml + i18n/en.yml  SEMUA teks per bahasa (kunci wajib sama persis, dicek di sini)
                 site.yml (kontak, link) · paket.yml (harga) · proyek.yml (kartu proyek)
                 alur.yml (animasi contoh) · produk.yml (template Etsy, dibuat dari repo ops)
    assets/      css, js, gambar (disalin apa adanya)
    static/      file yang disalin ke root situs (CNAME, robots.txt)
"""
import shutil
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "_site"
MACROS = ("header", "logo", "wa", "rupiah", "plan_card", "lightbox", "alur", "template_card", "footer", "kasus_pembuka",
          "kasus_kontak", "daftar_proyek", "tombol", "cara_kerja", "faq", "kontak_utama")
BAHASA = ("id", "en")


def load_data():
    data = {}
    for f in sorted((SRC / "data").glob("*.yml")):
        data[f.stem] = yaml.safe_load(f.read_text(encoding="utf-8"))
    data["i18n"] = {b: yaml.safe_load((SRC / "data" / "i18n" / f"{b}.yml").read_text(encoding="utf-8")) for b in BAHASA}
    return data


def cek_kembar(a, b, jalur="", masalah=None):
    """ID dan EN wajib berbentuk sama: kunci sama, jumlah item daftar (yang berisi objek) sama."""
    masalah = [] if masalah is None else masalah
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                masalah.append(f"{jalur}.{k}: hanya ada di {'en' if k not in a else 'id'}.yml")
            else:
                cek_kembar(a[k], b[k], f"{jalur}.{k}", masalah)
    elif isinstance(a, list) and isinstance(b, list):
        if any(isinstance(x, dict) for x in a + b):
            if len(a) != len(b):
                masalah.append(f"{jalur}: {len(a)} item di id.yml vs {len(b)} di en.yml")
            for i, (x, y) in enumerate(zip(a, b)):
                cek_kembar(x, y, f"{jalur}[{i}]", masalah)
    elif isinstance(a, (dict, list)) != isinstance(b, (dict, list)):
        masalah.append(f"{jalur}: jenis isi beda di id.yml dan en.yml")
    return masalah


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


def url_path(rel):
    return "/" + page_url("", rel).lstrip("/")


def build():
    data = load_data()
    beda = cek_kembar(data["i18n"]["id"], data["i18n"]["en"], "i18n")
    if beda:
        raise SystemExit("Versi ID dan EN tidak sama bentuknya:\n  - " + "\n  - ".join(beda))
    site = data["site"]
    env = Environment(loader=FileSystemLoader([str(SRC / "layouts"), str(SRC / "pages")]),
                      undefined=StrictUndefined, autoescape=False, keep_trailing_newline=True)
    produk = data["produk"]
    produk["tampil"] = [p for p in produk["produk"] if p.get("etsy")]  # hanya yang sudah ada link Etsy
    env.globals.update(site=site, paket=data["paket"]["paket"], alur_data=data["alur"], produk=produk,
                       i18n=data["i18n"], tahun=date.today().year, proyek=data["proyek"]["proyek"])
    base = env.get_template("base.html")
    imports = "{% from 'macros.html' import " + ", ".join(MACROS) + " with context %}"

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for f in (ROOT / "static").iterdir():
        shutil.copy2(f, OUT / f.name)

    # daftar halaman yang dibuat: (path sumber, path hasil, front matter, isi)
    jobs = []
    for src in sorted((SRC / "pages").rglob("*.html")):
        rel = src.relative_to(SRC / "pages")
        meta, body = split_front_matter(src.read_text(encoding="utf-8"), rel)
        if meta.get("bahasa"):  # satu kerangka, beberapa bahasa
            hasil = {b: (rel if b == "id" else Path(b) / rel) for b in meta["bahasa"]}
            alternates = {b: url_path(r) for b, r in hasil.items()}
            alternates["x-default"] = alternates["id"]
            for b, r in hasil.items():
                m = dict(meta, lang=b, alternates=alternates, **data["i18n"][b]["utama"]["meta"])
                jobs.append((rel, r, m, body))
        else:
            jobs.append((rel, rel, meta, body))

    pages = []
    dibuat = set()
    for rel, out_rel, meta, body in jobs:
        if out_rel in dibuat:
            raise SystemExit(f"{rel}: {out_rel} dibuat dua kali (bentrok dengan halaman lain)")
        dibuat.add(out_rel)
        for key in ("title", "description", "lang"):
            if not meta.get(key):
                raise SystemExit(f"{rel}: front matter wajib punya '{key}'")
        meta["url"] = page_url(site["url"], out_rel)
        if meta.get("layout") == "kasus":  # halaman studi kasus: kerangka dari macros.html, isi unik dari halaman
            body = ("<div class=\"wrap\">\n{{ header() }}\n<main>\n{{ kasus_pembuka() }}\n" + body.strip("\n")
                    + "\n{{ kasus_kontak() }}\n</main>{{ footer() }}</div>{{ lightbox() }}")
        t = data["i18n"][meta["lang"]]
        content = env.from_string(imports + body).render(page=meta, t=t)
        html = base.render(page=meta, content=content.strip("\n"))
        dest = OUT / out_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8", newline="\n")
        if meta.get("sitemap", True):
            pages.append(meta["url"])
        print("  ", out_rel.as_posix())

    urls = "\n".join(f"  <url><loc>{u}</loc></url>" for u in pages)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8", newline="\n")
    print(f"OK: {len(pages)} halaman -> {OUT.name}/")


if __name__ == "__main__":
    build()
