"""Gambar Bobbi barista (karakter ORIGINAL Kemang Data) untuk bagian Alur kerja.

    python tools/gen_barista.py        # tulis ulang SVG Bobbi di src/layouts/macros.html, lalu python build.py

Semua pose dibangun dari bagian tubuh yang sama (KAKI, BADAN, KEPALA, lengan, tangan), jadi ubah warna/bentuk
di sini sekali dan semua pose ikut berubah. Hasil ditulis di antara penanda BOBBI:MULAI dan BOBBI:SELESAI
di macros.html (macro cara_kerja). Jangan edit SVG di macros.html langsung.

Pose: aksi1 terima berkas, aksi2 merapikan, aksi3 poster laporan, aksi4 tanda tangan (dipilih saat Bobbi berhenti
di meja 1-4), b-samping = berjalan (hadap kiri; hadap kanan dicerminkan lewat CSS). Animasi kecil tiap aksi
(class a1-kertas, a2-kiri/kanan, a3-bar, a4-pena/centang) ada di assets/css/style.css; logika gerak di
assets/js/alur-kerja.js. viewBox semua pose "-10 0 80 100", koordinat badan 0-60.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MACROS = ROOT / "src" / "layouts" / "macros.html"
MULAI, SELESAI = "{#- BOBBI:MULAI (dibuat tools/gen_barista.py) -#}", "{#- BOBBI:SELESAI -#}"

# Warna: kulit, rambut, baju, celana, sepatu, celemek teal, kuning logo
SKIN, SKIN2, HAIR, SHIRT, SHIRT2, PANTS, SHOE, TEAL, YEL = "#F2C29B", "#E9B48A", "#23262E", "#33415E", "#2A364F", "#1F2A44", "#0B1220", "#0E7C7B", "#F2C811"

KAKI = (f'<rect x="21" y="78" width="7" height="17" rx="3" fill="{PANTS}"/><rect x="32" y="78" width="7" height="17" rx="3" fill="{PANTS}"/>'
        f'<rect x="18" y="93" width="11" height="5" rx="2.5" fill="{SHOE}"/><rect x="31" y="93" width="11" height="5" rx="2.5" fill="{SHOE}"/>')
BADAN = (f'<rect x="15" y="41" width="30" height="41" rx="11" fill="{SHIRT}"/><rect x="26" y="34" width="8" height="8" rx="2" fill="{SKIN2}"/>'
         f'<path d="M21 47h18v32a4 4 0 0 1-4 4H25a4 4 0 0 1-4-4z" fill="{TEAL}"/>'
         f'<path d="M21 47l-3-5M39 47l3-5" stroke="{TEAL}" stroke-width="2.4" stroke-linecap="round"/>'
         '<circle cx="27" cy="74" r="1.5" fill="#fff"/><circle cx="30" cy="74" r="1.5" fill="#fff"/><circle cx="30" cy="71" r="1.5" fill="#fff"/>'
         f'<circle cx="33" cy="74" r="1.5" fill="#fff"/><circle cx="33" cy="71" r="1.5" fill="#fff"/><circle cx="33" cy="68" r="1.5" fill="{YEL}"/>')
KEPALA = (f'<circle cx="30" cy="23" r="13" fill="{SKIN}"/>'
          f'<path d="M17 22c0-9 6-14 13-14s13 5 13 13c-3-3-7-5-11-5-5 0-10 2-15 6z" fill="{HAIR}"/>'
          f'<circle cx="25" cy="25" r="1.7" fill="{HAIR}"/><circle cx="35" cy="25" r="1.7" fill="{HAIR}"/>'
          f'<path d="M26 30c2.4 2 5.6 2 8 0" fill="none" stroke="{HAIR}" stroke-width="1.5" stroke-linecap="round"/>'
          '<circle cx="22" cy="29" r="2" fill="#F08F7A" opacity=".45"/><circle cx="38" cy="29" r="2" fill="#F08F7A" opacity=".45"/>')
KEPALA_FOKUS = KEPALA.replace('cy="25" r="1.7"', 'cy="26" r="1.7"')  # melihat ke bawah (merapikan, tanda tangan)


def lengan(x1, y1, x2, y2, warna=SHIRT):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{warna}" stroke-width="7" stroke-linecap="round"/>'


def tangan(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3.6" fill="{SKIN2}"/>'


def kertas(x, y, w, h, warna, rot=0, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<g{c} transform="rotate({rot} {x + w / 2} {y + h / 2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="#fff" stroke="#C9D1DC" stroke-width=".8"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="3" rx="1.5" fill="{warna}"/>'
            f'<path d="M{x + 2.5} {y + 6.5}h{w - 5}M{x + 2.5} {y + 9.5}h{w - 8}" stroke="#C9D1DC" stroke-width="1"/></g>')


def svg(cls, isi):
    return f'<svg class="{cls}" viewBox="-10 0 80 100">{isi}</svg>'


# 1. Terima berkas: tumpukan 3 berkas (kasir, GoFood, Shopee) di depan dada, naik-turun
AKSI1 = svg("b-aksi1", KAKI + BADAN + KEPALA
            + lengan(17, 47, 20, 60) + lengan(43, 47, 40, 60)
            + '<g class="a1-kertas">' + kertas(15, 49, 22, 16, TEAL, -8) + kertas(21, 47, 22, 16, "#E07A3F", 5) + kertas(18, 51, 22, 16, YEL, -1) + '</g>'
            + tangan(18, 61) + tangan(42, 61))
# 2. Rapikan: kertas di dua tangan bergantian naik-turun (menyortir)
AKSI2 = svg("b-aksi2", KAKI + BADAN + KEPALA_FOKUS
            + '<g class="a2-kiri">' + lengan(16, 47, 6, 56) + kertas(-6, 46, 14, 11, TEAL, -10) + tangan(6, 57) + '</g>'
            + '<g class="a2-kanan">' + lengan(44, 47, 54, 56) + kertas(52, 46, 14, 11, YEL, 10) + tangan(54, 57) + '</g>')
# 3. Poster laporan: papan grafik di depan dada, batang tumbuh (yang merah = channel margin tipis)
AKSI3 = svg("b-aksi3", KAKI + BADAN + KEPALA
            + lengan(17, 47, 9, 50) + lengan(43, 47, 51, 50)
            + '<rect x="4" y="44" width="52" height="34" rx="3" fill="#fff" stroke="#C9D1DC" stroke-width="1"/>'
            + f'<rect x="4" y="44" width="52" height="5" rx="2" fill="{TEAL}"/>'
            + '<path d="M10 73h40" stroke="#C9D1DC" stroke-width="1"/>'
            + f'<rect class="a3-bar" x="13" y="53" width="8" height="20" fill="{TEAL}"/>'
            + '<rect class="a3-bar" x="26" y="58" width="8" height="15" fill="#7FC4C0"/>'
            + '<rect class="a3-bar a3-merah" x="39" y="63" width="8" height="10" fill="#D9534F"/>'
            + tangan(7, 50) + tangan(53, 50))
# 4. Tanda tangan: papan klip di tangan kiri, pena di tangan kanan bergerak, centang muncul
AKSI4 = svg("b-aksi4", KAKI + BADAN + KEPALA_FOKUS
            + lengan(17, 47, 14, 62)
            + '<rect x="10" y="48" width="26" height="30" rx="2.5" fill="#8A6A4A"/>'
            + '<rect x="13" y="52" width="20" height="24" rx="1" fill="#fff"/>'
            + '<rect x="18" y="46.5" width="10" height="4" rx="1.5" fill="#B8BFC9"/>'
            + '<path d="M15.5 57h15M15.5 60.5h11" stroke="#C9D1DC" stroke-width="1"/>'
            + f'<path class="a4-centang" d="M17 68l3.5 3.5 7-7" fill="none" stroke="{TEAL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            + tangan(14, 63)
            + '<g class="a4-pena">' + lengan(43, 47, 33, 62) + '<path d="M30 70l6-9" stroke="#101B2D" stroke-width="2" stroke-linecap="round"/>' + tangan(34, 63) + '</g>')

# Jalan (hadap kiri; hadap kanan = dicerminkan lewat CSS)
SAMPING = svg("b-samping",
              f'<g class="kaki-a"><rect x="25" y="78" width="7" height="17" rx="3" fill="{PANTS}" transform="rotate(18 28 78)"/>'
              f'<rect x="27" y="92" width="11" height="5" rx="2.5" fill="{SHOE}" transform="rotate(18 28 78)"/></g>'
              f'<g class="kaki-b"><rect x="25" y="78" width="7" height="17" rx="3" fill="{PANTS}" transform="rotate(-16 28 78)"/>'
              f'<rect x="17" y="92" width="11" height="5" rx="2.5" fill="{SHOE}" transform="rotate(-16 28 78)"/></g>'
              f'<rect x="19" y="41" width="22" height="41" rx="10" fill="{SHIRT}"/><rect x="26" y="34" width="8" height="8" rx="2" fill="{SKIN2}"/>'
              f'<path d="M19 48h9v31a4 4 0 0 1-4 4h-1a4 4 0 0 1-4-4z" fill="{TEAL}"/>'
              f'<circle cx="23" cy="66" r="1.5" fill="#fff"/><circle cx="23" cy="62" r="1.5" fill="{YEL}"/>'
              + lengan(29, 47, 22, 66, SHIRT2) + tangan(21, 68)
              + f'<circle cx="29" cy="23" r="13" fill="{SKIN}"/>'
              f'<path d="M17 18c3-8 10-11 16-9 6 2 10 8 9 16-2-4-5-7-9-8-5-2-11-1-16 1z" fill="{HAIR}"/>'
              f'<path d="M16 24l-3 2 3 1" fill="{SKIN}" stroke="{SKIN}"/><circle cx="21" cy="24" r="1.7" fill="{HAIR}"/>'
              f'<path d="M18 30c2 1.4 4 1.4 6 .4" fill="none" stroke="{HAIR}" stroke-width="1.5" stroke-linecap="round"/>'
              '<circle cx="24" cy="28.5" r="2" fill="#F08F7A" opacity=".45"/>')



def main():
    s = MACROS.read_text(encoding="utf-8")
    blok = MULAI + '<div class="ak-barista" data-pose="aksi1">' + AKSI1 + AKSI2 + AKSI3 + AKSI4 + SAMPING + "</div>" + SELESAI
    if MULAI in s:
        s = re.sub(re.escape(MULAI) + ".*?" + re.escape(SELESAI), lambda m: blok, s, count=1, flags=re.S)
    else:  # pertama kali: ganti div Bobbi lama lalu pasang penanda
        i = s.index('<div class="ak-barista"')
        j = s.index("</div></div>", i) + len("</div>")
        s = s[:i] + blok + s[j:]
    MACROS.write_text(s, encoding="utf-8")
    print("OK: Bobbi barista ditulis ke", MACROS.relative_to(ROOT), "-> jalankan python build.py")


if __name__ == "__main__":
    main()
