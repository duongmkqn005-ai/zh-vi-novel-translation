# Nguồn thiết kế và giới hạn

Khảo sát GitHub ngày 05/10/2026. Bộ này được viết mới cho nhu cầu Trung–Việt của người dùng; không sao chép mã hay prompt của các repo bên dưới và không đóng gói dữ liệu từ điển của họ. Các link là nguồn tham khảo thiết kế, không phải phụ thuộc cài đặt. Giấy phép của repo ngoài áp dụng khi thực sự dùng lại code/dữ liệu của repo đó.

| Nguồn | Điều đã xem / ý tưởng hữu ích | Giới hạn cho nhu cầu này |
|---|---|---|
| [minruixu/translator.skill](https://github.com/minruixu/translator.skill/blob/main/SKILL.md) | Các chế độ dịch, giải nghĩa slang/hàm ý, tra web khi chưa chắc, quản lý thuật ngữ | Skill tổng quát, có nhiều chế độ không phục vụ tiểu thuyết Trung–Việt; ví dụ hàm ý không phải bằng chứng để gán ý định nhân vật |
| [JimLiu/baoyu-skills — baoyu-translate](https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-translate/SKILL.md) | Phân tích, nháp, rà, sửa và nhuận sắc; glossary và chia phần | Mặc định đích zh-CN, glossary tích hợp EN–ZH, có bước cấu hình và công cụ riêng; cần thiết kế riêng cho Việt |
| [Cheng-cheng9669/web-novel-library](https://github.com/Cheng-cheng9669/web-novel-library/blob/main/SKILL.md) | Bộ nhớ tác phẩm, glossary/style/summary, tiến độ tiếp tục, phát hiện nguồn đổi | Quản lý thư viện và workflow; không thay thế hướng dẫn văn phong và xưng hô Việt |
| [hongfei/codex-book-translation](https://github.com/hongfei/codex-book-translation/blob/main/SKILL.md) | Đối chiếu nguồn, giữ cấu trúc, glossary và style sheet | Thiên về xử lý sách và sản xuất ebook; quá nặng nếu chỉ dịch chương TXT/đoạn chat |
| [dynamotn/QuickTranslator](https://github.com/dynamotn/QuickTranslator) | Công cụ chuyển Hán–Việt/Vietphrase trên Windows | Không phải agent skill; repo đã archive ngày 30/12/2020. Bản convert cần được dịch/biên tập lại theo nguyên tác |

Những phần riêng của bộ này: mặc định Trung → Việt; tên Hán–Việt; xưng hô theo quan hệ có hướng và thời điểm; giữ giọng đa thể loại; phân biệt chứng cứ slang với suy luận; bảo toàn manh mối và sự mơ hồ; bàn giao một bản Việt sạch; bộ nhớ độc lập cho từng tác phẩm.

Khảo sát này chưa tìm thấy bộ sẵn có bao trùm đầy đủ các yêu cầu trên. Đây là kết quả của các repo đã tìm và đọc, không phải khẳng định GitHub không có bất kỳ skill Trung–Việt nào. Chưa có thử nghiệm chất lượng dịch trên bản thảo thực tế của người dùng.
