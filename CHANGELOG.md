# Catatan Perubahan

Paling baru di atas. Satu baris per PR.

## 2026-11-24
- PR: Link booking Cal.com diisi (`cal.com/kemangdata-pcij5n/30min`), tombol booking tampil di kontak halaman utama & studi kasus ID/EN.
- PR: Tombol booking konsultasi 30 menit (Cal.com) lewat data: `booking:` di `src/data/site.yml` + tombol `link: booking` di i18n (kontak halaman utama & studi kasus, ID & EN). Kosong = tidak tampil. Menggantikan PR #9.
- PR: ID & EN jadi satu kerangka. `src/pages/index.html` dibuat jadi / dan /en/ (`bahasa: [id, en]`), semua teks di `src/data/i18n/id.yml` + `en.yml` (menggantikan teks.yml, konten.yml dan src/pages/en/index.html). Urutan bagian & menu sama: Masalah, Contoh, Jasa, Proyek, (Template), Cara kerja, Tentang, FAQ, Kontak. Contoh per pasar (Kopi Senja/Rupiah vs Juniper/USD). EN dapat contoh showcase + tombol tanya paket; ID dapat bagian Template. Build gagal kalau kunci ID/EN beda. Gaya bicara "saya".
- PR #15: Menu EN jadi Services · Projects · About · Contact (Problems dihapus), ID jadi Contoh · Jasa · Tentang · Kontak. Bagian kontak halaman utama dirampingkan: 2 tombol utama (ID: WhatsApp + Email, EN: Upwork + Email), LinkedIn/GitHub cukup di footer, tidak lagi setinggi 1 layar penuh.
- PR C (refactor 3/3): Cara kerja, FAQ dan kontak halaman utama dari `src/data/konten.yml` (macro `cara_kerja()`, `faq()`, `kontak_utama()`, `tombol()`). `check_site.py` sekarang juga menolak inline style selain variabel CSS, link kontak yang ditulis manual, dan halaman tanpa header/footer macro. HTML hasil build identik dengan sebelumnya.
- PR B (refactor 2/3): Kartu proyek dari `src/data/proyek.yml` (ID & EN), 4 halaman studi kasus pakai layout `kasus` (pembuka, kontak, layar penuh dari data; isi unik tetap di halaman). Proyek event `tampil: false` (tidak dipromosikan, halaman tetap ada). Tombol kontak studi kasus EN diseragamkan (Upwork, Email, WhatsApp). Inline style catatan demo jadi class `.note.demo`.
- PR A (refactor 1/3): Menu & footer dari data (`src/data/teks.yml`), halaman cukup `{{ header() }}` + `{{ footer() }}`. Footer baru 3 kolom (Jelajahi, Hubungi) di semua halaman. Menu Proyek di halaman ID (desktop). Aturan HP pakai class `nhp`/`nkecil`. Isi halaman lain identik (dicek per halaman).
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
