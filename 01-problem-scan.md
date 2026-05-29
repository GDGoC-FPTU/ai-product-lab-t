# 01 — Problem Scan & Quick Problem Cards

**Lab:** AI Product Scoping — Vin Smart Future  
**Scope:** Phase 1 & Phase 2  
**Thành viên nhóm:** Nguyễn Đức Khang — MSSV: 2A202600588; Mạc Văn Thanh — MSSV: 2A202600638

> Ghi chú dữ liệu: các con số dưới đây là ước lượng phục vụ scoping lab, chưa phải số liệu nội bộ chính thức của Vingroup. Khi triển khai thật cần kiểm chứng bằng log điều vận, ticket system, dữ liệu app hoặc khảo sát thực địa.

---

## Phase 1 — SCAN: Danh sách bài toán vận hành

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | Xanh SM | Stakeholder Pain | Tài xế báo xe điện còn pin rất thấp trong khi đang trên đường đón/trả khách. Điều phối viên phải tra vị trí, trạm sạc còn chỗ và quyết định có cần xe sạc/cứu hộ di động hay không. |
| 2 | Vinhomes | Lặp lại | Ban quản lý đọc phản ánh cư dân trên app, phân loại thủ công sang kỹ thuật, vệ sinh, an ninh hoặc phí dịch vụ. |
| 3 | VinFast | AI-upgrade | Khách hàng mô tả lỗi xe bằng tiếng Việt tự nhiên; CSKH mất thời gian phân loại nhóm lỗi ban đầu trước khi chuyển cho xưởng dịch vụ. |
| 4 | Vinpearl | Tốn thời gian | Quản lý khách sạn phải đọc review từ Booking, Agoda, Google Maps để phát hiện phàn nàn khẩn cấp như phòng bẩn, check-in chậm hoặc thái độ nhân viên. |
| 5 | Vinmec | Tốn thời gian | Bác sĩ mất 20-30 phút soạn tóm tắt xuất viện từ bệnh án, xét nghiệm và ghi chú điều trị. |
| 6 | VinFast | Lặp lại | Bộ phận tài chính đối chiếu hóa đơn sạc điện từ nhiều nguồn, kiểm tra lệch số tiền, thời gian sạc và mã trạm. |

---

## Chọn top 3 bài toán để Quick-Assess

Tôi chọn 3 bài toán có input ngôn ngữ tự nhiên, workflow rõ và có thể đặt boundary an toàn:

1. **Xanh SM — hỗ trợ xử lý sự cố pin thấp của tài xế**  
   Giá trị vận hành cao vì ảnh hưởng trực tiếp tới tài xế, khách hàng và độ sẵn sàng của xe.

2. **Vinhomes — phân loại phản ánh cư dân**  
   Dữ liệu dạng text, rủi ro vừa phải nếu bắt buộc nhân viên duyệt trước khi gửi phản hồi.

3. **VinFast — phân loại mô tả lỗi xe**  
   Phù hợp để LLM trích xuất triệu chứng, nhưng không được để AI kết luận nguyên nhân kỹ thuật cuối cùng.

---

## Quick Problem Card #1 — Xanh SM Critical Battery Incident Triage

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Điều phối viên Xanh SM mất nhiều thời gian xử lý  │
│ tình huống tài xế báo pin thấp hoặc xe sắp hết pin.         │
│                                                             │
│ Công ty thành viên: [x] Xanh SM                             │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ - Tài xế cần chỉ dẫn nhanh để tránh xe chết máy giữa đường  │
│ - Điều phối viên phải xử lý nhiều case trong giờ cao điểm   │
│ - Khách hàng bị chậm chuyến nếu xe không tiếp tục vận hành  │
│                                                             │
│ Workflow thủ công hiện tại:                                 │
│   1. Tài xế gọi hoặc nhắn app báo pin thấp                  │
│   → 2. Điều phối viên hỏi biển số, vị trí, % pin            │
│   → 3. Tra bản đồ và dashboard trạm sạc còn trụ trống       │
│   → 4. Soạn hướng dẫn gửi tài xế hoặc gọi xe sạc di động    │
│   → 5. Theo dõi trạng thái đến khi case đóng                │
│                                                             │
│ Bước tốn thời gian/lỗi nhất:                                │
│ - Bước 3-4: tra cứu trạm phù hợp và viết hướng dẫn          │
│ - Ước tính: 10-12 phút/case phức tạp                        │
│                                                             │
│ AI có thể hỗ trợ ở bước nào?                                │
│ - Bước 3-4: nhận dữ liệu vị trí/pin, kiểm tra rule an toàn, │
│   gợi ý action và draft tin nhắn cho điều phối viên duyệt.  │
│                                                             │
│ Metric thành công:                                          │
│ - Giảm thời gian triage từ 15 phút xuống dưới 3 phút.       │
│ - 98% case pin <5% không bị đề xuất trạm sạc xa hơn 5km.    │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule + LLM  [ ] Agent    │
└─────────────────────────────────────────────────────────────┘
```

**Nhận xét nhanh:** Đây là bài toán nên dùng Rule + LLM Feature. Rule quyết định boundary an toàn như pin dưới 5% thì không đề xuất trạm xa. LLM chỉ soạn nháp và giải thích dễ hiểu cho điều phối viên.

---

## Quick Problem Card #2 — Vinhomes Resident Issue Triage

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Ban quản lý Vinhomes mất thời gian đọc và phân    │
│ loại phản ánh cư dân để chuyển đúng bộ phận xử lý.          │
│                                                             │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ - Nhân viên ban quản lý tòa nhà                              │
│ - Cư dân chờ phản hồi                                       │
│ - Bộ phận kỹ thuật/vệ sinh/an ninh nhận ticket sai          │
│                                                             │
│ Workflow thủ công hiện tại:                                 │
│   1. Cư dân gửi phản ánh trên app hoặc hotline              │
│   → 2. Nhân viên đọc nội dung phản ánh                      │
│   → 3. Tự phân loại: kỹ thuật / vệ sinh / an ninh / phí     │
│   → 4. Chuyển ticket cho bộ phận phụ trách                  │
│   → 5. Theo dõi và phản hồi lại cư dân                      │
│                                                             │
│ Bước tốn thời gian/lỗi nhất:                                │
│ - Bước 2-3: đọc nội dung và phân loại thủ công              │
│ - Ước tính: 4-6 phút/ticket                                 │
│                                                             │
│ AI có thể hỗ trợ ở bước nào?                                │
│ - Bước 2-3: gợi ý category, priority, bộ phận xử lý và      │
│   draft phản hồi ban đầu.                                   │
│                                                             │
│ Metric thành công:                                          │
│ - Giảm thời gian phân loại từ 5 phút xuống dưới 30 giây.    │
│ - Ít nhất 90% ticket được route đúng sau human review.      │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

**Nhận xét nhanh:** Phù hợp với LLM Feature, nhưng phản hồi cuối vẫn phải do nhân viên duyệt. Các case phí, tranh chấp pháp lý hoặc an toàn phải escalated.

---

## Quick Problem Card #3 — VinFast Vietnamese Fault Description Triage

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: CSKH VinFast khó phân loại nhanh mô tả lỗi xe     │
│ bằng tiếng Việt tự nhiên từ khách hàng.                     │
│                                                             │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ - Nhân viên CSKH tiếp nhận case                              │
│ - Kỹ thuật viên nhận ticket chưa đủ thông tin               │
│ - Khách hàng phải mô tả lại lỗi nhiều lần                   │
│                                                             │
│ Workflow thủ công hiện tại:                                 │
│   1. Khách hàng mô tả lỗi qua hotline/app                   │
│   → 2. CSKH đọc nội dung và hỏi thêm triệu chứng            │
│   → 3. CSKH tự đoán nhóm lỗi ban đầu                        │
│   → 4. Tạo ticket cho xưởng dịch vụ hoặc đội kỹ thuật       │
│   → 5. Kỹ thuật viên kiểm tra lại và phân loại chính xác    │
│                                                             │
│ Bước tốn thời gian/lỗi nhất:                                │
│ - Bước 2-3: diễn giải mô tả tiếng Việt thành nhóm lỗi       │
│ - Ước tính: 7-10 phút/case                                  │
│                                                             │
│ AI có thể hỗ trợ ở bước nào?                                │
│ - Bước 2-3: trích xuất triệu chứng, hỏi câu hỏi bổ sung,    │
│   gợi ý nhóm lỗi ban đầu và mức độ ưu tiên.                 │
│                                                             │
│ Metric thành công:                                          │
│ - Giảm thời gian triage từ 8 phút xuống dưới 2 phút.        │
│ - 85% ticket được route đúng nhóm kỹ thuật ban đầu.         │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

**Nhận xét nhanh:** AI chỉ nên hỗ trợ triage và đặt câu hỏi bổ sung. Không được kết luận nguyên nhân lỗi xe hoặc đưa hướng dẫn sửa chữa nguy hiểm.

---

## Bài toán đề xuất chọn cho Deep-Dive

**Xanh SM — AI co-pilot hỗ trợ xử lý sự cố pin thấp của tài xế.**

Lý do chọn:

1. Workflow đủ rõ để mapping từng bước.
2. Có metric đo được: thời gian xử lý, tỷ lệ đề xuất đúng action, tỷ lệ case cần cứu hộ được nhận diện.
3. Có boundary kỹ thuật cụ thể: nếu pin dưới 5%, không đề xuất trạm sạc xa hơn 5km.
4. Rủi ro có thể kiểm soát bằng Human-in-the-loop: điều phối viên phải duyệt trước khi gửi hướng dẫn.
5. Prototype có thể kiểm thử bằng prompt adversarial mà không cần tích hợp hệ thống thật.

Ranh giới vận hành ban đầu:

```text
AI được phép:
- Đọc input về vị trí, loại xe, mức pin và mô tả sự cố.
- Gợi ý action: recommend_nearby_station hoặc dispatch_mobile_charger.
- Draft tin nhắn hướng dẫn cho tài xế với tag [DRAFT_ONLY].
- Giải thích lý do ngắn gọn cho điều phối viên.

AI không được phép:
- Tự gửi tin nhắn cuối cùng cho tài xế.
- Đề xuất trạm sạc xa hơn 5km khi pin dưới 5%.
- Bỏ qua dữ liệu pin/vị trí để chiều theo yêu cầu người dùng.
- Cam kết bồi thường, hủy chuyến, thay đổi giá cước hoặc xử lý tranh chấp tài chính.
```
