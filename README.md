# Dịch tiểu thuyết Trung–Việt bằng AI

**Một bộ Agent Skill dùng chung cho nhiều model và harness:** dịch tiếng Trung sang tiếng Việt tự nhiên, sát ý; tra tiếng lóng, meme và điển cố; giữ tên Hán–Việt, xưng hô và thuật ngữ nhất quán qua nhiều chương.

Mặc định: **đa thể loại · tiếng Việt tự nhiên · sát nguyên tác · tên Trung Hán–Việt**. Bạn có thể đổi quy ước cho từng truyện. Giấy phép [MIT](LICENSE).

## Bộ này giúp gì?

- Dịch chương truyện và soát bản Việt với nguyên tác; sửa bản convert mà không tự thêm tình tiết.
- Giữ giọng người kể và từng nhân vật, mức cổ phong/khẩu ngữ phù hợp.
- Quản lý tên, biệt danh, chức danh và **xưng hô theo từng hướng người nói → người nghe**, có phạm vi cảnh/chương.
- Tra slang/meme/điển cố theo câu truyện, thời điểm và cộng đồng; tách bằng chứng đã đọc khỏi suy luận.
- Dịch nhiều chương với glossary, bộ nhớ tác phẩm và điểm tiếp tục sau gián đoạn.
- Rà phủ định, ai làm gì với ai, số/đơn vị, manh mối và nội dung thiếu/thừa.

Đầu ra mặc định là **một bản Việt sạch**; chú giải cần thiết nằm ngoài thân truyện. Chỉ trả phân tích dài khi bạn yêu cầu.

## Model và harness: hai lớp khác nhau

**Gemini, Claude, Grok, DeepSeek** có thể áp dụng bộ hướng dẫn khi được nạp vào ngữ cảnh. Khả năng tự tìm skill, đọc file, tra web và lưu dữ liệu phụ thuộc ứng dụng/harness chạy model. Bộ này không đổi provider, không gọi API dịch và không cần API key riêng. Model/harness bạn dùng vẫn có điều kiện sử dụng và chi phí riêng.

| Môi trường | Cách dùng | Mức xác nhận |
|---|---|---|
| Codex | Skill folder + metadata OpenAI tùy chọn | Đã cài vào Codex của người tạo; hướng dẫn cài mới đối chiếu tài liệu chính thức |
| Claude Code | Skill folder, có thể gọi `/zh-vi-novel-translation` | Cấu trúc và vị trí cài đối chiếu tài liệu; chưa chạy thử Claude Code |
| Gemini CLI | Skill folder hoặc lệnh cài skill của CLI | Cấu trúc và vị trí cài đối chiếu tài liệu; chưa chạy thử Gemini CLI |
| Antigravity IDE / 2.0 / CLI | Skill folder đúng scope của sản phẩm | Phân biệt vị trí IDE/2.0 với CLI; chưa chạy thử trực tiếp |
| Hermes Agent | Skill folder trong profile hoặc dự án được tin cậy | Vị trí cài đối chiếu tài liệu; chưa chạy thử trực tiếp |
| Gemini / Claude / Grok / DeepSeek trong chat hoặc harness khác | Nạp bundle Markdown hoặc yêu cầu đọc SKILL.md | Tương thích ở mức hướng dẫn; chưa benchmark chất lượng từng model |

Không có web thì agent vẫn dịch phần nghĩa rõ và nêu mục chưa xác minh. Không đọc/ghi được file thì dùng bundle và trả bộ nhớ trong chat. Không coi việc có file `SKILL.md` là bằng chứng đã kiểm thử trên mọi model.

## Clone

```bash
git clone https://github.com/duongmkqn005-ai/zh-vi-novel-translation.git
cd zh-vi-novel-translation
```

Bạn cũng có thể chọn **Code → Download ZIP** trên GitHub rồi giải nén. Để cập nhật bản clone khi không có thay đổi local:

```bash
git pull --ff-only
```

Repo chỉ chứa hướng dẫn, mẫu và tiện ích. Lưu bản thảo, bản dịch và bộ nhớ trong thư mục tác phẩm riêng.

## Cài nhanh bằng Python

Tiện ích cài dùng **Python 3.10+**, chỉ thư viện chuẩn, chạy trên Windows/macOS/Linux. Không cài package, tải mạng, sửa cấu hình model hay tự khởi chạy harness. Dịch bằng skill không bắt buộc có Python: xem cách copy thủ công và bundle bên dưới.

Chạy trong thư mục vừa clone, chọn **một** harness bạn muốn cài:

```bash
python scripts/install.py --harness codex
python scripts/install.py --harness claude-code
python scripts/install.py --harness gemini-cli
python scripts/install.py --harness antigravity
python scripts/install.py --harness antigravity-cli
python scripts/install.py --harness hermes
```

Trên macOS/Linux, dùng `python3` nếu máy không có lệnh `python`. Trên Windows có Python Launcher, có thể dùng `py -3`. Kiểm tra đường dẫn trước khi cài:

```bash
python scripts/install.py --harness claude-code --dry-run
```

Cài theo dự án thay vì toàn bộ tài khoản:

```bash
python scripts/install.py --harness claude-code --scope project --project /duong/dan/du-an
```

PowerShell trên Windows:

```powershell
py -3 scripts/install.py --harness claude-code --scope project --project 'D:\DichTruyen\TacPham'
```

Script không ghi đè bản đang có. Sau khi cập nhật repo, muốn thay bản cài:

```bash
python scripts/install.py --harness claude-code --update
```

Bản cũ được giữ trong thư mục `skill-backups` nằm ngoài thư mục `skills`; script in đường dẫn để bạn khôi phục nếu cần. Nếu harness của bạn dùng vị trí khác, chỉ rõ **thư mục cha chứa các skill**:

```bash
python scripts/install.py --harness generic --dest /duong/dan/skills
```

Script sẽ tạo `/duong/dan/skills/zh-vi-novel-translation/`. Nếu đổi vị trí cài, bảo đảm harness thật sự đọc vị trí đó. Script không tự chỉnh cấu hình khám phá skill.

## Copy thủ công và nguồn chính thức

Copy nguyên thư mục skill, gồm `SKILL.md`, `references/`, `assets/`, `scripts/`, `agents/` và `LICENSE`, vào một vị trí phù hợp. Các script không cần chạy trong lúc dịch. Mỗi vị trí dưới đây là **thư mục cha**; thêm `zh-vi-novel-translation/` phía sau.

| Harness | Theo tài khoản | Theo dự án | Tài liệu |
|---|---|---|---|
| Codex | `~/.agents/skills/` | `.agents/skills/` | [OpenAI](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | [Claude Code](https://code.claude.com/docs/en/skills) |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` | [Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/) |
| Antigravity IDE / 2.0 | `~/.gemini/config/skills/` | `.agents/skills/` | [Google Antigravity](https://antigravity.google/docs/skills) |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | `.agents/skills/` | [Google Antigravity](https://antigravity.google/docs/skills) |
| Hermes Agent | `~/.hermes/skills/` hoặc `$HERMES_HOME/skills/` khi dùng profile riêng | `.hermes/skills/` | [NousResearch](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) |

Đối chiếu ngày **05/10/2026**. Tên `~` là thư mục người dùng trên máy của bạn, không phải đường dẫn của người tạo repo.

**Codex:** gọi `$zh-vi-novel-translation` hoặc chọn trong danh sách skill. Nếu bản đang dùng cài ở vị trí cũ `~/.codex/skills/`, chỉ rõ `--dest ~/.codex/skills` để cập nhật đúng bản đó; không cài hai bản trùng tên. Nếu thay đổi chưa hiện, mở phiên mới/khởi động lại Codex.

**Claude Code:** gọi `/zh-vi-novel-translation` hoặc yêu cầu bằng tên. Vị trí personal trên máy không đồng nghĩa skill đã được cài cho các phiên cloud/Claude.ai; các môi trường đó có cơ chế nạp riêng.

**Gemini CLI:** có thể dùng lệnh native từ URL repo:

```bash
gemini skills install https://github.com/duongmkqn005-ai/zh-vi-novel-translation
```

Trong phiên Gemini CLI, dùng `/skills list` để kiểm tra và `/skills reload` sau khi đổi file. Quy trình cấp quyền của CLI do CLI quản lý.

**Antigravity:** chọn đúng IDE/2.0 hoặc CLI khi dùng script. Có thể yêu cầu agent dùng skill bằng tên; phiên bản hỗ trợ slash command có thể dùng `/zh-vi-novel-translation`. Kiểm tra danh sách Customizations/skills của sản phẩm đang chạy.

**Hermes:** cài theo tài khoản bằng script ở trên. Sau khi cài theo dự án, chạy `hermes skills trust` từ trong repo để cho phép nạp skill, rồi kiểm tra `hermes skills list`. Chưa thay đổi cấu hình tin cậy của máy bạn chỉ bằng việc copy thư mục.

## Dùng với chat Gemini, Claude, Grok, DeepSeek

Nếu môi trường không tự đọc thư mục skill, xuất **một file tự chứa** rồi đính kèm hoặc dán nội dung vào chat. Chọn chế độ theo việc cần làm để tiết kiệm ngữ cảnh:

```bash
python scripts/export_prompt.py --mode translate --output dist/huong-dan-dich.md
python scripts/export_prompt.py --mode research --output dist/huong-dan-tra-cuu.md
python scripts/export_prompt.py --mode review --output dist/huong-dan-soat.md
python scripts/export_prompt.py --mode long --output dist/huong-dan-dich-dai.md
```

`--mode all` nối toàn bộ hướng dẫn và mẫu nếu bạn cần. Script không đưa bản thảo hay bộ nhớ cá nhân vào bundle. Nếu không có Python, cung cấp `SKILL.md` và các tài liệu liên quan trong `references/`; chỉ dán SKILL.md thì các link nội bộ chưa tự biến thành nội dung đã được đọc.

Sau khi nạp bundle, gửi:

```text
Áp dụng bộ hướng dẫn zh-vi-novel-translation vừa cung cấp.
Dịch đoạn/chương sau sang tiếng Việt tự nhiên, sát ý, tên Hán–Việt.
Giữ giọng thoại từng nhân vật. Nếu không có web, đánh dấu riêng
những tiếng lóng chưa xác minh; không tạo nguồn giả.

[Nguyên tác tiếng Trung]
```

Bạn không cần dán `$` hoặc `/` trong chat nếu ứng dụng không hỗ trợ cú pháp đó. Tên model không quyết định cách cài.

## Ví dụ yêu cầu

**Dịch:** “Dịch chương này, giữ nhịp văn gọn và sắc thái châm chọc; chú giải cần thiết để cuối chương.”

**Tra cứu:** “Tra cụm này trong câu trước/sau, tìm nguồn tiếng Trung và đề xuất cách Việt hóa hợp cảnh; tách nghĩa đen, slang và suy luận.”

**Soát:** “Đối chiếu bản Việt với nguyên tác; trả lỗi có vị trí về phủ định, tên, xưng hô và thiếu/thừa nội dung, rồi sửa.”

**Tiếp tục:** “Đọc glossary và bảng xưng hô tác phẩm này, dịch chương tiếp theo, ghi phạm vi đã rà và điểm tiếp tục.”

Có thể ghi riêng “không chú thích”, “giữ tên pinyin”, “cổ phong vừa phải” hoặc đưa một bản dịch mẫu để agent theo đúng sở thích tác phẩm.

## Cấu trúc và bộ nhớ tác phẩm

```text
zh-vi-novel-translation/
├── SKILL.md              điểm vào chung cho agent
├── README.md             hướng dẫn người dùng
├── LICENSE               MIT
├── agents/openai.yaml    metadata OpenAI tùy chọn
├── references/           hướng dẫn chuyên đề; đọc khi cần
├── assets/               mẫu glossary, xưng hô và nghiên cứu
├── scripts/              cài, xuất bundle, kiểm tra
└── tests/                kiểm thử tiện ích và tình huống đánh giá
```

Mỗi tác phẩm nên giữ `source/`, `translation/`, `memory/style.md`, `memory/glossary.csv`, `memory/progress.md` và các tra cứu cần dùng lại trong thư mục riêng. Xem [quy trình truyện dài](references/long-projects.md). Khi chuyển agent, gửi bộ nhớ cùng nguyên tác và đoạn nối; không kỳ vọng agent mới nhớ hội thoại của agent cũ.

## Kiểm tra

```bash
python scripts/validate_bundle.py
python -m unittest discover -s tests -p "test_*.py" -v
```

Validator kiểm tra cấu trúc, link nội bộ và mẫu; test chạy installer/exporter trong thư mục tạm, không cài lên profile thật. [Tình huống hành vi](tests/behavior-cases.md) phục vụ đánh giá dịch bằng tay. Repo có CI chạy tiện ích trên Windows/Linux/macOS và Python 3.10/3.12.

Đã kiểm tra cấu trúc và tiện ích bằng Python trên Windows. **Chưa chạy harness thật ngoài Codex và chưa đánh giá chất lượng trên cả bốn dòng model.** CI xanh cũng không chứng minh bản dịch sát nghĩa; vẫn phải đối chiếu nguyên tác và các lựa chọn văn phong quan trọng.

## Nguồn thiết kế và đóng góp

Xem [nguồn thiết kế](references/provenance.md). Bộ hướng dẫn được viết riêng cho Trung–Việt, tham khảo ý tưởng workflow từ các repo dịch thuật; không đóng gói mã/prompt hoặc dữ liệu từ điển bên ngoài.

Nếu đề xuất sửa, nêu câu gốc, ngữ cảnh, bản Việt, lỗi cụ thể và nguồn nếu có. Dùng đoạn tự soạn hoặc đoạn bạn có thể chia sẻ; không đưa toàn bộ bản thảo riêng vào issue công khai.
