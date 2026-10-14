"""Offline contract tests using mocked installation; these are not live proof."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install
import release_check
from verify import VerificationError


class ReleaseCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name).resolve()
        self.source = 'https://github.com/example/ui-design-agent'
        self.ref = 'a' * 40
        self.evidence = {
            'source': self.source, 'commit': self.ref, 'version': '0.1.0',
            'installed_path': str(self.home / 'plugins/cache/ui-design-agents/ui-design-agent/revision'),
            'discovered_skill': 'ui-design-agent:ui-design', 'enabled': True,
        }

    def test_success_preserves_identity_and_discovery_evidence(self):
        with patch.object(install, 'install', return_value=self.evidence) as installer:
            result = release_check.release_check(self.source, self.ref, 'custom-codex', self.home)
        installer.assert_called_once_with(self.source, self.ref, codex='custom-codex', codex_home=str(self.home))
        self.assertEqual(result, dict(self.evidence, plugin_id=install.IDENTITY))
        self.assertNotIn('plugin_id', self.evidence)

    def test_default_home_is_temporary_and_cleaned(self):
        homes = []
        def fake_install(source, ref, codex, codex_home):
            home = Path(codex_home)
            self.assertTrue(home.is_dir())
            homes.append(home)
            return dict(self.evidence, installed_path=str(home / 'plugins/cache/ui-design-agents/ui-design-agent/revision'))
        with patch.object(install, 'install', side_effect=fake_install):
            release_check.release_check(self.source, self.ref)
        self.assertEqual(len(homes), 1)
        self.assertFalse(homes[0].exists())

    def test_invalid_inputs_never_install(self):
        cases = [(self.source, ref) for ref in ('main', 'HEAD', 'v1.2.3', 'a' * 39, None)]
        cases += [(source, self.ref) for source in ('http://github.com/o/r', '/local', 'https://github.com/o/r?token=x')]
        for source, ref in cases:
            with self.subTest(source=source, ref=ref), patch.object(install, 'install') as installer:
                with self.assertRaises(VerificationError):
                    release_check.release_check(source, ref, codex_home=self.home)
                installer.assert_not_called()

    def test_malformed_and_non_discovery_evidence(self):
        cases = [None, [], 'not JSON', {}, dict(self.evidence, extra=True)]
        for field in self.evidence:
            cases.append({key: value for key, value in self.evidence.items() if key != field})
        for field, values in {
            'source': [None, 'https://github.com/other/repo'],
            'commit': [None, 'b' * 40], 'version': [None, 1, 'latest'],
            'enabled': [False, 'true', 1, None],
            'discovered_skill': [None, '', [], 'other-skill'],
            'installed_path': [None, [], '', 'relative/path', '/outside/cache', '\x00',
                               str(self.home / 'plugins/cache/ui-design-agents/ui-design-agent')],
        }.items():
            cases.extend(dict(self.evidence, **{field: value}) for value in values)
        for evidence in cases:
            with self.subTest(evidence=evidence), patch.object(install, 'install', return_value=evidence):
                with self.assertRaises(VerificationError):
                    release_check.release_check(self.source, self.ref, codex_home=self.home)

    def test_cli_success_outputs_json(self):
        with patch.object(install, 'install', return_value=self.evidence), contextlib.redirect_stdout(io.StringIO()) as output:
            status = release_check.main(['--source', self.source, '--ref', self.ref, '--codex-home', str(self.home)])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue()), dict(self.evidence, plugin_id=install.IDENTITY))

    def test_cli_errors_never_emit_success_evidence(self):
        for error in (install.InstallError('discovery failed'), VerificationError('invalid evidence'), OSError('unavailable')):
            with self.subTest(error=error), patch.object(install, 'install', side_effect=error), contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()) as errors:
                status = release_check.main(['--source', self.source, '--ref', self.ref, '--codex-home', str(self.home)])
            self.assertEqual(status, 1)
            self.assertEqual(output.getvalue(), '')
            self.assertIn('Release verification failed:', errors.getvalue())

    def test_cli_requires_explicit_source_and_ref(self):
        for args in ([], ['--ref', self.ref], ['--source', self.source]):
            with self.subTest(args=args), patch.object(install, 'install') as installer, contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    release_check.main(args)
                self.assertEqual(raised.exception.code, 2)
                installer.assert_not_called()


if __name__ == '__main__':
    unittest.main()
