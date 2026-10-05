#!/usr/bin/env python3
"""Install the local skill. Standard library only; never downloads anything."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

NAME = 'zh-vi-novel-translation'
GLOBAL_DIRS = {
    'codex': '.agents/skills',
    'claude-code': '.claude/skills',
    'gemini-cli': '.gemini/skills',
    'antigravity': '.gemini/config/skills',
    'antigravity-cli': '.gemini/antigravity-cli/skills',
    'hermes': '.hermes/skills',
    'generic': '.agents/skills',
}
PROJECT_DIRS = {
    'codex': '.agents/skills',
    'claude-code': '.claude/skills',
    'gemini-cli': '.gemini/skills',
    'antigravity': '.agents/skills',
    'antigravity-cli': '.agents/skills',
    'hermes': '.hermes/skills',
    'generic': '.agents/skills',
}
PAYLOAD = ('SKILL.md', 'LICENSE', 'agents', 'assets', 'references', 'scripts')


def destination(harness, scope, project=None, dest=None):
    if dest:
        base = Path(dest).expanduser()
    elif scope == 'project':
        base = Path(project or Path.cwd()).expanduser() / PROJECT_DIRS[harness]
    else:
        if harness == 'hermes' and os.environ.get('HERMES_HOME'):
            base = Path(os.environ['HERMES_HOME']).expanduser() / 'skills'
        else:
            base = Path.home() / GLOBAL_DIRS[harness]
    # Do not traverse existing symlink directories during a managed installation.
    absolute = Path(os.path.abspath(base))
    for ancestor in (absolute, *absolute.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError(f'Thư mục cài là link/junction: {ancestor}. Hãy chọn --dest khác.')
    return absolute / NAME


def check_source(source):
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Không tìm thấy SKILL.md cạnh thư mục scripts.')
    for part in PAYLOAD:
        item = source / part
        if not item.exists():
            raise ValueError(f'Thiếu thành phần skill: {part}')
        for candidate in (item, *item.rglob('*')) if item.is_dir() else (item,):
            if candidate.is_symlink() or getattr(candidate, 'is_junction', lambda: False)():
                raise ValueError(f'Nguồn chứa link/junction: {candidate}')


def install(source, target, update=False, dry_run=False):
    source = source.resolve()
    target = Path(os.path.abspath(target))
    check_source(source)
    if target.name != NAME or target.parent == target:
        raise ValueError('Đích cài phải là thư mục riêng mang tên skill.')
    if target == source or source in target.parents or target in source.parents:
        raise ValueError('Nguồn và đích không được trùng/lồng nhau.')
    if target.is_symlink() or getattr(target, 'is_junction', lambda: False)():
        raise ValueError('Không ghi đè skill là link/junction.')
    if target.exists() and not update:
        raise ValueError(f'Đã có {target}. Dùng --update để cập nhật kèm bản sao lưu.')
    if target.exists() and not (target / 'SKILL.md').is_file():
        raise ValueError('Đích đã tồn tại nhưng không phải thư mục skill; không thay thế.')
    if dry_run:
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.' + NAME + '-stage-', dir=target.parent))
    backup = None
    try:
        for part in PAYLOAD:
            item = source / part
            if item.is_dir():
                shutil.copytree(item, stage / part, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(item, stage / part)
        if target.exists():
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            backup_root = target.parent.parent / 'skill-backups'
            if backup_root.is_symlink() or getattr(backup_root, 'is_junction', lambda: False)():
                raise ValueError('Thư mục backup là link/junction; không cập nhật.')
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / (NAME + '.backup-' + stamp + '-' + uuid.uuid4().hex[:8])
            # Verify absolute source and destination boundaries before moving on Windows.
            if target.resolve().parent != target.parent.resolve() or backup.resolve().parent != backup_root.resolve():
                raise ValueError('Đường dẫn cập nhật vượt thư mục cài.')
            target.rename(backup)
        try:
            stage.rename(target)
        except Exception:
            if backup is not None and not target.exists():
                backup.rename(target)
            raise
    finally:
        if stage.exists():
            # Remove only the temporary directory this function created, after checking its boundary.
            if stage.resolve().parent != target.parent.resolve() or not stage.name.startswith('.' + NAME + '-stage-'):
                raise ValueError('Không dọn thư mục tạm ngoài phạm vi cài.')
            shutil.rmtree(stage)
    return backup


def main():
    parser = argparse.ArgumentParser(description='Cài skill từ bản clone; không tải dữ liệu hay sửa cấu hình model.')
    parser.add_argument('--harness', choices=GLOBAL_DIRS, required=True)
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--project', help='Gốc dự án khi dùng --scope project.')
    parser.add_argument('--dest', help='Thư mục cha chứa các skill; script thêm tên skill phía sau.')
    parser.add_argument('--update', action='store_true', help='Cập nhật; giữ bản cũ trong skill-backups ở ngoài thư mục skills.')
    parser.add_argument('--dry-run', action='store_true', help='Kiểm tra và in đích; không ghi file.')
    args = parser.parse_args()
    if args.project and args.scope != 'project':
        parser.error('--project chỉ dùng cùng --scope project.')
    source = Path(__file__).resolve().parents[1]
    try:
        target = destination(args.harness, args.scope, args.project, args.dest)
        backup = install(source, target, args.update, args.dry_run)
    except (OSError, ValueError) as error:
        print(f'Lỗi: {error}', file=sys.stderr)
        return 1
    print(('Sẽ cài: ' if args.dry_run else 'Đã cài: ') + str(target))
    if backup:
        print('Bản cũ được giữ tại: ' + str(backup))
    if args.harness == 'hermes' and args.scope == 'project' and not args.dest:
        print('Chạy hermes skills trust trong dự án để cho phép nạp skill; xem README.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
