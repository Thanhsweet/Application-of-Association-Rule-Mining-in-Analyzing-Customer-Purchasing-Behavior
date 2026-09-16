# TỔNG HỢP CÂU HỎI HỘI ĐỒNG & CÂU TRẢ LỜI
## Đồ án chuyên ngành — Đề tài 19: Ứng dụng khai phá luật kết hợp phân tích hành vi mua sắm của khách hàng

> Cách dùng tài liệu này: mỗi câu trả lời được viết theo đúng trình tự nên nói. Số liệu **in đậm** là số liệu bắt buộc phải thuộc — hội đồng rất hay hỏi lại số. Cuối mỗi nhóm có "bẫy thường gặp" nếu có.

---

## 0. BẢNG SỐ LIỆU CẦN THUỘC LÒNG (mở đầu bằng cái này)

| Mục | Số liệu |
|---|---|
| Dữ liệu gốc | **541.909 dòng**, 8 thuộc tính, 12/2010–12/2011, cửa hàng bán lẻ trực tuyến Anh (UCI dataset 352) |
| Sau làm sạch | **527.634 dòng** (giảm 14.275 dòng ≈ 2,6%), **19.773 đơn hàng**, 3.997 mặt hàng |
| Thị trường phân tích | **Anh Quốc — 91,7%** số dòng (483.884 dòng), 17.901 giỏ hàng |
| Sau xây giỏ + lọc | **16.406 giỏ hàng**, **2.530 mặt hàng** (mặt hàng phải xuất hiện ≥ 30 giỏ; giỏ ≥ 2 mặt hàng) |
| Tham số cuối | min_support = **2%**, min_confidence = **35%**, min_lift = **1,2** |
| Kết quả khai phá | **483 tập phổ biến** (k=1: 353, k=2: 123, k=3: 7) → **202 luật** |
| Kiểm chứng | Khớp giáo trình **100%** (bộ mẫu 9 giao dịch); khớp FP-Growth **100%** ở cả 5 mức ngưỡng; khớp mlxtend **100%** bộ luật |
| Hiệu năng tại 2% | Apriori tự viết **1,60s** < Apriori mlxtend **2,29s** < FP-Growth **2,37s** |
| Luật nổi bật | Lift cao nhất **25,06** (bát kẹo Marshmallow hồng ↔ Dolly Mix cam, conf 77,9%); chén Regency: hồng+hoa hồng → xanh có **conf 90,3%, lift 15,89, conviction 9,7** |
| Bộ dữ liệu mẫu | 9 giao dịch, 5 mặt hàng I1–I5, min_sup = 2/9 ≈ 22,2%, min_conf = 2/3 ≈ 66,7%, L3 = {I1,I2,I3}, {I1,I2,I5} |

---

## PHẦN A — KHÁI NIỆM NỀN TẢNG

### A1. Luật kết hợp (association rule) là gì?
Luật kết hợp là mệnh đề có dạng **X → Y** (X, Y là hai tập mặt hàng rời nhau, khác rỗng), đọc là "nếu giỏ hàng chứa X thì có xu hướng chứa thêm Y". Được Agrawal và cộng sự đề xuất năm 1993 trong bài toán phân tích giỏ hàng thị trường (market basket analysis). Ví dụ thật trong đồ án: "chén Regency hồng → chén Regency xanh" với độ tin cậy 82,5%.

### A2. Tập phổ biến (frequent itemset) là gì? Quan hệ với luật?
Cho cơ sở dữ liệu giao dịch D, tập mặt hàng X được gọi là **tập phổ biến** nếu độ hỗ trợ sup(X) ≥ min_support (ngưỡng do người dùng đặt). Bài toán khai phá luật kết hợp có **2 giai đoạn**: (1) tìm toàn bộ tập phổ biến — giai đoạn nặng về tính toán, là nút thắt cổ chai; (2) sinh luật từ tập phổ biến và lọc theo độ tin cậy — chi phí thấp. Vì vậy các thuật toán chính (Brute-force, Apriori, FP-Growth) đều giải quyết giai đoạn 1.

### A3. Nêu công thức và ý nghĩa 5 độ đo.
Gọi T(X) là tập giao dịch chứa X, N là số giao dịch:
1. **Support**: sup(X→Y) = |T(X ∪ Y)| / |T| — luật xuất hiện trong bao nhiêu % số giỏ hàng. Đo "độ phổ biến".
2. **Confidence**: conf(X→Y) = sup(X ∪ Y) / sup(X) — trong các giỏ có X, bao nhiêu % có thêm Y. Đo "độ chắc chắn", chính là xác suất có điều kiện P(Y|X).
3. **Lift**: lift(X→Y) = conf(X→Y) / sup(Y) — mức tương quan. lift > 1: X và Y tương quan dương (X làm xác suất mua Y tăng lên lift lần); lift = 1: độc lập; lift < 1: tương quan âm.
4. **Leverage**: sup(X ∪ Y) − sup(X)·sup(Y) — chênh lệch tuyệt đối so với trường hợp độc lập.
5. **Conviction**: (1 − sup(Y)) / (1 − conf) — "số lần luật bị phủ nhận dự kiến"; conf = 1 thì conviction = ∞. Conviction 9,7 nghĩa là nếu luật sai, tần suất sai phải cao gấp 9,7 lần so với quan sát mới "bình thường".

### A4. Vì sao confidence cao chưa chắc luật có ý nghĩa?
Vì confidence chỉ là xác suất có điều kiện, không so sánh với xác suất "gốc" của Y. Ví dụ cực đoan: nếu Y xuất hiện trong 95% giỏ hàng thì mọi luật A → Y đều có conf ≈ 95% dù A và Y chẳng liên quan gì nhau. **Lift mới phát hiện hiện tượng này**: lift = conf/sup(Y) ≈ 1 nghĩa là độc lập. Trong đồ án có bằng chứng cụ thể: 2 luật I1 → I3 và I3 → I1 trên dữ liệu mẫu có conf = 66,7% (đạt ngưỡng) nhưng lift đúng bằng 1 — hai mặt hàng độc lập, luật vô nghĩa. Đó là lý do đồ án lọc luật bằng **cả ba ngưỡng** support + confidence + lift.

### A5. Lift và leverage khác nhau thế nào, khi nào dùng cái nào?
Cùng đo tương quan nhưng theo hai thang khác nhau: **lift là độ đo tương đối** (tỉ lệ), nhạy với các cặp support thấp — cặp hiếm nhưng rất gắn bó dễ có lift rất cao; **leverage là độ đo tuyệt đối** (hiệu số lượng), phản ánh số giao dịch "thực chất" mà luật giải thích được — một luật leverage nhỏ dù lift khủng chỉ tác động trên rất ít đơn hàng. Thực chiến: dùng lift để **xếp hạng độ gắn kết**, dùng leverage/support để **đánh giá quy mô tác động doanh thu**.

### A6. Phân tích giỏ hàng thị trường (market basket analysis) là gì, giải quyết bài toán gì?
Là ứng dụng kinh điển của khai phá luật kết hợp: từ tập hợp hóa đơn, tìm các nhóm mặt hàng thường được mua cùng nhau dưới dạng luật "nếu – thì", phục vụ: gợi ý sản phẩm, combo khuyến mãi, trưng bày liền kề, quản lý tồn kho theo cụm hàng liên quan. Đơn vị phân tích là **giỏ hàng** (một giao dịch), trong đồ án = một đơn hàng (InvoiceNo).

### A7. Quá trình KDD gồm những bước, khai phá dữ liệu đứng ở đâu?
KDD (Knowledge Discovery in Databases) gồm: dữ liệu → làm sạch → tích hợp → chọn & biến đổi → **khai phá dữ liệu** → đánh giá mẫu tin → tri thức. Khai phá dữ liệu là bước trung tâm sinh ra mẫu tin/quy luật; phần lớn công việc thực tế (chiếm đa số thời gian) lại nằm ở các bước trước nó — điều này đúng với đồ án: làm sạch và xây giỏ hàng chiếm phần lớn thời gian thực hiện.

### A8. Đơn vị "giao dịch" trong đề tài là gì, tại sao?
Giao dịch = **một đơn hàng (InvoiceNo)**, biểu diễn bằng tập các tên sản phẩm (không trùng lặp). Lý do: luật kết hợp cần mô hình hóa hành vi **đồng xuất hiện trong một lần mua**; CustomerID không phù hợp vì một khách hàng mua nhiều lần theo thời gian, gộp theo khách sẽ trộn các mục đích mua khác nhau lại với nhau.

### A9. Phân biệt luật kết hợp với phân lớp/hồi quy?
Phân lớp và hồi quy là **học có giám sát** (có nhãn, dự đoán biến mục tiêu, đánh giá bằng accuracy/RMSE...). Luật kết hợp là **học không giám sát**: không có biến mục tiêu, tìm mọi quy luật đồng xuất hiện X → Y trong dữ liệu. Vì vậy không có "tập kiểm tra chính xác kiểu accuracy"; chất lượng luật được đánh giá bằng các độ đo thống kê (support/confidence/lift) và bằng **kiểm chứng chéo giữa các cài đặt độc lập** — chính là cách đồ án đã làm.

### A10. Ứng dụng thật của luật kết hợp ngoài bán lẻ?
Phân tích giỏ hàng là ứng dụng tiêu biểu, nhưng kỹ thuật dùng được cho bất kỳ bài toán đồng xuất hiện nào: gợi ý khóa học/môn học (sinh viên học môn này thường học tiếp môn kia), phân tích triệu chứng đi kèm trong y tế, phân tích từ đồng xuất hiện trong NLP, gợi ý trang web/nghe nhạc, phân tích nhật ký truy cập. Trong danh sách 30 đề tài của khoa, đề tài 13 (hệ gợi ý sản phẩm) có thể dùng trực tiếp bộ luật của đồ án này làm lõi offline.

---

## PHẦN B — THUẬT TOÁN (trọng tâm rubric 50% + 30%)

### B1. Thuật toán brute-force hoạt động thế nào, độ phức tạp bao nhiêu?
Sinh **toàn bộ** tập con khác rỗng của tập mặt hàng I — tổng cộng 2^m − 1 tập (m là số mặt hàng) — bằng phép tổ hợp theo từng cấp k, sau đó quét toàn bộ giao dịch đếm support từng tập và lọc theo min_support. Độ phức tạp mũ: O(2^m · n). Với bộ mẫu 5 mặt hàng: 31 tập con, thuật toán đã xét 30 ứng viên ở các cấp 1–4. Với 2.530 mặt hàng của dữ liệu thật, chỉ riêng số ứng viên đã là 2^2530 — phi vật chất, nên brute-force chỉ dùng làm **chuẩn so sánh tính đúng đắn** trên dữ liệu nhỏ.

### B2. Tính chất Apriori là gì, vì sao nó giúp cắt tỉa?
**Tính chất Apriori: "mọi tập con của một tập phổ biến đều là tập phổ biến"** (do sup là hàm đơn điệu giảm theo bao hàm tập hợp). Phát biểu ngược: nếu X không phổ biến thì **mọi** tập lớn hơn chứa X đều không phổ biến. Nhờ vậy, khi sinh ứng viên cấp k chỉ cần kiểm tra: một ứng viên có **bất kỳ** tập con (k−1) nào không nằm trong F(k−1) là bị loại **ngay không cần đếm**. Ví dụ trong đồ án: {I3, I5} chỉ xuất hiện 1/9 lần → không phổ biến → 4 ứng viên cấp 3 chứa nó hoặc các tập con không phổ biến khác ({I1,I3,I5}, {I2,I3,I4}, {I2,I3,I5}, {I2,I4,I5}) bị cắt ngay, chỉ còn 2 ứng viên phải quét đếm — giảm 67% công việc đếm ở cấp đó.

### B3. Trình bày 3 bước lặp của Apriori.
Tại mỗi cấp k = 1, 2, ... :
1. **Join (kết nối):** sinh C(k) từ F(k−1) bằng cách ghép các cặp tập (k−1)-mặt hàng **có chung (k−2) phần tử đầu tiên** (sau khi sắp xếp) — cách này sinh ứng viên không trùng lặp.
2. **Prune (cắt tỉa):** loại mọi ứng viên có ít nhất một tập con (k−1) không thuộc F(k−1) (theo tính chất Apriori).
3. **Quét (scan):** duyệt toàn bộ giao dịch, đếm support các ứng viên còn lại, giữ lại F(k).
Lặp đến khi F(k) = ∅. Tổng số lần quét dữ liệu = số cấp k tồn tại.

### B4. Trên bộ mẫu 9 giao dịch, Apriori chạy ra gì?
- **C1/L1:** quét đếm 5 mặt hàng: I1(6), I2(7), I3(6), I4(2), I5(2) — cả 5 phổ biến (min_sup = 2).
- **C2/L2:** join sinh 10 cặp (prune 0 vì mọi tập con cấp 1 đều phổ biến); quét 10, giữ 6 cặp: I1I2(4), I1I3(4), I1I5(2), I2I3(4), I2I4(2), I2I5(2).
- **C3/L3:** join sinh 6 ứng viên, **prune cắt 4**, quét 2, giữ: I1I2I3(2), I1I2I5(2).
- **C4:** join sinh 1 ứng viên (I1I2I3I5) nhưng bị **prune toàn bộ** → dừng.
Kết quả khớp 100% đáp án chuẩn trong giáo trình Han & Kamber.

### B5. FP-Growth hoạt động thế nào? Vì sao nó không phải sinh ứng viên?
FP-Growth (Han, Pei, Yin — SIGMOD 2000) nén dữ liệu vào **cây FP**: (1) quét lần 1 đếm tần suất từng mặt hàng, sắp theo thứ tự giảm dần và loại mặt hàng không phổ biến; (2) quét lần 2, mỗi giao dịch sắp theo thứ tự tần suất rồi chèn vào cây — các giao dịch có tiền tố chung **dùng chung nhánh** (nút lưu mặt hàng + bộ đếm), kèm **header table** nối các nút cùng mặt hàng thành danh sách liên kết. Sau đó khai phá **đệ quy**: với từng mặt hàng ở cuối header table, truy các đường đi tiền tố (conditional pattern base), dựng "cây FP có điều kiện" rồi lặp lại. Không sinh/kiểm tra ứng viên nào — chính cấu trúc cây đã mã hóa sẵn các đồng xuất hiện. Chỉ quét dữ liệu **2 lần** (Apriori quét số lần bằng số cấp).

### B6. So sánh Apriori và FP-Growth: cái nào khi nào thắng?
- **Apriori thắng / đủ tốt** khi: dữ liệu thưa, min_support cao (ít cấp, ít ứng viên), bộ nhớ hạn chế. Đơn giản, dễ truy vết từng bước.
- **FP-Growth thắng** khi: dữ liệu dày đặc, min_support thấp (Apriori sinh rất nhiều ứng viên cấp 2–3 trong khi FP-tree nén tốt), cần tốc độ và số lần quét ít. Nhược: tốn bộ nhớ cho cây trên dữ liệu thưa, cấu trúc phức tạp cài đặt, khó truy vết.
- Trong thực nghiệm của đồ án ở ngưỡng 1,5–6% trên dữ liệu bán lẻ thưa, ba cài đặt cùng một cấp độ tốc độ (giây đơn vị) — đúng như lý thuyết: chênh lệch lớn chỉ xuất hiện khi hạ support sâu hơn nữa hoặc dữ liệu dày đặc hơn.

### B7. Vì sao chọn FP-Growth làm "thuật toán chưa học"?
Ba lý do: (1) cùng giải đúng bài toán khai phá tập phổ biến nên so sánh được trực tiếp với Apriori; (2) là thuật toán kinh điển phải biết trong khai phá dữ liệu, có giá trị học thuật; (3) đề tài cho phép dùng thư viện cho thuật toán quá phức tạp — FP-Growth với cây FP và thủ tục đệ quy là ứng viên phù hợp nhất. Quan trọng hơn, dùng nó như **điểm kiểm chứng chéo độc lập** cho Apriori tự cài đặt: hai cài đặt bằng hai cách hoàn toàn khác nhau mà ra cùng kết quả thì kết quả đáng tin.

### B8. Nhược điểm của Apriori?
(1) Quét dữ liệu nhiều lần (mỗi cấp 1 lần) — tốn I/O trên dữ liệu đĩa; (2) sinh nhiều ứng viên trung gian, đặc biệt cấp 2 là C(m,2) với m = số mặt hàng cấp 1 (2.530 mặt hàng → hơn 3 triệu cặp tiềm năng nếu không lọc tốt); (3) tốn kém khi min_support thấp. Các cải tiến: đếm theo tid-list/hash-tree, phân vùng, lấy mẫu, FP-Growth.

### B9. Vì sao giới hạn tập phổ biến ở độ dài k ≤ 3?
Ba lý do: (1) ở min_support 2% dữ liệu tự nhiên chỉ còn 7 tập 3-mặt hàng và **không có** tập 4-mặt hàng — giới hạn này không bỏ mất gì; (2) số luật sinh từ tập k mặt hàng tăng theo cấp số nhân (2^k − 2 luật/tập) → luật 4+ vế khó diễn giải, khó hành động; (3) về nghiệp vụ, luật "mua A+B thì mua C" đã đủ để thiết kế combo/gợi ý; luật dài hơn chủ yếu mang tính học thuật.

### B10. Nếu hội đồng hỏi "độ phức tạp tổng thể của chương trình"?
- Brute-force: O(2^m · n · k̄) — mũ theo số mặt hàng.
- Apriori: không có giới hạn đa thức chặt vì phụ thuộc số ứng viên thực tế |C(k)|; chi phí mỗi cấp O(n · |C(k)|) theo cài đặt quét, hoặc O(Σ|tidlist|) theo cài đặt giao tập. Thực nghiệm: tăng từ 0,15s (6%) lên 3,04s (1,5%) khi số tập tăng 26 → 943, cho thấy chi phí tỷ lệ với độ rộng kết quả, không phải với m.
- FP-Growth: dựng cây O(n · L̄) (L̄ = số mặt hàng/giỏ) + chi phí khai phá đệ quy tỷ lệ với số mẫu tin.

### B11. Điểm khác biệt giữa cách em sinh ứng viên và cách vét cạn?
Cùng đếm support bằng quét, khác ở **không gian ứng viên**: brute-force sinh toàn bộ C(m,k) tập con cấp k (không nhìn kết quả cấp trước); Apriori sinh ứng viên cấp k **chỉ từ** tập phổ biến cấp k−1 và cắt tỉa theo tính chất Apriori. Trên bộ mẫu: brute-force đếm 30 ứng viên, Apriori chỉ đếm 17 — tổng tiết kiệm 43%, và chênh lệch càng lớn khi dữ liệu lớn.

### B12. Phân biệt Apriori với ECLAT?
ECLAT đổi sang **biểu diễn dọc** (vertical): mỗi mặt hàng lưu danh sách giao dịch (tid-list), support của tập = kích thước phép **giao** các tid-list; khai phá theo chiến lược đi sâu (DFS) thay vì theo cấp (BFS). Lưu ý kỹ thuật: phiên bản Apriori tối ưu cho dữ liệu lớn trong đồ án thực chất **kết hợp khung sinh ứng viên theo cấp của Apriori với cách đếm giao tid-list của ECLAT** — đây chính là lý do nó chạy nhanh hơn cài đặt trên ma trận one-hot của mlxtend.

### B13. Vì sao không dùng thư viện cho cả Apriori mà tự cài?
Vì rubric của đề tài yêu cầu **2 thuật toán trong chương trình phải tự lập trình hoàn chỉnh** (mức 3 = 50% điểm), và mục đích học phần là rèn tư duy cài đặt. Thư viện mlxtend được dùng đúng vai trò đề tài cho phép: thuật toán chưa học (FP-Growth) + đối chiếu kết quả.

### B14. Nếu bỏ tính chất Apriori (prune) thì chuyện gì xảy ra?
Thì Apriori suy giảm về brute-force theo cấp: phải quét đếm mọi ứng viên sinh ra từ join, bao gồm các ứng viên "chết" chắc chắn không phổ biến. Trên bộ mẫu: cấp 3 phải đếm 6 thay vì 2 ứng viên (tăng 3 lần); trên dữ liệu lớn ở support thấp, các ứng viên chết bùng nổ theo cấp số nhân và thời gian chạy sẽ tăng nhiều lần.

---

## PHẦN C — CÀI ĐẶT & KỸ THUẬT LẬP TRÌNH

### C1. Vì sao dùng frozenset cho mỗi giao dịch?
Ba lý do: (1) **frozenset hashable** nên làm khóa dictionary để đếm và lưu trong tập hợp kết quả; (2) phép `issubset` kiểm tra chứa-tập-hợp O(k) — đúng bằng cỗ máy cần cho việc đếm support; (3) tự động **khử trùng lặp** phần tử trong giỏ (mua 2 cái cùng sản phẩm vẫn tính là 1 mặt hàng — đúng mô hình luật kết hợp).

### C2. Bước đếm support được cài đặt thế nào, có phiên bản nào khác?
Hai phiên bản, cùng thuật toán:
- **Bản minh họa** (`do_support_quet`): với mỗi giao dịch, duyệt mọi ứng viên và kiểm tra `issubset` — O(n · |C|), dễ đọc, dùng cho dữ liệu mẫu có truy vết.
- **Bản dữ liệu lớn** (`apriori_nhanh`): xây **chỉ mục ngược** item → tập các tid (số thứ tự giao dịch). Support của tập X = kích thước **phép giao** các tid-list của phần tử trong X. Chỉ "chạm" đúng các giao dịch liên quan, không quét dữ liệu rỗng — đây là lý do chính khiến bản tự viết nhanh hơn mlxtend (mlxtend quét ma trận one-hot dày đặc 16.406 × 2.530).

### C3. Điều kiện join `a[:-1] == b[:-1]` nghĩa là gì?
Đây là kỹ thuật **F(k−1) × F(k−1)** chuẩn của Apriori: sau khi sắp các tập (k−1) theo thứ tự từ điển, hai tập chỉ được ghép nếu **giống nhau (k−2) phần tử đầu**; khi đó hợp của chúng có đúng k phần tử, mỗi tổ hợp chỉ sinh **đúng một lần** — không trùng, không sót. Không có điều kiện này sẽ sinh trùng lặp và ứng viên thừa.

### C4. Sinh luật cài đặt thế nào?
Với mỗi tập phổ biến X (|X| ≥ 2), duyệt mọi tập con khác rỗng A của X (dùng combinations), B = X − A; tra support của X, A, B từ kết quả khai phá rồi tính conf = sup(X)/sup(A), lift = conf/sup(Y), leverage, conviction; giữ luật thoa min_conf và min_lift. Đã kiểm chứng chéo: bộ 202 luật **trùng khớp từng cặp** với `association_rules` của mlxtend.

### C5. TransactionEncoder là gì, tại sao cần ma trận one-hot?
Là công cụ của mlxtend biến danh sách giỏ hàng (mỗi giỏ = tập mặt hàng) thành **ma trận nhị phân** n_giỏ × m_mặt hàng (ô = 1 nếu mặt hàng có trong giỏ). FP-Growth của mlxtend nhận đầu vào là DataFrame one-hot này. Lưu ý: ma trận 16.406 × 2.530 chỉ ~41 triệu ô boolean (~41MB) nên nằm gọn trong bộ nhớ.

### C6. Vì sao bản Apriori tự viết chạy nhanh hơn cả thư viện? (câu hay bị hỏi)
Ba nguyên nhân, theo thứ tự quan trọng: (1) **cách đếm**: giao tid-list chỉ xử lý các giao dịch thực sự chứa mặt hàng (danh sách ngắn, ~26 mặt hàng/giỏ trung bình), trong khi mlxtend quét ma trận one-hot dày đặc; (2) bỏ qua sớm các ứng viên chết nhờ prune trước khi đếm; (3) chi phí khung tổng quát của thư viện (kiểm tra kiểu dữ liệu, tạo DataFrame kết quả...). Đây là bài học rút ra: **cấu trúc dữ liệu cho bước đếm quan trọng không kém thuật toán** — và cũng phải nói công bằng: là so sánh một cài đặt chuyên biệt cho dạng dữ liệu này với một thư viện đa dụng, không phải "thư viện chậm".

### C7. Ngôn ngữ/thư viện dùng gì, vì sao Python?
Python 3.12; pandas (xử lý dữ liệu), matplotlib (trực quan hóa), openpyxl (đọc Excel), mlxtend (FP-Growth + đối chiếu). Chọn Python vì: hệ sinh thái khai phá dữ liệu mạnh nhất, mã dễ đọc dễ minh họa từng bước (phục vụ rubric), và phần "thuật toán chính" (Brute-force, Apriori, sinh luật) **hoàn toàn tự viết**, thư viện chỉ dùng cho FP-Growth và đối chiếu — đúng yêu cầu đề tài.

### C8. Kiểm chứng chéo được thiết kế thế nào?
Ba lớp độc lập: (1) bộ mẫu 9 giao dịch có **đáp án chuẩn trong giáo trình** → so tự động L1/L2/L3; (2) Apriori tự viết so với FP-Growth mlxtend ở **5 mức min_support** (6%, 4%, 3%, 2%, 1,5%) — so số tập và so chính xác tập hợp các tập; (3) bộ luật tự sinh so với `association_rules` của mlxtend theo cặp (vế trước, vế sau). Cả ba lớp đều **khớp 100%**. Ý nghĩa: hai cài đặt độc lập cùng ra kết quả → xác suất cả hai cùng sai cùng một kiểu là rất thấp → kết quả đáng tin.

### C9. Chương trình "truy vết từng bước" nghĩa là gì, phục vụ gì?
Các hàm Apriori/brute-force có tham số `trace`: mỗi bước (C1, L1, C2... kèm danh sách ứng viên bị cắt ở prune) được ghi lại và in ra — đúng yêu cầu "thực hiện thuật toán theo từng bước" của đề tài. Đây là cơ sở của Bảng 2.2, 2.3 trong báo cáo và là nội dung trực tiếp khi giảng viên yêu cầu "chạy tay" một ví dụ.

---

## PHẦN D — DỮ LIỆU & TIỀN XỬ LÝ

### D1. Bộ dữ liệu Online Retail là gì?
Dữ liệu giao dịch **thực** của một cửa hàng bán lẻ trực tuyến đăng ký tại Anh, công khai trên UCI Machine Learning Repository (dataset 352): **541.909 dòng × 8 thuộc tính** từ 01/12/2010 đến 09/12/2011. Thuộc tính: InvoiceNo (mã đơn, đơn hủy có tiền tố C), StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country. Đây là bộ dữ liệu chuẩn thường dùng cho bài toán luật kết hợp vì quy mô lớn và có đủ "nhiễu" thực tế để thực hành làm sạch.

### D2. Quy trình làm sạch gồm những bước nào, vì sao?
1. Bỏ dòng thiếu Description (không định danh được mặt hàng).
2. Bỏ toàn bộ **đơn hủy/trả hàng** — mã đơn có tiền tố "C", Quantity âm: chúng phản ánh hành vi trả lại, không phải hành vi mua.
3. Giữ Quantity > 0 và UnitPrice > 0 (loại dòng dữ liệu lỗi giá 0/âm).
4. Chuẩn hóa Description (in hoa, gọn khoảng trắng) và bỏ các **khoản dịch vụ** không phải sản phẩm: POSTAGE, CARRIAGE, BANK CHARGES, AMAZON FEE, MANUAL, SAMPLES... — nếu giữ, chúng sẽ tạo ra luật giả "mọi đơn → phí vận chuyển" vô nghĩa.
Kết quả: còn 527.634 dòng (giảm 2,6%).

### D3. Vì sao chỉ phân tích Anh Quốc?
Anh chiếm **91,7%** dữ liệu (483.884 dòng); 37 quốc gia còn lại rải mỏng, nhiều quốc gia chỉ vài trăm đơn. Nếu gộp tất cả để tính support chung, các luật "quốc tế" lẫn vào thị trường chính; nếu phân tích riêng từng quốc gia thì phần lớn không đủ dữ liệu cho một ngưỡng support thống nhất có ý nghĩa thống kê. Chọn thị trường lớn nhất là quyết định cân bằng giữa độ phủ và độ tin cậy — và được ghi rõ là hạn chế (mục 3.8) kèm hướng cải tiến.

### D4. Vì sao loại mặt hàng xuất hiện dưới 30 giỏ?
Ba lý do: (1) **thống kê** — luật từ mặt hàng chỉ xuất hiện vài lần không đáng tin (support tối đa < 0,2%); (2) **ý nghĩa hành động** — doanh nghiệp không thể xây combo/gợi ý trên sản phẩm bán rất chậm hoặc mới ra mắt; (3) **khả thi tính toán** — giảm m từ 3.997 xuống 2.530 giúp không gian ứng viên cấp 2 nhỏ lại đáng kể. Ngưỡng 30 giỏ ≈ 0,17% — rất thấp, chỉ cắt phần "nhiễu đuôi".

### D5. Vì sao bỏ giỏ chỉ có 1 mặt hàng?
Luật kết hợp yêu cầu cả vế trước và vế sau khác rỗng — giỏ 1 mặt hàng không thể sinh bất kỳ luật nào, giữ lại chỉ làm tăng N (mẫu số support) một cách vô ích và pha loãng mọi độ đo.

### D6. Đơn hàng hủy chiếm bao nhiêu, việc bỏ chúng có làm mất thông tin không?
Không ghi riêng con số chính xác trong báo cáo (thuộc nhóm 14.275 dòng bị loại cùng các dòng Quantity/UnitPrice ≤ 0 và thiếu mô tả). Bỏ chúng là **chủ đích mô hình hóa**: mục tiêu là hành vi mua, không phải hành vi trả hàng. Nếu muốn khai phá lý do hủy hàng thì đó là một bài toán khác, cần xử lý riêng.

### D7. Khám phá dữ liệu (EDA) cho thấy gì?
- **Top sản phẩm**: WHITE HANGING HEART T-LIGHT HOLDER (2.162 đơn), JUMBO BAG RED RETROSPOT (1.935), REGENCY CAKESTAND 3 TIER (1.685) — đều là đồ trang trí/quà tặng giá nhỏ, mua kèm tự nhiên.
- **Tính mùa vụ**: số đơn tăng mạnh từ tháng 8, đỉnh tháng 11 (gần 2.500 đơn) trước Giáng sinh; tháng 12/2011 thấp bất thường vì dữ liệu chỉ có 9 ngày đầu tháng.
- **Phân bố giỏ**: trung vị 15 mặt hàng/giỏ, trung bình 26,4, đuôi phải dài — tồn tại đơn sỉ hàng trăm mặt hàng (khách buôn).

### D8. Phát hiện nào từ EDA dẫn được vào kết quả khai phá?
Hai điều: (1) tính mùa vụ Giáng sinh giải thích vì sao các luật hàng Noel (sao–tim gỗ Bắc Âu) có lift rất cao — cùng "mục đích mua" trong cùng mùa; (2) sự tồn tại của đơn sỉ cho thấy nên (ở hướng phát triển) tách phân khúc khách buôn/khách lẻ trước khi khai phá để luật "thuần" hơn.

---

## PHẦN E — THAM SỐ, ĐÁNH GIÁ VÀ CÁC CÂU "VÌ SAO CHỌN"

### E1. Vì sao chọn min_support = 2%?
Là lựa chọn có căn cứ thực nghiệm, không tùy tiện: đồ án quét **5 mức** từ 6% xuống 1,5% (26 → 943 tập phổ biến). 2% ≈ 328 giỏ hàng là điểm cân bằng: đủ chặt để mỗi luật có ít nhất vài trăm giao dịch ủng hộ (đáng tin thống kê), đủ lỏng để giữ lại các cụm sản phẩm thú vị (483 tập, trong đó 123 cặp và 7 bộ ba). Hạ sâu hơn (1,5%) cho thêm 460 tập nữa nhưng phần lớn là cặp hiếm khó hành động, và thời gian khai phá tăng.

### E2. Vì sao min_confidence = 35% và min_lift = 1,2?
Confidence 35% là ngưỡng "một phần ba giỏ có X sẽ có Y" — với hành vi mua đa dạng đây đã là tín hiệu mạnh; đặt cao hơn (70–80%) sẽ chỉ còn luật giữa các biến thể cùng dòng sản phẩm, mất các luật giữa các dòng. Lift 1,2 là "rào chắn chống luật vô nghĩa": loại mọi quan hệ yếu hơn 20% so với độc lập (như cặp I1–I3 lift = 1 ở dữ liệu mẫu). Ba ngưỡng cùng tác động: support đảm bảo quy mô, confidence đảm bảo độ chắc chắn, lift đảm bảo tương quan thật.

### E3. Nếu tăng/giảm ngưỡng thì kết quả thay đổi thế nào?
- **Giảm min_support** → số tập tăng gần bậc số nhân (483 → 943 khi 2% → 1,5%), xuất hiện thêm luật hiếm-lift-cao, thời gian chạy tăng, rủi ro luật nhiễu tăng.
- **Tăng min_confidence** → luật ít đi nhưng mỗi luật chắc chắn hơn; các luật "vét" như X → mặt hàng bán chạy sẽ bị loại bớt.
- **Tăng min_lift** → chỉ còn tương quan rất gắt (các biến thể cùng dòng).
Nguyên tắc nói với hội đồng: ngưỡng là **tham số nghiệp vụ** — thay đổi theo mục tiêu ứng dụng (gợi ý cá nhân chấp nhận support thấp hơn; combo đại trà cần support cao).

### E4. Làm sao biết luật tìm được "đúng" mà không có ground truth?
Ba cơ chế: (1) **kiểm chứng tính đúng đắn cài đặt** bằng đáp án chuẩn giáo trình và kiểm chứng chéo hai cài đặt độc lập (đã khớp 100%); (2) các luật có **ý nghĩa kinh doanh tự nhiên** (biến thể cùng dòng sản phẩm mua cùng nhau — hợp lý thị giác và nghiệp vụ); (3) ngưỡng thống kê đảm bảo mỗi luật có ≥ ~328 giao dịch ủng hộ. Phải thẳng thắn: luật kết hợp cho thấy **tương quan**, không chứng minh **nhân quả**.

### E5. Luật có mang tính nhân quả không? (bẫy kinh điển)
**Không.** X → Y nghĩa là chúng đồng xuất hiện nhiều hơn mức ngẫu nhiên, không nói X "gây ra" Y. Ví dụ: luật giữa các món hàng Giáng sinh có lift cao một phần do **yếu tố chung là mùa vụ** (confounder). Vì vậy các đề xuất kinh doanh nên được hiểu là gợi ý thử nghiệm (A/B test combo trước khi nhân rộng), không phải chân lý.

### E6. Có luật dư thừa (redundant) không, xử lý thế nào?
Có, hiện tượng tự nhiên của khai luật: từ một tập phổ biến X sinh ra nhiều luật con — ví dụ "A+B → C" và "A → C" cùng tồn tại; luật con thường "mềm" hơn (confidence thấp hơn hoặc bằng). Trong báo cáo, các luật được xếp hạng theo lift/confidence nên nhóm dư thừa tự nhiên tụm dưới bảng; hướng cải tiến có thể nêu: lọc luật dư thừa theo nguyên tắc "chỉ giữ luật nếu confidence của nó lớn hơn mọi luật cha của nó" (minimal/non-redundant rules).

### E7. So sánh kết quả của em với các nghiên cứu/lời giải trên cùng bộ dữ liệu này?
Bộ Online Retail là bộ chuẩn, nhiều hướng dẫn phân tích dùng cùng quy trình (lọc UK, xây giỏ theo InvoiceNo, mlxtend, support ~2%): kết quả định tính trùng — nhóm Regency teacup, Lunch/Jumbo bag, hàng Giáng sinh chính là các cụm hay xuất hiện. Điểm khác của đồ án: (1) **tự cài đặt và kiểm chứng chéo** thay vì chỉ gọi thư viện; (2) đo hiệu năng 3 thuật toán cùng dữ liệu; (3) diễn giải thành đề xuất nghiệp vụ cụ thể.

### E8. Độ tin cậy thống kê: với 16.406 giỏ thì support 2% đủ tin chưa?
Khoảng tin cậy 95% cho tỉ lệ p ≈ 2% với n = 16.406 có bánwidth ± ~0,2% (xấp xỉ 1,96·√(p(1−p)/n) ≈ 0,0021) — nhỏ hơn nhiều so với khoảng cách giữa các ngưỡng, tức số liệu đủ lớn để các luật tại ngưỡng có ý nghĩa thống kê. Đây cũng là lý do không khai phá luật cho quốc gia chỉ vài trăm đơn.

---

## PHẦN F — KẾT QUẢ & DIỄN GIẢI KINH DOANH

### F1. Kết quả khai phá chính là gì?
Từ 16.406 giỏ × 2.530 mặt hàng, min_sup 2%: **483 tập phổ biến** (353 đơn, 123 cặp, 7 bộ ba); lọc conf ≥ 35% và lift ≥ 1,2 còn **202 luật**, khớp 100% với mlxtend. Không có tập 4-mặt hàng ở ngưỡng này.

### F2. Ba "cụm" luật quan trọng nhất và ý nghĩa?
1. **Biến thể cùng dòng sản phẩm** (lift 16–25): bộ 3 màu chén Regency, cặp sao–tim gỗ Giáng sinh Bắc Âu, 2 họa tiết túi sưởi tay, cặp bát kẹo 2 màu. Nghĩa: khách có tâm lý **"sưu tầm trọn bộ"**. Ứng dụng: gợi ý "hoàn thiện bộ sưu tập" (xem 1 màu → gợi ngay màu còn lại), combo trọn bộ.
2. **Cụm túi JUMBO BAG / LUNCH BAG** (support cao nhất 2–4%, lift 3,6–7,6): các mẫu túi mua cùng nhau. Ứng dụng: trưng bày liền kề, gói mua 2–3 túi khác mẫu.
3. **Hàng mùa Giáng sinh**: luật sao→tim gỗ lift 24,8; doanh số đỉnh tháng 11. Ứng dụng: từ tháng 9–10 gom gian hàng Noel, nhập tồn theo cụm liên quan.

### F3. Vì sao lift cao nhất lại là những cặp support chỉ ~2%? (bẫy hay gặp)
Vì lift là độ đo **tương đối**: các cặp hiếm dễ có tỉ lệ đồng xuất hiện "gấp nhiều lần" ngẫu nhiên mà quy mô nhỏ. Cặp bát kẹo có lift 25,06 nghĩa là mua cùng nhau gấp 25 lần mức độc lập, nhưng chỉ trong ~335 giỏ. Ngược lại cụm túi có support 3–4% (vài trăm đến hơn 600 giỏ) nhưng lift 3,6–7,6 — phổ biến hơn, gắn kết ít hơn. Đó là lý do cần **cả hai thang đo** khi ra quyết định: lift để tìm quan hệ gắt, support/leverage để cân theo quy mô.

### F4. Luật đáng chú ý nhất về mặt thống kê là luật nào?
"Chén Regency hồng + chén Regency hoa hồng → chén Regency xanh": **conf 90,3%, lift 15,89, conviction 9,7, sup 3%** (~492 giỏ). Nghĩa: khách đã có 2/3 bộ ba màu thì 9/10 mua nốt màu thứ ba — tín hiệu cực mạnh cho chiến lược "bán nốt bộ sưu tập" (gợi ý đúng thời điểm, gói trọn bộ giảm nhẹ).

### F5. Nhận xét gì từ biểu đồ support–confidence (Hình 3.6)?
Không có luật nào nằm ở góc "support cao + confidence cao" — đặc trưng ngành quà tặng: không có cặp hàng nào "luôn đi cùng nhau" trong đa số đơn; các quan hệ mạnh tập trung ở vùng support thấp – confidence cao (chính là các biến thể cùng dòng). Điều này chỉ ra chiến lược gợi ý nên nhắm **theo ngữ cảnh sản phẩm đang xem**, không phải "bán kèm cho mọi đơn hàng".

### F6. Heatmap (Hình 3.8) nói lên điều gì?
Trên nhóm luật có support cao nhất (các luật 1–1), ba khối tương quan rõ: nội bộ cụm JUMBO/LUNCH bag (lift 3,3–7,6), nội bộ Regency (12,9) và xuyên giữa JUMBO↔LUNCH. Ý nghĩa vận hành: có thể "gom cụm" khi trưng bày/nhập kho — các mẫu trong cùng khối nên ở gần nhau và bổ sung tồn kho cùng lúc.

### F7. Từ bộ luật này xây hệ gợi ý thế nào? (liên hệ đề tài 13)
Bước offline (đã làm): khai phá luật, lưu bảng X → [(Y, lift×conf), ...]. Bước online: khách xem/thêm sản phẩm A vào giỏ → tra mọi luật có A (hoặc giỏ hiện tại) ở vế trước → chấm điểm vế sau theo lift × confidence → gợi ý top-k, loại trừ mặt hàng đã có trong giỏ. Nhờ luật tính offline, bước online chỉ là **tra bảng** — rất nhẹ, phù hợp ứng dụng web đơn giản.

### F8. Đề xuất nào có thể A/B test đầu tiên?
Combo "trọn bộ 3 màu chén Regency giảm nhẹ" so với nhóm đối chứng mua lẻ từng màu; đo tăng doanh thu/đơn và tỉ lệ khách mua đủ bộ. Lý do chọn: luật nền tảng có conf 90% — cơ hội chuyển hóa cao nhất và đo lường đơn giản.

---

## PHẦN G — PHẢN BIỆN, HẠN CHẾ, HƯỚNG PHÁT TRIỂN (câu "khó")

### G1. Hạn chế lớn nhất của đồ án? (hãy chủ động nhận)
Bốn hạn chế, đã ghi rõ mục 3.8: (1) chỉ phân tích Anh (91,7% dữ liệu) — các thị trường nhỏ không đủ data cho ngưỡng thống nhất; (2) bỏ mặt hàng < 30 giỏ — không có luật cho hàng mới/bán chậm; (3) chưa tách khách sỉ khỏi khách lẻ — đơn sỉ làm "dày" không gian luật theo cách riêng của nó; (4) thời gian chạy phụ thuộc máy. Cách nói: nhận hạn chế trước khi bị hỏi, kèm hướng khắc phục cụ thể (G2, G3).

### G2. Nếu có thêm thời gian, cải tiến gì đầu tiên?
Theo thứ tự ưu tiên: (1) **tự cài FP-Growth** (cây FP + conditional tree) để so sánh đủ ba cài đặt thuần tự viết — đi sâu nhất vào tinh thần học phần; (2) **phân khúc RFM khách hàng rồi khai luật riêng từng phân khúc** (khách buôn và khách lẻ có luật khác nhau); (3) lọc luật dư thừa (non-redundant rules); (4) tích hợp luật vào web gợi ý có A/B test.

### G3. Vì sao không dùng machine learning "xịn hơn" (deep learning, collaborative filtering)?
Luật kết hợp có ba lợi thế đúng bài toán: **giải thích được** (mỗi luật là một câu nghiệp vụ, không phải hộp đen), **bẫy được theo yêu cầu đề tài** (đề tài 19 bắt buộc association rules), và **rẻ khi vận hành** (khai phá offline, tra bảng online). Collaborative filtering/deep learning phù hợp hơn khi có dữ liệu tương tác người–sản phẩm theo thời gian thực và cần cá nhân hóa từng người; ngược lại chúng kém giải thích và cần nhiều dữ liệu hơn. Hai hướng không loại trừ nhau: luật kết hợp là baseline + tầng kinh doanh, mô hình học máy là tầng cá nhân hóa.

### G4. Nếu dữ liệu gấp 100 lần (54 triệu dòng), phương án của em có chạy nổi không?
Thang hiện tại bị chặn ở: ma trận one-hot (phải chuyển sparse), TransactionEncoder, và cài đặt tid-list giữ toàn bộ trong RAM. Phương án mở rộng: (1) dùng **sparse matrix** + PySpark MLlib (FP-Growth phân tán) hoặc cài đặt C++ hiệu năng cao (như của Borgelt); (2) lấy mẫu chiến lược hoặc khai phá theo khối thời gian; (3) hạ bớt mặt hàng hiếm sớm (đã làm). Về nguyên lý, FP-Growth mở rộng tốt hơn Apriori khi scale vì không sinh ứng viên — nhưng ở quy mô 16k giỏ, cài đặt hiện tại đủ và nhanh hơn.

### G5. Nếu min_support để 0,01% thì sao?
Số tập phổ biến bùng nổ (có thể hàng triệu), thời gian tăng theo, và phần lớn luật sẽ là nhiễu thống kê (cặp xuất hiện cùng vài lần). Có thể dùng kỹ thuật "khai phá trên mẫu tin đóng/cực đại" (closed/maximal itemsets) để giảm số kết quả mà không mất thông tin — nêu được cái tên này là điểm cộng.

### G6. Câu hỏi về đạo đức/riêng tư dữ liệu khách hàng?
Dữ liệu giao dịch phục vụ phân tích tổng hợp (aggregate), không định danh cá nhân trong đồ án (CustomerID không dùng để khai luật). Thực tiễn doanh nghiệp cần: ẩn danh hóa/pseudonymization, tuân thủ quy định bảo vệ dữ liệu, và cẩn trọng để gợi ý không trở thành "khủng hoảng quyền riêng tư" (hiện tượng người dùng cảm thấy bị theo dõi quá kỹ).

### G7. Vì sao báo cáo không có "accuracy" như các đồ án học máy khác?
Vì luật kết hợp là **học không giám sát** — không có nhãn đúng để đo accuracy. "Chất lượng" được thay bằng: (1) đúng đắn cài đặt (kiểm chứng ba lớp — khớp 100%); (2) ngưỡng thống kê (mỗi luật ≥ ~328 giao dịch, khoảng tin cậy support ± 0,2%); (3) giá trị nghiệp vụ (các cụm luật hợp lý và hành động được). Nếu muốn đánh giá dự đoán, có thể làm "leave-one-out": giấu một mặt hàng, xem luật có đoán đúng mặt hàng trong giỏ không — đây là hướng mở, chưa làm trong thời gian đồ án.

### G8. Hội đồng bảo: "trong ví dụ mẫu, I4 chỉ mua kèm I2 — vậy khuyến mãi gắn I4 với I2 ư?" (câu kiểm tra hiểu lift)
Cẩn trọng: luật I4 → I2 có conf 100% nhưng support chỉ 2/9 và lift 1,286 (không cao). Conf = 100% chỉ vì I4 **chưa bao giờ** xuất hiện ngoài T2 và T4 (cả hai đều có I2) — mẫu quá nhỏ. Đúng ra phải hỏi ngược "sup(I4) là bao nhiêu" trước khi kết luận. Bài học tổng quát: với support thấp, confidence cao dễ gây ảo giác; phải xem đồng thời cả ba độ đo — chính là lý do quy trình lọc luật của đồ án dùng ba ngưỡng.

---

## MẸO TRẢ LỜI TRƯỚC HỘI ĐỒNG

1. **Cấu trúc 3 tầng cho mọi câu**: (1) câu chốt 1 dòng → (2) công thức/con số → (3) ví dụ cụ thể từ đồ án của mình. Ví dụ câu "lift là gì?": "Lift đo mức tương quan — bằng conf chia sup(Y) — luật bát kẹo của em có lift 25 nghĩa là mua cùng nhau gấp 25 lần mức độc lập."
2. **Thuộc lòng bảng số liệu phần 0** — hội đồng hỏi ngược số rất thường (vì sao 2%? 202 luật là nhiều hay ít?).
3. Nếu bị hỏi vướng, quay về **kiểm chứng chéo**: "kết quả của em được khớp 100% giữa hai cài đặt độc lập" — điểm tựa vững nhất của đồ án.
4. Chuẩn bị **chạy tay bộ mẫu 9 giao dịch**: L1 → L2 (6 cặp) → prune cấp 3 (bị cắt {I1,I3,I5}, {I2,I3,I4}, {I2,I3,I5}, {I2,I4,I5}) → L3. Đây là bài tập hội đồng hay giao tại chỗ.
5. Nhận hạn chế **trước** khi bị chỉ (mục G1) — thái độ khoa học, cộng điểm.
6. Khi trình slide 7 (Apriori từng bước), nói chậm ở **bước prune** — đây là chỗ thể hiện hiểu sâu nhất và là câu hỏi bẫy nhiều nhất.
