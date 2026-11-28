"""Karakter ORIGINAL Kemang Data (gaya kartun lembut): Bobbi (analis data, dari foto: wajah lonjong, rambut pendek rapi,
alis tebal, kulit sawo matang, kaos hitam + lanyard ID Kemang Data) dan pemilik kedai (celemek). Satu sumber untuk:
  - panggung animasi hero (4 adegan, 12 detik)     -> macro panggung_hero() di src/layouts/macros.html
  - Bobbi di bagian Alur kerja (aksi meja 1-4 + jalan) -> blok KARAKTER:ALUR di macro cara_kerja
  - CSS animasinya                                  -> blok KARAKTER:CSS di assets/css/style.css

    python tools/gen_karakter.py && python build.py

Ubah warna/bentuk di sini, JANGAN edit SVG di macros.html langsung. Teks (papan adegan, nama tokoh, aria-label)
diambil dari i18n: utama.cara_kerja.langkah[].papan dan utama.hero.tokoh_klien / tokoh_bobbi / animasi_alt.
viewBox semua pose "0 0 100 160". Kelas animasi diawali "k-" (karakter) dan "pg-" (panggung) supaya tidak bentrok.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MACROS = ROOT / "src" / "layouts" / "macros.html"
STYLE = ROOT / "assets" / "css" / "style.css"

INK = "#23262E"
BOBBI = dict(kulit="#DDA984", kulit2="#CC966F", hidung="#B57A55", rambut="#1E1C1F", pipi="#E0715C",
             baju="#1F2124", celana="#3A4358", sepatu="#15171B")
KLIEN = dict(kulit="#D9A07A", kulit2="#C98E68", hidung="#B9805C", rambut="#3B2A22", pipi="#E0715C",
             baju="#E07A3F", celana="#2E3A52", sepatu="#1B2130")
TEAL, YEL = "#0E7C7B", "#F2C811"


# ---------------------------------------------------------------- bagian tubuh
def rambut_bobbi():
    """Quiff (referensi Bobbi): rambut depan naik & tersapu ke kanan Bobbi (= kiri layar), ujung bergumpal bulat,
    sejumput jatuh di dahi, cambang pendek meruncing di dalam garis wajah. Digambar menghadap kanan layar lalu dicerminkan.
    TURUN = puncak diturunkan dari tinggi referensi (lebih kalem). Kelas rb/rh = warna mode gelap."""
    TURUN = 6

    def y(v):
        return round(v + TURUN * (26 - v) / 17, 2) if v < 26 else v
    r = BOBBI["rambut"]
    cermin = '<g transform="matrix(-1 0 0 1 100 0)">'
    belakang = f'{cermin}<path class="rb" d="M27 44C25.5 33 32 {y(23)} 50 {y(21)}C68 {y(23)} 74.5 33 73 44Z" fill="{r}"/></g>'
    quiff = (f'<path class="rb" d="M28.6 46.2L26.4 45.8C26 40.5 26.5 35 28.2 31C29.8 {y(27)} 32.4 {y(23.4)} 36 {y(21)}'
             f'C39 {y(15)} 48 {y(11.5)} 56 {y(13)}C60 {y(13.8)} 63 {y(15.5)} 64 {y(18.5)}C61.5 {y(17)} 59 {y(16.8)} 57 {y(17.5)}'
             f'C62 {y(14.5)} 67.5 {y(15.5)} 69.6 {y(19.5)}C71.6 {y(22.5)} 72.8 27 73.2 31C73.6 35.5 73.9 40 73.6 45.8L71.4 46.2'
             f'C71.4 43.6 71.2 41.4 70.6 39.8C68.6 37 64 35.6 58 35.8C52 36 47 37 44 38.5C42 39.5 41 41 41.2 43'
             f'C39.6 41.8 39 40 38.6 38.8C35 39 31.4 39.6 29.4 40.4C28.9 42.2 28.6 44.2 28.6 46.2Z" fill="{r}"/>')
    kilap = (f'<path class="rh" d="M39.5 28.5C41.5 {y(22.5)} 45.5 {y(18.5)} 50.5 {y(16.8)}C46.2 {y(19.6)} 42.8 {y(23.2)} 40.2 28.8Z'
             f'M55.5 27C57.5 {y(23)} 60.5 {y(20.4)} 64.5 {y(19.4)}C61.2 {y(21.4)} 58.6 {y(24)} 56.2 27.3Z" fill="#55525C"/>')
    return belakang, f"{cermin}{quiff}{kilap}</g>"


def latar_kantor():
    """Latar kantor ORIGINAL di belakang panggung hero (pucat supaya karakter menonjol; area di belakang kepala tenang).
    viewBox 560x372 = dinding di atas lantai. Warna lewat class lk-* (ada versi mode gelap di CSS)."""
    s = ['<svg viewBox="0 0 560 372" preserveAspectRatio="xMidYMax slice" aria-hidden="true">']
    s.append('<rect class="lk-kaca" x="170" y="34" width="220" height="230" rx="4"/>')
    for x, w, h in ((178, 26, 110), (206, 22, 150), (230, 30, 90), (262, 24, 175), (288, 34, 125), (324, 22, 160), (348, 30, 100), (380, 10, 135)):
        s.append(f'<rect class="lk-gedung" x="{x}" y="{264 - h}" width="{w}" height="{h}"/>')
    s.append('<path class="lk-bingkai" d="M170 34h220v230H170zM243 34v230M317 34v230M170 110h220M170 188h220" fill="none" stroke-width="5"/>')
    for x in (215, 345):  # lampu gantung
        s.append(f'<path class="lk-tali" d="M{x} 0v24" stroke-width="2"/><path class="lk-gelap" d="M{x - 13} 42q13-20 26 0z"/>'
                 f'<circle cx="{x}" cy="43" r="3" fill="{YEL}" opacity=".7"/>')
    s.append('<circle class="lk-jam" cx="470" cy="44" r="20" stroke-width="3.5"/><path class="lk-jarum" d="M470 32v12l8 5" fill="none" stroke-width="2.6" stroke-linecap="round"/>')
    s.append('<rect class="lk-gelap" x="8" y="150" width="56" height="222" rx="2"/>')
    for y in (205, 262, 318):
        s.append(f'<rect class="lk-rak" x="11" y="{y}" width="50" height="4"/>')
    s.append(f'<rect x="16" y="186" width="7" height="19" fill="{TEAL}" opacity=".45"/><rect x="25" y="190" width="6" height="15" fill="{YEL}" opacity=".5"/>'
             '<rect class="lk-sedang" x="33" y="184" width="8" height="21"/><rect class="lk-sedang" x="20" y="298" width="26" height="20"/>'
             f'<rect x="45" y="246" width="10" height="16" fill="{TEAL}" opacity=".35"/>')
    s.append('<rect class="lk-bingkai2" x="70" y="40" width="74" height="46" rx="2" stroke-width="3"/>')
    s.append(f'<path d="M78 76l14-12 12 7 14-14 18-4" fill="none" stroke="{TEAL}" stroke-width="2.6" opacity=".55" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append('<rect class="lk-sedang" x="205" y="318" width="150" height="9" rx="2"/><rect class="lk-gelap" x="214" y="327" width="9" height="45"/><rect class="lk-gelap" x="337" y="327" width="9" height="45"/>'
             '<rect class="lk-gelap" x="246" y="264" width="66" height="44" rx="3"/><rect class="lk-layar" x="250" y="268" width="58" height="36" rx="2"/>'
             f'<rect x="257" y="285" width="8" height="15" fill="{TEAL}" opacity=".7"/><rect x="268" y="277" width="8" height="23" fill="{TEAL}" opacity=".7"/>'
             f'<rect x="279" y="289" width="8" height="11" fill="{YEL}" opacity=".8"/><rect x="290" y="281" width="8" height="19" fill="{TEAL}" opacity=".5"/>'
             '<rect class="lk-gelap" x="275" y="308" width="8" height="10"/>'
             f'<rect class="lk-sedang" x="326" y="300" width="13" height="18" rx="2"/><path d="M332 300c-8-10-4-20 1-22 3 9 2 16-1 22zm1 0c4-10 10-13 14-11-2 7-8 11-14 11z" fill="{TEAL}" opacity=".55"/>')
    s.append("</svg>")
    return "".join(s)


KEPALA_SKALA = .82  # proporsi kepala (1 = gaya chibi lama). Diperkecil supaya tidak terlihat kekanakan


def _kepala_kecil(svg, cx=50, cy=84):
    """Perkecil kepala dengan pusat di dagu (leher tetap tersambung)."""
    return f'<g transform="translate({cx} {cy}) scale({KEPALA_SKALA}) translate({-cx} {-cy})">{svg}</g>'


def kepala_bobbi(o, ekspresi="senyum"):
    """Bobbi (dari foto formal): wajah lonjong, rambut side part disapu ke kanan + undercut, alis melengkung halus,
    kumis tipis samar. Rambut 2 lapis (isi kubah di balik wajah + sapuan depan) supaya tidak ada celah."""
    r, s = o["rambut"], []
    belakang, depan = rambut_bobbi()
    s.append(belakang)
    s.append(f'<ellipse cx="25.5" cy="58" rx="5" ry="7" fill="{o["kulit2"]}"/><ellipse cx="74.5" cy="58" rx="5" ry="7" fill="{o["kulit2"]}"/>')
    s.append(f'<path d="M50 26c15 0 25 11 25 27 0 19-11 33-25 33S25 72 25 53c0-16 10-27 25-27z" fill="{o["kulit"]}"/>')
    s.append(depan)
    s.append(f'<path d="M35 47.8q5.5-1.6 11 0M54 47.8q5.5-1.6 11 0" fill="none" stroke="{r}" stroke-width="3.2" stroke-linecap="round"/>')
    if ekspresi == "senang":
        s.append(f'<path d="M36 58q4.5-5 9 0M55 58q4.5-5 9 0" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    else:
        dy = 1.6 if ekspresi == "fokus" else 0
        for x in (40.5, 59.5):
            s.append(f'<ellipse cx="{x}" cy="57" rx="4.2" ry="4.8" fill="#fff"/><circle cx="{x + .4}" cy="{58 + dy}" r="3" fill="{INK}"/>'
                     f'<circle cx="{x + 1.4}" cy="{56.7 + dy}" r="1" fill="#fff"/>')
    s.append(f'<path d="M50 60q-2.2 7 1.2 8" fill="none" stroke="{o["hidung"]}" stroke-width="2" stroke-linecap="round"/>')
    s.append(f'<path d="M44 72.5q6 1.6 12 0" fill="none" stroke="{r}" stroke-width="1.3" opacity=".22" stroke-linecap="round"/>')
    if ekspresi == "senang":
        s.append('<path d="M42 75q8 11 16 0z" fill="#8C2F39"/><path d="M45 78q5 4 10 0z" fill="#E9787A"/>')
    elif ekspresi == "fokus":
        s.append('<path d="M45.5 76q4.5 2 9 0" fill="none" stroke="#8C2F39" stroke-width="2.2" stroke-linecap="round"/>')
    else:
        s.append('<path d="M44 75q6 6.5 12 0z" fill="#8C2F39"/><path d="M46 76.8q4 2.6 8 0z" fill="#E9787A"/>')
    return _kepala_kecil("".join(s))


def kepala(o, siapa, ekspresi="senyum"):
    if siapa == "bobbi":
        return kepala_bobbi(o, ekspresi)
    s = []
    # pemilik kedai: sanggul + rambut samping
    # kuncir kuda di belakang kepala (terlihat di sisi kanan) + ikat rambut
    s.append(f'<path d="M66 28C80 18 94 28 93 46C92 60 86 70 80 76C83 64 83 54 78 46C75 41 71 38 67 37Z" fill="{o["rambut"]}"/>'
             '<path d="M80 30C87 34 89 44 87 54" fill="none" stroke="#5A4336" stroke-width="1.3" stroke-linecap="round"/>'
             f'<ellipse cx="68" cy="31" rx="3.4" ry="4.6" fill="{TEAL}" transform="rotate(35 68 31)"/>')
    s.append(f'<path d="M21 60c-4-26 10-38 29-38s33 12 29 38c-3 6-6 9-9 10l1-14c-6-8-16-11-21-11s-15 3-21 11l1 14c-3-1-6-4-9-10z" fill="{o["rambut"]}"/>')
    s.append(f'<ellipse cx="24" cy="56" rx="5.5" ry="7.5" fill="{o["kulit2"]}"/><ellipse cx="76" cy="56" rx="5.5" ry="7.5" fill="{o["kulit2"]}"/>')
    s.append(f'<ellipse cx="50" cy="55" rx="27" ry="29" fill="{o["kulit"]}"/>')
    s.append(f'<path d="M23 55c-2-19 10-31 27-31s29 12 27 31c-4-8-11-13-19-15-3 5-10 7-17 7-8 0-14 3-18 8z" fill="{o["rambut"]}"/>')
    alis_y = 43 if ekspresi == "senang" else 45
    alis = "M34 46.5q6-1 12-4.5M54 42q6 3.5 12 4.5" if ekspresi == "bingung" else f"M34 {alis_y}q6-4 12 0M54 {alis_y}q6-4 12 0"  # bingung: ujung dalam naik
    s.append(f'<path d="{alis}" fill="none" stroke="{o["rambut"]}" stroke-width="2.8" stroke-linecap="round"/>')
    if ekspresi == "senang":  # mata tersenyum ^^
        s.append(f'<path d="M35.5 56q4.5-5 9 0M55.5 56q4.5-5 9 0" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    else:
        dy = 1.6 if ekspresi == "fokus" else 0
        for x in (40, 60):
            s.append(f'<ellipse cx="{x}" cy="55" rx="4.4" ry="5.2" fill="#fff"/><circle cx="{x + .5}" cy="{56 + dy}" r="3.1" fill="{INK}"/>'
                     f'<circle cx="{x + 1.6}" cy="{54.6 + dy}" r="1.1" fill="#fff"/>')
        if siapa == "klien":
            s.append(f'<path d="M35 52l-2.5-2M65 52l2.5-2" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')
    s.append(f'<path d="M50 59q-2.5 5 1 6" fill="none" stroke="{o["hidung"]}" stroke-width="2" stroke-linecap="round"/>')
    if ekspresi == "senang":
        s.append('<path d="M40 67q10 13 20 0z" fill="#8C2F39"/><path d="M43 71q7 6 14 0z" fill="#E9787A"/>')
    elif ekspresi == "fokus":
        s.append('<path d="M45 70q5 3 10 0" fill="none" stroke="#8C2F39" stroke-width="2.2" stroke-linecap="round"/>')
    elif ekspresi == "bingung":  # mulut bergelombang
        s.append('<path d="M43 71q2.3-2.4 4.6 0t4.6 0t4.6 0" fill="none" stroke="#8C2F39" stroke-width="2.2" stroke-linecap="round"/>')
    else:
        s.append('<path d="M42 68q8 9 16 0z" fill="#8C2F39"/><path d="M44.5 70.5q5.5 4 11 0z" fill="#E9787A"/>')
    if siapa == "klien":
        s.append(f'<circle cx="23" cy="66" r="2" fill="{YEL}"/><circle cx="77" cy="66" r="2" fill="{YEL}"/>')
    return _kepala_kecil("".join(s))


def kaki(o):
    return (f'<rect x="37" y="132" width="11" height="20" rx="4" fill="{o["celana"]}"/><rect x="52" y="132" width="11" height="20" rx="4" fill="{o["celana"]}"/>'
            f'<rect x="33" y="148" width="16" height="7" rx="3.5" fill="{o["sepatu"]}"/><rect x="51" y="148" width="16" height="7" rx="3.5" fill="{o["sepatu"]}"/>')


def badan(o, siapa):
    s = [f'<rect x="44" y="78" width="12" height="12" rx="3" fill="{o["kulit2"]}"/>',
         f'<rect x="28" y="86" width="44" height="52" rx="16" fill="{o["baju"]}"/>']
    if siapa == "bobbi":  # kaos hitam + lanyard kuning + ID card logo Kemang Data
        # leher digambar DI ATAS kaos (menyambung dari dagu ke kerah, tanpa garis hitam di antaranya)
        s.append(f'<path d="M44 78h12v9q-6 6-12 0z" fill="{o["kulit2"]}"/><path d="M42 86.5q8 8 16 0z" fill="{o["kulit2"]}"/>')
        s.append(f'<path d="M40 89l10 25 10-25" fill="none" stroke="{YEL}" stroke-width="2.6"/>')
        s.append('<rect x="43" y="112" width="14" height="18" rx="2" fill="#fff"/>')
        for cx, cy, c in ((47, 125, TEAL), (50.5, 125, TEAL), (50.5, 121.5, TEAL), (54, 125, TEAL), (54, 121.5, TEAL), (54, 118, YEL)):
            s.append(f'<circle cx="{cx}" cy="{cy}" r="1.5" fill="{c}"/>')
    else:  # celemek krem pemilik kedai
        s.append('<path d="M35 98h30v34a6 6 0 0 1-6 6H41a6 6 0 0 1-6-6z" fill="#EADBB9"/>'
                 '<path d="M35 98l-4-9M65 98l4-9" stroke="#EADBB9" stroke-width="3.4" stroke-linecap="round"/>'
                 '<rect x="42" y="112" width="16" height="10" rx="2" fill="#DCCBA4"/>')
    return "".join(s)


def lengan(o, x1, y1, x2, y2):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{o["baju"]}" stroke-width="11" stroke-linecap="round"/>'


def tangan(o, x, y):
    return f'<circle cx="{x}" cy="{y}" r="5.5" fill="{o["kulit2"]}"/>'


def kertas(x, y, w, h, warna, rot=0):
    return (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#fff" stroke="#C9D1DC"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="4.5" rx="2" fill="{warna}"/>'
            f'<path d="M{x + 4} {y + 10}h{w - 8}M{x + 4} {y + 15}h{w - 12}" stroke="#C9D1DC" stroke-width="1.6"/></g>')


def svg(isi, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 100 160" aria-hidden="true" focusable="false">{isi}</svg>'


# ---------------------------------------------------------------- pose
def kepala_samping(o, siapa):
    """Tampak samping (menghadap kanan): satu mata, hidung menonjol. Pemilik kedai: sanggul + anting. Bobbi: quiff."""
    r = o["rambut"]
    if siapa == "bobbi":
        # quiff tampak samping: satu massa bervolume (bukan selembar), naik di depan dengan ujung membulat, setinggi tampak depan
        rambut = (f'<path d="M30 58C24 48 23 35 31 27C37 21 45 19 53 19C59 14 69 12 76 15C82 18 85 24 82 30C80 34 78 37 76 41'
                  f'C70 38 64 37 58 38C53 39 50 43 49 48V55C46 56 43 56 41 54C40 50 39 47 37 46C35 50 33 55 30 58Z" fill="{r}"/>'
                  '<path d="M41 25C50 20 61 18 71 20M47 31C55 27 64 26 73 28" fill="none" stroke="#3A3740" stroke-width="1.5" stroke-linecap="round"/>')
        alis, hiasan = 3.4, ""
    else:
        # rambut turun sampai tengkuk + garis helaian disisir ke belakang
        rambut = (f'<path d="M26 64C21 38 34 24 54 24C68 24 77 33 78 45C72 40 64 38 56 39C50 40 46 44 45 50C44 58 41 66 37 74C33 75 29 71 26 64Z" fill="{r}"/>'
                  '<path d="M70 33C58 26 44 27 33 33M66 38C56 34 44 34 34 36M58 43C50 40 42 39 35 39" fill="none" stroke="#5A4336" stroke-width="1.3" stroke-linecap="round"/>')
        alis, hiasan = 2.8, f'<circle cx="45" cy="67" r="2" fill="{YEL}"/>'
    # sanggul: dua gulungan + ikat rambut + helaian (tampak samping, di belakang atas kepala)
    # kuncir kuda: diikat di belakang atas kepala, melengkung lalu jatuh ke bawah (dengan helaian)
    sanggul = (f'<path d="M33 31C24 20 9 22 6 36C3 50 9 64 19 74C18 64 19 53 23 46C26 41 29 38 33 37Z" fill="{r}"/>'
               '<path d="M27 29C17 28 11 37 11 48M28 34C21 36 17 44 17 54" fill="none" stroke="#5A4336" stroke-width="1.3" stroke-linecap="round"/>'
               f'<ellipse cx="32" cy="34" rx="3.4" ry="5" fill="{TEAL}" transform="rotate(-20 32 34)"/>') if siapa != "bobbi" else ""
    return _kepala_kecil(sanggul + f'<ellipse cx="52" cy="55" rx="25" ry="29" fill="{o["kulit"]}"/><path d="M77 55q5.5 4 .6 9.5" fill="{o["kulit"]}"/>' + rambut
            + f'<ellipse cx="45" cy="58" rx="4.6" ry="6.6" fill="{o["kulit2"]}"/>' + hiasan
            + f'<path d="M60 47q5.5-3.6 11 0" fill="none" stroke="{r}" stroke-width="{alis}" stroke-linecap="round"/>'
            + f'<ellipse cx="66" cy="56" rx="3.8" ry="4.8" fill="#fff"/><circle cx="67.6" cy="57" r="2.7" fill="{INK}"/><circle cx="68.4" cy="55.8" r=".9" fill="#fff"/>'
            + '<path d="M64.5 70.5q4.5 3.4 9 0" fill="none" stroke="#8C2F39" stroke-width="2.2" stroke-linecap="round"/>')


def badan_samping(o, siapa):
    """Badan tampak samping: ramping. Pemilik kedai: celemek di depan. Bobbi: kaos + lanyard + ID card."""
    s = (f'<rect x="46" y="78" width="11" height="12" rx="3" fill="{o["kulit2"]}"/>'
         f'<rect x="39" y="86" width="26" height="52" rx="11" fill="{o["baju"]}"/>')
    if siapa == "bobbi":
        return s + f'<path d="M53 87l7 20" stroke="{YEL}" stroke-width="2.4"/><rect x="56" y="105" width="9" height="12" rx="1.5" fill="#fff"/>'
    return s + '<path d="M58 97h8v35a5 5 0 0 1-5 5h-3z" fill="#EADBB9"/>'


def langkah_samping(o, maju):
    """Satu fase langkah tampak samping. maju=True: fase MELANGKAH (kaki terbuka lebar, tangan ke depan).
    maju=False: fase MELINTAS (kaki rapat, satu kaki terangkat, tangan ke belakang). Dua fase harus beda bentuk,
    karena kedua kaki sewarna: menukar kaki depan/belakang saja tidak terlihat bergerak."""
    def kaki_(sudut, angkat=0):
        return (f'<g transform="translate(0 {-angkat}) rotate({sudut} 51.5 131)"><rect x="46" y="130" width="11" height="19" rx="4" fill="{o["celana"]}"/>'
                f'<rect x="45" y="145" width="18" height="7" rx="3.5" fill="{o["sepatu"]}"/></g>')
    if maju:
        return kaki_(24) + kaki_(-26), lengan(o, 52, 95, 66, 121) + tangan(o, 67, 123)
    return kaki_(3) + kaki_(-10, 5), lengan(o, 52, 95, 42, 122) + tangan(o, 41, 124)


def pose(o, siapa, aksi, cls=""):
    k, B = kaki(o), badan(o, siapa)
    if aksi == "lambai":
        isi = (k + B + lengan(o, 31, 94, 26, 126) + tangan(o, 26, 128)
               + kepala(o, siapa) + '<g class="k-lambai">' + lengan(o, 69, 94, 92, 80) + tangan(o, 96, 76) + '</g>')
    elif aksi == "berkas":
        isi = (k + B + lengan(o, 31, 94, 36, 118) + lengan(o, 69, 94, 64, 118)
               + '<g class="k-naik">' + kertas(27, 100, 36, 26, TEAL, -8) + kertas(37, 98, 36, 26, "#E07A3F", 6) + kertas(32, 103, 36, 26, YEL, -1) + '</g>'
               + tangan(o, 34, 120) + tangan(o, 66, 120) + kepala(o, siapa))
    elif aksi == "laptop":
        isi = (k + B + '<g class="k-ketik">' + lengan(o, 31, 94, 38, 120) + lengan(o, 69, 94, 62, 120) + '</g>'
               + '<rect x="18" y="96" width="64" height="34" rx="3" fill="#2b3446"/><rect x="21.5" y="99.5" width="57" height="27" rx="1.5" fill="#e8f3f1"/>'
               + f'<rect class="k-baris" x="26" y="104" width="30" height="3.6" fill="{TEAL}"/><rect class="k-baris k-b2" x="26" y="110" width="42" height="3.6" fill="#7FC4C0"/>'
               + f'<rect class="k-baris k-b3" x="26" y="116" width="24" height="3.6" fill="{YEL}"/>'
               + '<path d="M12 130h76l-6 7H18z" fill="#3a4358"/>' + tangan(o, 38, 128) + tangan(o, 62, 128) + kepala(o, siapa, "fokus"))
    elif aksi == "poster":
        isi = (k + B + lengan(o, 31, 94, 18, 100) + lengan(o, 69, 94, 82, 100)
               + '<rect x="10" y="94" width="80" height="52" rx="4" fill="#fff" stroke="#C9D1DC" stroke-width="1.4"/>'
               + f'<rect x="10" y="94" width="80" height="7" rx="3" fill="{TEAL}"/><path d="M18 139h64" stroke="#C9D1DC" stroke-width="1.4"/>'
               + f'<rect class="k-bar" x="22" y="108" width="13" height="31" fill="{TEAL}"/><rect class="k-bar" x="43" y="116" width="13" height="23" fill="#7FC4C0"/>'
               + '<rect class="k-bar k-merah" x="64" y="124" width="13" height="15" fill="#D9534F"/>'
               + tangan(o, 15, 100) + tangan(o, 85, 100) + kepala(o, siapa))
    elif aksi == "senang":
        isi = (k + B + lengan(o, 31, 94, 16, 66) + tangan(o, 14, 62) + lengan(o, 69, 94, 84, 66) + tangan(o, 86, 62)
               + '<text x="50" y="12" text-anchor="middle" font-size="14">✨</text>' + kepala(o, siapa, "senang"))
    elif aksi == "jempol":
        isi = (k + B + lengan(o, 31, 94, 26, 126) + tangan(o, 26, 128)
               + kepala(o, siapa, "senang") + lengan(o, 69, 94, 90, 84) + tangan(o, 93, 80)
               + f'<path d="M93 75v-8" stroke="{o["kulit2"]}" stroke-width="4.5" stroke-linecap="round"/>')
    elif aksi == "jalan":  # menghadap depan, 2 variasi kaki (kaki-a / kaki-b) diganti JS saat melangkah
        isi = (f'<g class="kaki-a"><rect x="36" y="132" width="11" height="20" rx="4" fill="{o["celana"]}" transform="rotate(10 42 132)"/>'
               f'<rect x="31" y="148" width="16" height="7" rx="3.5" fill="{o["sepatu"]}" transform="rotate(10 42 132)"/>'
               f'<rect x="52" y="132" width="11" height="18" rx="4" fill="{o["celana"]}"/><rect x="51" y="146" width="16" height="7" rx="3.5" fill="{o["sepatu"]}"/></g>'
               f'<g class="kaki-b"><rect x="37" y="132" width="11" height="18" rx="4" fill="{o["celana"]}"/><rect x="33" y="146" width="16" height="7" rx="3.5" fill="{o["sepatu"]}"/>'
               f'<rect x="53" y="132" width="11" height="20" rx="4" fill="{o["celana"]}" transform="rotate(-10 58 132)"/>'
               f'<rect x="53" y="148" width="16" height="7" rx="3.5" fill="{o["sepatu"]}" transform="rotate(-10 58 132)"/></g>'
               + B + lengan(o, 31, 94, 24, 124) + tangan(o, 23, 126) + lengan(o, 69, 94, 76, 124) + tangan(o, 77, 126) + kepala(o, siapa))
    elif aksi == "samping":  # berjalan tampak samping (menghadap kanan); kaki-a/kaki-b = 2 fase langkah, diganti CSS
        ka, ta = langkah_samping(o, True)
        kb, tb = langkah_samping(o, False)
        isi = (f'<g class="kaki-a">{ka}</g><g class="kaki-b">{kb}</g>' + badan_samping(o, siapa)
               + f'<g class="kaki-a">{ta}</g><g class="kaki-b">{tb}</g>' + kepala_samping(o, siapa))
    elif aksi == "pusing":  # adegan masalah: tangan memegang kepala, wajah bingung, keringat (pertanyaan di balon)
        isi = (k + B + kepala(o, siapa, "bingung")
               + lengan(o, 31, 94, 26, 66) + tangan(o, 26, 63) + lengan(o, 69, 94, 74, 66) + tangan(o, 74, 63)
               + '<path d="M75 45q4 6 0 9q-4-3 0-9z" fill="#7FC4E8"/>')
    elif aksi == "diri":  # berdiri menunggu, tangan di samping
        isi = (k + B + lengan(o, 31, 94, 26, 126) + tangan(o, 26, 128) + lengan(o, 69, 94, 74, 126) + tangan(o, 74, 128) + kepala(o, siapa))
    elif aksi == "salam":  # bersalaman: pemilik kedai menjulurkan tangan kanan ke kanan, Bobbi tangan kiri ke kiri
        if siapa == "bobbi":
            isi = (k + B + lengan(o, 69, 94, 74, 126) + tangan(o, 74, 128) + kepala(o, siapa, "senang")
                   + '<g class="k-salam">' + lengan(o, 31, 94, 14, 104) + f'<path d="M14 104L3 108" stroke="{o["kulit2"]}" stroke-width="7.5" stroke-linecap="round"/>'
                   + tangan(o, 1, 108.5) + '</g>')
        else:
            isi = (k + B + lengan(o, 31, 94, 26, 126) + tangan(o, 26, 128) + kepala(o, siapa, "senang")
                   + '<g class="k-salam">' + lengan(o, 69, 94, 86, 104) + f'<path d="M86 104L97 108" stroke="{o["kulit2"]}" stroke-width="7.5" stroke-linecap="round"/>'
                   + tangan(o, 99, 108.5) + '</g>')
    else:
        raise ValueError(aksi)
    return svg(isi, cls)


# ---------------------------------------------------------------- keluaran
def blok_alur():
    """Bobbi di Alur kerja: aksi1 terima berkas, aksi2 laptop, aksi3 poster, aksi4 jempol, b-samping = jalan."""
    poses = [pose(BOBBI, "bobbi", a, f"b-aksi{i}") for i, a in enumerate(("berkas", "laptop", "poster", "jempol"), 1)]
    poses.append(pose(BOBBI, "bobbi", "jalan", "b-samping"))
    return '<div class="ak-barista" data-pose="aksi1">' + "".join(poses) + "</div>"


def properti_masalah():
    """Adegan 0: nota berserakan di lantai + 3 HP (kasir, ojek online, marketplace) penuh notifikasi. Tanpa logo merek."""
    s = ['<svg viewBox="0 0 280 300" preserveAspectRatio="xMinYMax meet" aria-hidden="true">']
    for x, y, r in ((18, 284, -14), (70, 290, 9), (150, 286, -6), (196, 291, 15)):
        s.append(f'<g transform="rotate({r} {x + 15} {y})"><rect x="{x}" y="{y - 8}" width="30" height="16" rx="1.5" fill="#fff" stroke="#C9D1DC"/>'
                 f'<path d="M{x + 4} {y - 3}h20M{x + 4} {y + 2}h14" stroke="#C9D1DC" stroke-width="1.6"/></g>')
    for i, (x, y, warna, ikon) in enumerate(((206, 40, "#2E9E5B", "motor"), (236, 104, "#E07A3F", "tas"), (200, 160, TEAL, "nota"))):
        isi = {"motor": f'<circle cx="{x + 9}" cy="{y + 30}" r="4" fill="none" stroke="#fff" stroke-width="2"/><circle cx="{x + 23}" cy="{y + 30}" r="4" fill="none" stroke="#fff" stroke-width="2"/><path d="M{x + 9} {y + 30}l6-8h6l2 8" fill="none" stroke="#fff" stroke-width="2"/>',
               "tas": f'<rect x="{x + 8}" y="{y + 20}" width="16" height="14" rx="2" fill="#fff"/><path d="M{x + 12} {y + 20}v-3a4 4 0 0 1 8 0v3" fill="none" stroke="#fff" stroke-width="2"/>',
               "nota": f'<rect x="{x + 9}" y="{y + 16}" width="14" height="20" rx="1" fill="#fff"/><path d="M{x + 12} {y + 22}h8M{x + 12} {y + 26}h8M{x + 12} {y + 30}h5" stroke="{TEAL}" stroke-width="1.5"/>'}[ikon]
        s.append(f'<g class="k-naik" style="--d:{i * .25}s"><rect x="{x}" y="{y}" width="32" height="52" rx="5" fill="#2b3446"/>'
                 f'<rect x="{x + 3}" y="{y + 6}" width="26" height="40" rx="2" fill="{warna}"/>{isi}'
                 f'<circle cx="{x + 30}" cy="{y + 2}" r="7" fill="#D9534F"/><text x="{x + 30}" y="{y + 5.5}" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">{9 - i * 3}</text></g>')
    s.append("</svg>")
    return "".join(s)


# ---------------------------------------------------------------- cerita 3 adegan di panggung hero
# 1 kedai: pemilik kedai pusing dengan datanya -> (berjalan, latar bergeser) 2 kantor: datang ke Bobbi, serahkan data
# -> 3 kantor: Bobbi mengembalikan laporan, klien senang, lalu salaman.
DURASI = 21.5                                         # detik per putaran
ADEGAN = ((0, 5), (6.5, 14), (14, 21))                # (mulai, selesai) tiap adegan = tiap kotak di bilah langkah
ADEGAN_ATTR = ";".join(f"{a},{b}" for a, b in ADEGAN)  # untuk assets/js/panggung.js (kursor sejalan bilah langkah)
JALAN = (5, 6.5)                                      # pemilik kedai berjalan ke kantor, latar bergeser
SERAH, TERBANG, KERJA = (6.5, 8), (8, 9.4), (9.4, 14)   # adegan 2: serahkan berkas -> kertas terbang ke Bobbi -> Bobbi mengerjakan
TARA, SALAM = (14, 18.8), (18.8, 21)                  # adegan 3: dashboard muncul ("tara!"), klien senang -> salaman
LW, LH = 560, 350                                                   # viewBox latar (dinding di atas lantai)


def _pct(t):
    return round(t / DURASI * 100, 3)


def _jendela(*rentang):
    """Keyframes opacity: tampil hanya di rentang detik yang diberikan."""
    k = ["0%{opacity:0}"]
    for a, b in rentang:
        k.append(f"{_pct(a) - .01 if a else 0}%{{opacity:0}}{_pct(a)}%{{opacity:1}}{_pct(b) - .01}%{{opacity:1}}{_pct(b)}%{{opacity:0}}")
    k.append("100%{opacity:0}")
    return "".join(k)


def tanaman(pot, opasitas):
    """Tanaman pot di pojok kanan bawah latar kedai."""
    daun = "M527 300c-14-18-8-40 2-44 6 16 4 32-2 44zm2 0c8-20 22-26 30-22-4 14-16 22-30 22zm-4 0c-10-14-26-16-32-10 6 10 18 12 32 10z"
    return f'<rect x="512" y="300" width="30" height="50" rx="3" fill="{pot}"/><path d="{daun}" fill="{TEAL}" opacity="{opasitas}"/>'


def _svg_latar(isi, cls="pg-redup"):
    return f'<svg class="{cls}" viewBox="0 0 {LW} {LH}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">{isi}</svg>'


def latar_kedai():
    """Kedai kopi ORIGINAL (hangat) yang sedang kacau: nota berserakan di konter + tanaman."""
    s = [f'<rect width="{LW}" height="{LH}" fill="#F7EFE4"/><rect y="262" width="{LW}" height="88" fill="#EBDDCB"/><rect y="258" width="{LW}" height="5" fill="#D9C4AA"/>',
         '<rect x="18" y="48" width="134" height="160" rx="3" fill="#E4F0F4" stroke="#CFB596" stroke-width="5"/><path d="M85 48v160M18 128h134" stroke="#CFB596" stroke-width="4"/>'
         '<path d="M14 40h142l-8 18H22z" fill="#E07A3F" opacity=".85"/><path d="M36 40l-6 18M60 40l-4 18M84 40v18M108 40l4 18M132 40l6 18" stroke="#fff" stroke-width="5" opacity=".6"/>',
         '<rect x="200" y="36" width="160" height="104" rx="4" fill="#2F3B36" stroke="#A9784F" stroke-width="6"/>'
         '<text x="280" y="60" text-anchor="middle" font-size="15" font-weight="800" fill="#F4F1E8" font-family="sans-serif" letter-spacing="2">MENU</text>'
         '<path d="M216 76h70M216 92h58M216 108h76M216 124h50" stroke="#F4F1E8" stroke-width="3" opacity=".7" stroke-linecap="round"/>'
         '<path d="M316 76h28M322 92h22M314 108h30M324 124h20" stroke="#F2C811" stroke-width="3" opacity=".8" stroke-linecap="round"/>']
    for y in (88, 150):
        s.append(f'<rect x="398" y="{y}" width="140" height="6" rx="2" fill="#A9784F"/>')
        for i, c in enumerate(("#fff", "#E07A3F", "#fff", TEAL, "#fff")):
            s.append(f'<rect x="{406 + i * 26}" y="{y - 18}" width="16" height="18" rx="2" fill="{c}" stroke="#D9C4AA"/>')
    for x in (120, 470):
        s.append(f'<path d="M{x} 0v20" stroke="#A9784F" stroke-width="2"/><path d="M{x - 14} 40q14-22 28 0z" fill="#3B3A36"/><circle cx="{x}" cy="41" r="3.4" fill="{YEL}"/>')
    s.append('<rect x="190" y="246" width="250" height="12" rx="2" fill="#8A5A3B"/><rect x="198" y="258" width="234" height="92" fill="#B5845A"/>'
             '<path d="M276 262v84M354 262v84" stroke="#9C6E48" stroke-width="3"/>'
             '<rect x="214" y="196" width="58" height="50" rx="5" fill="#8E99A8"/><rect x="222" y="204" width="42" height="14" rx="2" fill="#5C6B7A"/>'
             '<rect x="232" y="222" width="6" height="10" fill="#3B3A36"/><rect x="248" y="222" width="6" height="10" fill="#3B3A36"/><rect x="228" y="236" width="30" height="6" rx="2" fill="#5C6B7A"/>'
             '<path d="M336 246l6-30h44l6 30z" fill="#5C6B7A"/><rect x="346" y="204" width="36" height="16" rx="2" fill="#BFE3DF"/>')
    for x, y, r in ((296, 236, -12), (318, 240, 10), (402, 238, -6), (420, 232, 14)):
        s.append(f'<g transform="rotate({r} {x + 9} {y})"><rect x="{x}" y="{y - 6}" width="18" height="12" rx="1" fill="#fff" stroke="#D9C4AA"/>'
                 f'<path d="M{x + 3} {y - 2}h12M{x + 3} {y + 2}h8" stroke="#C9D1DC" stroke-width="1.3"/></g>')
    s.append(tanaman("#C98E68", ".75"))
    return _svg_latar("".join(s))


def dashboard_tara():
    """Dashboard yang muncul di adegan 3 ("tara!"): kartu laporan + grafik + kilau. Judul dari i18n (h.dashboard_judul)."""
    kilau = "".join(f'<path class="pg-kilau" style="--d:{d}s" d="M{x} {y - 9}l2.6 6.4 6.4 2.6-6.4 2.6L{x} {y + 9}l-2.6-6.4-6.4-2.6 6.4-2.6z" fill="{YEL}"/>'
                    for x, y, d in ((14, 22, 0), (290, 16, .3), (300, 92, .6), (8, 96, .9)))
    batang = "".join(f'<rect class="k-bar" x="{150 + i * 36}" y="{100 - h}" width="24" height="{h}" rx="2" fill="{c}"/>'
                     for i, (h, c) in enumerate(((58, TEAL), (40, "#7FC4C0"), (22, "#D9534F"), (48, TEAL))))
    return (f'<svg viewBox="0 0 310 120" aria-hidden="true">{kilau}'
            '<rect x="22" y="8" width="266" height="104" rx="8" fill="#fff" stroke="#C9D1DC" stroke-width="1.5"/>'
            f'<path d="M22 16a8 8 0 0 1 8-8h250a8 8 0 0 1 8 8v12H22z" fill="{TEAL}"/>'
            '<text x="34" y="23.5" font-size="11" font-weight="700" fill="#fff" font-family="sans-serif">{{ h.dashboard_judul }}</text>'
            f'<rect x="34" y="40" width="96" height="30" rx="4" fill="#EAF4F3"/><path d="M42 62l14-10 12 6 16-14 22-4" fill="none" stroke="{TEAL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect x="34" y="76" width="44" height="26" rx="4" fill="#FFF8D6"/><rect x="86" y="76" width="44" height="26" rx="4" fill="#EAF4F3"/>'
            f'<path d="M40 86h28M40 94h20M92 86h28M92 94h18" stroke="#9AA6B5" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M144 100h148" stroke="#C9D1DC" stroke-width="1.5"/>{batang}</svg>')


def kertas_terbang():
    """3 lembar data yang terbang dari tangan pemilik kedai ke Bobbi (adegan 2)."""
    return "".join(f'<div class="pg-kertas pg-k{i}"><svg viewBox="-2 -2 40 30" aria-hidden="true">{kertas(0, 0, 36, 26, w)}</svg></div>'
                   for i, w in enumerate((TEAL, "#E07A3F", YEL), 1))


def css_panggung():
    """CSS panggung hero + keyframes yang dihitung dari garis waktu (ADEGAN/JALAN/SERAH/TERBANG/KERJA/TARA/SALAM/DURASI)."""
    D = f"{DURASI}s"
    geser = f"0%,{_pct(JALAN[0])}%{{transform:none}}{_pct(JALAN[1])}%,100%{{transform:translateX(-50%)}}"
    t = _pct(sum(JALAN) / 2)
    lantai = (f"0%,{t - .2}%{{background:var(--lantai-kedai);border-color:var(--garis-kedai)}}"
              f"{t}%,100%{{background:var(--lantai-kantor);border-color:var(--garis-kantor)}}")
    maju = f"0%,{_pct(JALAN[0])}%{{transform:none}}{_pct(JALAN[1])}%,100%{{transform:translateX(70%)}}"
    vis = {"a0": [ADEGAN[0]], "aj": [JALAN], "srh": [SERAH], "tng": [(TERBANG[0], KERJA[1])], "sng": [TARA], "sal": [SALAM],
           "lmb": [(SERAH[0], TERBANG[1])], "ktk": [KERJA], "jmp": [TARA], "balon3": [(TARA[0] + .8, TARA[1])]}
    kf = "".join(f"@keyframes pg-{k}{{{_jendela(*v)}}}" for k, v in vis.items())
    kf += "".join(f"@keyframes pg-aktif{i}{{0%,{_pct(a) - .01 if a else 0}%{{background:transparent;color:var(--muted)}}{_pct(a)}%,{_pct(b) - .01}%{{background:var(--teal);color:#fff}}"
                  f"{_pct(b)}%,100%{{background:transparent;color:var(--muted)}}}}" for i, (a, b) in enumerate(ADEGAN, 1))
    # kertas terbang: dari dada pemilik kedai (kiri) melengkung ke laptop Bobbi (kanan), berselang 0,2 dtk
    for i in range(3):
        a, b = TERBANG[0] + i * .2, TERBANG[0] + i * .2 + 1
        m = (a + b) / 2
        kf += (f"@keyframes pg-k{i + 1}{{0%,{_pct(a) - .01}%{{opacity:0;left:44%;bottom:205px}}{_pct(a)}%{{opacity:1;left:44%;bottom:205px}}"
               f"{_pct(m)}%{{left:58%;bottom:{265 - i * 12}px}}{_pct(b) - .01}%{{opacity:1;left:72%;bottom:175px}}{_pct(b)}%,100%{{opacity:0;left:72%;bottom:175px}}}}")
    # "tara!": dashboard melompat muncul lalu diam sampai akhir salaman
    ta, tb = TARA[0], SALAM[1]
    kf += (f"@keyframes pg-tara{{0%,{_pct(ta) - .01}%{{opacity:0;transform:scale(.3)}}{_pct(ta)}%{{opacity:1;transform:scale(.3)}}"
           f"{_pct(ta + .35)}%{{transform:scale(1.08)}}{_pct(ta + .6)}%,{_pct(tb) - .01}%{{opacity:1;transform:none}}{_pct(tb)}%,100%{{opacity:0;transform:none}}}}")
    anim = "".join(f".pg-{k}{{animation:pg-{k} {D} infinite}}" for k in vis if k != "balon3")
    anim += "".join(f".pg-k{i}{{animation:pg-k{i} {D} infinite}}" for i in (1, 2, 3))
    aktif = "".join(f".pg-langkah .l{i}{{animation:pg-aktif{i} {D} infinite}}" for i in range(1, len(ADEGAN) + 1))
    return f"""/* Panggung hero = cerita 3 adegan ({DURASI} dtk, dibuat css_panggung()): 1 pemilik kedai pusing -> 2 datang ke Bobbi, berkas
   TERBANG ke Bobbi, Bobbi mengerjakan di laptop -> 3 "tara!" dashboard muncul, klien senang + salaman. Latar bergeser (2 panel: kedai, kantor).
   Desktop: kursor menggeser cerita maju/mundur (assets/js/panggung.js). */
:root{{--lantai-kedai:#E3D2BD;--garis-kedai:#CFB596;--lantai-kantor:var(--p2);--garis-kantor:var(--line)}}
[data-theme="dark"]{{--lantai-kedai:#3A3129;--garis-kedai:#5A4A3A}}
.panggung{{position:relative;height:470px;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.pg-jalur{{position:absolute;left:0;top:0;width:200%;height:calc(100% - 98px);display:flex;animation:pg-geser {D} infinite ease-in-out}}
.pg-panel{{position:relative;flex:0 0 50%;height:100%}}.pg-panel>svg{{position:absolute;inset:0;width:100%;height:100%}}
.pg-lantai{{position:absolute;left:0;right:0;bottom:52px;height:46px;border-top:2px solid;animation:pg-lantai {D} infinite}}
.panggung .tokoh{{position:absolute;bottom:82px;width:192px;height:307px;z-index:2}}.pg-panel .tokoh{{bottom:-16px}}
.panggung .pose{{position:absolute;inset:0;opacity:0}}.panggung .tokoh svg{{width:100%;height:100%;overflow:visible}}
.panggung .nama{{position:absolute;left:50%;bottom:-24px;transform:translateX(-50%);white-space:nowrap;font-size:13px;font-weight:600;color:var(--muted);z-index:3}}
.panggung .klien{{left:4%;animation:pg-maju {D} infinite ease-in-out}}.panggung .bobbi{{right:4%}}
.panggung .klien .nama{{left:0;transform:none}}.panggung .bobbi .nama{{left:auto;right:0;transform:none}}  /* label menjauh satu sama lain: tidak bertumpuk di panggung sempit */
{anim}
.pg-aj .kaki-b{{animation:pg-kaki .36s steps(1) infinite}}.pg-aj .kaki-a{{animation:pg-kaki .36s steps(1) infinite reverse}}
.pg-aj svg{{animation:pg-ayun .18s ease-in-out infinite alternate}}.panggung.mundur .pg-aj{{transform:scaleX(-1)}}
.k-salam{{animation:pg-salam .3s ease-in-out infinite alternate}}
.pg-salaman{{position:absolute;right:4%;bottom:82px;width:396px;height:307px;opacity:0;z-index:3}}.pg-salaman svg{{width:100%;height:100%;overflow:visible}}
.pg-kertas{{position:absolute;width:44px;height:34px;opacity:0;z-index:4}}.pg-kertas svg{{width:100%;height:100%}}
.pg-tara{{position:absolute;top:12px;left:25%;width:50%;opacity:0;z-index:4;transform-origin:50% 100%;animation:pg-tara {D} infinite}}.pg-tara svg{{width:100%;display:block}}
.pg-kilau{{transform-box:fill-box;transform-origin:center;animation:pg-kilau 1.2s ease-in-out infinite;animation-delay:var(--d)}}
.pg-masalah{{position:absolute;left:0;bottom:-16px;width:50%;height:300px}}.pg-masalah svg{{width:100%;height:100%}}.pg-masalah .k-naik{{animation-delay:var(--d)}}
.pg-balon{{position:absolute;max-width:240px;padding:9px 14px;border-radius:14px;background:#fff;border:2px solid #101b2d;color:#101b2d;font:700 15px/1.25 "Familjen Grotesk",sans-serif;opacity:0;z-index:5}}
.pg-balon::after{{content:"";position:absolute;left:24px;bottom:-9px;width:14px;height:14px;background:#fff;border:2px solid #101b2d;border-top:0;border-left:0;transform:rotate(45deg)}}
.pg-b0{{top:28px;left:10%;animation:pg-a0 {D} infinite}}.pg-b3{{top:150px;left:2%;max-width:165px;animation:pg-balon3 {D} infinite}}
.pg-b3::after{{left:auto;right:-9px;bottom:auto;top:18px;border:2px solid #101b2d;border-left:0;border-bottom:0}}
.pg-tirai{{position:absolute;inset:0;background:var(--panel);z-index:9;pointer-events:none;animation:pg-tirai {D} infinite}}
.pg-langkah{{position:absolute;left:0;right:0;bottom:0;height:52px;margin:0;padding:6px;list-style:none;display:flex;gap:6px;background:var(--panel);border-top:1px solid var(--line);z-index:6}}
.pg-langkah li{{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;border-radius:8px;font:600 14px/1.15 "Familjen Grotesk",sans-serif;color:var(--muted);text-align:center}}
.pg-langkah b{{display:grid;place-items:center;flex:none;width:22px;height:22px;border-radius:50%;background:rgba(128,128,128,.2);color:inherit;font-size:12px}}
{aktif}
[data-theme="dark"] .pg-redup{{filter:brightness(.6) saturate(.85)}}
@keyframes pg-geser{{{geser}}}@keyframes pg-lantai{{{lantai}}}@keyframes pg-maju{{{maju}}}
@keyframes pg-tirai{{0%{{opacity:1}}2.5%,{_pct(DURASI - .5)}%{{opacity:0}}100%{{opacity:1}}}}
{kf}
@keyframes pg-kaki{{0%{{opacity:1}}50%{{opacity:0}}}}@keyframes pg-ayun{{to{{transform:translateY(-4px)}}}}@keyframes pg-salam{{to{{transform:translateY(4px)}}}}
@keyframes pg-kilau{{0%,100%{{opacity:.2;transform:scale(.5)}}50%{{opacity:1;transform:scale(1.15)}}}}
@media(max-width:760px){{.hero2 .panggung{{order:-1;height:340px}}.panggung .tokoh{{width:124px;height:198px}}.panggung .klien{{left:3%}}.panggung .bobbi{{right:3%}}
.pg-langkah{{gap:3px;padding:5px 4px}}.pg-langkah li{{flex-direction:column;gap:2px;font-size:10.5px}}.pg-langkah b{{width:17px;height:17px;font-size:10px}}
.panggung .nama{{font-size:11px}}.pg-masalah{{height:200px}}.pg-balon{{font-size:12px;padding:6px 10px;max-width:160px}}.pg-b0{{top:20px;left:6%}}
.pg-b3{{top:96px;max-width:110px}}.pg-salaman{{right:3%;width:256px;height:198px}}.pg-tara{{top:8px;left:20%;width:60%}}.pg-kertas{{width:30px;height:23px;margin-bottom:-70px}}}}
@media (prefers-reduced-motion:reduce){{.pg-jalur{{transform:translateX(-50%)}}.panggung .klien{{transform:translateX(70%)}}
.panggung .pg-sng,.panggung .pg-jmp,.panggung .pg-b3,.panggung .pg-tara{{opacity:1}}.pg-tirai{{opacity:0}}.pg-lantai{{background:var(--lantai-kantor);border-color:var(--garis-kantor)}}
.pg-langkah .l3{{background:var(--teal);color:#fff}}}}
"""


def macro_hero():
    def pose_(o, siapa, aksi, kelas):
        return f'<div class="pose {kelas}">{pose(o, siapa, aksi)}</div>'
    klien = "".join((pose_(KLIEN, "klien", "pusing", "pg-a0"), pose_(KLIEN, "klien", "samping", "pg-aj"), pose_(KLIEN, "klien", "berkas", "pg-srh"),
                     pose_(KLIEN, "klien", "diri", "pg-tng"), pose_(KLIEN, "klien", "senang", "pg-sng")))
    bobbi = "".join((pose_(BOBBI, "bobbi", "lambai", "pg-lmb"), pose_(BOBBI, "bobbi", "laptop", "pg-ktk"),
                     pose_(BOBBI, "bobbi", "jempol", "pg-jmp")))

    def isi(svg_):  # isi <svg> tanpa pembungkusnya
        return svg_[svg_.index(">") + 1:svg_.rindex("</svg>")]
    # salaman = SATU gambar berisi dua tokoh, jadi tangan pasti bertemu di ukuran layar apa pun
    salaman = (f'<svg viewBox="0 0 198 160" aria-hidden="true"><g>{isi(pose(KLIEN, "klien", "salam"))}</g>'
               f'<g transform="translate(98 0)">{isi(pose(BOBBI, "bobbi", "salam"))}</g></svg>')
    return ("{% macro panggung_hero() -%}\n"
            "{%- set h = i18n[page.lang].utama.hero -%}\n"
            f'<div class="panggung rv" role="img" aria-label="{{{{ h.animasi_alt }}}}" data-durasi="{DURASI * 1000}" data-adegan="{ADEGAN_ATTR}">\n'
            '<div class="pg-lantai"></div>\n<div class="pg-jalur">\n'
            f'<div class="pg-panel">{latar_kedai()}<div class="pg-masalah">{properti_masalah()}</div></div>\n'
            f'<div class="pg-panel">{latar_kantor()}<div class="tokoh bobbi">{bobbi}<span class="nama">{{{{ h.tokoh_bobbi }}}}</span></div></div>\n</div>\n'
            '<div class="pg-balon pg-b0">{{ h.balon_masalah }}</div><div class="pg-balon pg-b3">{{ h.balon_hasil }}</div>\n'
            f'<div class="tokoh klien">{klien}<span class="nama">{{{{ h.tokoh_klien }}}}</span></div>\n'
            f'<div class="pg-salaman pg-sal">{salaman}</div>\n{kertas_terbang()}\n<div class="pg-tara">{dashboard_tara()}</div>\n'
            '<div class="pg-tirai"></div>\n'
            '<ol class="pg-langkah">{% for x in h.adegan %}<li class="l{{ loop.index }}"><b>{{ loop.index }}</b>{{ x }}</li>{% endfor %}</ol>\n'
            "</div>\n{%- endmacro %}")


CSS = """/* Gerak kecil karakter (k-*) */
.k-lambai{transform-box:view-box;transform-origin:69px 94px;animation:k-lambai .6s ease-in-out infinite alternate}
@keyframes k-lambai{to{transform:rotate(-14deg)}}
.k-naik{animation:k-naik 1.2s ease-in-out infinite}@keyframes k-naik{50%{transform:translateY(-4px)}}
.k-ketik{animation:k-ketik .35s ease-in-out infinite alternate}@keyframes k-ketik{to{transform:translateY(2px)}}
.k-baris{transform-box:fill-box;transform-origin:left;animation:k-baris 3s steps(6) infinite}.k-b2{animation-delay:.4s}.k-b3{animation-delay:.8s}
@keyframes k-baris{0%{transform:scaleX(.2)}60%,100%{transform:scaleX(1)}}
.k-uap{animation:k-uap 1.6s ease-in-out infinite}@keyframes k-uap{50%{transform:translateY(-3px);opacity:.4}}
.k-bar{transform-box:fill-box;transform-origin:bottom;animation:k-bar 3s ease-out infinite}.k-merah{animation-delay:.3s}
@keyframes k-bar{0%{transform:scaleY(.15)}35%,100%{transform:scaleY(1)}}
@@PANGGUNG@@/* Latar kantor (panel 1 panggung, dibuat latar_kantor()) */
.lk-kaca{fill:#EAF2F6}.lk-gedung{fill:#DCE5EC}.lk-bingkai{stroke:#D3DBE4}.lk-bingkai2{fill:#F7F9FB;stroke:#C9D1DC}
.lk-tali{stroke:#B8C1CD}.lk-gelap{fill:#C9D1DC}.lk-sedang{fill:#DCE2EA}.lk-rak{fill:#B8C1CD}.lk-layar{fill:#F4F8FA}.lk-jam{fill:#F7F9FB;stroke:#B8C1CD}.lk-jarum{stroke:#8E99A8}
[data-theme="dark"] .lk-kaca{fill:#1B2A40}[data-theme="dark"] .lk-gedung{fill:#22344D}[data-theme="dark"] .lk-bingkai{stroke:#2A3A52}[data-theme="dark"] .lk-bingkai2{fill:#1A2638;stroke:#2F405A}
[data-theme="dark"] .lk-tali{stroke:#33445E}[data-theme="dark"] .lk-gelap{fill:#2A3A52}[data-theme="dark"] .lk-sedang{fill:#223047}[data-theme="dark"] .lk-rak{fill:#33445E}
[data-theme="dark"] .lk-layar{fill:#1F2D42}[data-theme="dark"] .lk-jam{fill:#1A2638;stroke:#33445E}[data-theme="dark"] .lk-jarum{stroke:#6D7C92}
/* Bobbi di Alur kerja (viewBox 100x160) */
.ak-barista{width:70px;height:112px}
@media(max-width:860px){.ak-barista{width:50px;height:80px}}
/* mode gelap: rambut abu-abu arang supaya siluet tidak tenggelam di latar gelap */
[data-theme="dark"] .rb{fill:#3B3943}[data-theme="dark"] .rh{fill:#6A6772}
[data-theme="dark"] .tokoh svg,[data-theme="dark"] .ak-barista svg{filter:drop-shadow(0 0 1.5px rgba(255,255,255,.35))}
@media (prefers-reduced-motion:reduce){.k-lambai,.k-naik,.k-ketik,.k-baris,.k-uap,.k-bar,.panggung *,.panggung .klien{animation:none!important}}"""


CSS = CSS.replace("@@PANGGUNG@@", css_panggung())


def ganti(teks, mulai, selesai, isi, pertama):
    if mulai in teks:
        return re.sub(re.escape(mulai) + ".*?" + re.escape(selesai), lambda m: mulai + isi + selesai, teks, count=1, flags=re.S)
    return pertama(teks, mulai + isi + selesai)


def hasil():
    """Isi macros.html & style.css SETELAH blok karakter dibangkitkan (tanpa menulis). Dipakai main() dan tools/check_site.py."""
    m = MACROS.read_text(encoding="utf-8")

    def alur_pertama(s, blok):  # pertama kali: ganti div Bobbi lama di macro cara_kerja
        i = s.index('<div class="ak-barista"')
        j = s.index("</div></div>", i) + len("</div>")
        return s[:i] + blok + s[j:]

    m = ganti(m, "{#- KARAKTER:ALUR:MULAI -#}", "{#- KARAKTER:ALUR:SELESAI -#}", blok_alur(), alur_pertama)
    m = ganti(m, "{#- KARAKTER:HERO:MULAI (dibuat tools/gen_karakter.py) -#}\n", "\n{#- KARAKTER:HERO:SELESAI -#}", macro_hero(),
              lambda s, blok: s.rstrip("\n") + "\n\n" + blok + "\n")
    c = STYLE.read_text(encoding="utf-8")
    c = ganti(c, "/* KARAKTER:CSS:MULAI (dibuat tools/gen_karakter.py) */\n", "\n/* KARAKTER:CSS:SELESAI */", CSS,
              lambda s, blok: s.rstrip("\n") + "\n" + blok + "\n")
    return m, c


def main():
    m, c = hasil()
    MACROS.write_text(m, encoding="utf-8")
    STYLE.write_text(c, encoding="utf-8")
    print("OK: karakter ditulis ke macros.html (hero + alur kerja) dan style.css -> jalankan python build.py")


if __name__ == "__main__":
    main()
