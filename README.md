# Kemang Data: website

Sumber website [kemangdata.my.id](https://kemangdata.my.id).

**Cara mengubah yang paling sering:**

| Mau ubah | Edit file |
|---|---|
| Harga atau isi paket | `src/data/paket.yml` |
| Nomor WhatsApp, email, link Upwork/LinkedIn | `src/data/site.yml` |
| Teks halaman | `src/pages/...` (halaman utama: `src/pages/index.html`, Inggris: `src/pages/en/index.html`) |
| Header, footer, tombol WA | `src/layouts/macros.html` |
| Warna, ukuran, tata letak | `assets/css/style.css` |

Setiap PR otomatis dirakit dan dicek oleh GitHub Actions. Setelah di-merge ke `main`, website tayang dalam 1–2 menit.

Detail struktur dan aturan: [CLAUDE.md](CLAUDE.md). Riwayat perubahan: [CHANGELOG.md](CHANGELOG.md).
