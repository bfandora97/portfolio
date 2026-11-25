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
    s = ['<svg class="pg-latar" viewBox="0 0 560 372" preserveAspectRatio="xMidYMax slice" aria-hidden="true">']
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
    s.append(f'<ellipse cx="33" cy="68" rx="4" ry="2.4" fill="{o["pipi"]}" opacity=".3"/><ellipse cx="67" cy="68" rx="4" ry="2.4" fill="{o["pipi"]}" opacity=".3"/>')
    return "".join(s)


def kepala(o, siapa, ekspresi="senyum"):
    if siapa == "bobbi":
        return kepala_bobbi(o, ekspresi)
    s = []
    # pemilik kedai: sanggul + rambut samping
    s.append(f'<circle cx="50" cy="20" r="11" fill="{o["rambut"]}"/>')
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
    s.append(f'<ellipse cx="32" cy="65" rx="4.5" ry="2.8" fill="{o["pipi"]}" opacity=".4"/><ellipse cx="68" cy="65" rx="4.5" ry="2.8" fill="{o["pipi"]}" opacity=".4"/>')
    if siapa == "klien":
        s.append(f'<circle cx="23" cy="66" r="2" fill="{YEL}"/><circle cx="77" cy="66" r="2" fill="{YEL}"/>')
    return "".join(s)


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
        rambut = (f'<path d="M26 60C23 34 36 19 57 19C72 20 80 30 78 43C73 37 64 35 56 37C50 39 47 45 46 52C43 57 36 60 26 60Z" fill="{r}"/>'
                  f'<path d="M54 23C61 13 73 13 80 22C76 20.5 70 21 65 25Z" fill="{r}"/>')
        alis, hiasan = 3.4, ""
    else:
        # rambut turun sampai tengkuk + garis helaian disisir ke belakang
        rambut = (f'<path d="M26 64C21 38 34 24 54 24C68 24 77 33 78 45C72 40 64 38 56 39C50 40 46 44 45 50C44 58 41 66 37 74C33 75 29 71 26 64Z" fill="{r}"/>'
                  '<path d="M66 30C56 26 44 28 36 36M60 34C50 32 42 36 37 44" fill="none" stroke="#5A4336" stroke-width="1.4" stroke-linecap="round"/>')
        alis, hiasan = 2.8, f'<circle cx="45" cy="67" r="2" fill="{YEL}"/>'
    # sanggul: dua gulungan + ikat rambut + helaian (tampak samping, di belakang atas kepala)
    sanggul = (f'<ellipse cx="28" cy="30" rx="11" ry="9" fill="{r}" transform="rotate(-28 28 30)"/>'
               f'<path d="M19 27C13 20 17 12 25 14C29 15 30 20 28 24Z" fill="{r}"/>'
               '<path d="M21 31C25 26 31 25 35 28M23 36C27 32 32 32 36 34M20 21C22 18 25 18 27 20" fill="none" stroke="#5A4336" stroke-width="1.3" stroke-linecap="round"/>'
               f'<path d="M33 38L39 33" stroke="{TEAL}" stroke-width="3.4" stroke-linecap="round"/>') if siapa != "bobbi" else ""
    return (sanggul + f'<ellipse cx="52" cy="55" rx="25" ry="29" fill="{o["kulit"]}"/><path d="M77 55q5.5 4 .6 9.5" fill="{o["kulit"]}"/>' + rambut
            + f'<ellipse cx="45" cy="58" rx="4.6" ry="6.6" fill="{o["kulit2"]}"/>' + hiasan
            + f'<path d="M60 47q5.5-3.6 11 0" fill="none" stroke="{r}" stroke-width="{alis}" stroke-linecap="round"/>'
            + f'<ellipse cx="66" cy="56" rx="3.8" ry="4.8" fill="#fff"/><circle cx="67.6" cy="57" r="2.7" fill="{INK}"/><circle cx="68.4" cy="55.8" r=".9" fill="#fff"/>'
            + '<path d="M64.5 70.5q4.5 3.4 9 0" fill="none" stroke="#8C2F39" stroke-width="2.2" stroke-linecap="round"/>'
            + f'<ellipse cx="63" cy="65.5" rx="4" ry="2.4" fill="{o["pipi"]}" opacity=".4"/>')


def badan_samping(o, siapa):
    """Badan tampak samping: ramping. Pemilik kedai: celemek di depan. Bobbi: kaos + lanyard + ID card."""
    s = (f'<rect x="46" y="78" width="11" height="12" rx="3" fill="{o["kulit2"]}"/>'
         f'<rect x="39" y="86" width="26" height="52" rx="11" fill="{o["baju"]}"/>')
    if siapa == "bobbi":
        return s + f'<path d="M53 87l7 20" stroke="{YEL}" stroke-width="2.4"/><rect x="56" y="105" width="9" height="12" rx="1.5" fill="#fff"/>'
    return s + '<path d="M58 97h8v35a5 5 0 0 1-5 5h-3z" fill="#EADBB9"/>'


def langkah_samping(o, maju):
    """Satu fase langkah: kaki depan/belakang (diputar dari pinggul) + tangan berayun berlawanan."""
    def kaki_(sudut):
        return (f'<g transform="rotate({sudut} 51.5 131)"><rect x="46" y="130" width="11" height="19" rx="4" fill="{o["celana"]}"/>'
                f'<rect x="45" y="145" width="18" height="7" rx="3.5" fill="{o["sepatu"]}"/></g>')
    a, b = (-22, 20) if maju else (20, -22)
    tgn = (lengan(o, 52, 95, 66, 121) + tangan(o, 67, 123)) if maju else (lengan(o, 52, 95, 38, 121) + tangan(o, 37, 123))
    return kaki_(b) + kaki_(a), tgn


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
    elif aksi == "kopi":
        isi = (k + B + lengan(o, 31, 94, 40, 116) + lengan(o, 69, 94, 60, 116)
               + '<rect x="41" y="104" width="18" height="20" rx="3" fill="#fff" stroke="#C9D1DC"/><path d="M59 108h4a4 4 0 0 1 0 9h-4" fill="none" stroke="#C9D1DC" stroke-width="2"/>'
               + '<path class="k-uap" d="M46 100c-3-4 3-6 0-10M54 100c-3-4 3-6 0-10" fill="none" stroke="#9AA8BF" stroke-width="1.8" stroke-linecap="round"/>'
               + tangan(o, 41, 117) + tangan(o, 59, 117) + kepala(o, siapa))
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
    elif aksi == "ttd":
        isi = (k + B + lengan(o, 31, 94, 30, 120)
               + '<rect x="22" y="98" width="38" height="44" rx="3" fill="#8A6A4A"/><rect x="26" y="104" width="30" height="34" rx="1.5" fill="#fff"/>'
               + '<rect x="34" y="96" width="14" height="6" rx="2" fill="#B8BFC9"/><path d="M30 111h22M30 116h16" stroke="#C9D1DC" stroke-width="1.6"/>'
               + f'<path class="k-centang" d="M32 128l5 5 10-10" fill="none" stroke="{TEAL}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
               + tangan(o, 30, 122) + '<g class="k-pena">' + lengan(o, 69, 94, 56, 122)
               + '<path d="M50 136l9-14" stroke="#101B2D" stroke-width="3" stroke-linecap="round"/>' + tangan(o, 57, 123) + '</g>'
               + kepala(o, siapa, "fokus"))
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
    elif aksi == "duduk_laptop":  # Bobbi duduk di kursi, laptop di atas meja (tampak belakang layar + logo), mengetik
        logo = "".join(f'<circle cx="{cx}" cy="{cy}" r="1.6" fill="{c}"/>' for cx, cy, c in
                       ((46, 118, TEAL), (50, 118, TEAL), (50, 114, TEAL), (54, 118, TEAL), (54, 114, TEAL), (54, 110, YEL)))
        isi = ('<rect x="18" y="66" width="64" height="66" rx="10" fill="#9AA6B5"/>'
               '<g transform="translate(0 14)">' + B + '<g class="k-ketik">' + lengan(o, 31, 94, 40, 112) + lengan(o, 69, 94, 60, 112) + '</g>' + kepala(o, siapa) + '</g>'
               '<rect x="24" y="100" width="52" height="28" rx="3" fill="#D5DBE3" stroke="#AEB8C5" stroke-width="1.2"/>' + logo +
               '<rect x="2" y="127" width="112" height="8" rx="2" fill="#8E99A8"/><rect x="6" y="135" width="104" height="22" rx="2" fill="#B8C1CD"/>'
               '<path d="M6 146h104" stroke="#A3AEBC" stroke-width="1.2"/>')
    elif aksi == "duduk_kopi":  # pemilik kedai duduk di sofa sambil memegang kopi
        isi = ('<rect x="-8" y="90" width="116" height="50" rx="14" fill="#7FA9A8"/>'
               '<g transform="translate(0 8)">' + B + lengan(o, 31, 94, 40, 116) + lengan(o, 69, 94, 60, 116)
               + '<rect x="41" y="104" width="18" height="20" rx="3" fill="#fff" stroke="#C9D1DC"/><path d="M59 108h4a4 4 0 0 1 0 9h-4" fill="none" stroke="#C9D1DC" stroke-width="2"/>'
               + '<path class="k-uap" d="M46 100c-3-4 3-6 0-10M54 100c-3-4 3-6 0-10" fill="none" stroke="#9AA8BF" stroke-width="1.8" stroke-linecap="round"/>'
               + tangan(o, 41, 117) + tangan(o, 59, 117) + kepala(o, siapa) + '</g>'
               + '<rect x="-8" y="134" width="116" height="14" rx="6" fill="#6A9695"/>'
               + f'<rect x="37" y="138" width="11" height="13" rx="4" fill="{o["celana"]}"/><rect x="52" y="138" width="11" height="13" rx="4" fill="{o["celana"]}"/>'
               + f'<rect x="33" y="148" width="16" height="7" rx="3.5" fill="{o["sepatu"]}"/><rect x="51" y="148" width="16" height="7" rx="3.5" fill="{o["sepatu"]}"/>'
               + '<rect x="-16" y="110" width="14" height="42" rx="6" fill="#6A9695"/><rect x="102" y="110" width="14" height="42" rx="6" fill="#6A9695"/>'
               + '<rect x="-8" y="152" width="6" height="6" fill="#4E6E6D"/><rect x="102" y="152" width="6" height="6" fill="#4E6E6D"/>')
    elif aksi == "pusing":  # adegan masalah: tangan memegang kepala, wajah bingung, keringat (pertanyaan di balon)
        isi = (k + B + kepala(o, siapa, "bingung")
               + lengan(o, 31, 94, 21, 64) + tangan(o, 21, 61) + lengan(o, 69, 94, 79, 64) + tangan(o, 79, 61)
               + '<path d="M80 40q4 6 0 9q-4-3 0-9z" fill="#7FC4E8"/>')
    elif aksi == "salam":  # bersalaman: pemilik kedai menjulurkan tangan kanan ke kanan, Bobbi tangan kiri ke kiri
        if siapa == "bobbi":
            isi = (k + B + lengan(o, 69, 94, 74, 126) + tangan(o, 74, 128) + kepala(o, siapa, "senang")
                   + '<g class="k-salam">' + lengan(o, 31, 94, 6, 108) + tangan(o, 1, 108) + '</g>')
        else:
            isi = (k + B + lengan(o, 31, 94, 26, 126) + tangan(o, 26, 128) + kepala(o, siapa, "senang")
                   + '<g class="k-salam">' + lengan(o, 69, 94, 94, 108) + tangan(o, 99, 108) + '</g>')
    elif aksi == "diri":  # berdiri santai, tangan di samping
        isi = (k + B + lengan(o, 31, 94, 26, 126) + tangan(o, 26, 128) + lengan(o, 69, 94, 74, 126) + tangan(o, 74, 128) + kepala(o, siapa))
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


# ---------------------------------------------------------------- cerita "perjalanan" di panggung hero
# 0 kedai kacau -> (berjalan) 1 kantor: serahkan berkas -> (berjalan) 2 meja kerja: Bobbi merapikan, pemilik kedai di sofa
# -> (pemilik kedai pulang) 3 kedai: Bobbi DATANG membawa laporan -> 4 kedai yang sama jadi ramai: cek & bayar.
DURASI = 31                                                       # detik per putaran
ADEGAN = ((0, 5), (6.5, 11.5), (13, 18), (19.5, 25), (25, 30.5))  # (mulai, selesai) tiap adegan
JALAN = ((5, 6.5), (11.5, 13), (18, 19.5))                        # latar bergeser: 1 pemilik kedai -> kantor, 2-3 Bobbi -> ruang kerja -> kedai
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


def _svg_latar(isi, cls="pg-redup"):
    return f'<svg class="{cls}" viewBox="0 0 {LW} {LH}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">{isi}</svg>'


def latar_kedai(kacau):
    """Kedai kopi ORIGINAL (hangat). kacau=True: nota berserakan + tanaman. kacau=False: rapi + grup .pg-ramai
    (papan BUKA + pelanggan ngopi) yang muncul di adegan 4."""
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
    if kacau:
        for x, y, r in ((296, 236, -12), (318, 240, 10), (402, 238, -6), (420, 232, 14)):
            s.append(f'<g transform="rotate({r} {x + 9} {y})"><rect x="{x}" y="{y - 6}" width="18" height="12" rx="1" fill="#fff" stroke="#D9C4AA"/>'
                     f'<path d="M{x + 3} {y - 2}h12M{x + 3} {y + 2}h8" stroke="#C9D1DC" stroke-width="1.3"/></g>')
        s.append(f'<rect x="512" y="300" width="30" height="50" rx="3" fill="#C98E68"/>'
                 f'<path d="M527 300c-14-18-8-40 2-44 6 16 4 32-2 44zm2 0c8-20 22-26 30-22-4 14-16 22-30 22zm-4 0c-10-14-26-16-32-10 6 10 18 12 32 10z" fill="{TEAL}" opacity=".75"/>')
    else:
        ramai = [f'<path d="M64 66l21-12 21 12" fill="none" stroke="#8A5A3B" stroke-width="1.5"/><rect x="58" y="66" width="54" height="22" rx="3" fill="{TEAL}"/>'
                 '<text x="85" y="82" text-anchor="middle" font-size="12" font-weight="800" fill="#fff" font-family="sans-serif">{{ h.papan_buka }}</text>']
        for x, baju, rambut in ((440, "#7FA9C9", "#3B2A22"), (500, "#D9534F", "#1E1C1F")):
            ramai.append(f'<rect x="{x - 4}" y="300" width="44" height="6" rx="2" fill="#8A5A3B"/><rect x="{x + 15}" y="306" width="6" height="44" fill="#8A5A3B"/>'
                         f'<rect x="{x + 4}" y="262" width="26" height="40" rx="10" fill="{baju}"/><circle cx="{x + 17}" cy="250" r="12" fill="#D9A07A"/>'
                         f'<path d="M{x + 5} 248a12 12 0 0 1 24 0q-12-6-24 0z" fill="{rambut}"/><rect x="{x + 26}" y="290" width="9" height="10" rx="2" fill="#fff" stroke="#D9C4AA"/>'
                         f'<path class="k-uap" d="M{x + 29} 286c-2-3 2-4 0-7" fill="none" stroke="#B8C1CD" stroke-width="1.5" stroke-linecap="round"/>')
        s.append(f'<g class="pg-ramai">{"".join(ramai)}</g>')
    return _svg_latar("".join(s))


def latar_kerja():
    """Meja kerja Bobbi: papan catatan tempel + layar dinding: data acak -> baris rapi (berulang). Sofa & meja ada di pose karakter."""
    s = [f'<rect width="{LW}" height="{LH}" fill="#EEF3F6"/><rect y="262" width="{LW}" height="88" fill="#E3EAF0"/>',
         '<rect x="30" y="46" width="130" height="96" rx="3" fill="#D9C4AA" stroke="#A9784F" stroke-width="4"/>']
    for x, y, c in ((42, 58, YEL), (78, 62, "#7FC4C0"), (114, 56, "#F4A6A0"), (48, 98, "#7FC4C0"), (86, 102, YEL), (120, 96, "#fff")):
        s.append(f'<rect x="{x}" y="{y}" width="26" height="26" fill="{c}" transform="rotate({(x % 7) - 3} {x + 13} {y + 13})"/>')
    s.append('<rect x="200" y="14" width="190" height="94" rx="5" fill="#2b3446"/><rect x="207" y="21" width="176" height="80" rx="2" fill="#F4F8FA"/>')
    acak = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="6" fill="{c}" transform="rotate({r} {x} {y})"/>'
                   for x, y, w, c, r in ((216, 30, 40, "#E07A3F", 12), (280, 44, 56, TEAL, -9), (226, 62, 30, YEL, 20), (300, 76, 50, "#D9534F", -15),
                                         (330, 30, 36, "#7FC4C0", 8), (220, 86, 52, "#9AA6B5", -6)))
    rapi = "".join(f'<rect x="216" y="{29 + i * 11.5}" width="{w}" height="7" fill="{c}"/>'
                   for i, (w, c) in enumerate(((150, TEAL), (120, "#7FC4C0"), (140, TEAL), (96, "#7FC4C0"), (132, YEL), (110, TEAL))))
    s.append(f'<g class="pg-acak">{acak}</g><g class="pg-rapi">{rapi}</g>')
    s.append(f'<rect x="512" y="300" width="30" height="50" rx="3" fill="#C9D1DC"/>'
             f'<path d="M527 300c-14-18-8-40 2-44 6 16 4 32-2 44zm2 0c8-20 22-26 30-22-4 14-16 22-30 22z" fill="{TEAL}" opacity=".6"/>')
    return _svg_latar("".join(s))


def css_panggung():
    """CSS panggung hero + keyframes yang dihitung dari garis waktu (ADEGAN/JALAN/DURASI)."""
    D = f"{DURASI}s"
    geser = ["0%{transform:none}"]
    for i, (a, b) in enumerate(JALAN, 1):
        geser.append(f"{_pct(a)}%{{transform:translateX(-{25 * (i - 1)}%)}}{_pct(b)}%{{transform:translateX(-{25 * i}%)}}")
    geser.append("100%{transform:translateX(-75%)}")
    t1, t3 = _pct(sum(JALAN[0]) / 2), _pct(sum(JALAN[2]) / 2)
    kedai = "background:var(--lantai-kedai);border-color:var(--garis-kedai)"
    kantor = "background:var(--lantai-kantor);border-color:var(--garis-kantor)"
    lantai = f"0%,{t1 - .2}%{{{kedai}}}{t1}%,{t3 - .2}%{{{kantor}}}{t3}%,100%{{{kedai}}}"
    maju = f"0%,{_pct(JALAN[0][0])}%{{transform:none}}{_pct(JALAN[0][1])}%,100%{{transform:translateX(70%)}}"
    a0, a1, a2, a3, a4 = ADEGAN
    vis = {"a0": [a0], "a1": [a1], "a2": [a2], "a3": [a3], "a4": [a4],
           "aj": [JALAN[0]], "bj": [JALAN[1], JALAN[2]],                       # yang berjalan: pemilik kedai (1x), Bobbi (2x)
           "nk": [(a0[0], a1[1]), (a3[0], a4[1])], "nb": [JALAN[1], (JALAN[2][0], a4[1])],  # label nama ikut tokohnya
           "balon3": [(a3[0] + .8, a3[1])], "ramai": [a4]}
    kf = "".join(f"@keyframes pg-{k}{{{_jendela(*v)}}}" for k, v in vis.items())
    kf += "".join(f"@keyframes pg-aktif{i}{{0%,{_pct(a) - .01}%{{background:transparent;color:var(--muted)}}{_pct(a)}%,{_pct(b) - .01}%{{background:var(--teal);color:#fff}}"
                  f"{_pct(b)}%,100%{{background:transparent;color:var(--muted)}}}}" for i, (a, b) in enumerate(ADEGAN[1:], 1))
    anim = "".join(f".pg-{k}{{animation:pg-{k} {D} infinite}}" for k in vis if k != "balon3")
    return f"""/* Panggung hero = cerita "perjalanan" ({DURASI} dtk, dibuat css_panggung()): kedai kacau -> pemilik kedai ke kantor, serahkan data
   -> Bobbi ke ruang kerja -> Bobbi ke kedai bawa laporan -> salaman di kedai yang ramai. Yang berjalan tampak samping, latar bergeser (.pg-jalur = 4 panel).
   Desktop: kursor menggeser cerita maju/mundur (assets/js/panggung.js). */
:root{{--lantai-kedai:#E3D2BD;--garis-kedai:#CFB596;--lantai-kantor:var(--p2);--garis-kantor:var(--line)}}
[data-theme="dark"]{{--lantai-kedai:#3A3129;--garis-kedai:#5A4A3A}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--lantai-kedai:#3A3129;--garis-kedai:#5A4A3A}}}}
.panggung{{position:relative;height:470px;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.pg-jalur{{position:absolute;left:0;top:0;width:400%;height:calc(100% - 98px);display:flex;animation:pg-geser {D} infinite ease-in-out}}
.pg-panel{{position:relative;flex:0 0 25%;height:100%}}.pg-panel>svg{{position:absolute;inset:0;width:100%;height:100%}}
.pg-lantai{{position:absolute;left:0;right:0;bottom:52px;height:46px;border-top:2px solid;animation:pg-lantai {D} infinite}}
.panggung .tokoh{{position:absolute;bottom:82px;width:192px;height:307px;z-index:2}}.pg-panel .tokoh{{bottom:-16px;opacity:0}}
.panggung .pose{{position:absolute;inset:0;opacity:0}}.panggung .tokoh svg{{width:100%;height:100%;overflow:visible}}
.panggung .nama{{position:absolute;left:50%;bottom:-24px;transform:translateX(-50%);white-space:nowrap;font-size:13px;font-weight:600;color:var(--muted);z-index:3}}
.panggung .klien{{left:4%;animation:pg-maju {D} infinite ease-in-out}}.panggung .bobbi{{right:4%}}.panggung .nama.pg-nk,.panggung .nama.pg-nb{{opacity:0}}
{anim}
.pg-aj .kaki-b,.pg-bj .kaki-b{{animation:pg-kaki .36s steps(1) infinite}}.pg-aj .kaki-a,.pg-bj .kaki-a{{animation:pg-kaki .36s steps(1) infinite reverse}}
.pg-aj svg,.pg-bj svg{{animation:pg-ayun .18s ease-in-out infinite alternate}}.panggung.mundur .pg-aj,.panggung.mundur .pg-bj{{transform:scaleX(-1)}}
.k-salam{{animation:pg-salam .3s ease-in-out infinite alternate}}
.pg-masalah{{position:absolute;left:0;bottom:-16px;width:50%;height:300px}}.pg-masalah svg{{width:100%;height:100%}}.pg-masalah .k-naik{{animation-delay:var(--d)}}
.pg-acak{{animation:pg-acak 2.6s infinite alternate}}.pg-rapi{{animation:pg-rapi 2.6s infinite alternate}}
.pg-balon{{position:absolute;max-width:240px;padding:9px 14px;border-radius:14px;background:#fff;border:2px solid #101b2d;color:#101b2d;font:700 15px/1.25 "Familjen Grotesk",sans-serif;opacity:0;z-index:4}}
.pg-balon::after{{content:"";position:absolute;left:24px;bottom:-9px;width:14px;height:14px;background:#fff;border:2px solid #101b2d;border-top:0;border-left:0;transform:rotate(45deg)}}
.pg-b0{{top:28px;left:10%;animation:pg-a0 {D} infinite}}.pg-b3{{top:28px;left:24%;animation:pg-balon3 {D} infinite}}
.pg-tirai{{position:absolute;inset:0;background:var(--panel);z-index:9;pointer-events:none;animation:pg-tirai {D} infinite}}
.pg-langkah{{position:absolute;left:0;right:0;bottom:0;height:52px;margin:0;padding:6px;list-style:none;display:flex;gap:6px;background:var(--panel);border-top:1px solid var(--line);z-index:5}}
.pg-langkah li{{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;border-radius:8px;font:600 14px/1.15 "Familjen Grotesk",sans-serif;color:var(--muted);text-align:center}}
.pg-langkah b{{display:grid;place-items:center;flex:none;width:22px;height:22px;border-radius:50%;background:rgba(128,128,128,.2);color:inherit;font-size:12px}}
.pg-langkah .l1{{animation:pg-aktif1 {D} infinite}}.pg-langkah .l2{{animation:pg-aktif2 {D} infinite}}.pg-langkah .l3{{animation:pg-aktif3 {D} infinite}}.pg-langkah .l4{{animation:pg-aktif4 {D} infinite}}
[data-theme="dark"] .pg-redup{{filter:brightness(.6) saturate(.85)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .pg-redup{{filter:brightness(.6) saturate(.85)}}}}
@keyframes pg-geser{{{"".join(geser)}}}@keyframes pg-lantai{{{lantai}}}@keyframes pg-maju{{{maju}}}
@keyframes pg-tirai{{0%{{opacity:1}}1.5%,{_pct(DURASI - .5)}%{{opacity:0}}100%{{opacity:1}}}}
{kf}
@keyframes pg-kaki{{0%{{opacity:1}}50%{{opacity:0}}}}@keyframes pg-ayun{{to{{transform:translateY(-4px)}}}}@keyframes pg-salam{{to{{transform:translateY(4px)}}}}
@keyframes pg-acak{{0%,35%{{opacity:1}}50%,100%{{opacity:0}}}}@keyframes pg-rapi{{0%,35%{{opacity:0}}50%,100%{{opacity:1}}}}
@media(max-width:760px){{.hero2 .panggung{{order:-1;height:340px}}.panggung .tokoh{{width:124px;height:198px}}.panggung .klien{{left:3%}}.panggung .bobbi{{right:3%}}
.pg-langkah{{gap:3px;padding:5px 4px}}.pg-langkah li{{flex-direction:column;gap:2px;font-size:10.5px}}.pg-langkah b{{width:17px;height:17px;font-size:10px}}
.panggung .nama{{font-size:11px}}.pg-masalah{{height:200px}}.pg-balon{{font-size:12px;padding:6px 10px;max-width:160px}}.pg-b0{{top:20px;left:6%}}.pg-b3{{top:20px;left:14%}}}}
@media (prefers-reduced-motion:reduce){{.pg-jalur{{transform:translateX(-75%)}}.panggung .klien{{transform:translateX(70%)}}
.panggung .pg-a3,.panggung .pg-b3,.panggung .nama.pg-nk,.panggung .nama.pg-nb{{opacity:1}}.pg-tirai{{opacity:0}}.pg-lantai{{background:var(--lantai-kedai);border-color:var(--garis-kedai)}}
.pg-langkah .l3{{background:var(--teal);color:#fff}}.pg-rapi,.pg-ramai,.pg-panel .tokoh{{opacity:0}}}}
"""


def macro_hero():
    def pose_(o, siapa, aksi, kelas):
        return f'<div class="pose {kelas}">{pose(o, siapa, aksi)}</div>'

    def panel(latar, isi=""):
        return f'<div class="pg-panel">{latar}{isi}</div>'
    nama_b = '<span class="nama">{{ h.tokoh_bobbi }}</span>'
    klien = "".join((pose_(KLIEN, "klien", "pusing", "pg-a0"), pose_(KLIEN, "klien", "samping", "pg-aj"), pose_(KLIEN, "klien", "berkas", "pg-a1"),
                     pose_(KLIEN, "klien", "senang", "pg-a3"), pose_(KLIEN, "klien", "salam", "pg-a4")))
    bobbi = "".join((pose_(BOBBI, "bobbi", "samping", "pg-bj"), pose_(BOBBI, "bobbi", "poster", "pg-a3"), pose_(BOBBI, "bobbi", "salam", "pg-a4")))
    kantor = latar_kantor().replace('class="pg-latar" viewBox="0 0 560 372"', 'viewBox="0 0 560 372"', 1)
    return ("{% macro panggung_hero() -%}\n"
            "{%- set h = i18n[page.lang].utama.hero -%}{%- set l = i18n[page.lang].utama.cara_kerja.langkah -%}\n"
            f'<div class="panggung rv" role="img" aria-label="{{{{ h.animasi_alt }}}}" data-durasi="{DURASI * 1000}">\n'
            '<div class="pg-lantai"></div>\n<div class="pg-jalur">\n'
            + panel(latar_kedai(True), f'<div class="pg-masalah">{properti_masalah()}</div>') + "\n"
            + panel(kantor, f'<div class="tokoh bobbi pg-a1">{pose(BOBBI, "bobbi", "lambai")}{nama_b}</div>') + "\n"
            + panel(latar_kerja(), f'<div class="tokoh bobbi pg-a2">{pose(BOBBI, "bobbi", "duduk_laptop")}{nama_b}</div>') + "\n"
            + panel(latar_kedai(False)) + "\n</div>\n"
            '<div class="pg-balon pg-b0">{{ h.balon_masalah }}</div><div class="pg-balon pg-b3">{{ h.balon_hasil }}</div>\n'
            f'<div class="tokoh klien">{klien}<span class="nama pg-nk">{{{{ h.tokoh_klien }}}}</span></div>\n'
            f'<div class="tokoh bobbi">{bobbi}<span class="nama pg-nb">{{{{ h.tokoh_bobbi }}}}</span></div>\n'
            '<div class="pg-tirai"></div>\n'
            '<ol class="pg-langkah">{% for x in l %}<li class="l{{ loop.index }}"><b>{{ loop.index }}</b>{{ x.papan }}</li>{% endfor %}</ol>\n'
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
.k-pena{animation:k-pena .5s ease-in-out infinite alternate}@keyframes k-pena{to{transform:translate(-5px,1px)}}
.k-centang{stroke-dasharray:24;animation:k-centang 3s ease-out infinite}@keyframes k-centang{0%,40%{stroke-dashoffset:24}70%,100%{stroke-dashoffset:0}}
@@PANGGUNG@@/* Latar kantor (panel 1 panggung, dibuat latar_kantor()) */
.lk-kaca{fill:#EAF2F6}.lk-gedung{fill:#DCE5EC}.lk-bingkai{stroke:#D3DBE4}.lk-bingkai2{fill:#F7F9FB;stroke:#C9D1DC}
.lk-tali{stroke:#B8C1CD}.lk-gelap{fill:#C9D1DC}.lk-sedang{fill:#DCE2EA}.lk-rak{fill:#B8C1CD}.lk-layar{fill:#F4F8FA}.lk-jam{fill:#F7F9FB;stroke:#B8C1CD}.lk-jarum{stroke:#8E99A8}
[data-theme="dark"] .lk-kaca{fill:#1B2A40}[data-theme="dark"] .lk-gedung{fill:#22344D}[data-theme="dark"] .lk-bingkai{stroke:#2A3A52}[data-theme="dark"] .lk-bingkai2{fill:#1A2638;stroke:#2F405A}
[data-theme="dark"] .lk-tali{stroke:#33445E}[data-theme="dark"] .lk-gelap{fill:#2A3A52}[data-theme="dark"] .lk-sedang{fill:#223047}[data-theme="dark"] .lk-rak{fill:#33445E}
[data-theme="dark"] .lk-layar{fill:#1F2D42}[data-theme="dark"] .lk-jam{fill:#1A2638;stroke:#33445E}[data-theme="dark"] .lk-jarum{stroke:#6D7C92}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .lk-kaca{fill:#1B2A40}:root:not([data-theme="light"]) .lk-gedung{fill:#22344D}:root:not([data-theme="light"]) .lk-bingkai{stroke:#2A3A52}
:root:not([data-theme="light"]) .lk-bingkai2{fill:#1A2638;stroke:#2F405A}:root:not([data-theme="light"]) .lk-tali{stroke:#33445E}:root:not([data-theme="light"]) .lk-gelap{fill:#2A3A52}
:root:not([data-theme="light"]) .lk-sedang{fill:#223047}:root:not([data-theme="light"]) .lk-rak{fill:#33445E}:root:not([data-theme="light"]) .lk-layar{fill:#1F2D42}
:root:not([data-theme="light"]) .lk-jam{fill:#1A2638;stroke:#33445E}:root:not([data-theme="light"]) .lk-jarum{stroke:#6D7C92}}
/* Bobbi di Alur kerja (viewBox 100x160) */
.ak-barista{width:70px;height:112px}
@media(max-width:860px){.ak-barista{width:50px;height:80px}}
/* mode gelap: rambut abu-abu arang supaya siluet tidak tenggelam di latar gelap */
[data-theme="dark"] .rb{fill:#3B3943}[data-theme="dark"] .rh{fill:#6A6772}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .rb{fill:#3B3943}:root:not([data-theme="light"]) .rh{fill:#6A6772}}
[data-theme="dark"] .tokoh svg,[data-theme="dark"] .ak-barista svg{filter:drop-shadow(0 0 1.5px rgba(255,255,255,.35))}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tokoh svg,:root:not([data-theme="light"]) .ak-barista svg{filter:drop-shadow(0 0 1.5px rgba(255,255,255,.35))}}
@media (prefers-reduced-motion:reduce){.k-lambai,.k-naik,.k-ketik,.k-baris,.k-uap,.k-bar,.k-pena,.k-centang,.panggung *,.panggung .klien{animation:none!important}}"""


CSS = CSS.replace("@@PANGGUNG@@", css_panggung())


def ganti(teks, mulai, selesai, isi, pertama):
    if mulai in teks:
        return re.sub(re.escape(mulai) + ".*?" + re.escape(selesai), lambda m: mulai + isi + selesai, teks, count=1, flags=re.S)
    return pertama(teks, mulai + isi + selesai)


def main():
    m = MACROS.read_text(encoding="utf-8")

    def alur_pertama(s, blok):  # pertama kali: ganti div Bobbi lama di macro cara_kerja
        i = s.index('<div class="ak-barista"')
        j = s.index("</div></div>", i) + len("</div>")
        return s[:i] + blok + s[j:]

    m = ganti(m, "{#- KARAKTER:ALUR:MULAI -#}", "{#- KARAKTER:ALUR:SELESAI -#}", blok_alur(), alur_pertama)
    m = ganti(m, "{#- KARAKTER:HERO:MULAI (dibuat tools/gen_karakter.py) -#}\n", "\n{#- KARAKTER:HERO:SELESAI -#}", macro_hero(),
              lambda s, blok: s.rstrip("\n") + "\n\n" + blok + "\n")
    MACROS.write_text(m, encoding="utf-8")
    c = STYLE.read_text(encoding="utf-8")
    c = ganti(c, "/* KARAKTER:CSS:MULAI (dibuat tools/gen_karakter.py) */\n", "\n/* KARAKTER:CSS:SELESAI */", CSS,
              lambda s, blok: s.rstrip("\n") + "\n" + blok + "\n")
    STYLE.write_text(c, encoding="utf-8")
    print("OK: karakter ditulis ke macros.html (hero + alur kerja) dan style.css -> jalankan python build.py")


if __name__ == "__main__":
    main()
