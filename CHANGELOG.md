# Catatan Perubahan

Paling baru di atas. Satu baris per PR.

## 2026-11-24
- PR #11: Bagian "Ready-made templates" di /en/ (checkout langsung ke Etsy + disclaimer merek Etsy). `src/data/produk.yml` dibuat otomatis dari katalog produk di repo ops (`python produk/kd.py katalog`); hanya produk berstatus live + ada link Etsy yang tampil.

## 2026-11-21
- PR #10: Animasi contoh 3 adegan (berantakan → digabung → laporan di HP) di halaman utama ID/EN dan studi kasus. Isi di `src/data/alur.yml` (fiktif), tampilan di macro `alur()` + CSS 7c + `assets/js/alur.js`. Bisa dijeda; reduced motion = gambar diam.
- PR #8: File verifikasi Google Search Console (`static/googlefdbe962ee824253f.html`). Jangan dihapus, atau verifikasi Google akan hilang.
- PR #7: Pesan website diubah jadi berbasis masalah klien. ID untuk UMKM lokal (hero, "Masalah yang sering kami bantu", Contoh hasil, nama jasa = manfaat, proyek event dikecilkan). EN untuk toko online internasional (hero + "Problems I solve").

## 2026-11-20
- PR #6: Versi Inggris dilengkapi (Cara kerja, Tentang + foto, FAQ, paket bulanan $120) + studi kasus UMKM versi Inggris.
- PR #5: Foto di bagian Tentang dibuat lebih lebar dan tajam.
- PR #4: Foto Bobbi di bagian "Tentang Kemang Data".
- PR #3: Struktur dirapikan. Halaman dirakit dari template (`src/`), harga dari `paket.yml`, gambar di `assets/img/`, CSS disatukan tanpa tambalan. Ada pengecekan otomatis (link, gambar, anchor, sitemap) dan tayang otomatis lewat GitHub Actions. Tampilan tidak berubah.
- PR #2: Halaman utama Bahasa Indonesia untuk UMKM, Jasa & Harga, Cara kerja, Tentang, FAQ, studi kasus UMKM (data fiktif), versi Inggris di `/en/`, Open Graph, sitemap, robots.

## 2026-11-17
- PR #1: Perbaikan efek header saat scroll, tampilan HP, tombol tanpa gaya, favicon, email kontak.
