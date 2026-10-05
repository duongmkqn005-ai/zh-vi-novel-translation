# Dùng cùng một skill trên nhiều môi trường

## Model và harness

Gemini, Claude, Grok và DeepSeek là các dòng model. Khả năng tự tìm skill, đọc file, tra web và lưu bộ nhớ thuộc về ứng dụng/harness chạy model. Không kết luận “hỗ trợ native skill” chỉ từ tên model. Bộ này cung cấp hướng dẫn Markdown và tài liệu đi kèm; chất lượng dịch và khả năng làm đúng hướng dẫn vẫn cần đánh giá theo model, phiên bản và công cụ thực tế.

Codex, Claude Code, Gemini CLI, Antigravity và Hermes Agent có cách khám phá skill riêng. Hướng dẫn cài và nguồn chính thức ở README. Không đổi cấu hình provider/API key hoặc cài một harness mới chỉ để dịch một đoạn.

## Ba mức khả năng

| Môi trường | Cách thực hiện |
|---|---|
| Khám phá Agent Skills và đọc file | Đọc SKILL.md rồi chỉ mở reference liên quan; bộ nhớ trong dự án nếu được phép |
| Có file/tool nhưng không khám phá skill | Yêu cầu đọc SKILL.md theo đường dẫn cụ thể; xử lý tương tự |
| Chỉ nhận prompt hoặc file đính kèm | Nạp bundle phù hợp do scripts/export_prompt.py tạo; nhận nguyên tác và bộ nhớ trong chat |

Không đọc được thư mục thì không giả định link tương đối trên GitHub hoặc trong file đính kèm đã được tự tải. Script xuất bundle nối toàn văn reference cần thiết vào cùng tài liệu, mỗi phần có nhãn đường dẫn. Khi dùng bundle, tìm phần phụ lục có đúng đường dẫn thay vì cố mở một file không tồn tại trong môi trường.

## Chuyển tác phẩm từ agent A sang agent B

Chuyển nguyên tác chương hiện tại, bản dịch nối gần nhất, glossary, bảng xưng hô có hướng, quy ước giọng và tiến độ. Các trường giữ nguyên giữa các môi trường; dùng UTF-8 có dấu. Không chỉ gửi một tóm tắt cốt truyện rồi kỳ vọng agent mới nhớ đúng tên và xưng hô.

Nếu chỉ làm trong chat, có thể trả một gói tiếp tục ngắn sau phần dịch theo yêu cầu:

```text
Tác phẩm / phiên bản nguồn:
Đã dịch và rà đến:
Điểm bắt đầu phần tiếp theo:
Quy ước văn phong:
Tên / thuật ngữ mới hoặc thay đổi:
Xưng hô và thời điểm đổi:
Sự kiện đã xác nhận cần giữ:
Điểm chưa chắc và nguồn thực sự đã đọc:
```

Không chèn gói này vào thân truyện. Khi người dùng yêu cầu chỉ bản dịch, giữ mặc định trả bản sạch; cung cấp gói tiếp tục riêng khi họ yêu cầu lưu/chuyển hoặc lúc dừng một nhiệm vụ dài.

## Thiếu công cụ không đồng nghĩa thiếu mọi khả năng

Không có web: dịch phần nghĩa rõ, tách mục cần tra sau, nói rõ chưa xác minh. Không có shell: bỏ qua script cài/xuất, dùng nội dung đã được cung cấp. Không có quyền ghi: trả dữ liệu cần lưu, không nhận đã tạo file. Không có hỏi đáp tương tác: nêu giả định hợp lý rồi tiếp tục; chỉ dừng phần phụ thuộc khi thiếu dữ kiện làm đổi nghĩa trọng yếu.

Không yêu cầu công cụ không có hoặc tự tạo schema tool của một nhà cung cấp khác. Không tự truyền bản thảo sang một dịch vụ/model khác. Bộ này không cần API key để nạp hướng dẫn; phí dùng model/harness hiện tại do môi trường đó quyết định.

## Giới hạn tương thích

Tuân thủ format không chứng minh chất lượng dịch trên mọi model. Khi chuyển môi trường, thử một đoạn có phủ định, tên, thoại và slang; đối chiếu nguyên tác trước khi giao nhiều chương. Đọc tests/behavior-cases.md trong repo nếu cần một tập tình huống đánh giá bằng tay; không coi danh sách đó là kết quả đã chạy trên Gemini/Claude/Grok/DeepSeek.
