import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load('install')
exporter = load('export_prompt')
validator = load('validate_bundle')


class ToolsTest(unittest.TestCase):
    def test_validate_repo(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_new_install_keeps_exact_payload_and_excludes_repo_data(self):
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / 'skills' / installer.NAME
            installer.install(ROOT, target)
            self.assertEqual((target / 'SKILL.md').read_bytes(), (ROOT / 'SKILL.md').read_bytes())
            self.assertEqual(validator.validate(target), [])
            self.assertFalse((target / '.git').exists())
            self.assertFalse((target / 'tests').exists())
            for relative in ('references/slang-research.md', 'assets/glossary-template.csv', 'scripts/export_prompt.py'):
                self.assertEqual((target / relative).read_bytes(), (ROOT / relative).read_bytes())

    def test_existing_install_refused_without_update(self):
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / 'skills' / installer.NAME
            installer.install(ROOT, target)
            (target / 'SKILL.md').write_text('local edit', encoding='utf-8')
            with self.assertRaises(ValueError):
                installer.install(ROOT, target)
            self.assertEqual((target / 'SKILL.md').read_text(encoding='utf-8'), 'local edit')

    def test_update_preserves_local_edits_outside_discovery_directory(self):
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / 'skills' / installer.NAME
            installer.install(ROOT, target)
            (target / 'SKILL.md').write_text('local edit', encoding='utf-8')
            (target / 'personal.txt').write_text('keep me', encoding='utf-8')
            backup = installer.install(ROOT, target, update=True)
            self.assertEqual((backup / 'SKILL.md').read_text(encoding='utf-8'), 'local edit')
            self.assertEqual((backup / 'personal.txt').read_text(encoding='utf-8'), 'keep me')
            self.assertFalse(backup.is_relative_to(target.parent))
            self.assertEqual((target / 'SKILL.md').read_bytes(), (ROOT / 'SKILL.md').read_bytes())
            self.assertFalse((target / 'personal.txt').exists())

    def test_dry_run_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as scratch:
            parent = Path(scratch) / 'not-created'
            installer.install(ROOT, parent / installer.NAME, dry_run=True)
            self.assertFalse(parent.exists())

    def test_refuses_non_skill_target_and_nested_paths(self):
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / installer.NAME
            target.mkdir()
            (target / 'important.txt').write_text('keep', encoding='utf-8')
            with self.assertRaises(ValueError):
                installer.install(ROOT, target, update=True)
            self.assertEqual((target / 'important.txt').read_text(encoding='utf-8'), 'keep')
            with self.assertRaises(ValueError):
                installer.install(ROOT, ROOT / 'nested' / installer.NAME, dry_run=True)

    def test_destination_mapping_without_touching_real_profile(self):
        with tempfile.TemporaryDirectory() as scratch:
            with patch.object(installer.Path, 'home', return_value=Path(scratch)), patch.dict(installer.os.environ, {}, clear=True):
                for harness, relative in installer.GLOBAL_DIRS.items():
                    self.assertEqual(installer.destination(harness, 'user'), Path(scratch) / relative / installer.NAME)
            project = Path(scratch) / 'myproject'
            self.assertEqual(installer.destination('claude-code', 'project', str(project)), project / '.claude/skills' / installer.NAME)

    def test_export_modes_include_requested_raw_resources_once(self):
        for mode, extra in exporter.MODES.items():
            bundle = exporter.build(ROOT, mode)
            for relative in dict.fromkeys(exporter.COMMON + extra):
                self.assertIn((ROOT / relative).read_text(encoding='utf-8').rstrip(), bundle)
                self.assertEqual(bundle.count('## Tài liệu: ' + relative + '\n'), 1)
            self.assertNotIn('metadata:\n', bundle)

    def test_export_cli_no_overwrite(self):
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / 'bundle.md'
            command = [sys.executable, '-X', 'utf8', str(ROOT / 'scripts/export_prompt.py'), '--mode', 'long', '--output', str(target)]
            first = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(first.returncode, 0, first.stderr)
            original = target.read_bytes()
            second = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(target.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
