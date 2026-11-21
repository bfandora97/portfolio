"""Gambar preview link (Open Graph) 1200x630 untuk WhatsApp, LinkedIn, dll.

    python tools/gen_og.py assets/img/og-image.png          # versi Indonesia
    python tools/gen_og.py assets/img/og-image-en.png en    # versi Inggris

Ubah HEADLINE / SUB di bawah kalau pesan utama website berubah.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

TEXT = {
    "id": (["Jualan ramai, tapi", "untung sebenarnya", "tidak kelihatan?"],
           ["Laporan outlet, GoFood/GrabFood & Shopee", "jadi satu laporan otomatis di HP"]),
    "en": (["Selling on many", "channels but can't see", "your real profit?"],
           ["Shopify, Amazon, Etsy & marketplace reports", "in one dashboard that updates itself"]),
}
HEADLINE, SUB = TEXT[sys.argv[2] if len(sys.argv) > 2 else "id"]
FONT = "C:/Windows/Fonts/" if sys.platform == "win32" else "/usr/share/fonts/truetype/dejavu/"
TEAL, YEL, INK, WHITE = (14, 124, 123), (242, 200, 17), (16, 27, 45), (255, 255, 255)


def f(size, bold=False):
    if sys.platform == "win32":
        return ImageFont.truetype(FONT + ("arialbd.ttf" if bold else "arial.ttf"), size)
    return ImageFont.truetype(FONT + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)


im = Image.new("RGB", (1200, 630), TEAL)
d = ImageDraw.Draw(im)
for i in range(12):  # motif titik & batang, sama seperti hero website
    for j in range(14):
        on = j >= 14 - (3 + i)
        r = 6 if on else 3
        x, y = 760 + i * 34, 90 + j * 34
        if x > 1160:
            continue
        top = on and j == 14 - (3 + i)
        d.ellipse((x - r, y - r, x + r, y + r), fill=YEL if top else (WHITE if on else (60, 150, 149)))
d.rounded_rectangle((64, 64, 112, 112), 12, fill=YEL)
d.text((75, 70), "K", font=f(34, True), fill=INK)
d.text((128, 72), "Kemang Data", font=f(32, True), fill=WHITE)
for k, line in enumerate(HEADLINE):
    d.text((64, 190 + k * 66), line, font=f(54, True), fill=WHITE if k == 0 else YEL)
for k, line in enumerate(SUB):
    d.text((64, 430 + k * 38), line, font=f(26), fill=WHITE)
d.text((64, 550), "kemangdata.my.id", font=f(26, True), fill=YEL)
im.save(sys.argv[1], optimize=True)
print("saved", sys.argv[1])
