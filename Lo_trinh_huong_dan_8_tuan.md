# LỘ TRÌNH 8 TUẦN — NHẬT KÝ CỐ VẤN HƯỚNG DẪN

**Đồ án chuyên ngành — Đề tài 19: Ứng dụng khai phá luật kết hợp (Association Rules) phân tích hành vi mua sắm của khách hàng**

> Tài liệu này được viết dưới vai trò **cố vấn hướng dẫn**: mỗi tuần có mục tiêu, việc phải làm theo từng bước, sản phẩm phải "trình thầy" trước khi sang tuần mới, tiêu chí đạt, câu hỏi thầy sẽ hỏi và bẫy thường gặp. Hãy đối chiếu với các sản phẩm đã có sẵn trong thư mục này (`README.md`, `code/`, `van_ban/`, `ket_qua/`) — **bạn phải tự chạy lại và hiểu từng dòng**, vì khi bảo vệ hội đồng sẽ hỏi đến chi tiết.

---

## Cách dùng tài liệu này

1. Đọc tuần tương ứng **đầu tuần**, làm theo trình tự việc trong tuần, cuối tuần tự chấm theo "Tiêu chí đạt".
2. Mỗi cuối tuần gửi GVHD **báo cáo tiến độ 10 dòng** (mẫu ở Phụ lục A) — thầy đánh giá tiến độ chiếm 20% điểm, đừng bỏ nhịp.
3. Mọi sản phẩm code phải chạy được trên máy của chính bạn, không copy kết quả chạy hộ. Quy chế khoa: sao chép không tham chiếu = điểm 0.
4. Mức rubric của đề tài: **Mức 1** chạy từng bước → **Mức 2** áp dụng dữ liệu riêng → **Mức 3** lập trình hoàn chỉnh. Lộ trình dưới đây thiết kế để bạn chạm Mức 3 ở cả 3 tiêu chí.

---

## TUẦN 1 — Hiểu bài toán, chốt đề cương

**Mục tiêu:** nắm đúng bài toán khai phá luật kết hợp; nộp đề cương được GVHD chấp nhận (đề cương = 20% điểm, hạn nộp chậm nhất 2 tuần sau khi nhận đồ án).

**Việc cần làm (khuyến nghị theo ngày):**

| Ngày | Việc |
|---|---|
| 1–2 | Đọc đề tài 19 trong danh sách 30 đề tài + rubric. Gạch chân 3 từ khóa: "2 thuật toán đã học", "1 thuật toán chưa học", "phân tích – trực quan hóa – đánh giá". Chọn: đã học = **Brute-force + Apriori**; chưa học = **FP-Growth**. |
| 3 | Đọc Chương 6 (Frequent Pattern Analysis) giáo trình Han, Kamber, Pei — *Data Mining: Concepts and Techniques* (3rd ed.), đặc biệt ví dụ AllElectronics 9 giao dịch. Đọc bài gốc Agrawal 1993 (chỉ cần mục 1–3). |
| 4 | Viết **đề cương** theo mẫu khoa (5 mục: Đặt vấn đề / Cơ sở lý luận / Nội dung & phương pháp / Dự kiến kết quả / Kế hoạch tiến độ). Đối chiếu với `van_ban/De_cuong_do_an.docx` đã có — tự viết lại bằng ngôn ngữ của mình, chép nguyên văn không được phép. |
| 5 | Chuẩn bị môi trường: Python 3.12, cài pandas / matplotlib / openpyxl / mlxtend (xem `README.md` mục 2). Tải thành công bộ dữ liệu Online Retail từ UCI để chắc chắn không vướng giữa chừng. |
| 6–7 | Gửi đề cương + gặp GVHD lần 1: xin nhận xét, chốt phạm vi (dùng Anh Quốc làm thị trường phân tích chính) và timeline. |

**Sản phẩm trình thầy:** file đề cương (mềm + in), ảnh chụp môi trường chạy được `import pandas, mlxtend`.

**Tiêu chí đạt:** GVHD đồng ý đề cương; máy chạy được `python -c "import pandas, mlxtend"`; bạn trả lời được "luật kết hợp là gì" bằng 2 câu ngắn.

**Câu hỏi thầy sẽ hỏi:** "Vì sao chọn Apriori làm thuật toán trọng tâm?" — gợi ý: kinh điển, dễ cài đúng, có tính chất prune mạnh, là chuẩn so sánh với FP-Growth.

**Bẫy thường gặp:** viết đề cương quá mơ hồ ("nghiên cứu về khai phá dữ liệu") — thầy sẽ trả lại. Đề cương phải có **đầu vào – đầu ra cụ thể** và **bộ dữ liệu nêu tên**.

---

## TUẦN 2–3 — Cài đặt Brute-force + Apriori, minh họa từng bước, kiểm chứng giáo trình

**Mục tiêu:** chạm Mức 3 (lập trình hoàn chỉnh) cho 2 thuật toán đã học — đây là 50% rubric, đừng làm qua loa.

**Việc cần làm:**

1. **Cài đặt brute-force** (mở rộng tập con bằng `itertools.combinations`, quét đếm support, lọc ngưỡng). Tự viết, không dùng thư viện khai phá.
2. **Cài đặt Apriori** đủ 3 bước: **join** (sinh C_k từ F_{k−1} có chung k−2 phần tử đầu) → **prune** (loại ứng viên có tập con không phổ biến) → **quét** đếm. In được **trace từng bước** C_k / L_k — Mức 1 của rubric nằm ở đây.
3. Chạy trên **bộ mẫu 9 giao dịch của giáo trình** (I1–I5, min_sup = 2/9 ≈ 22,2%) — đối chiếu kết quả code với đáp án chuẩn: L1 5 tập, L2 6 cặp, L3 = {I1,I2,I3}, {I1,I2,I5}.
4. Tự viết **bộ sinh luật** (confidence, lift, leverage, conviction) — không dùng `mlxtend.association_rules` ở bước này, dùng nó chỉ để **kiểm tra chéo** kết quả mình.
5. Viết phần "2.2–2.4" của báo cáo song song với code (đừng để dồn tuần 8).

**Đối chiếu sản phẩm mẫu:** `code/thuat_toan.py` (hàm `brute_force`, `apriori`, `tao_luat_ket_hop`), `code/01_minh_hoa_tung_buoc.py`, kết quả chuẩn trong `ket_qua/minh_hoa_tung_buoc.txt` (mục 4: "KHOP HOAN TOAN voi giao trinh").

**Tiêu chí đạt:** chạy `01_minh_hoa_tung_buoc.py` thấy dòng kiểm chứng "KHOP 100%"; giải thích được vì sao C3 chỉ còn 2 ứng viên sau khi prune loại 4 (gợi ý: {I3,I5} chỉ xuất hiện 1/9); vẽ tay được cây sinh ứng viên C2 → C3.

**Câu hỏi thầy sẽ hỏi:** "Tính chất Apriori là gì, prune dựa vào đó thế nào?" — "Mọi tập con của tập phổ biến đều phổ biến; ngược lại nếu X không phổ biến thì mọi tập chứa X cũng không, nên cắt trước khi đếm."

**Bẫy thường gặp:** (1) sinh ứng viên mà quên điều kiện "chung k−2 phần tử đầu" → sinh trùng; (2) đếm support quên chuẩn hóa theo n; (3) dùng tập thường (set) làm khóa dict — phải dùng `frozenset`.

---

## TUẦN 4 — FP-Growth (kỹ thuật chưa học) + thiết kế kiểm chứng chéo

**Mục tiêu:** hiểu nguyên lý cây FP đủ sâu để bảo vệ (30% rubric), dùng thư viện hợp lý đúng tinh thần đề tài.

**Việc cần làm:**

1. Đọc bài gốc Han, Pei, Yin (SIGMOD 2000) *chỉ phần ý tưởng*: cây FP nén dữ liệu thế nào, header table, conditional FP-tree, vì sao chỉ cần 2 lần quét.
2. Vẽ tay cây FP cho bộ mẫu 9 giao dịch (đặt min_sup = 2) — thầy hay yêu cầu vẽ cây FP khi hỏi phần chưa học.
3. Gọi `mlxtend.frequent_patterns.fpgrowth` (xem cách dùng trong `code/02_phan_tich_du_lieu_lon.py` mục 4) và chạy thử trên bộ mẫu 9 giao dịch.
4. **Thiết kế kiểm chứng chéo**: so số tập phổ biến của Apriori tự viết với FP-Growth ở nhiều ngưỡng support — đây là "tín hiệu an toàn" xuyên suốt đồ án.
5. Đọc bảng so sánh lý thuyết (Bảng 2.5 báo cáo): số lần quét dữ liệu, ưu nhược từng thuật toán — chuẩn bị cho câu hỏi bảo vệ.

**Tiêu chí đạt:** FP-Growth trả về đúng 483 tập khi min_sup = 2% trên dữ liệu thật (khớp Apriori tự viết — xem Bảng 3.2 báo cáo); bạn vẽ được cây FP mẫu trên giấy trong < 10 phút.

**Câu hỏi thầy sẽ hỏi:** "Vì sao FP-Growth nhanh hơn Apriori?" — gợi ý: không sinh ứng viên, dữ liệu nén vào cây, chỉ quét 2 lần; Apriori phải quét bằng số cấp k và sinh nhiều ứng viên trung gian.

**Bẫy thường gặp:** nói "dùng thư viện nên không cần hiểu" — hội đồng sẽ hỏi cây FP ngay. Nếu chỉ trả lời được API mà không hiểu cấu trúc, mục 30% bị trừ nặng.

---

## TUẦN 5–6 — Dữ liệu Online Retail: làm sạch, khám phá, xây giỏ hàng

**Mục tiêu:** biến 541.909 dòng thô thành ma trận one-hot sạch — chất lượng luật cuối cùng quyết định ở đây.

**Việc cần làm (tuần 5):**

1. Tải + nạp `Online Retail.xlsx` (UCI dataset 352) bằng `pd.read_excel`; ghi lại **số dòng từng bước làm sạch** để vào bảng 3.x của báo cáo.
2. Làm sạch theo trình tự (xem mục 3.2 báo cáo): bỏ dòng thiếu Description → bỏ đơn hủy (InvoiceNo bắt đầu 'C', Quantity âm) → giữ Quantity > 0 và UnitPrice > 0 → chuẩn hóa tên sản phẩm → bỏ khoản dịch vụ (postage, bank charges…). Kết quả chuẩn: còn 527.634 dòng.
3. Chọn thị trường Anh (91,7% dữ liệu) — viết được lý do: đủ dữ liệu thống kê cho ngưỡng support thống nhất.

**Việc cần làm (tuần 6):**

4. EDA: top 10 sản phẩm theo số đơn (Hình 3.1), số đơn theo tháng — ghi nhận **đỉnh tháng 11 gần 2.500 đơn** (mùa Giáng sinh), phân bố số mặt hàng/giỏ (trung vị 15).
5. Xây giỏ hàng theo InvoiceNo; lọc mặt hàng xuất hiện ≥ 30 giỏ; bỏ giỏ < 2 mặt hàng → **16.406 giỏ, 2.530 mặt hàng**.
6. Mã hóa one-hot bằng `TransactionEncoder`. Ghi chú: 16.406 × 2.530 ô — vừa đủ bộ nhớ, đừng thêm bớt tùy tiện.

**Đối chiếu:** `code/02_phan_tich_du_lieu_lon.py` mục (1)–(3); hình `hinh_anh/fig01…fig03`; số chuẩn trong `ket_qua/tong_ket.json`.

**Tiêu chí đạt:** chạy lại pipeline ra đúng các con số chuẩn ở trên; trả lời được "vì sao bỏ mặt hàng hiếm (< 30 giỏ)?" (luật từ mặt hàng hiếm thiếu ý nghĩa thống kê và giá trị hành động).

**Bẫy thường gặp:** (1) quên bỏ đơn hủy → luật toàn rác kiểu "POST → POST"; (2) giữ cả giỏ 1 mặt hàng → không sinh được luật nhưng làm chậm; (3) xóa trùng bằng `drop_duplicates` sai cột làm biến dạng giỏ hàng.

---

## TUẦN 7 — Khai phá, so sánh hiệu năng, trực quan hóa, ý nghĩa kinh doanh

**Mục tiêu:** chạm Mức 3 tiêu chí 3 của rubric ("phân tích sâu, có ý nghĩa thực tiễn") — 20% điểm.

**Việc cần làm:**

1. Chạy 3 thuật toán ở 5 ngưỡng support (6% → 1,5%), lập bảng thời gian (Bảng 3.2) + vẽ Hình 3.4. Chọn **min_support = 2%** làm ngưỡng chính, nêu lý do (≈ 328 giỏ — đủ ý nghĩa thống kê, còn lại các cụm sản phẩm thú vị).
2. Sinh luật với conf ≥ 35%, lift ≥ 1,2 → **202 luật**; kiểm chứng chéo bộ luật với mlxtend (phải khớp 100%).
3. Trực quan hóa 4 góc nhìn: scatter support–confidence (Hình 3.6), top lift (3.7), heatmap các luật support cao (3.8), số tập theo k (3.5).
4. **Diễn giải kinh doanh — phần làm nên điểm cộng:** gom luật thành 3 nhóm (biến thể cùng dòng sản phẩm — bộ 3 màu chén Regency, cặp sao–tim gỗ; cụm túi Jumbo/Lunch; hàng mùa Noel) → 3 nhóm đề xuất: gợi ý "hoàn thiện bộ sưu tập", combo/trưng bày liên quan, vận hành theo mùa. Xem Bảng 3.4 + slide 15.
5. Viết xong Chương 3 nháp; gửi GVHD xem lần 2 (cuối tuần 7).

**Tiêu chí đạt:** bạn chỉ ra được 3 cụm luật trên heatmap mà không nhìn file; giải thích "confidence cao nhưng lift = 1 thì luật vô nghĩa" bằng ví dụ I1→I3 trong dữ liệu mẫu.

**Bẫy thường gặp:** (1) bày 202 luật không nhóm → hội đồng thấy "máy móc"; (2) quên ngưỡng lift → luật vô nghĩa lọt vào top; (3) so sánh thời gian chạy không cùng máy/cùng dữ liệu → kết luận vô căn cứ.

---

## TUẦN 8 — Hoàn thiện báo cáo + slides, nộp, chuẩn bị bảo vệ

**Việc cần làm:**

1. Ghép toàn bộ thành **báo cáo theo mẫu khoa** (bìa → mục lục → mở đầu → 3 chương → kết luận → TLLTK → phụ lục code); format Times New Roman 13, lề 3-2-3-2 cm. Đối chiếu `van_ban/Bao_cao_do_an.docx`. Điền tên/lớp/GVHD, cập nhật mục lục (Update Field).
2. Làm **16 slide bảo vệ** (đối chiếu `van_ban/Slides_bao_ve.pptx`) — nguyên tắc: mỗi slide 1 thông điệp, số liệu phải khớp báo cáo, không nhồi chữ.
3. Tự chạy lại toàn bộ pipeline từ đầu trên máy sạch, chụp lại kết quả — đảm bảo tính tái lập.
4. **Diễn tập bảo vệ** (danh sách câu hỏi dự kiến):

| Câu hỏi | Gợi ý trả lời |
|---|---|
| Support/confidence/lift khác nhau thế nào? | 1.1 báo cáo + ví dụ luật Regency conf 90% nhưng phải kèm lift 15,9 mới có nghĩa |
| Vì sao min_support chọn 2%? | ≈ 328/16.406 giỏ; thử 5 ngưỡng, 2% là điểm cân bằng (483 tập, đủ cụm thú vị) |
| Brute-force và Apriori chênh nhau thế nào trên dữ liệu mẫu? | 30 ứng viên so với 17 (Bảng 2.2 vs 2.3); trên dữ liệu lớn là chênh bậc mũ |
| FP-Growth cài đặt thế nào? | Nguyên lý cây FP + 2 lần quét; dùng thư viện vì cấu trúc phức tạp — đúng điều kiện đề tài cho phép |
| Kết quả tin được không? | Kiểm chứng 3 lớp: giáo trình 100% — FP-Growth 100% ở 5 ngưỡng — bộ luật 100% với mlxtend |
| Ứng dụng ra sao? | Bảng 3.4: gợi ý hoàn thiện bộ sưu tập, combo cụm túi, vận hành mùa vụ; nền tảng hệ gợi ý |
| Hạn chế? | Mục 3.8: chỉ thị trường Anh, bỏ mặt hàng hiếm, chưa tách đơn sỉ, luật ≤ 3 vế |

5. In 2 bản báo cáo (GVHD + hội đồng), xin **chữ ký đồng ý bảo vệ** của GVHD — nhớ trước hạn quy định.

---

## Phụ lục A — Mẫu báo cáo tiến độ tuần gửi GVHD (10 dòng)

```
Tuần N — Họ tên, lớp
1. Việc đã làm trong tuần: …
2. Kết quả định lượng đạt được: … (ví dụ: 483 tập phổ biến, khớp 100% với FP-Growth)
3. Vướng mắc cần thầy tư vấn: … (càng cụ thể càng tốt)
4. Kế hoạch tuần tới: …
5. File/bằng chứng đính kèm: … (code, hình, bảng)
```

## Phụ lục B — Checklist tổng trước khi nộp

- [ ] Đề cương đã được GVHD ký chấp nhận (đúng hạn 2 tuần)
- [ ] Báo cáo: bìa đúng mẫu, mục lục đã Update Field, số trang đúng, hình/bảng được tham chiếu trong văn bản
- [ ] Tên SV / lớp / GVHD / năm đã điền ở cả 3 tài liệu (đề cương, báo cáo, slide 1)
- [ ] Code chạy được từ đầu đến cuối trên máy khác (theo README mục 2)
- [ ] Mọi trích dẫn đều có trong TLLTK; không copy không tham chiếu (quy chế: điểm 0)
- [ ] 2 bản in báo cáo + 1 file mềm đồ án (code + báo cáo + dữ liệu mẫu)
- [ ] Đã diễn tập bảo vệ ≥ 1 lần, thời lượng 10–12 phút + trả lời câu hỏi

---

*Tài liệu cố vấn này đi kèm bộ sản phẩm đồ án; xem `README.md` để chạy lại toàn bộ kết quả.*
