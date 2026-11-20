"""Gambar dashboard demo UMKM "Kopi Senja" (data fiktif, seed tetap).

    python tools/gen_umkm.py assets/img
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import io, os, sys

OUT = sys.argv[1]
rng = np.random.default_rng(2026)
TEAL, YEL, INK, MUT, LINE, BG, PANEL = "#0E7C7B", "#F2C811", "#101B2D", "#52607A", "#D9DFE7", "#F4F6F8", "#FFFFFF"
plt.rcParams["font.family"] = "Segoe UI"

# ---------- synthetic data ----------
products = [  # name, price, cost, weight, channels allowed
    ("Es Kopi Susu Senja", 22000, 8000, 30, "OGS"),
    ("Kopi Aren Literan 1L", 95000, 42000, 4, "OGS"),
    ("Americano", 20000, 6000, 12, "OG"),
    ("Cafe Latte", 28000, 10000, 12, "OG"),
    ("Matcha Latte", 30000, 13000, 8, "OG"),
    ("Croissant Butter", 25000, 11000, 9, "OG"),
    ("Roti Bakar Cokelat", 22000, 9000, 6, "OG"),
    ("Kopi Bubuk Senja 250g", 85000, 38000, 3, "OS"),
    ("Red Velvet Latte", 32000, 14000, 1.2, "OG"),
    ("Kue Lumpur Pandan", 18000, 9000, 0.9, "O"),
]
P = pd.DataFrame(products, columns=["produk", "harga", "hpp", "w", "ch"])
channels = {"Outlet Kemang": "O", "Outlet Tebet": "O", "GoFood/GrabFood": "G", "Shopee": "S"}
comm = {"Outlet Kemang": 0.0, "Outlet Tebet": 0.0, "GoFood/GrabFood": 0.20, "Shopee": 0.11}
base = {"Outlet Kemang": 80, "Outlet Tebet": 55, "GoFood/GrabFood": 42, "Shopee": 6}
days = pd.date_range("2026-01-01", "2026-06-30")
hours = np.arange(7, 23)
hour_w = np.array([3, 5, 6, 5, 6, 8, 7, 6, 10, 13, 14, 12, 8, 6, 4, 2], float)
rows = []
for ch, code in channels.items():
    pm = P[P.ch.str.contains(code)].reset_index(drop=True)
    pw = pm.w / pm.w.sum()
    for d in days:
        growth = 1 + 0.05 * (d.month - 1)
        wk = 1.25 if d.weekday() >= 5 else 1.0
        if ch == "Shopee": wk = 1.0
        ram = 0.85 if (pd.Timestamp("2026-02-18") <= d <= pd.Timestamp("2026-03-19") and ch.startswith("Outlet")) else 1.0
        n = rng.poisson(base[ch] * growth * wk * ram)
        h = rng.choice(hours, n, p=hour_w / hour_w.sum())
        k = rng.choice(len(pm), n, p=pw)
        q = 1 + rng.poisson(0.35, n)
        for hh, kk, qq in zip(h, k, q):
            rows.append((d, ch, hh, kk if False else pm.produk[kk], qq))
T = pd.DataFrame(rows, columns=["tgl", "channel", "jam", "produk", "qty"]).merge(P[["produk", "harga", "hpp"]], on="produk")
T["omzet"] = T.qty * T.harga
T["laba"] = T.omzet * (1 - T.channel.map(comm)) - T.qty * T.hpp
tot = T.omzet.sum(); ntrx = len(T); atv = tot / ntrx; margin = T.laba.sum() / tot
mon = T.groupby([T.tgl.dt.month, "channel"]).omzet.sum().unstack()[list(channels)] / 1e6
top = T.groupby("produk").omzet.sum().sort_values(ascending=False)
heat = T[T.channel != "Shopee"].groupby([T.tgl.dt.weekday, "jam"]).size().unstack().reindex(columns=hours, fill_value=0)
heat = heat / len(days) * 7  # avg trx per weekday-slot
cm = T.groupby("channel").laba.sum() / T.groupby("channel").omzet.sum()
qty = T.groupby("produk").qty.sum()
stock = {"Red Velvet Latte": (160, "Sirup red velvet"), "Kue Lumpur Pandan": (95, "Kue (pcs)"),
         "Kopi Bubuk Senja 250g": (140, "Pack 250g"), "Roti Bakar Cokelat": (60, "Roti tawar")}
print(f"total {tot/1e6:.1f} jt, trx {ntrx}, atv {atv:.0f}, margin {margin:.3f}")
print(cm); print(top); print(qty.sort_values())

def rp(x):
    return "Rp " + f"{x:,.0f}".replace(",", ".")

# ---------- figure ----------
W, H = 1600, 1000
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=BG)
def ax_px(x, y, w, h, **kw):  # top-left pixel coords
    return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H], **kw)
def panel(x, y, w, h, title=None, sub=None):
    a = ax_px(x, y, w, h); a.set_xlim(0, w); a.set_ylim(h, 0); a.axis("off")
    a.add_patch(FancyBboxPatch((0.5, 0.5), w - 1, h - 1, boxstyle="round,pad=0,rounding_size=6", fc=PANEL, ec=LINE, lw=1))
    if title: a.text(20, 30, title, fontsize=14, weight="bold", color=INK, va="center")
    if sub: a.text(20, 52, sub, fontsize=10.5, color=MUT, va="center")
    return a

# header
hd = ax_px(0, 0, W, 88); hd.set_xlim(0, W); hd.set_ylim(88, 0); hd.axis("off")
hd.add_patch(Rectangle((0, 0), W, 88, fc=INK))
hd.add_patch(Rectangle((0, 84), W, 4, fc=YEL))
hd.text(40, 34, "Kopi Senja", fontsize=22, weight="bold", color="white", va="center")
hd.text(40, 64, "Dashboard Penjualan  ·  Jan – Jun 2026  ·  Outlet Kemang, Outlet Tebet, GoFood/GrabFood, Shopee", fontsize=11.5, color="#C9D3E0", va="center")
hd.add_patch(FancyBboxPatch((1290, 26), 270, 34, boxstyle="round,pad=0,rounding_size=17", fc=YEL, ec="none"))
hd.text(1425, 43, "Data fiktif untuk demo", fontsize=12, weight="bold", color=INK, ha="center", va="center")
hd.text(1270, 43, "Update otomatis tiap hari 06.00", fontsize=10.5, color="#C9D3E0", ha="right", va="center")

# KPI tiles
kp = [("Total penjualan", f"Rp {tot/1e9:.2f} M".replace(".", ","), f"+{(mon.sum(axis=1).iloc[5]/mon.sum(axis=1).iloc[0]-1)*100:.0f}% Jun vs Jan"),
      ("Jumlah transaksi", f"{ntrx:,}".replace(",", "."), f"± {ntrx/len(days):.0f} transaksi / hari"),
      ("Rata-rata per transaksi", rp(round(atv, -2)), "semua channel"),
      ("Margin kotor", f"{margin*100:.1f}%".replace(".", ","), f"Outlet {cm['Outlet Kemang']*100:.0f}%  ·  GoFood/GrabFood {cm['GoFood/GrabFood']*100:.0f}%  ·  Shopee {cm['Shopee']*100:.0f}%")]
x0, gap, tw = 40, 20, (W - 80 - 60) / 4
for i, (lab, val, note) in enumerate(kp):
    a = panel(x0 + i * (tw + gap), 108, tw, 112)
    a.add_patch(Rectangle((0.5, 0.5), 5, 111, fc=TEAL if i < 3 else YEL, ec="none"))
    a.text(22, 28, lab, fontsize=11.5, color=MUT, va="center")
    a.text(22, 64, val, fontsize=26, weight="bold", color=INK, va="center")
    a.text(22, 94, note, fontsize=10, color=TEAL if i == 0 else MUT, va="center")

# monthly trend stacked bar
chcol = {"Outlet Kemang": TEAL, "Outlet Tebet": "#7FC4C0", "GoFood/GrabFood": YEL, "Shopee": "#E07A3F"}
panel(40, 240, 900, 360, "Omzet bulanan per channel", "Juta Rupiah")
a = ax_px(100, 315, 820, 245)
bottom = np.zeros(6)
mlab = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"]
for ch in channels:
    a.bar(mlab, mon[ch].values, bottom=bottom, color=chcol[ch], width=0.62, label=ch, edgecolor=PANEL, lw=1.2)
    bottom += mon[ch].values
for i, b in enumerate(bottom):
    a.text(i, b + 4, f"{b:.0f}", ha="center", va="bottom", fontsize=10.5, color=INK, weight="bold")
a.set_ylim(0, bottom.max() * 1.15)
for s in ["top", "right", "left"]: a.spines[s].set_visible(False)
a.spines["bottom"].set_color(LINE)
a.tick_params(colors=MUT, labelsize=10.5, length=0)
a.grid(axis="y", color=LINE, lw=0.8); a.set_axisbelow(True)
a.legend(ncol=4, frameon=False, fontsize=10.5, loc="lower right", bbox_to_anchor=(1.0, 1.02), handlelength=1, handleheight=1, borderaxespad=0)
a.text(1.5, bottom[1:3].max() + 22, "Ramadan", ha="center", fontsize=9.5, color=MUT, style="italic")

# top 5 products
panel(960, 240, 600, 360, "5 produk terlaris", "Omzet Jan – Jun, juta Rupiah")
a = ax_px(1150, 320, 380, 250)
t5 = top.head(5)[::-1] / 1e6
a.barh(t5.index, t5.values, color=[LINE if False else TEAL] * 4 + [YEL], height=0.6)
cols = [TEAL] * 5; cols[-1] = YEL
for bar, c in zip(a.patches, cols): bar.set_color(c)
for i, v in enumerate(t5.values):
    a.text(v + t5.max() * 0.02, i, f"{v:.0f}", va="center", fontsize=10.5, color=INK, weight="bold")
a.set_xlim(0, t5.max() * 1.15); a.set_xticks([])
for s in a.spines.values(): s.set_visible(False)
a.tick_params(length=0, labelsize=11, colors=INK)

# heatmap
panel(40, 620, 900, 350, "Jam ramai (outlet + GoFood/GrabFood)", "Rata-rata transaksi per jam, per hari")
a = ax_px(110, 700, 810, 220)
cmap = LinearSegmentedColormap.from_list("k", ["#F2F6F8", "#BFE0DE", TEAL, "#0A4F4E"])
a.imshow(heat.values, aspect="auto", cmap=cmap)
a.set_yticks(range(7)); a.set_yticklabels(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
a.set_xticks(range(len(hours))); a.set_xticklabels([f"{h:02d}" for h in hours])
a.tick_params(length=0, labelsize=10, colors=MUT)
for s in a.spines.values(): s.set_visible(False)
a.set_xticks(np.arange(-.5, len(hours)), minor=True); a.set_yticks(np.arange(-.5, 7), minor=True)
a.grid(which="minor", color=PANEL, lw=2); a.tick_params(which="minor", length=0)
pk0, pk1 = list(hours).index(15), list(hours).index(18)
a.add_patch(Rectangle((pk0 - .5, -.5), pk1 - pk0 + 1, 7, fill=False, ec=YEL, lw=2.5))
a.text(pk0 + 1.5, -0.75, "Jam ramai 15.00 – 18.00", ha="center", va="bottom", fontsize=10, color=INK, weight="bold")

# slow movers table
p = panel(960, 620, 600, 350, "Produk kurang laku / stok menumpuk", "Jan – Jun 2026, semua channel")
cx = [20, 245, 340, 450]
hdr = ["Produk", "Terjual", "Stok", "Saran"]
p.add_patch(Rectangle((12, 72), 576, 32, fc="#EAEEF3", ec="none"))
for x, t in zip(cx, hdr): p.text(x, 88, t, fontsize=11, weight="bold", color=INK, va="center")
sm = [("Red Velvet Latte", "Hentikan"), ("Kue Lumpur Pandan", "Hentikan"),
      ("Kopi Bubuk Senja 250g", "Promo bundling"), ("Roti Bakar Cokelat", "Kurangi stok")]
for r, (nm, sar) in enumerate(sm):
    y = 128 + r * 46
    st, unit = stock[nm]
    p.text(cx[0], y, nm, fontsize=11, color=INK, va="center")
    p.text(cx[1], y, f"{qty[nm]:,}".replace(",", "."), fontsize=11, color=INK, va="center")
    p.text(cx[2], y, f"{st}", fontsize=11, color=INK, va="center")
    bad = sar == "Hentikan"
    p.add_patch(FancyBboxPatch((cx[3], y - 12), 126, 24, boxstyle="round,pad=0,rounding_size=12",
                               fc="#F6E3DF" if bad else "#E3F1F0", ec="none"))
    p.text(cx[3] + 63, y, sar, fontsize=10, color="#A23B2A" if bad else TEAL, ha="center", va="center", weight="bold")
    p.plot([12, 588], [y + 23, y + 23], color=LINE, lw=0.8)
p.text(20, 322, "Stok = sisa per 30 Jun (unit). Margin online lebih tipis karena komisi aplikasi.", fontsize=9.5, color=MUT, va="center")

buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=100, facecolor=BG); buf.seek(0)
img = Image.open(buf).convert("RGB")
def save(im, path, colors=160):
    q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) if colors else im
    q.save(path, optimize=True)
    print(path, im.size, os.path.getsize(path) // 1024, "KB")
save(img, os.path.join(OUT, "umkm-sales-dashboard.png"), 160)
save(img.resize((800, 500), Image.LANCZOS), os.path.join(OUT, "umkm-sales-dashboard-thumb.png"), 0)
