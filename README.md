# Đồ án chuyên ngành — Đề tài 19

**Ứng dụng khai phá luật kết hợp (Association Rules) phân tích hành vi mua sắm của khách hàng**

Học phần: Đồ án chuyên ngành (31221207) — Khoa Toán - Tin, Trường ĐH Sư phạm - ĐH Đà Nẵng

---

## 1. Sản phẩm

| Tệp | Nội dung |
|---|---|
| `van_ban/De_cuong_do_an.docx` (+ `.pdf`) | Đề cương theo mẫu khoa (5 mục + bảng kế hoạch 8 tuần) |
| `van_ban/Bao_cao_do_an.docx` (+ `.pdf`) | Báo cáo đồ án 30 trang: bìa theo mẫu, mục lục tự động, Mở đầu, Chương 1–3, Kết luận, Tài liệu tham khảo, Phụ lục mã nguồn |
| `van_ban/Slides_bao_ve.pptx` (+ `.pdf`) | 16 slide thuyết trình bảo vệ |
| `code/thuat_toan.py` | Tự cài đặt Brute-force + Apriori (join/prune/quét, có truy vết từng bước), Apriori tối ưu tid-list cho dữ liệu lớn, tự sinh luật (support/confidence/lift/leverage/conviction) |
| `code/01_minh_hoa_tung_buoc.py` | Chạy từng bước trên bộ mẫu 9 giao dịch (Han & Kamber), tự kiểm chứng khớp đáp án giáo trình — xuất `ket_qua/minh_hoa_tung_buoc.txt` |
| `code/02_phan_tich_du_lieu_lon.py` | Toàn bộ quy trình trên dữ liệu thật Online Retail (làm sạch, EDA, giỏ hàng, khai phá 3 thuật toán, kiểm chứng chéo, 8 hình, các bảng kết quả) |
| `hinh_anh/` | 8 hình đã dùng trong báo cáo/slides |
| `ket_qua/` | `minh_hoa_tung_buoc.txt`, `tap_pho_bien.csv`, `luat_ket_hop.csv`, `top15_luat_theo_lift.csv`, `top15_luat_theo_confidence.csv`, `so_sanh_hieu_nang.csv`, `tong_ket.json` |

## 2. Cách chạy

```bash
# môi trường (Python 3.12+)
uv venv .venv -p 3.12 && source .venv/bin/activate
uv pip install pandas numpy matplotlib openpyxl mlxtend pypdf requests

# tải dữ liệu Online Retail (UCI, ~24MB) và giải nén
curl -L -o /tmp/online_retail.zip "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
unzip /tmp/online_retail.zip -d /tmp/doan19/data/     # được Online Retail.xlsx
# (nếu dùng đường dẫn khác, sửa biến DU_LIEU trong code/02_phan_tich_du_lieu_lon.py)

# 1) minh họa từng bước + kiểm chứng giáo trình
python code/01_minh_hoa_tung_buoc.py

# 2) quy trình đầy đủ trên dữ liệu thật (~4 phút)
python code/02_phan_tich_du_lieu_lon.py
```

## 3. Kết quả chính

- Dữ liệu mẫu 9 giao dịch: L1/L2/L3 **khớp 100%** đáp án chuẩn giáo trình Han & Kamber (min_sup = 2/9).
- Dữ liệu thật: 541.909 dòng → 527.634 sau làm sạch → thị trường Anh (91,7%) → **16.406 giỏ hàng, 2.530 mặt hàng**.
- min_support = 2%: **483 tập phổ biến** (353/123/7 theo k) — Apriori tự viết **≡ FP-Growth (mlxtend)** ở cả 5 mức ngưỡng.
- min_confidence = 35%, min_lift = 1,2: **202 luật** — trùng khớp từng cặp với thư viện mlxtend.
- Hiệu năng tại 2%: Apriori tự cài đặt 1,60s < Apriori mlxtend 2,29s < FP-Growth 2,37s (đếm support bằng chỉ mục ngược tid-list).

## 4. Việc cần làm trước khi nộp

1. Điền **họ tên sinh viên, lớp, GVHD** vào trang bìa Đề cương + Báo cáo + slide 1, và ngày bắt đầu/kết thúc trong bảng kế hoạch tiến độ của Đề cương.
2. Mở file Word → nhấp chuột phải vào **Mục lục** → **Update Field** để cập nhật số trang.
3. Đọc kỹ Chương 2 và 3 để chuẩn bị trả lời câu hỏi bảo vệ (gợi ý câu hỏi nằm trong slide 7–14).
