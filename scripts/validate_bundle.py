#!/usr/bin/env python3
"""Validate this bundle's controlled format using only the standard library."""
import ast
import csv
from pathlib import Path
import re
import sys
import unicodedata


def validate(root):
    errors = []
    required = ('SKILL.md', 'LICENSE', 'agents/openai.yaml',
                'assets/glossary-template.csv', 'assets/series-memory-template.md',
                'assets/research-note-template.md', 'references/portability.md')
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f'Thiếu: {relative}')
    if errors:
        return errors
    source = (root / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', source, re.S)
    if not match:
        errors.append('Frontmatter phải nằm đầu SKILL.md, không BOM, với dấu --- riêng dòng.')
    else:
        name = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', match[1], re.M)
        if not name or name[1] != 'zh-vi-novel-translation' or len(name[1]) > 64:
            errors.append('Tên skill không hợp lệ.')
        description = re.search(r'^description: ("[^\n]*")$', match[1], re.M)
        try:
            value = ast.literal_eval(description[1]) if description else ''
            if not isinstance(value, str) or not 1 <= len(value) <= 1024:
                errors.append('Description phải có 1–1024 ký tự trong chuỗi có ngoặc kép.')
        except (ValueError, SyntaxError):
            errors.append('Description không đúng dạng chuỗi của bộ này.')
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(part in ('.git', '__pycache__', 'work', 'dist') for part in path.relative_to(root).parts):
            continue
        if path.suffix not in ('.md', '.yaml', '.py', '.csv', '.yml'):
            continue
        text = path.read_text(encoding='utf-8')
        if text != unicodedata.normalize('NFC', text):
            errors.append(f'Unicode chưa NFC: {path.relative_to(root)}')
        if path.suffix == '.md':
            # Links in fenced code/examples are data, not navigable document links.
            visible = re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)
            for target in re.findall(r'\]\(([^)\s]+)\)', visible):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                    errors.append(f'Link lỗi/ngoài gói: {path.relative_to(root)} → {target}')
    with (root / 'assets/glossary-template.csv').open(encoding='utf-8', newline='') as handle:
        rows = list(csv.reader(handle))
    expected = ['source', 'target', 'category', 'scope', 'status', 'first_seen', 'evidence', 'notes']
    if rows != [expected]:
        errors.append('Mẫu glossary phải chỉ chứa đúng header; không chứa dữ liệu tác phẩm.')
    return errors


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    for error in errors:
        print(error)
    if not errors:
        print('Hợp lệ: frontmatter cơ bản, file cần thiết, link nội bộ, Unicode NFC và mẫu glossary.')
        print('Kiểm tra này không đánh giá độ đúng của bản dịch hoặc chứng nhận mọi harness.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
