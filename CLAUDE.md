# kemangdata.my.id: repo website (PUBLIC)

Website Kemang Data. Halaman dirakit oleh `build.py` (Python + Jinja2) ke `_site/`, lalu GitHub Actions menayangkannya ke GitHub Pages setiap ada merge ke `main`.

## Struktur

```
src/pages/        isi tiap halaman. Halaman utama = SATU kerangka untuk 2 bahasa (`bahasa:` di front matter):
                    index.html   -> /           & /id/           (Beranda: hero cerita, masalah, cara kerja, 3 paket)
                    tentang.html -> /about/     & /id/tentang/   (profil, cara kerja, FAQ)
                    layanan.html -> /services/  & /id/layanan/   (semua paket, contoh hasil, studi kasus, produk digital)
                    kontak.html  -> /contact/   & /id/kontak/    (booking, WA/Upwork, email, Temukan kami)
                  BAHASA UTAMA = INGGRIS di '/' (sejak 25 Nov 2026); Indonesia di '/id/'. Alamat lama dialihkan lewat src/data/pengalihan.yml
                  + halaman studi kasus (layout kasus)
src/layouts/      base.html (kerangka <head>, script) + macros.html (header, wa(), plan_card, lightbox, ...)
src/data/i18n/    id.yml + en.yml: SEMUA teks per bahasa (menu, footer, halaman utama, label). Kunci wajib sama persis (build gagal kalau beda)
src/data/         site.yml (WA, email, link) + paket.yml (HARGA, satu-satunya sumber) + alur.yml (isi animasi contoh, data fiktif) + proyek.yml (kartu proyek, tampil ya/tidak) + produk.yml (template Etsy, DIBUAT OTOMATIS dari repo ops: `python produk/kd.py katalog`, jangan diedit manual)
assets/css/       style.css (dikelompokkan per bagian, lihat komentar di atasnya)
assets/js/        theme.js (mode gelap + header), home.js (animasi halaman utama), case.js (tab gambar + layar penuh), alur.js (animasi contoh 3 adegan)
assets/img/       semua gambar
static/           disalin ke root situs (CNAME, robots.txt)
tools/            check_site.py (cek link/gambar/anchor/sitemap), gen_umkm.py (gambar dashboard demo UMKM),
                  gen_karakter.py (karakter Bobbi + pemilik kedai: panggung hero & Alur kerja; JANGAN edit SVG/CSS-nya langsung)
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
- Nomor WA, email, link profil, booking Cal.com, Instagram, TikTok: hanya di `src/data/site.yml` (kosong = tidak tampil). Toko Etsy: `toko:` di `src/data/produk.yml`.
- Menu = Tentang · Layanan · Kontak (di HP: Layanan · Kontak). Judul/deskripsi tiap halaman di i18n `halaman.<nama>`; halaman baru = file di `src/pages/` dengan `bahasa: {id: ..., en: ...}` + `halaman: <nama>`.
- Link WA dibuat dengan `{{ wa("pesan") }}`.
- **ID dan EN sama bentuknya.** Satu kerangka, teks di `src/data/i18n/id.yml` dan `en.yml` dengan kunci yang sama. Isi boleh menyesuaikan pasar (contoh Kopi Senja + Rupiah untuk ID, toko online + USD untuk EN), bagian/urutan/menu tidak boleh beda. Menambah teks = tambahkan di KEDUA file. Gaya bicara: "saya" / "I".
- Menu & footer: JANGAN ditulis di halaman. Halaman cukup memanggil `{{ header() }}` dan `{{ footer() }}`; isinya dari `src/data/i18n/<bahasa>.yml` sesuai `lang` + `menu` (utama/kasus) di front matter. Tombol ganti bahasa otomatis dari `alternates`. Di HP maksimal 3 link (`hp: false` untuk sisanya), tanpa burger menu.
- **Mode gelap**: `theme.js` selalu menulis `data-theme` (pilihan tersimpan atau ikut sistem), jadi aturan gelap cukup `[data-theme="dark"] ...` sekali. Jangan tambah blok `@media (prefers-color-scheme:dark)`.
- **Karakter**: `tools/check_site.py` gagal kalau blok KARAKTER di macros.html/style.css beda dengan hasil `tools/gen_karakter.py` (lupa jalankan / diedit manual) atau ada pose yang tidak dipakai.
- **Anti kode berulang**: kalau sesuatu muncul 2x atau lebih, jadikan data (`src/data/`) + macro (`macros.html`). ID & EN berbagi macro, isinya terpisah per bahasa. `style="..."` hanya untuk variabel CSS (`--d`); link WA/email/Upwork/LinkedIn hanya dari `site.yml`. Dicek otomatis oleh `tools/check_site.py` (build gagal kalau dilanggar).
- Halaman utama (`src/pages/index.html`): semua teks dari `t.utama` (i18n). Macro `cara_kerja()`, `faq()`, `kontak_utama()`, `daftar_proyek()`, `tombol(daftar)`. Tombol: `link` = url / upwork / email / linkedin / github / `"wa:pesan"`.
- Studi kasus: front matter `layout: kasus` + `kasus:` (judul, langkah, kpi, galeri, kontak); pembuka, tombol kontak, galeri layar penuh dan footer dibuat otomatis. Halaman hanya berisi bagian unik. Tambahkan juga kartunya di `src/data/proyek.yml`.
- Halaman baru: buat file di `src/pages/` dengan front matter (`title`, `description`, `lang` wajib; `menu: utama` untuk halaman utama, `og_image`, `og_type`, `scripts`, `alternates`, `sitemap: false` opsional). Sitemap otomatis.
- Link internal & gambar pakai path absolut (`/assets/img/x.png`, `/#contact`).
- **Repo ini public**: tidak boleh ada data kantor, data klien asli, nama perusahaan asli dari pekerjaan kantor, atau catatan internal. Data demo harus fiktif dan diberi label.
- Fase sekarang menyasar toko online internasional via Upwork (`/`, Inggris = bahasa utama) + UMKM Indonesia (`/id/`), dengan halaman yang sama bentuknya. Link untuk calon klien Indonesia (WA, Fastwork, prospek) pakai `https://kemangdata.my.id/id/`. Ganti alamat halaman = tambahkan alamat lama ke `src/data/pengalihan.yml`. Jangan menonjolkan industri pameran/event.
