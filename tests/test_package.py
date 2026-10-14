import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import verify
import install

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / 'plugin'
        shutil.copytree(ROOT / 'plugins/ui-design-agent', self.root)
    def tearDown(self):
        self.temporary.cleanup()
    def assertRejected(self):
        with self.assertRaises(verify.VerificationError):
            verify.verify(self.root)
    def test_original_package(self):
        self.assertEqual(verify.verify(self.root)['version'], '0.1.0')
    def test_vendor_tampered(self):
        (self.root / 'skills/ui-design/vendor/interface-design/SKILL.md').write_text('modified')
        self.assertRejected()
    def test_vendor_missing(self):
        (self.root / 'skills/ui-design/vendor/interface-design/SKILL.md').unlink()
        self.assertRejected()
    def test_vendor_extra(self):
        (self.root / 'skills/ui-design/vendor/interface-design/unreviewed.sh').write_text('extra')
        self.assertRejected()
    def test_package_extra(self):
        (self.root / 'hooks.json').write_text('{}')
        self.assertRejected()
    def test_symlink(self):
        (self.root / 'escape').symlink_to('/etc/passwd')
        self.assertRejected()
    def test_path_traversal(self):
        for relative in ('../escape', '/absolute', 'a/../../escape', 'a\\b'):
            with self.subTest(relative=relative), self.assertRaises(verify.VerificationError):
                verify.safe_path(self.root, relative)
    def test_lock_traversal(self):
        path = self.root / 'dependencies.lock.json'
        data = json.loads(path.read_text())
        data['dependencies'][0]['files']['../escape'] = '0' * 64
        path.write_text(json.dumps(data))
        self.assertRejected()
    def test_compatibility_mismatch(self):
        path = self.root / 'compatibility.json'
        data = json.loads(path.read_text())
        data['intake_contract'] = 'unknown/v2'
        path.write_text(json.dumps(data))
        self.assertRejected()
    def test_extra_manifest_execution_field(self):
        path = self.root / 'plugin.json'
        data = json.loads(path.read_text())
        data['hooks'] = {'command': 'untrusted'}
        path.write_text(json.dumps(data))
        self.assertRejected()
    def test_broken_reference_even_with_fresh_inventory(self):
        path = self.root / 'skills/ui-design/SKILL.md'
        path.write_text(path.read_text() + '\n[Missing](missing.md)\n')
        verify.write_inventory(self.root)
        self.assertRejected()

class InstallerTests(unittest.TestCase):
    def test_ref_rejects_unpinned(self):
        for ref in ('main', 'HEAD', 'v1', 'abc123', '--help', 'v1.2.3;bad'):
            with self.subTest(ref=ref), self.assertRaises(verify.VerificationError):
                install.resolve_ref(install.SOURCE, ref, {})
    def test_exact_commit_does_not_query_remote(self):
        with patch.object(install, 'run') as run:
            self.assertEqual(install.resolve_ref(install.SOURCE, 'a' * 40, {}), 'a' * 40)
            run.assert_not_called()
    def test_annotated_tag_resolves_commit(self):
        with patch.object(install, 'run', return_value='a' * 40 + '\trefs/tags/v1.2.3\n' + 'b' * 40 + '\trefs/tags/v1.2.3^{}\n'):
            self.assertEqual(install.resolve_ref(install.SOURCE, 'v1.2.3', {}), 'b' * 40)
    def test_unknown_tag(self):
        with patch.object(install, 'run', return_value=''):
            with self.assertRaises(verify.VerificationError):
                install.resolve_ref(install.SOURCE, 'v1.2.3', {})
    def test_source_rejects_credentials_and_non_github(self):
        for source in ('https://user:secret@github.com/o/r', 'http://github.com/o/r', 'https://example.com/o/r', 'https://github.com/o/r?token=secret', '/local/path'):
            with self.subTest(source=source), self.assertRaises(verify.VerificationError):
                install.source_url(source)
    def test_command_failure_does_not_echo_secret(self):
        result = subprocess.CompletedProcess(['codex'], 1, stdout='secret-token', stderr='secret-token')
        with patch.object(subprocess, 'run', return_value=result):
            with self.assertRaises(install.InstallError) as raised:
                install.run(['codex', 'plugin', 'list'], {})
        self.assertNotIn('secret-token', str(raised.exception))
    def test_command_timeout(self):
        with patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired('codex', 1)):
            with self.assertRaises(install.InstallError):
                install.run(['codex'], {})
    def test_enabled_readback(self):
        self.assertIsNotNone(install.enabled_plugin({'installed': [{'name': 'ui-design-agent', 'enabled': True}]}))
        self.assertIsNone(install.enabled_plugin({'installed': [{'name': 'ui-design-agent', 'enabled': False}]}))
    def test_failure_before_registration(self):
        with tempfile.TemporaryDirectory() as home, patch.object(install, 'run', side_effect=install.InstallError('clone failed')):
            with self.assertRaisesRegex(install.InstallError, 'Nothing was registered'):
                install.install(install.SOURCE, 'a' * 40, codex_home=home)
    def test_discovery_failure_after_registration_is_explicit(self):
        with tempfile.TemporaryDirectory() as home:
            cache = Path(home) / 'plugins/cache/ui-design-agents/ui-design-agent/local'
            shutil.copytree(ROOT / 'plugins/ui-design-agent', cache)
            def fake_run(args, env, timeout=90):
                if 'clone' in args:
                    shutil.copytree(ROOT, Path(args[-1]), ignore=shutil.ignore_patterns('.git', '__pycache__'))
                    return ''
                if 'rev-parse' in args:
                    return 'a' * 40
                if args[:3] == ['codex', 'plugin', 'list']:
                    return json.dumps({'installed': [{'name': 'ui-design-agent', 'enabled': True}]})
                return json.dumps({'installedPath': str(cache)})
            with patch.object(install, 'run', side_effect=fake_run), patch.object(install, 'discover', side_effect=install.InstallError('discovery failed')):
                with self.assertRaisesRegex(install.InstallError, 'Registration may remain'):
                    install.install(install.SOURCE, 'a' * 40, codex_home=home)
    def test_drifted_installed_cache_is_rejected(self):
        with tempfile.TemporaryDirectory() as home:
            cache = Path(home) / 'plugins/cache/ui-design-agents/ui-design-agent/local'
            shutil.copytree(ROOT / 'plugins/ui-design-agent', cache)
            (cache / 'compatibility.json').write_text('{}')
            def fake_run(args, env, timeout=90):
                if 'clone' in args:
                    shutil.copytree(ROOT, Path(args[-1]), ignore=shutil.ignore_patterns('.git', '__pycache__'))
                if 'rev-parse' in args:
                    return 'a' * 40
                if args[:3] == ['codex', 'plugin', 'list']:
                    return json.dumps({'installed': [{'name': 'ui-design-agent', 'enabled': True}]})
                return json.dumps({'installedPath': str(cache)})
            with patch.object(install, 'run', side_effect=fake_run), patch.object(install, 'discover') as discover:
                with self.assertRaises(install.InstallError):
                    install.install(install.SOURCE, 'a' * 40, codex_home=home)
                discover.assert_not_called()

if __name__ == '__main__':
    unittest.main()
