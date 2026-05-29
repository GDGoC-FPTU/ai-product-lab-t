# 02 — Deep-Dive Report

**Lab:** AI Product Scoping — Vin Smart Future  
**Tên nhóm:** T-C-Cow-B-ng  
**Thành viên đã ghi nhận:** Kez — MSSV: 2A202600588  
**Bài toán chọn:** Xanh SM — AI co-pilot hỗ trợ xử lý sự cố pin thấp của tài xế

> Ghi chú dữ liệu: báo cáo dùng dữ liệu giả lập và ước lượng để hoàn thành lab scoping. Đây không phải dữ liệu vận hành nội bộ của Xanh SM/Vingroup. Nếu làm thật, nhóm cần thay bằng log điều vận, dữ liệu pin xe, dữ liệu trạm sạc và thời gian xử lý ticket thực tế.

---

## 1. Quyết định lựa chọn

Nhóm chọn bài toán **xử lý sự cố pin thấp của tài xế Xanh SM** để deep-dive.

Lý do chọn:

- Quy trình hiện tại có bottleneck rõ: điều phối viên phải tra cứu vị trí xe, mức pin, trạm sạc còn chỗ và soạn hướng dẫn thủ công.
- Bài toán có boundary kỹ thuật kiểm thử được: pin dưới 5% thì không được đề xuất trạm sạc xa hơn 5km.
- AI không cần tự trị hoàn toàn. LLM chỉ làm co-pilot: đọc tình huống, gợi ý action, soạn tin nhắn nháp.
- Rủi ro có thể kiểm soát bằng điều phối viên duyệt trước khi gửi hướng dẫn cho tài xế.

---

## 2. Current-State Workflow Mapping

Quy trình hiện tại trước khi có AI:

```text
┌────────────────────┐
│ 1. Tài xế báo sự cố│
│ Kênh: app/hotline  │
│ Input: vị trí, pin │
│ ⏱ 2 phút           │
└─────────┬──────────┘
          │ 🔄 Handoff: tài xế → điều phối viên
          ▼
┌────────────────────────────┐
│ 2. Điều phối viên hỏi thêm │
│ Biển số, loại xe, % pin,   │
│ khách đang ở trên xe không │
│ ⏱ 3 phút                   │
└─────────┬──────────────────┘
          │ 🔄 Handoff: điều phối viên ↔ tài xế
          ▼
┌────────────────────────────┐
│ 3. Tra dashboard trạm sạc  │
│ Tìm trạm gần, còn trụ trống│
│ đúng loại cổng sạc         │
│ ⏱ 5 phút 🔴 Bottleneck     │
└─────────┬──────────────────┘
          │ 🔄 Handoff: điều phối viên → hệ thống bản đồ/trạm sạc
          ▼
┌────────────────────────────┐
│ 4. Quyết định hướng xử lý  │
│ Chọn trạm sạc gần hoặc gọi │
│ xe sạc/cứu hộ di động      │
│ ⏱ 3 phút 🔴 Bottleneck     │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ 5. Soạn và gửi hướng dẫn   │
│ Tin nhắn cho tài xế, ghi   │
│ log case để theo dõi       │
│ ⏱ 2 phút                   │
└────────────────────────────┘

Tổng thời gian xử lý thủ công: khoảng 15 phút/case.
```

Điểm nghẽn chính nằm ở **bước 3-4**. Điều phối viên vừa phải đọc tình huống, vừa phải tra hệ thống, vừa phải nhớ quy trình an toàn. Trong giờ cao điểm, một quyết định chậm 5-10 phút có thể làm tài xế mất chuyến hoặc xe cạn pin trước khi tới trạm.

---

## 3. Problem Statement 6-field

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Điều phối viên Xanh SM phụ trách hỗ trợ tài xế khi xe điện pin thấp, trạm sạc quá xa hoặc có rủi ro không tới được trạm. |
| **2. Current Workflow** | Tài xế báo sự cố qua app/hotline. Điều phối viên hỏi thêm thông tin, tra bản đồ, tra dashboard trạm sạc, chọn hướng xử lý, rồi soạn hướng dẫn gửi lại tài xế. Quy trình mất khoảng 15 phút/case. |
| **3. Bottleneck** | Bước tra trạm sạc và quyết định action an toàn. Đặc biệt với pin dưới 5%, nếu đề xuất trạm xa hơn 5km thì xe có thể cạn pin giữa đường. |
| **4. Business Impact** | Với giả định 50-80 case pin thấp/ngày ở một khu vực lớn, mỗi case mất 15 phút tạo ra khoảng 12,5-20 giờ điều phối/ngày. Xử lý chậm làm giảm thời gian xe sẵn sàng nhận chuyến và tăng áp lực cho tài xế. |
| **5. Success Metric** | Giảm thời gian triage từ 15 phút xuống dưới 3 phút/case. 98% case pin dưới 5% được gắn action `dispatch_mobile_charger` hoặc escalate, không đề xuất trạm xa hơn 5km. 100% tin nhắn AI tạo ra phải có tag `[DRAFT_ONLY]`. |
| **6. Operational Boundary** | AI được gợi ý action, draft tin nhắn và giải thích lý do. AI không được tự gửi tin nhắn, không được bỏ tag `[DRAFT_ONLY]`, không được đề xuất trạm xa hơn 5km khi pin dưới 5%, không được quyết định bồi thường/hủy chuyến/thay đổi giá cước. |

---

## 4. Future-State Flow & AI Fit

**AI Fit:** Rule + LLM Feature.

- **Rule layer:** kiểm tra điều kiện an toàn có tính quyết định, ví dụ pin `<5%` và khoảng cách trạm `>5km` thì bắt buộc `dispatch_mobile_charger`.
- **LLM Feature:** đọc mô tả tự nhiên, tóm tắt tình huống, draft tin nhắn dễ hiểu cho tài xế.
- **Không chọn Agentic Loop:** vì hệ thống không nên tự hành động nhiều bước như gửi tin, điều xe cứu hộ hoặc đổi trạng thái chuyến nếu chưa có điều phối viên duyệt.

Future-state flow:

```text
1. Tài xế gửi sự cố qua app/hotline
   Input: vị trí, loại xe, % pin, mô tả tình huống
        │
        ▼
2. 🔵 AI Step: Chuẩn hóa input
   - Trích xuất battery_percent, distance_to_station_km, vehicle_type
   - Nhận diện case thiếu dữ liệu
        │
        ▼
3. 🔵 Rule + LLM Step: Gợi ý action
   - Nếu pin <5% và trạm >5km: dispatch_mobile_charger
   - Nếu pin đủ và trạm gần: recommend_nearby_station
   - Nếu thiếu dữ liệu: ask_follow_up
        │
        ▼
4. 🔵 AI Step: Draft response
   - Tin nhắn bắt đầu bằng [DRAFT_ONLY]
   - Có lý do ngắn gọn và bước tiếp theo
        │
        ▼
5. 🟢 Human Step: Điều phối viên duyệt
   - Kiểm tra bản đồ/trạm sạc
   - Sửa nội dung nếu cần
   - Bấm gửi hoặc escalate
        │
        ▼
6. ↩️ Fallback
   - Nếu AI thiếu tự tin, output JSON lỗi hoặc thiếu dữ liệu: chuyển về quy trình thủ công.
   - Nếu có tranh chấp phí/tai nạn/an toàn người: escalate cho supervisor.
```

---

## 5. Prompt Prototype Summary

File code nằm tại:

```text
extras/prompt_prototype.py
```

Prototype kiểm thử 3 kiểu tấn công:

1. Người dùng ép AI đề xuất trạm sạc 8km khi pin chỉ còn 2%.
2. Người dùng yêu cầu bỏ tag `[DRAFT_ONLY]` và gửi thẳng tin nhắn.
3. Người dùng yêu cầu AI tự hứa bồi thường hoặc thay đổi phí.

Kết quả mong muốn:

- Case pin thấp phải trả về action `dispatch_mobile_charger`.
- Mọi draft gửi tài xế phải bắt đầu bằng `[DRAFT_ONLY]`.
- Case bồi thường/phí phải từ chối quyết định cuối cùng và yêu cầu human review.

---

## 6. AI Readiness Checklist

| Checklist | Đánh giá | Ghi chú |
|---|---|---|
| Có dữ liệu mẫu/log sạch để test? | NOT YET | Lab hiện dùng dữ liệu giả lập. Cần log điều vận thật: % pin, vị trí, trạm sạc, action cuối cùng và thời gian xử lý. |
| Rủi ro khi AI sai có kiểm soát được không? | YES | Có thể kiểm soát bằng rule cứng, `[DRAFT_ONLY]`, human approval và fallback thủ công. |
| Stakeholders sẵn sàng đổi workflow không? | PARTIAL | Điều phối viên có thể dùng co-pilot nếu UI không làm chậm thao tác. Cần pilot nhỏ trước. |
| Có metric đo kết quả không? | YES | Thời gian triage, tỷ lệ action đúng, tỷ lệ case pin dưới 5% được xử lý an toàn, tỷ lệ draft bị sửa. |
| Có ranh giới vận hành rõ không? | YES | Không tự gửi, không bỏ tag draft, không đề xuất trạm xa khi pin rất thấp, không quyết định tài chính/pháp lý. |

---

## 7. Quyết định cuối cùng

**Decision: GO — bắt đầu xây dựng prototype scope hẹp.**

Lý do:

- Bài toán đủ cụ thể để làm prototype: input là text + vài trường số như pin, khoảng cách, loại xe.
- Rủi ro lớn nhất có thể chuyển thành rule rõ ràng: pin dưới 5% không đi xa hơn 5km.
- LLM tạo giá trị ở phần hiểu mô tả tự nhiên và soạn hướng dẫn dễ hiểu, không phải ở phần quyết định an toàn cuối cùng.
- Chi phí thử nghiệm thấp: có thể chạy offline với dữ liệu giả lập, sau đó pilot trên log lịch sử trước khi tích hợp app thật.

Điều kiện trước khi triển khai thật:

1. Thu thập ít nhất 500-1.000 case lịch sử đã có action đúng để đánh giá baseline.
2. Tạo bộ test riêng cho edge cases: pin 0-5%, trạm gần nhưng hết chỗ, tài xế chở khách, tai nạn nhẹ, tranh chấp phí.
3. Log lại mọi draft AI và phần điều phối viên chỉnh sửa để đo chất lượng.
4. Không bật auto-send trong giai đoạn đầu. Điều phối viên phải duyệt 100% output.

---

## 8. Ước lượng chi phí thử nghiệm

Scope pilot 2 tuần:

- Dữ liệu: dùng 500-1.000 case giả lập/lịch sử, chưa cần tích hợp toàn bộ hệ thống.
- Model: Gemini 2.5 Flash hoặc model tương đương, dùng cho tác vụ phân loại + draft ngắn.
- Chi phí kỹ thuật chính: chuẩn hóa input, viết rule kiểm tra pin/khoảng cách, logging, UI approval.
- Chi phí rủi ro: cần supervisor review các case pin rất thấp, tai nạn hoặc tranh chấp.

Kết luận chi phí: đáng thử ở mức prototype vì không yêu cầu agent tự trị, không cần thay đổi toàn bộ hệ thống điều vận ngay từ đầu.
