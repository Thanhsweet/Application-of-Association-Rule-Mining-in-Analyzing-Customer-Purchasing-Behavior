# -*- coding: utf-8 -*-
"""
=============================================================================
 File: 02_phan_tich_du_lieu_lon.py
 Noi dung: Ap dung khai pha luat ket hop tren du lieu that
   Bo du lieu: "Online Retail" (UCI Machine Learning Repository)
               ~541.900 dong, 25.900 don hang, 01/12/2010 - 09/12/2011,
               cua mot cua hang ban le truc tuyen tai Anh.
 Quy trinh:
   (1) Doc + lam sach du lieu
   (2) Kham pha du lieu (EDA) + truc quan hoa
   (3) Xay dung "gio hang" theo don hang (InvoiceNo)
   (4) Ma hoa One-hot, khai pha tap pho bien bang 3 thuat toan:
         - Apriori tu cai dat (apriori_nhanh)
         - Apriori thu vien mlxtend
         - FP-Growth thu vien mlxtend (thuat toan CHUA HOC)
   (5) Kiem chung cheo: ket qua Apriori tu viet == FP-Growth thu vien
   (6) Tao luat ket hop + phan tich y nghia kinh doanh
   (7) Luu bang ket qua, hinh anh, va tong_ket.json cho bao cao
=============================================================================
"""

import os
import sys
import json
import time
import warnings
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori as ml_apriori, fpgrowth as ml_fpgrowth, association_rules as ml_rules

from thuat_toan import apriori_nhanh, tao_luat_ket_hop

# ---------------------------------------------------------------------------
# Cau hinh chung
# ---------------------------------------------------------------------------
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DU_LIEU = "/tmp/doan19/data/Online Retail.xlsx"
HINH = os.path.join(GOC, "hinh_anh")
KQ = os.path.join(GOC, "ket_qua")
os.makedirs(HINH, exist_ok=True); os.makedirs(KQ, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.grid": True, "grid.alpha": 0.3,
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
})
MAU_CHINH, MAU_PHU = "#1f5fa8", "#e8833a"

tong_ket = {}

# ===========================================================================
# (1) DOC + LAM SACH DU LIEU
# ===========================================================================
print("== (1) Doc du lieu ==")
t0 = time.perf_counter()
df = pd.read_excel(DU_LIEU, engine="openpyxl")
print(f"   Doc xong {len(df):,} dong trong {time.perf_counter()-t0:.1f}s")
tong_ket["so_dong_goc"] = int(len(df))
tong_ket["so_cot_goc"] = int(df.shape[1])

# Lam sach theo quy trinh chuan cho bo du lieu nay:
#  - bo dong thieu mo ta san pham (Description rong)
#  - bo don hang huy (ma hoa don bat dau bang 'C', Quantity am)
#  - chi giu Quantity > 0 va UnitPrice > 0
#  - bo cac khoan thu dich vu khong phai san pham (postage, chi phi ngan hang...)
df = df.dropna(subset=["Description"]).copy()
df["InvoiceNo"] = df["InvoiceNo"].astype(str)
don_huy = df["InvoiceNo"].str.startswith("C")
df = df[~don_huy]
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
df["Description"] = (df["Description"].astype(str)
                     .str.upper().str.strip()
                     .str.replace(r"\s+", " ", regex=True))
dich_vu = ["POSTAGE", "POST", "DOTCOM POSTAGE", "CARRIAGE", "BANK CHARGES",
           "AMAZON FEE", "MANUAL", "SAMPLES", "PADS", "ADJUST"]
mask_dv = df["Description"].str.startswith(tuple(dich_vu))
df = df[~mask_dv]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print(f"   Sau lam sach: {len(df):,} dong | {df['InvoiceNo'].nunique():,} don hang | "
      f"{df['Description'].nunique():,} mat hang")
tong_ket["so_dong_sach"] = int(len(df))
tong_ket["so_don_hang_sach"] = int(df["InvoiceNo"].nunique())
tong_ket["so_mat_hang_sach"] = int(df["Description"].nunique())

# Giao dich phan tich chinh: thuong mai dien tu tai Anh quoc (chiem da so don hang)
df_uk = df[df["Country"] == "United Kingdom"].copy()
tong_ket["ti_le_uk"] = round(float(len(df_uk) / len(df)), 4)
print(f"   Phan tich chinh tren United Kingdom: {len(df_uk):,} dong "
      f"({tong_ket['ti_le_uk']*100:.1f}%)")

# ===========================================================================
# (2) EDA + TRUC QUAN HOA
# ===========================================================================
print("== (2) EDA ==")

# --- Hinh 1: Top 10 san pham ban chay (theo so don hang) ---
top_sp = (df_uk.groupby("Description")["InvoiceNo"].nunique()
          .sort_values(ascending=False).head(10))
fig, ax = plt.subplots(figsize=(8, 4.2))
y = np.arange(len(top_sp))[::-1]
ax.barh(y, top_sp.values, color=MAU_CHINH)
ax.set_yticks(y)
ax.set_yticklabels([t[:38] + ("…" if len(t) > 38 else "") for t in top_sp.index], fontsize=8.5)
ax.set_xlabel("Số đơn hàng chứa sản phẩm")
ax.set_title("Top 10 sản phẩm xuất hiện trong nhiều đơn hàng nhất (Anh Quốc)", fontsize=10.5)
for yi, v in zip(y, top_sp.values):
    ax.text(v + 40, yi, f"{v:,}", va="center", fontsize=8)
fig.savefig(os.path.join(HINH, "fig01_top_san_pham.png")); plt.close(fig)

# --- Hinh 2: So don hang theo thang ---
don_thang = df_uk.assign(thang=df_uk["InvoiceDate"].dt.to_period("M")) \
                 .groupby("thang")["InvoiceNo"].nunique()
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.bar([str(t) for t in don_thang.index], don_thang.values, color=MAU_CHINH)
ax.set_ylabel("Số đơn hàng")
ax.set_title("Số đơn hàng theo tháng (12/2010 – 12/2011)", fontsize=10.5)
ax.tick_params(axis="x", rotation=60, labelsize=8)
fig.savefig(os.path.join(HINH, "fig02_don_hang_theo_thang.png")); plt.close(fig)

# --- Hinh 3: Phan bo so mat hang moi gio hang ---
gio_raw = df_uk.groupby("InvoiceNo")["Description"].apply(set)
so_mh = gio_raw.apply(len)
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.hist(so_mh.clip(upper=60), bins=40, color=MAU_PHU, edgecolor="white")
ax.axvline(so_mh.median(), color=MAU_CHINH, ls="--",
           label=f"Trung vị = {so_mh.median():.0f}")
ax.set_xlabel("Số mặt hàng trong 1 giỏ hàng (cắt tại 60)")
ax.set_ylabel("Số giỏ hàng")
ax.set_title("Phân bố số lượng mặt hàng theo giỏ hàng", fontsize=10.5)
ax.legend()
fig.savefig(os.path.join(HINH, "fig03_hist_gio_hang.png")); plt.close(fig)
tong_ket["gio_hang_uk"] = int(len(gio_raw))
tong_ket["mat_hang_tb_gio"] = round(float(so_mh.mean()), 2)
tong_ket["trung_vi_gio"] = float(so_mh.median())

# ===========================================================================
# (3) XAY DUNG GIO HANG + MA HOA ONE-HOT
# ===========================================================================
print("== (3) Xay dung gio hang ==")
gio_hang = [frozenset(t) for t in gio_raw.values]

# Loai mat hang hiem (chi xuat hien trong < 30 gio hang) de giam nhieu va
# tang kha thi — mot luat neu nhuoc suport rat thap cung it gia tri hanh dong.
dem_mh = {}
for t in gio_hang:
    for i in t:
        dem_mh[i] = dem_mh.get(i, 0) + 1
SO_LUOT_TOI_THIEU = 30
gio_hang = [frozenset(i for i in t if dem_mh.get(i, 0) >= SO_LUOT_TOI_THIEU)
            for t in gio_hang]
gio_hang = [t for t in gio_hang if len(t) >= 2]     # gio 1 mat hang khong ra luat
tap_hang = sorted({i for t in gio_hang for i in t})
print(f"   Gio hang: {len(gio_hang):,} | mat hang (xuất hiện ≥ {SO_LUOT_TOI_THIEU} giỏ): {len(tap_hang):,}")
tong_ket["gio_hang_phan_tich"] = int(len(gio_hang))
tong_ket["mat_hang_phan_tich"] = int(len(tap_hang))
tong_ket["so_luot_toi_thieu_mh"] = SO_LUOT_TOI_THIEU

te = TransactionEncoder()
ma_tran = te.fit(gio_hang).transform(gio_hang)
onehot = pd.DataFrame(ma_tran, columns=te.columns_)

# ===========================================================================
# (4) KHAI PHA TAP PHO BIEN BANG 3 THUAT TOAN + SO SANH HIEU NANG
# ===========================================================================
print("== (4) Khai pha tap pho bien — so sanh hieu nang ==")
cac_nguong = [0.06, 0.04, 0.03, 0.02, 0.015]
bang_hieu_nang = []
for ms in cac_nguong:
    # --- Apriori tu cai dat ---
    t0 = time.perf_counter(); F = apriori_nhanh(gio_hang, ms); t1 = time.perf_counter() - t0
    so_tap_tu_viet = sum(len(v) for v in F.values())
    # --- Apriori mlxtend ---
    t0 = time.perf_counter()
    fml = ml_apriori(onehot, min_support=ms, use_colnames=True, low_memory=True)
    t2 = time.perf_counter() - t0
    # --- FP-Growth mlxtend ---
    t0 = time.perf_counter()
    ffp = ml_fpgrowth(onehot, min_support=ms, use_colnames=True)
    t3 = time.perf_counter() - t0
    bang_hieu_nang.append({"min_support": ms, "apriori_tu_viet_s": round(t1, 2),
                           "apriori_mlxtend_s": round(t2, 2), "fpgrowth_s": round(t3, 2),
                           "so_tap_pho_bien": int(len(ffp)), "apriori_tuviet_so_tap": so_tap_tu_viet})
    print(f"   sup={ms}: Apriori(tviet)={t1:.1f}s | Apriori(mlxtend)={t2:.1f}s | "
          f"FP-Growth={t3:.1f}s | so tap: tviet={so_tap_tu_viet}, fpgrowth={len(ffp)}")
pd.DataFrame(bang_hieu_nang).to_csv(os.path.join(KQ, "so_sanh_hieu_nang.csv"),
                                    index=False, encoding="utf-8-sig")
tong_ket["bang_hieu_nang"] = bang_hieu_nang

# --- Hinh 4: Do chay thoi gian 3 thuat toan ---
bn = pd.DataFrame(bang_hieu_nang)
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.plot(bn["min_support"], bn["apriori_tu_viet_s"], "o-", color=MAU_CHINH, label="Apriori (tự cài đặt)")
ax.plot(bn["min_support"], bn["apriori_mlxtend_s"], "s-", color=MAU_PHU, label="Apriori (thư viện mlxtend)")
ax.plot(bn["min_support"], bn["fpgrowth_s"], "^-", color="#2e8b57", label="FP-Growth (thư viện mlxtend)")
ax.set_xlabel("min_support"); ax.set_ylabel("Thời gian chạy (giây, thang log)")
ax.set_yscale("log")
ax.set_title("So sánh thời gian chạy 3 thuật toán khai phá tập phổ biến", fontsize=10.5)
ax.legend()
ax.invert_xaxis()
fig.savefig(os.path.join(HINH, "fig04_so_sanh_hieu_nang.png")); plt.close(fig)

# ===========================================================================
# (5) CHON THONG SO + KIEM CHUNG CHEO APRIORI vs FP-GROWTH
# ===========================================================================
MIN_SUP = 0.02
print(f"== (5) Chon min_support = {MIN_SUP} — kiem chung cheo ==")
t0 = time.perf_counter(); F = apriori_nhanh(gio_hang, MIN_SUP); t_ap = time.perf_counter() - t0
tap_pho_bien = {k: {u: c for u, c in L.items()} for k, L in F.items()}
N = len(gio_hang)
so_tap_theo_k = {k: len(v) for k, v in tap_pho_bien.items()}
tong_ket.update({"min_sup_chon": MIN_SUP, "thoi_gian_apriori_s": round(t_ap, 2),
                 "so_tap_theo_k": {str(k): v for k, v in so_tap_theo_k.items()}})
print(f"   Apriori tu viet: {sum(so_tap_theo_k.values())} tap {so_tap_theo_k} trong {t_ap:.1f}s")

ffp = ml_fpgrowth(onehot, min_support=MIN_SUP, use_colnames=True)
fp_sets = {frozenset(c) for c in ffp["itemsets"]}
ap_sets = {u for L in tap_pho_bien.values() for u in L}
khop = fp_sets == ap_sets
print(f"   FP-Growth: {len(fp_sets)} tap | Giao/kiem chung: {'KHOP 100%' if khop else 'LECH!'}")
tong_ket["kiem_chung_fpgrowth_khop"] = bool(khop)
if not khop:
    print("   Thu lai voi bo so khac..."); sys.exit(1)

# luu CSV cac tap pho bien
hang_tap = []
for k, L in tap_pho_bien.items():
    for u, c in L.items():
        hang_tap.append({"cac_mat_hang": " + ".join(sorted(u)), "k": k,
                         "so_gio_hang": c, "support": round(c / N, 5)})
pd.DataFrame(hang_tap).sort_values(["k", "support"], ascending=[True, False]) \
  .to_csv(os.path.join(KQ, "tap_pho_bien.csv"), index=False, encoding="utf-8-sig")

# --- Hinh 5: So tap pho bien theo k ---
fig, ax = plt.subplots(figsize=(6.5, 3.6))
ks = sorted(so_tap_theo_k)
ax.bar([f"k = {k}" for k in ks], [so_tap_theo_k[k] for k in ks], color=MAU_CHINH)
for i, k in enumerate(ks):
    ax.text(i, so_tap_theo_k[k], f"{so_tap_theo_k[k]:,}", ha="center", va="bottom", fontsize=9)
ax.set_ylabel("Số tập phổ biến")
ax.set_title(f"Số lượng tập phổ biến theo độ dài k (min_support = {MIN_SUP})", fontsize=10.5)
ax.set_yscale("log")
fig.savefig(os.path.join(HINH, "fig05_tap_pho_bien_theo_k.png")); plt.close(fig)

# ===========================================================================
# (6) TAO LUAT KET HOP + PHAN TICH Y NGHIA KINH DOANH
# ===========================================================================
MIN_CONF, MIN_LIFT = 0.35, 1.2
luat = tao_luat_ket_hop(tap_pho_bien, N, min_conf=MIN_CONF, min_lift=MIN_LIFT)
print(f"== (6) Luat ket hop: {len(luat)} luat (conf>={MIN_CONF}, lift>={MIN_LIFT}) ==")

# Kiem chung cheo luat voi thu vien mlxtend
fml = ml_apriori(onehot, min_support=MIN_SUP, use_colnames=True)
rml = ml_rules(fml, metric="confidence", min_threshold=MIN_CONF)
rml = rml[rml["lift"] >= MIN_LIFT]
bo_ml = {(frozenset(a), frozenset(c)) for a, c in zip(rml["antecedents"], rml["consequents"])}
bo_tv = {(l["truoc"], l["sau"]) for l in luat}
print(f"   Luat tu viet: {len(bo_tv)} | luat mlxtend: {len(bo_ml)} | "
      f"{'KHOP 100%' if bo_ml == bo_tv else 'LECH!'}")
tong_ket.update({"min_conf": MIN_CONF, "min_lift": MIN_LIFT,
                 "so_luat": len(bo_tv), "kiem_chung_luat_khop": bool(bo_ml == bo_tv)})

# bang luat day du
hang_luat = []
for l in luat:
    hang_luat.append({
        "luat": " → ".join([" + ".join(sorted(l["truoc"])), " + ".join(sorted(l["sau"]))]),
        "support": round(l["sup_X"], 4), "confidence": round(l["conf"], 4),
        "lift": round(l["lift"], 4), "leverage": round(l["leverage"], 4),
        "conviction": round(l["conviction"], 3),
    })
df_luat = pd.DataFrame(hang_luat)
df_luat.to_csv(os.path.join(KQ, "luat_ket_hop.csv"), index=False, encoding="utf-8-sig")

# top 15 luat theo lift va top 15 theo confidence
top_lift = df_luat.sort_values("lift", ascending=False).head(15)
top_conf = df_luat.sort_values("confidence", ascending=False).head(15)
top_lift.to_csv(os.path.join(KQ, "top15_luat_theo_lift.csv"), index=False, encoding="utf-8-sig")
top_conf.to_csv(os.path.join(KQ, "top15_luat_theo_confidence.csv"), index=False, encoding="utf-8-sig")
tong_ket["top10_theo_lift"] = top_lift.head(10).to_dict("records")
tong_ket["top10_theo_conf"] = top_conf.head(10).to_dict("records")

# --- Hinh 6: Scatter support vs confidence, mau = lift ---
fig, ax = plt.subplots(figsize=(7.5, 5))
sc = ax.scatter(df_luat["support"], df_luat["confidence"], c=df_luat["lift"],
                cmap="viridis", s=28, alpha=0.75, edgecolors="k", linewidths=0.2)
plt.colorbar(sc, label="Lift")
ax.set_xlabel("Support (A ∪ B)"); ax.set_ylabel("Confidence")
ax.set_title(f"Phân bố {len(df_luat)} luật kết hợp theo support–confidence (màu = lift)", fontsize=10.5)
fig.savefig(os.path.join(HINH, "fig06_scatter_luat.png")); plt.close(fig)

# --- Hinh 7: Top 10 luat theo lift (barh) ---
def rut_gon(s, n=30):
    return s if len(s) <= n else s[: n - 1] + "…"

fig, ax = plt.subplots(figsize=(9.4, 4.8))
t10 = top_lift.head(10).iloc[::-1]
nhan = []
for _, r in t10.iterrows():
    truoc, sau = r["luat"].split(" → ")
    nhan.append(f"{rut_gon(truoc, 34)} → {rut_gon(sau, 26)}")
y = np.arange(len(t10))
ax.barh(y, t10["lift"], color=MAU_PHU)
ax.set_yticks(y); ax.set_yticklabels(nhan, fontsize=8)
ax.set_xlabel("Lift")
ax.set_title("Top 10 luật kết hợp có lift cao nhất", fontsize=10.5)
for yi, (v, c) in enumerate(zip(t10["lift"], t10["confidence"])):
    ax.text(v + 0.05, yi, f"conf={c:.2f}", va="center", fontsize=7.5)
ax.set_xlim(0, t10["lift"].max() * 1.18)
fig.savefig(os.path.join(HINH, "fig07_top_luat_lift.png")); plt.close(fig)

# --- Hinh 8: Heatmap lift cua cac luat co support cao nhat (chi luat 1-1) ---
# Giao dien bo tro cho Hinh 7 (luat lift cao): day la cac luat "cot song"
# xuat hien trong nhieu gio hang nhat.
luat_11 = [l for l in luat if len(l["truoc"]) == 1 and len(l["sau"]) == 1]
luat_11.sort(key=lambda l: -l["sup_X"])
top_a, top_b = [], []
for l in luat_11:
    a = " + ".join(sorted(l["truoc"])); b = " + ".join(sorted(l["sau"]))
    if a not in top_a and len(top_a) < 8:
        top_a.append(a)
    if b not in top_b and len(top_b) < 8:
        top_b.append(b)
nhan_a = [rut_gon(a, 30) for a in top_a]
nhan_b = [rut_gon(b, 30) for b in top_b]
M = np.full((len(top_a), len(top_b)), np.nan)
vi_tri = {(" + ".join(sorted(l["truoc"])), " + ".join(sorted(l["sau"]))): l for l in luat_11}
for i, a in enumerate(top_a):
    for j, b in enumerate(top_b):
        l = vi_tri.get((a, b))
        if l is not None:
            M[i, j] = l["lift"]
fig, ax = plt.subplots(figsize=(9, 5))
im = ax.imshow(M, cmap="YlGnBu", aspect="auto")
ax.set_xticks(range(len(top_b))); ax.set_xticklabels(nhan_b, rotation=45, ha="right", fontsize=7.5)
ax.set_yticks(range(len(top_a))); ax.set_yticklabels(nhan_a, fontsize=7.5)
vmax_hm = np.nanmax(M)
for i in range(len(top_a)):
    for j in range(len(top_b)):
        if not np.isnan(M[i, j]):
            mau_chu = "white" if M[i, j] > 0.6 * vmax_hm else "#1a2430"
            ax.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=7, color=mau_chu)
ax.set_title("Giá trị lift của các luật có support cao nhất (8 vế trước × 8 vế sau)", fontsize=10.5)
ax.grid(False)
plt.colorbar(im, label="Lift")
fig.savefig(os.path.join(HINH, "fig08_heatmap_luat.png")); plt.close(fig)

# ===========================================================================
# (7) LUU TONG KET
# ===========================================================================
with open(os.path.join(KQ, "tong_ket.json"), "w", encoding="utf-8") as f:
    json.dump(tong_ket, f, ensure_ascii=False, indent=2)
print("== Xong! Da luu hinh_anh/, ket_qua/, tong_ket.json ==")
