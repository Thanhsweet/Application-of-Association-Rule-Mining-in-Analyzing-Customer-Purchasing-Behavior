# -*- coding: utf-8 -*-
"""
=============================================================================
 File: 01_minh_hoa_tung_buoc.py
 Noi dung: Chay tung buoc (step-by-step) Brute-force, Apriori va viec tao luat
 ket hop tren BO DU LIEU MAU 9 giao dich (vi du kinh dien AllElectronics trong
 giao trinh "Data Mining: Concepts and Techniques" - Han & Kamber),
 min_support = 2/9 ≈ 22.2%, min_confidence = 2/3 ≈ 66.7%.
 Ket qua chay duoc ghi vao ket_qua/minh_hoa_tung_buoc.txt de trinh bay trong bao cao.
=============================================================================
"""

import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thuat_toan import brute_force, apriori, tao_luat_ket_hop, _lam_dep_label

# -----------------------------------------------------------------------------
# BO DU LIEU MAU: 9 giao dich, 5 mat hang (I1..I5)
# -----------------------------------------------------------------------------
GIAO_DICH_MAU = [
    {"I1", "I2", "I5"},          # T1
    {"I2", "I4"},                # T2
    {"I2", "I3"},                # T3
    {"I1", "I2", "I4"},          # T4
    {"I1", "I3"},                # T5
    {"I2", "I3"},                # T6
    {"I1", "I3"},                # T7
    {"I1", "I2", "I3", "I5"},    # T8
    {"I1", "I2", "I3"},          # T9
]

MIN_SUP = 2 / 9          # 22.2%
MIN_CONF = 2 / 3         # 66.7%
N = len(GIAO_DICH_MAU)

lines = []
def in_(s=""):
    print(s)
    lines.append(s)

in_("=" * 74)
in_("BO DU LIEU MAU (9 giao dich, min_support = 2/9 = 22.2%, min_conf = 2/3 = 66.7%)")
in_("=" * 74)
for i, t in enumerate(GIAO_DICH_MAU, 1):
    in_(f"  T{i}: {_lam_dep_label(t)}")
in_()

# -----------------------------------------------------------------------------
# 1. BRUTE-FORCE
# -----------------------------------------------------------------------------
in_("=" * 74)
in_("1. THUAT TOAN BRUTE-FORCE (VET CAN)")
in_("=" * 74)
trace_bf = []
F_bf = brute_force(GIAO_DICH_MAU, MIN_SUP, trace=trace_bf)
for buoc, du_lieu, dem in trace_bf:
    if buoc == "PHAN TU":
        in_(f"Tap phan tu: {_lam_dep_label(du_lieu)}  (2^5 - 1 = 31 tap con xet duyet)")
    elif buoc.startswith("C"):
        in_(f"[{buoc}] Sinh tat ca {len(du_lieu)} tap ung vien {len(next(iter(du_lieu))) if du_lieu else '?'} phan tu:")
        for u in du_lieu:
            c = dem.get(u, 0)
            in_(f"    {_lam_dep_label(u)}: support = {c}/{N} = {c/N:.3f}")
    elif buoc.startswith("L"):
        in_(f"[{buoc}] Tap pho bien sau loc (sup >= 22.2%):")
        for u, c in sorted(du_lieu.items(), key=lambda x: sorted(x[0])):
            in_(f"    {_lam_dep_label(u)}: support = {c}/{N} = {c/N:.3f}")
        in_()

# -----------------------------------------------------------------------------
# 2. APRIORI
# -----------------------------------------------------------------------------
in_("=" * 74)
in_("2. THUAT TOAN APRIORI (TU CAI DAT - JOIN + PRUNE + QUET)")
in_("=" * 74)
trace_ap = []
F_ap, _ = apriori(GIAO_DICH_MAU, MIN_SUP, trace=trace_ap)
for buoc in trace_ap:
    ten = buoc[0]
    if ten == "C1":
        _, cac_uong_vien, dem = buoc
        in_(f"[C1] Quet dem support tung mat hang:")
        for u in sorted(cac_uong_vien, key=lambda x: sorted(x)):
            c = dem[u]
            in_(f"    {_lam_dep_label(u)}: support = {c}/{N} = {c/N:.3f}")
    elif ten == "L1":
        in_(f"[L1] Tap pho bien cap 1 (sup >= 22.2%):")
        for u, c in sorted(buoc[1].items(), key=lambda x: sorted(x[0])):
            in_(f"    {_lam_dep_label(u)}: support = {c}/{N} = {c/N:.3f}")
    elif ten.startswith("C"):
        cac_uong_vien, dem, bi_cat = buoc[1], buoc[2], buoc[3]
        in_(f"[{ten}] JOIN sinh {len(cac_uong_vien) + len(bi_cat)} ung vien, "
             f"PRUNE loai {len(bi_cat)} ung vien co tap con khong pho bien:")
        for u in bi_cat:
            in_(f"    {_lam_dep_label(u)}  <- BI CAT (ton tai tap con khong thuoc L{k_ if (k_:=int(ten[1:])-1) else 0})")
        for u in sorted(cac_uong_vien, key=lambda x: sorted(x)):
            c = dem.get(u, 0)
            in_(f"    {_lam_dep_label(u)}: support = {c}/{N} = {c/N:.3f}")
    elif ten.startswith("L") and ten != "L1":
        in_(f"[{ten}] Tap pho bien sau quet:")
        for u, c in sorted(buoc[1].items(), key=lambda x: sorted(x[0])):
            in_(f"    {_lam_dep_label(u)}: support = {c}/{N} = {c/N:.3f}")
        in_()

# -----------------------------------------------------------------------------
# 3. TAO LUAT KET HOP
# -----------------------------------------------------------------------------
in_("=" * 74)
in_("3. TAO LUAT KET HOP (min_conf = 66.7%, min_lift = 1)")
in_("=" * 74)
luat = tao_luat_ket_hop(F_ap, N, min_conf=MIN_CONF, min_lift=1.0)
in_(f"So luat thoa dieu kien: {len(luat)}")
in_(f"{'Luat':<28}{'sup(A∪B)':>9}{'conf':>8}{'lift':>8}{'leverage':>10}")
for l in luat:
    in_(f"{_lam_dep_label(l['truoc'])+' -> '+_lam_dep_label(l['sau']):<28}"
        f"{l['sup_X']:>9.3f}{l['conf']:>8.3f}{l['lift']:>8.3f}{l['leverage']:>10.3f}")

# -----------------------------------------------------------------------------
# 4. KIEM CHUNG VOI KET QUA SACH GIAO KHOA (Han & Kamber)
# -----------------------------------------------------------------------------
in_()
in_("=" * 74)
in_("4. KIEM CHUNG VOI KET QUA CHUAN TRONG GIAO TRINH (Han & Kamber)")
in_("=" * 74)
in_("Giao trinh cho ket qua (min_sup = 2/9):")
in_("  L1 = {I1, I2, I3, I4, I5}")
in_("  L2 = {I1,I2}:4, {I1,I3}:4, {I1,I5}:2, {I2,I3}:4, {I2,I4}:2, {I2,I5}:2")
in_("  L3 = {I1,I2,I3}:2, {I1,I2,I5}:2")
kq_chuan = {
    1: {"I1", "I2", "I3", "I4", "I5"},
    2: [("I1","I2"), ("I1","I3"), ("I1","I5"), ("I2","I3"),
        ("I2","I4"), ("I2","I5")],
    3: [("I1","I2","I3"), ("I1","I2","I5")],
}
def chuan_hoa(x):
    """Chuan hoa 1 tap thanh tuple chuoi sap xep tang dan de so sanh."""
    if isinstance(x, frozenset):
        return tuple(sorted(x))
    if isinstance(x, (tuple, list)):
        return tuple(sorted(x))
    return (x,)                       # chuoi don "I1"

ok = True
for k, kq in kq_chuan.items():
    nhan_duoc = {chuan_hoa(u) for u in F_ap.get(k, {})}
    chuan = {chuan_hoa(x) for x in kq}
    dung = nhan_duoc == chuan
    ok &= dung
    in_(f"  L{k}: {'DUNG' if dung else 'SAI'}  "
         f"(code: {len(nhan_duoc)} tap | chuan: {len(chuan)} tap)")
in_(f"\n==> KET LUAN KIEM CHUNG: {'KHOP HOAN TOAN voi giao trinh' if ok else 'CO LECH - can kiem tra lai!'}")

# Luu ket qua de trinh bay trong bao cao
out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ket_qua")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "minh_hoa_tung_buoc.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n[Da luu] ket_qua/minh_hoa_tung_buoc.txt")
