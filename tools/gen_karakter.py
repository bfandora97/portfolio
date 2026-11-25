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
def kepala_bobbi(o, ekspresi="senyum"):
    """Bobbi (dari foto formal): wajah lonjong, rambut side part disapu ke kanan + undercut, alis melengkung halus,
    kumis tipis samar. Rambut 2 lapis (isi kubah di balik wajah + sapuan depan) supaya tidak ada celah."""
    r, s = o["rambut"], []
    s.append(f'<path class="rb" d="M70 37C69 25 60 19 50 19S31 25 30 37Z" fill="{r}"/>')  # isi kubah di balik wajah
    s.append(f'<ellipse cx="25.5" cy="58" rx="5" ry="7" fill="{o["kulit2"]}"/><ellipse cx="74.5" cy="58" rx="5" ry="7" fill="{o["kulit2"]}"/>')
    s.append(f'<path d="M50 26c15 0 25 11 25 27 0 19-11 33-25 33S25 72 25 53c0-16 10-27 25-27z" fill="{o["kulit"]}"/>')
    # side part disapu ke kanan Bobbi (= kiri layar): digambar menghadap kanan layar lalu dicerminkan.
    # garis rambut ~y36 (dahi pas), ujung kecil jatuh di depan, sudut belahan bulat, samping ramping (undercut lewat siluet)
    s.append('<g transform="matrix(-1 0 0 1 100 0)">')
    # undercut = rambut cukur tipis (bukan botak): menyambung dari sudut pelipis, mengikuti kepala sampai atas telinga
    s.append(f'<path class="rb" d="M30 40.6C28.2 40.6 26.7 41.4 26.2 43C25.7 46 25.6 49 25.8 52L28.9 52.4C28.7 49 28.9 46 30 43.4Z'
             f'M71.4 38.8C72.8 39.4 73.6 40.8 73.9 42.5C74.4 45.5 74.5 49 74.3 52L71.1 52.4C71.3 49 71.1 45.5 70.1 42.6Z" fill="{r}" opacity=".5"/>')
    s.append(f'<path class="rb" d="M38 39.5L36.6 26.2C31.8 27.4 28.4 31.6 28.2 37.6C28.2 39.2 28.4 40.6 28.8 41.8C31.6 40.5 34.8 39.8 38 39.5Z" fill="{r}"/>')
    s.append(f'<path class="rb" d="M38 39.5C36 36 35.2 31 36.2 27C38 20.5 43.5 16.5 50.5 16.2C59 15.8 67 19 70.8 24.8C72.8 28 73 33 71.9 39.5'
             f'C69.6 37.8 67.6 38.6 65.6 41.2C64.6 38.2 61.6 36.4 57 36C50.5 35.5 44 36.8 38 39.5Z" fill="{r}"/>')
    # helaian: satu panjang meruncing + satu pendek (bentuk sabit, bukan garis rata)
    s.append('<path class="rh" d="M40 33.2C44 24 54 20 65.4 22.4C55 21.6 46 25 41.3 33.6ZM45.2 35.8C49.6 31.2 55 29.6 61.2 30C55.6 30.8 50.6 32.6 46 36.2Z" fill="#55525C"/>')
    s.append('</g>')
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
    s.append(f'<path d="M34 {alis_y}q6-4 12 0M54 {alis_y}q6-4 12 0" fill="none" stroke="{o["rambut"]}" stroke-width="2.8" stroke-linecap="round"/>')
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
    else:
        raise ValueError(aksi)
    return svg(isi, cls)


# ---------------------------------------------------------------- keluaran
def blok_alur():
    """Bobbi di Alur kerja: aksi1 terima berkas, aksi2 laptop, aksi3 poster, aksi4 jempol, b-samping = jalan."""
    poses = [pose(BOBBI, "bobbi", a, f"b-aksi{i}") for i, a in enumerate(("berkas", "laptop", "poster", "jempol"), 1)]
    poses.append(pose(BOBBI, "bobbi", "jalan", "b-samping"))
    return '<div class="ak-barista" data-pose="aksi1">' + "".join(poses) + "</div>"


def macro_hero():
    def slot(o, siapa, aksi):
        return "".join(f'<div class="pose pg{i}">{pose(o, siapa, a)}</div>' for i, a in enumerate(aksi, 1))
    terbang = f'<svg viewBox="-2 -2 40 30" aria-hidden="true">{kertas(0, 0, 36, 26, TEAL)}</svg>'
    return ("{% macro panggung_hero() -%}\n"
            "{%- set h = i18n[page.lang].utama.hero -%}{%- set l = i18n[page.lang].utama.cara_kerja.langkah -%}\n"
            '<div class="panggung rv" role="img" aria-label="{{ h.animasi_alt }}">\n'
            f'<div class="tokoh klien">{slot(KLIEN, "klien", ("berkas", "kopi", "senang", "ttd"))}<span class="nama">{{{{ h.tokoh_klien }}}}</span></div>\n'
            f'<div class="pg-terbang">{terbang}</div>\n'
            f'<div class="tokoh bobbi">{slot(BOBBI, "bobbi", ("lambai", "laptop", "poster", "jempol"))}<span class="nama">{{{{ h.tokoh_bobbi }}}}</span></div>\n'
            '<div class="pg-lantai"></div>\n'
            '<ol class="pg-langkah">{% for x in l %}<li class="pg{{ loop.index }}"><b>{{ loop.index }}</b>{{ x.papan }}</li>{% endfor %}</ol>\n'
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
/* Panggung hero: 4 adegan x 3 detik (pg1..pg4); pemilik kedai masuk dari kiri, berkas terbang ke Bobbi.
   Bilah 4 langkah di bawah: semua langkah selalu terlihat, yang sedang dimainkan menyala. */
.panggung{position:relative;height:470px;background:radial-gradient(ellipse at 50% 100%,rgba(14,124,123,.13) 0,var(--panel) 70%);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.pg-lantai{position:absolute;left:0;right:0;bottom:52px;height:46px;background:var(--p2);border-top:2px solid var(--line)}
.panggung .tokoh{position:absolute;bottom:82px;width:192px;height:307px;z-index:2}
.panggung .pose{position:absolute;inset:0;opacity:0}.panggung .tokoh svg{width:100%;height:100%;overflow:visible}
.panggung .nama{position:absolute;left:50%;bottom:-24px;transform:translateX(-50%);white-space:nowrap;font-size:13px;font-weight:600;color:var(--muted);z-index:3}
.panggung .klien{left:4%;animation:pg-datang 12s infinite}.panggung .bobbi{right:4%}
.pg-langkah{position:absolute;left:0;right:0;bottom:0;height:52px;margin:0;padding:6px;list-style:none;display:flex;gap:6px;background:var(--panel);border-top:1px solid var(--line);z-index:3}
.pg-langkah li{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;border-radius:8px;font:600 14px/1.15 "Familjen Grotesk",sans-serif;color:var(--muted);text-align:center}
.pg-langkah b{display:grid;place-items:center;flex:none;width:22px;height:22px;border-radius:50%;background:rgba(128,128,128,.2);color:inherit;font-size:12px}
.pg-terbang{position:absolute;width:56px;height:42px;left:36%;bottom:272px;opacity:0;z-index:3;animation:pg-lempar 12s infinite}.pg-terbang svg{width:100%;height:100%}
.panggung .pg1{animation:pg-tampil 12s infinite 0s}.panggung .pg2{animation:pg-tampil 12s infinite -9s}
.panggung .pg3{animation:pg-tampil 12s infinite -6s}.panggung .pg4{animation:pg-tampil 12s infinite -3s}
.pg-langkah li.pg1,.pg-langkah li.pg2,.pg-langkah li.pg3,.pg-langkah li.pg4{animation-name:pg-aktif}
@keyframes pg-tampil{0%,24.5%{opacity:1}25%,100%{opacity:0}}
@keyframes pg-aktif{0%,24.5%{background:var(--teal);color:#fff}25%,100%{background:transparent;color:var(--muted)}}
@keyframes pg-datang{0%{transform:translateX(-170%)}12%,100%{transform:none}}
@keyframes pg-lempar{0%,18%{opacity:0;transform:none}20%{opacity:1}26%{opacity:1;transform:translate(385%,290%) rotate(8deg) scale(.6)}28%,100%{opacity:0}}
@media(max-width:760px){.hero2 .panggung{order:-1;height:340px}.panggung .tokoh{width:124px;height:198px}.panggung .klien{left:3%}.panggung .bobbi{right:3%}
.pg-langkah{gap:3px;padding:5px 4px}.pg-langkah li{flex-direction:column;gap:2px;font-size:10.5px}.pg-langkah b{width:17px;height:17px;font-size:10px}
.panggung .nama{font-size:11px}.pg-terbang{bottom:192px;width:36px;animation-name:pg-lempar-hp}}
@keyframes pg-lempar-hp{0%,18%{opacity:0;transform:none}20%{opacity:1}26%{opacity:1;transform:translate(385%,183%) rotate(8deg) scale(.6)}28%,100%{opacity:0}}
/* Bobbi di Alur kerja (viewBox 100x160) */
.ak-barista{width:70px;height:112px}
@media(max-width:860px){.ak-barista{width:50px;height:80px}}
/* mode gelap: rambut abu-abu arang supaya siluet tidak tenggelam di latar gelap */
[data-theme="dark"] .rb{fill:#3B3943}[data-theme="dark"] .rh{fill:#6A6772}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .rb{fill:#3B3943}:root:not([data-theme="light"]) .rh{fill:#6A6772}}
[data-theme="dark"] .tokoh svg,[data-theme="dark"] .ak-barista svg{filter:drop-shadow(0 0 1.5px rgba(255,255,255,.35))}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tokoh svg,:root:not([data-theme="light"]) .ak-barista svg{filter:drop-shadow(0 0 1.5px rgba(255,255,255,.35))}}
@media (prefers-reduced-motion:reduce){.k-lambai,.k-naik,.k-ketik,.k-baris,.k-uap,.k-bar,.k-pena,.k-centang,.panggung .pose,.pg-langkah li,.panggung .klien,.pg-terbang{animation:none}
.panggung .pg3{opacity:1}.pg-langkah li.pg3{background:var(--teal);color:#fff}}"""


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
