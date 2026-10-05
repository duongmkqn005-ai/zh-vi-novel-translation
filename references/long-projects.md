# Dịch truyện dài và tiếp tục qua nhiều phiên

Đối với dự án đã có cấu trúc, dùng cấu trúc đó. Khi người dùng yêu cầu lưu một tác phẩm mới, có thể khởi tạo nhẹ:

```text
ten-truyen/
  source/                 nguyên tác theo chương; không sửa
  translation/            bản Việt đã rà theo chương
  work/                   bản nháp và đối chiếu nếu cần
  memory/
    style.md              quy ước theo mẫu assets/series-memory-template.md
    glossary.csv          theo mẫu assets/glossary-template.csv
    progress.md           nguồn, phần đã rà, vị trí tiếp tục, điểm chưa chắc
    research.md           chỉ các tra cứu cần tái sử dụng
```

Không tạo hệ thống lưu trữ cho mỗi đoạn chat ngắn. Bộ nhớ nằm trong dự án của tác phẩm, không nằm trong skill hoặc dùng chung mọi truyện.

## Trước mỗi chương

Đọc style, các mục glossary và bảng xưng hô liên quan, diễn biến đã xác nhận đến chương đang dịch và đoạn nối gần nhất. Bản tóm tắt hỗ trợ nối ngữ cảnh nhưng nguyên tác mới quyết định nghĩa; mở lại đoạn gốc nếu tóm tắt mâu thuẫn hoặc quá sơ lược. Không xem trước chương chưa được giao chỉ để giải đáp một bí ẩn nếu có nguy cơ làm lộ/đổi điểm nhìn.

Glossary dùng chữ Hán gốc + loại + phạm vi/nghĩa làm khóa thực tế. CSV hỗ trợ các cột:

- `source`, `target`, `category`: cụm gốc, cách Việt, loại như name/alias/title/term/slang.
- `scope`: điều kiện áp dụng, nhân vật/cộng đồng, phạm vi thời gian/cảnh.
- `status`: `locked` (đã chốt), `provisional` (tạm dùng), `retired` (phương án cũ).
- `first_seen`, `evidence`, `notes`: vị trí xuất hiện, chứng cứ hoặc quyết định người dùng, sắc thái và lựa chọn tránh.

Không khóa một chữ đa nghĩa cho mọi câu. Khi người dùng chốt một tên, ghi evidence là quyết định người dùng; không giả thành nguồn từ điển. Các mục mới có thể tạm dùng để dịch tiếp. Chỉ đổi mục locked khi có quyết định mới hoặc đã thông báo lý do sửa một lỗi được xác minh; ghi ảnh hưởng đến chương cũ.

## Chia phần và lưu tiến độ

Chia theo cảnh và đoạn vừa với ngữ cảnh; không cắt giữa lượt thoại/câu nếu tránh được. Mỗi phần có vị trí bắt đầu/kết thúc rõ. Nếu đọc thêm đoạn lân cận để hiểu cảnh, phân biệt đó là ngữ cảnh với phạm vi thực sự cần dịch để không lặp khi ghép.

Giữ bản nguyên tác theo chương và ghi tên file/phiên bản; dùng hash nguồn nếu dự án có nhiều phiên bản dễ lẫn. Khi nguồn đổi, đánh dấu bản Việt cần rà lại thay vì coi đã hoàn tất. Không tự ghi đè chương đã rà khi chạy tiếp. Nếu sửa, lưu phiên bản/bản sao thích hợp và ghi đúng phần đổi.

Sau khi ghép, kiểm tra thứ tự, đầu/cuối, đầy đủ các cảnh/lượt thoại, tên, xưng hô và đoạn nối. Hai phần dịch riêng dễ lệch quan hệ dù cùng dùng glossary; đọc liền toàn cảnh để sửa.

Trong `progress.md`, ghi cho mỗi chương/phần: nguồn đã đọc, phạm vi đã dịch, đã đối chiếu nghĩa hay chưa, đã nhuận sắc hay chưa, đường dẫn thành phẩm, vấn đề mở và điểm tiếp tục. “Đã có nháp” không có nghĩa “đã hoàn thành”. Nếu không còn đủ thời gian/ngữ cảnh, lưu điểm nối chính xác; không báo cả sách xong.

## Bộ nhớ cốt truyện

Chỉ lưu sự kiện và quan hệ được nguyên tác xác nhận đến điểm hiện tại. Ghi nghi ngờ của nhân vật thành nghi ngờ; giữ danh tính chưa công bố là chưa công bố. Bộ nhớ là trợ giúp cho dịch nhất quán, không trở thành một bản giải thích lại tác phẩm.

Nếu cần xuất DOCX/PDF/EPUB, chọn công cụ/skill định dạng sẵn có và kiểm tra kết quả theo yêu cầu xuất file. Skill này không tự cài công cụ hoặc chuyển một yêu cầu dịch đoạn thành dự án xuất bản.
