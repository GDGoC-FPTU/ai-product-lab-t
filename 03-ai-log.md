# 03 — AI Log & Reflection

**Lab:** AI Product Scoping — Vin Smart Future  
**Thành viên nhóm:** Nguyễn Đức Khang — MSSV: 2A202600588;
**Bài toán:** Xanh SM — AI co-pilot hỗ trợ xử lý sự cố pin thấp của tài xế

---

## 1. Tôi đã dùng AI để làm gì?

Tôi dùng AI như một thought-partner trong ba việc chính.

Thứ nhất, AI giúp brainstorm các pain point trong hệ sinh thái Vingroup. Ban đầu tôi chỉ nghĩ chung chung về chatbot CSKH. Sau khi hỏi theo từng công ty thành viên như Xanh SM, Vinhomes, VinFast, Vinmec, các bài toán rõ hơn: điều phối xe pin thấp, phân loại phản ánh cư dân, phân loại mô tả lỗi xe, đọc review khách sạn và tóm tắt bệnh án.

Thứ hai, AI giúp ép bài toán về dạng có thể đo được. Ví dụ với Xanh SM, nếu chỉ viết “hỗ trợ tài xế khi hết pin” thì quá rộng. Sau khi phản biện, tôi thu hẹp thành: giảm thời gian triage từ khoảng 15 phút xuống dưới 3 phút, và với pin dưới 5% thì không đề xuất trạm sạc xa hơn 5km.

Thứ ba, AI hỗ trợ viết prompt prototype. Tôi dùng AI để nghĩ các adversarial prompts: người dùng yêu cầu bỏ tag `[DRAFT_ONLY]`, ép AI gửi thẳng tin nhắn, hoặc cố tình yêu cầu đề xuất trạm sạc xa trong tình huống pin rất thấp. Những test này giúp kiểm tra boundary thay vì chỉ viết prompt đẹp.

---

## 2. AI đã sai hoặc chưa đủ ở điểm nào?

AI có một lỗi quan trọng: ban đầu nó đề xuất giải pháp giống một agent tự trị hoàn toàn. Agent đó có thể tự tra trạm, tự chọn hướng xử lý và tự gửi hướng dẫn cho tài xế. Cách này nghe hiện đại nhưng không phù hợp với rủi ro vận hành.

Với bài toán pin thấp, nếu AI đề xuất sai trạm hoặc gửi tin quá sớm, xe có thể cạn pin giữa đường. Nếu tài xế đang chở khách, tác động không chỉ là mất thời gian mà còn ảnh hưởng trực tiếp tới trải nghiệm khách hàng và an toàn vận hành. Vì vậy, để AI tự gửi tin là vượt quá boundary.

AI cũng có xu hướng dùng metric hơi đẹp nhưng chưa có nguồn dữ liệu. Ví dụ “98% accuracy” nghe hợp lý, nhưng trong lab hiện tại chưa có log thật để chứng minh. Tôi phải ghi rõ đây là target metric, không phải kết quả đã đạt được.

---

## 3. Tôi đã sửa prompt và boundary như thế nào?

Tôi sửa theo hướng tách phần rule cứng khỏi phần LLM.

Rule cứng:

```text
Nếu battery_percent < 5 và nearest_station_distance_km > 5:
    action = dispatch_mobile_charger
```

LLM không được tự quyết định ngược rule này, dù user có yêu cầu “đang gấp”, “khách VIP”, hoặc “bỏ qua quy trình”.

Tôi cũng thêm yêu cầu mọi tin nhắn draft phải bắt đầu bằng:

```text
[DRAFT_ONLY]
```

Tag này nhắc rõ rằng output chỉ là bản nháp, không phải tin nhắn đã được phép gửi. Điều phối viên vẫn phải kiểm tra và duyệt.

Cuối cùng, tôi thêm fallback:

- Nếu thiếu dữ liệu pin/vị trí: hỏi thêm thông tin.
- Nếu có tai nạn, tranh chấp phí hoặc bồi thường: escalate cho supervisor.
- Nếu model không chắc chắn: chuyển về xử lý thủ công.

---

## 4. Bài học cá nhân

Bài học lớn nhất là không nên bắt đầu bằng câu hỏi “dùng AI gì?”. Nên bắt đầu từ workflow: ai đang làm, bước nào chậm, dữ liệu vào là gì, sai thì hậu quả ra sao, và con người cần duyệt ở đâu.

Trong bài này, LLM phù hợp để đọc mô tả tự nhiên và draft tin nhắn. Nhưng quyết định an toàn phải nằm ở rule và human review. Nếu bỏ phần rule, prompt dù viết kỹ vẫn có thể bị user dụ vượt ranh giới.

Nếu làm tiếp, tôi sẽ lấy dữ liệu lịch sử của các case điều vận pin thấp để tạo benchmark nhỏ. Mỗi case cần có: mức pin, khoảng cách trạm gần nhất, loại xe, action đúng, thời gian xử lý và ghi chú của điều phối viên. Khi đó mới đánh giá được prototype có thật sự tốt hơn workflow thủ công hay chỉ chạy được trên vài ví dụ đẹp.
