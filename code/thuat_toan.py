# -*- coding: utf-8 -*-
"""
=============================================================================
 DO AN CHUYEN NGANH - DE TAI 19
 Ung dung khai pha luat ket hop (Association Rules) phan tich
 hanh vi mua sam cua khach hang
-----------------------------------------------------------------------------
 File: thuat_toan.py
 Noi dung: Tu cai dat cac thuat toan khai pha tap pho bien va tao luat ket hop:
   1. Brute-force (vet can)      - thuat toan co ban da hoc
   2. Apriori                    - thuat toan trung tam da hoc (tu cai dat day du,
                                   co buoc join + prune, co truy vet tung buoc)
   3. Tao luat ket hop           - tu cai dat (confidence, lift, leverage, conviction)
   4. FP-Growth                  - thuat toan CHUA HOC, goi tu thu vien mlxtend
                                   (dung de so sanh hieu nang va kiem chung)
=============================================================================
"""

from itertools import combinations
from collections import defaultdict
import time


# =============================================================================
# 1. HAM PHU TRO CHUNG
# =============================================================================

def do_support_quet(giao_dich, ung_vien, n=None):
    """
    Quet toan bo giao dich de dem support cua tung tap ung vien (candidate).

    Tham so:
        giao_dich : list các tap (set/frozenset) - moi phan tu la 1 gio hang
        ung_vien  : list cac frozenset ung vien can dem
        n         : so giao dich (neu khong truyen se tu tinh)
    Tra ve:
        dict {frozenset: so_giao_dich_chua_tap_do}
    """
    if n is None:
        n = len(giao_dich)
    dem = {u: 0 for u in ung_vien}
    for t in giao_dich:
        t = frozenset(t)
        # tap rong luon la tap con cua moi giao dich
        for u in ung_vien:
            if u.issubset(t):
                dem[u] += 1
    return dem


def _lam_dep_label(tap):
    """Dinh dang mot tap item thanh chuoi '{a, b, c}' de in ra."""
    return "{" + ", ".join(sorted(tap)) + "}"


# =============================================================================
# 2. THUAT TOAN BRUTE-FORCE (VET CAN)
# =============================================================================
# Y tuong: xet TOAN BO cac tap con co the cua tap phan tu (ket hop toan hoc
# C(n,1) + C(n,2) + ... = 2^n - 1), dem support cua tung tap roi loc boi
# min_support. Do phuc tap mu, chi kha thi voi so luong phan tu nho.
# =============================================================================

def brute_force(giao_dich, min_sup, k_max=None, trace=None):
    """
    Khai pha tap pho bien bang thuat toan vet can.

    Tra ve: dict {k: {frozenset: so_lan_xuat_hien}} voi cac tap thoa min_sup.
    Neu truyen `trace` (list) thi tung buoc trung gian duoc ghi lai.
    """
    n = len(giao_dich)
    phan_tu = sorted({item for t in giao_dich for item in t})
    if k_max is None:
        k_max = len(phan_tu)

    ket_qua = {}
    if trace is not None:
        trace.append(("PHAN TU", phan_tu, None))

    for k in range(1, k_max + 1):
        # Buoc 1: sinh TAT CA tap con k phan tu (khong co prune)
        ung_vien = [frozenset(c) for c in combinations(phan_tu, k)]
        # Buoc 2: quet dem support tung ung vien
        dem = do_support_quet(giao_dich, ung_vien, n)
        # Buoc 3: loc boi min_support
        L_k = {u: c for u, c in dem.items() if c / n >= min_sup}
        if trace is not None:
            trace.append((f"C{k}", ung_vien, dict(dem)))
            trace.append((f"L{k}", L_k, None))
        if not L_k:
            break
        ket_qua[k] = L_k

    return ket_qua


# =============================================================================
# 3. THUAT TOAN APRIORI (TU CAI DAT DAY DU)
# =============================================================================
# Tinh chat Apriori: moi tap con cua 1 tap pho bien cung pho bien
# => neu X khong pho bien thi moi tap lon hon chua X deu khong pho bien.
# Hai buoc lap voi k = 1, 2, ...:
#   - Join  : sinh C(k) tu L(k-1) (F(k-1) x F(k-1))
#   - Prune : loai bo uong vien co tap con (k-1) phan tu nao do khong thuoc L(k-1)
#   - Quet  : dem support, giu lai L(k)
# =============================================================================

def apriori(giao_dich, min_sup, trace=None):
    """
    Khai pha tap pho bien bang thuat toan Apriori (tu cai dat).

    Tham so:
        giao_dich : list tap item (moi giao dich 1 set)
        min_sup   : nguong ho tro toi thieu (0 < min_sup <= 1)
        trace     : neu la list, tung buoc se duoc ghi de phuc vu trinh bay
    Tra ve:
        (F, dem_L1) voi F = {k: {frozenset: dem}}, dem theo SO LUOT xuat hien.
    """
    n = len(giao_dich)
    G = [frozenset(t) for t in giao_dich]

    # ---------- Buoc 1: tim L1 ----------
    dem1 = defaultdict(int)
    for t in G:
        for item in t:
            dem1[item] += 1
    L1 = {frozenset([i]): c for i, c in dem1.items() if c / n >= min_sup}
    if trace is not None:
        trace.append(("C1", [frozenset([i]) for i in sorted(dem1)],
                      {frozenset([i]): c for i, c in dem1.items()}))
        trace.append(("L1", L1, None))
    if not L1:
        return {}, dem1

    F = {1: L1}
    k = 2
    while F.get(k - 1):
        F_km1 = F[k - 1]
        tap_F_km1 = set(F_km1.keys())

        # ---------- Buoc 2 (JOIN): sinh C(k) tu F(k-1) ----------
        # chuan hoa moi tap (k-1) thanh tuple sap xep de join theo thu tu
        tap_sap_xep = sorted([sorted(u) for u in tap_F_km1])
        ung_vien = set()
        for i in range(len(tap_sap_xep)):
            for j in range(i + 1, len(tap_sap_xep)):
                a, b = tap_sap_xep[i], tap_sap_xep[j]
                if a[:-1] == b[:-1]:          # giong nhau k-2 phan tu dau
                    u = frozenset(a) | frozenset(b)
                    if len(u) == k:
                        ung_vien.add(u)

        # ---------- Buoc 3 (PRUNE): loai ung vien co tap con khong pho bien ----------
        C_k, bi_cat = [], []
        for u in ung_vien:
            if all(frozenset(sub) in tap_F_km1 for sub in combinations(u, k - 1)):
                C_k.append(u)
            else:
                bi_cat.append(u)

        # ---------- Buoc 4 (QUET): dem support cua C(k) ----------
        dem = do_support_quet(G, C_k, n)
        L_k = {u: c for u, c in dem.items() if c / n >= min_sup}

        if trace is not None:
            trace.append((f"C{k}", C_k, dict(dem), bi_cat))
            trace.append((f"L{k}", L_k, None))

        if L_k:
            F[k] = L_k
        k += 1

    return F, dem1


# =============================================================================
# 4. APRIORI TOI UU CHO DU LIEU LON (dem theo danh sach giao dich dung chung)
# =============================================================================
# Van la dung thuat toan Apriori, nhung buoc dem support khong quet lai toan
# bo giao dich voi tung ung vien, ma dung chi muc nguoc (inverted index):
#   item -> tap hop cac giao dich chua item.
# Support cua tap X = kich thuoc giao cua cac danh sach giao dich cua item.
# =============================================================================

def apriori_nhanh(giao_dich, min_sup, max_k=None):
    n = len(giao_dich)
    G = [frozenset(t) for t in giao_dich]
    chi_muc = defaultdict(set)                      # item -> tap tid
    for tid, t in enumerate(G):
        for item in t:
            chi_muc[item].add(tid)

    dem1 = {i: len(tids) for i, tids in chi_muc.items()}
    L1 = {frozenset([i]): c for i, c in dem1.items() if c / n >= min_sup}
    if not L1:
        return {}

    F = {1: L1}
    # tid-list cua cac tap pho bien hien tai
    tid_lists = {u: set.intersection(*(chi_muc[i] for i in u)) for u in L1}
    k = 2
    while F.get(k - 1) and (max_k is None or k <= max_k):
        F_km1 = F[k - 1]
        tap_F_km1 = set(F_km1.keys())
        tap_sap_xep = sorted([sorted(u) for u in tap_F_km1])
        ung_vien = set()
        for i in range(len(tap_sap_xep)):
            for j in range(i + 1, len(tap_sap_xep)):
                a, b = tap_sap_xep[i], tap_sap_xep[j]
                if a[:-1] == b[:-1]:
                    ung_vien.add(frozenset(a) | frozenset(b))

        L_k = {}
        for u in ung_vien:
            if not all(frozenset(sub) in tap_F_km1 for sub in combinations(u, k - 1)):
                continue                            # prune
            # dem support bang giao tid-list: chi tinh tren cac tap con da biet
            tids = set.intersection(*(tid_lists[frozenset(sub)]
                                      for sub in combinations(u, k - 1)))
            if len(tids) / n >= min_sup:
                L_k[u] = len(tids)
                tid_lists[u] = tids
        if L_k:
            F[k] = L_k
        k += 1
    return F


# =============================================================================
# 5. TAO LUAT KET HOP TU CAC TAP PHO BIEN (TU CAI DAT)
# =============================================================================
# Voi moi tap pho bien X (|X| >= 2) va moi phan hoach X = A ∪ B (A, B khac rong):
#   support(X)  = dem(X) / N
#   confidence(A->B) = support(X) / support(A)
#   lift(A->B)       = confidence / support(B)
#   leverage(A->B)   = support(X) - support(A)*support(B)
#   conviction(A->B) = (1 - support(B)) / (1 - confidence)
# Chi giu luat thoa min_conf (va min_lift neu co).
# =============================================================================

def tao_luat_ket_hop(F, n, min_conf=0.5, min_lift=1.0):
    """
    F : dict {k: {frozenset: dem}} ket qua khai pha tap pho bien
    n : so giao dich
    Tra ve: list dict luat, moi luat gom: truoc (A), sau (B), va cac do luong.
    """
    luat = []
    for k, L_k in F.items():
        if k < 2:
            continue
        for X, dem_X in L_k.items():
            sup_X = dem_X / n
            cac_phan_tu = sorted(X)
            for r in range(1, k):
                for A in combinations(cac_phan_tu, r):
                    A = frozenset(A)
                    B = X - A
                    dem_A = _dem_tap(F, A)
                    dem_B = _dem_tap(F, B)
                    if not dem_A or not dem_B:
                        continue
                    sup_A, sup_B = dem_A / n, dem_B / n
                    conf = sup_X / sup_A
                    lift = conf / sup_B
                    if conf < min_conf or lift < min_lift:
                        continue
                    lev = sup_X - sup_A * sup_B
                    conv = (1 - sup_B) / (1 - conf) if conf < 1 else float("inf")
                    luat.append({
                        "truoc": A, "sau": B,
                        "sup_X": sup_X, "sup_A": sup_A, "sup_B": sup_B,
                        "conf": conf, "lift": lift,
                        "leverage": lev, "conviction": conv,
                    })
    luat.sort(key=lambda d: (-d["lift"], -d["conf"]))
    return luat


def _dem_tap(F, u):
    """Tra ve so luot xuat hien cua tap u trong ket qua Apriori F (0 neu khong co)."""
    for k in (len(u),):
        L_k = F.get(k, {})
        if u in L_k:
            return L_k[u]
    return 0


def thoi_gian(ham, *a, **kw):
    """Do thoi gian chay cua 1 ham, tra ve (ket_qua, so_giay)."""
    t0 = time.perf_counter()
    kq = ham(*a, **kw)
    return kq, time.perf_counter() - t0
