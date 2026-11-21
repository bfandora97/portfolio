# kemangdata.my.id: repo website (PUBLIC)

Website Kemang Data. Halaman dirakit oleh `build.py` (Python + Jinja2) ke `_site/`, lalu GitHub Actions menayangkannya ke GitHub Pages setiap ada merge ke `main`.

## Struktur

```
src/pages/        isi tiap halaman; path file = URL (src/pages/en/index.html -> /en/)
src/layouts/      base.html (kerangka <head>, script) + macros.html (header, wa(), plan_card, lightbox, ...)
src/data/         site.yml (WA, email, link) + paket.yml (HARGA, satu-satunya sumber) + alur.yml (isi animasi contoh, data fiktif)
assets/css/       style.css (dikelompokkan per bagian, lihat komentar di atasnya)
assets/js/        theme.js (mode gelap + header), home.js (animasi halaman utama), case.js (tab gambar + layar penuh), alur.js (animasi contoh 3 adegan)
assets/img/       semua gambar
static/           disalin ke root situs (CNAME, robots.txt)
tools/            check_site.py (cek link/gambar/anchor/sitemap), gen_umkm.py (gambar dashboard demo UMKM)
build.py          merakit _site/ + sitemap.xml otomatis
```

## Cara kerja

```
pip install -r requirements.txt
python build.py && python tools/check_site.py
python -m http.server -d _site 8000      # http://localhost:8000
```

- Setiap perubahan: branch baru -> PR -> Bobbi yang merge. Jangan push langsung ke `main`.
- GitHub Actions (`.github/workflows/site.yml`) merakit + mengecek setiap PR; PR yang gagal cek tidak boleh di-merge.
- Tambah 1 baris di `CHANGELOG.md` di setiap PR.
- Perubahan tampilan: bandingkan screenshot sebelum/sesudah (desktop 1366 + HP 390, terang + gelap).

## Aturan isi

- **Harga hanya diubah di `src/data/paket.yml`.** Setelah itu, di repo ops (`kemang-data-ops`, folder induk) jalankan `tools/sync_marketplace.py` dan `tools/build_fastwork.py` supaya marketplace ikut.
- Nomor WA, email, link profil: hanya di `src/data/site.yml`. Link WA dibuat dengan `{{ wa("pesan") }}`.
- Halaman baru: buat file di `src/pages/` dengan front matter (`title`, `description`, `lang` wajib; `og_image`, `og_type`, `scripts`, `alternates`, `sitemap: false` opsional). Sitemap otomatis.
- Link internal & gambar pakai path absolut (`/assets/img/x.png`, `/#contact`).
- **Repo ini public**: tidak boleh ada data kantor, data klien asli, nama perusahaan asli dari pekerjaan kantor, atau catatan internal. Data demo harus fiktif dan diberi label.
- Fase sekarang menyasar UMKM Indonesia (halaman utama Bahasa Indonesia) + Upwork (`/en/`). Jangan menonjolkan industri pameran/event.
