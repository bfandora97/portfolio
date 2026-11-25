# Catatan Perubahan

Paling baru di atas. Satu baris per PR.

## 2026-11-25
- PR: rambut Bobbi tampak samping jadi quiff bervolume (bukan selembar).
- PR: langkah berjalan tampak samping: 2 fase yang beda bentuk (melangkah / melintas) supaya kaki terlihat bergerak; kuncir rapat ke kepala.
- PR: pemilik kedai: sanggul diganti kuncir kuda (depan & samping, helaian menyatu ke ikatan); salaman dengan pergelangan tangan.
- PR: alur hero sesuai Bobbi: pemilik kedai serahkan data -> Bobbi jalan ke ruang kerja -> Bobbi jalan ke kedai bawa laporan -> salaman; sanggul tampak samping lebih detail.
- PR: cerita hero: tanpa papan lokasi; Bobbi berjalan (tampak samping) datang ke kedai membawa laporan, kedai lalu ramai (ruang presentasi & HP dihapus).
- PR: pemilik kedai berjalan tampak samping (berbalik saat kursor mundur); di meja kerja Bobbi duduk dengan laptop di meja, pemilik kedai duduk di sofa.
- PR: hero jadi cerita perjalanan (kedai kacau -> kantor -> meja kerja -> ruang presentasi -> kedai ramai, 32 dtk): berjalan + latar bergeser, kursor menggeser cerita (desktop); CSS/JS diberi ?v=versi (anti cache lama).
- PR: hero jadi cerita 5 adegan (5 detik per adegan, 25 detik): masalah (pemilik kedai bingung, balon pertanyaan) -> kirim -> rapikan -> laporan (balon jawaban) -> cek & bayar.
- PR: Bobbi rambut quiff (dari referensi Bobbi, tersapu ke kanan Bobbi) + latar kantor di belakang panggung hero (gambar sendiri, ada versi gelap).
- PR: hero: papan langkah atas diganti bilah 4 langkah di bawah (yang aktif menyala), teks langkah lebih jelas (Kirim data, Saya rapikan, Laporan jadi, Cek & bayar), berkas terbang mendarat di tangan Bobbi.
- PR: Bobbi rambut side part disapu ke kanan + undercut, dahi proporsional + ujung rambut jatuh, helaian meruncing, rambut abu-abu arang di mode gelap, alis melengkung halus, kulit lebih terang (permintaan Bobbi).

## 2026-11-24
- PR: Garis hitam di leher Bobbi dihapus (leher digambar di atas kaos, menyambung dari dagu ke kerah).
- PR: Wajah Bobbi v2 dari foto formal (pilihan A): wajah lonjong, rambut pendek dengan jambul disapu ke samping (2 lapis, tidak ada celah putih), alis tebal lurus, kumis tipis; tetap kaos hitam + lanyard. Berlaku di hero & Alur kerja.
- PR: Hero tata letak B: judul kiri, panggung animasi kanan (HP: animasi di atas). 2 karakter original gaya kartun: Bobbi (analis data, mirip foto, kaos hitam + ID Kemang Data) & pemilik kedai; 4 adegan 12 detik (kirim berkas → laptop → poster laporan → tanda tangan). Bobbi di Alur kerja ikut gaya baru. Sumber: `tools/gen_karakter.py` (menggantikan gen_barista).
- PR: Bobbi barista punya aksi berbeda di tiap meja saat berhenti: 1 terima berkas, 2 merapikan (menyortir), 3 poster laporan (batang grafik tumbuh), 4 tanda tangan (pena + centang).
- PR: "Alur kerja" bergaya meja pesan (Kirim di sini → Saya racik → Ambil di sini → Cek, lalu bayar), memisahkan tugas Anda/saya + waktu, karakter original "Bobbi barista" (SVG) berjalan mengikuti kursor (desktop) / scroll (HP) dan meja terdekat menyala. Di beranda & Tentang (menggantikan Cara kerja lama). Langkah 2 menautkan repo pipeline + tanggal jalan terakhir (live).
- PR: Beranda lebih jelas dalam 5 detik: label "ini apa", judul manfaat, harga mulai + lama pengerjaan (otomatis dari paket.yml), "Dikerjakan langsung oleh Bobbi" + foto, contoh dashboard di kanan (ganti titik dekorasi), strip "Yang bisa saya bantu" (3 paket + template saat live). Urutan: hero → layanan → contoh → masalah.
- PR: Ikon kecil satu warna (Simple Icons CC0 + Lucide) di kolom Hubungi & Temukan kami footer dan halaman Kontak. Data ikon di `src/data/ikon.yml`, macro `ikon()`.
- PR: Footer: kolom Hubungi & Temukan kami urut A-Z otomatis, GitHub dihapus, WhatsApp ditambahkan di kolom Contact versi EN.
- PR: Bagian ajakan kontak besar di bawah Beranda/Tentang/Layanan dihapus (sudah ada halaman Kontak + footer). Macro `kontak_utama`, teks `utama.kontak`, CSS `.page2` dan parallax-nya ikut dihapus.
- PR: Perbaikan footer jatuh jadi 1 kolom di desktop (aturan grid CSS tidak sah), sekarang 4 kolom.
- PR: Website jadi beberapa halaman: Beranda (lebih pendek), Tentang (/tentang/, /en/about/), Layanan (/layanan/, /en/services/), Kontak (/kontak/, /en/contact/). Menu Tentang · Layanan · Kontak. "Temukan kami" (Etsy, Instagram, TikTok, LinkedIn, Upwork) di halaman Kontak + footer; akun kosong otomatis tersembunyi. build.py: URL beda per bahasa + meta per halaman dari i18n `halaman`. home.js aman di halaman tanpa kanvas.
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
