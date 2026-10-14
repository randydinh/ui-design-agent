#!/usr/bin/env python3
"""Verify a release through the real Git URL installer and validate its evidence.

Only full commit hashes are accepted: tags can move. By default installation uses
a temporary Codex home, removed on exit; its reported paths are historical evidence.
Pass --codex-home to retain an isolated installation for subsequent inspection.
This checks installation and fresh skill discovery, not model behavior.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import tempfile

import install
from verify import VerificationError, require


def validate_evidence(evidence, source, ref, codex_home):
    """Fail closed on incomplete, mismatched, or non-discovery installer results."""
    require(isinstance(evidence, dict), 'installer evidence must be an object')
    fields = {'source', 'commit', 'version', 'installed_path', 'discovered_skill', 'enabled'}
    require(set(evidence) == fields, 'unexpected installer evidence fields')
    require(evidence['source'] == source, 'installer source mismatch')
    require(evidence['commit'] == ref, 'installer commit mismatch')
    require(isinstance(evidence['version'], str) and
            re.fullmatch(r'\d+\.\d+\.\d+', evidence['version']) is not None,
            'invalid installed version')
    require(evidence['enabled'] is True, 'installed plugin is not enabled')
    require(evidence['discovered_skill'] in ('ui-design', 'ui-design-agent:ui-design'),
            'installed UI Design skill was not discovered')
    path = evidence['installed_path']
    require(isinstance(path, str) and bool(path) and '\x00' not in path,
            'invalid installed path')
    require(Path(path).is_absolute(), 'installed path must be absolute')
    cache = (Path(codex_home) / 'plugins/cache' / install.MARKETPLACE /
             'ui-design-agent').resolve()
    installed = Path(path).resolve()
    require(installed != cache and installed.is_relative_to(cache),
            'installed path outside expected cache')
    return dict(evidence, plugin_id=install.IDENTITY)


def release_check(source, ref, codex='codex', codex_home=None):
    install.source_url(source)
    require(isinstance(ref, str) and re.fullmatch(r'[0-9a-f]{40}', ref) is not None,
            'release verification requires an immutable 40-character commit hash')
    if codex_home is None:
        with tempfile.TemporaryDirectory(prefix='ui-design-release-') as home:
            return release_check(source, ref, codex, home)
    home = Path(codex_home).resolve()
    evidence = install.install(source, ref, codex=codex, codex_home=str(home))
    return validate_evidence(evidence, source, ref, home)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, help='Explicit HTTPS GitHub repository URL')
    parser.add_argument('--ref', required=True, help='Full immutable commit hash')
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--codex-home', help='Isolated Codex home to retain; default: temporary home')
    args = parser.parse_args(argv)
    try:
        evidence = release_check(args.source, args.ref, args.codex, args.codex_home)
        print(json.dumps(evidence, sort_keys=True))
    except (install.InstallError, VerificationError, OSError, ValueError) as exc:
        print('Release verification failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
