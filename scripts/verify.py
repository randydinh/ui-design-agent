#!/usr/bin/env python3
"""Offline integrity and compatibility checks; never execute package resources."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

PLUGIN = 'ui-design-agent'
INTAKE = 'temari-conversational-sme-intake/v1'
ADVISORY = 'ui-design-advisory/v1'

class VerificationError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def safe_path(root, relative):
    require(isinstance(relative, str) and relative and '\\' not in relative, 'invalid relative path')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and all(x not in ('..', '.') for x in path.parts), 'unsafe path: ' + relative)
    candidate = root.joinpath(*path.parts)
    require(not any(p.is_symlink() for p in [candidate, *candidate.parents] if p == root or root in p.parents), 'symlink: ' + relative)
    require(candidate.resolve().is_relative_to(root.resolve()), 'path escapes root')
    return candidate

def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise VerificationError('invalid or missing JSON: ' + str(path)) from exc

def inventory(root):
    result = {}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink: ' + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result

def plugin_root(path):
    path = Path(path).absolute()
    require(not path.is_symlink(), 'plugin root is symlink')
    return path / 'plugins' / PLUGIN if (path / 'plugins' / PLUGIN).is_dir() else path

def verify(path):
    root = plugin_root(path)
    actual = inventory(root)
    allowed_root = {'plugin.json', 'dependencies.lock.json', 'compatibility.json', 'license-review.json', 'package.files.json', '.codex-plugin', 'skills'}
    require({p.name for p in root.iterdir()} == allowed_root, 'unexpected plugin-root resource')
    require({p.name for p in (root / '.codex-plugin').iterdir()} == {'plugin.json'}, 'unexpected plugin configuration')
    require({p.name for p in (root / 'skills').iterdir()} == {'ui-design'}, 'unexpected top-level skill')
    for forbidden in ('hooks.json', '.mcp.json', 'mcp.json'):
        require(not (root / forbidden).exists(), 'executable integration forbidden')
    manifest = read_json(root / 'plugin.json')
    legacy = read_json(root / '.codex-plugin/plugin.json')
    require(set(manifest) == {'$schema', 'name', 'version', 'description'}, 'unexpected portable manifest fields')
    require(set(legacy) == {'name', 'version', 'description', 'skills'}, 'unexpected compatibility manifest fields')
    require(manifest['name'] == legacy['name'] == PLUGIN, 'plugin identity mismatch')
    require(manifest['version'] == legacy['version'] and re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'version mismatch')
    require(legacy['skills'] == './skills/', 'unexpected skill root')
    compatibility = read_json(root / 'compatibility.json')
    require(compatibility == {
        'schema_version': 1, 'plugin': PLUGIN, 'package_version': manifest['version'],
        'intake_contract': INTAKE, 'advisory_contract': ADVISORY,
        'entry_skill': 'skills/ui-design/SKILL.md', 'scope': 'advisory',
        'implementation_owner': 'caller-poteto-workflow', 'acceptance_owner': 'caller',
    }, 'compatibility declaration mismatch')
    lock = read_json(root / 'dependencies.lock.json')
    require(lock.get('schema_version') == 1, 'unsupported dependency schema')
    names = set()
    licenses = read_json(root / 'license-review.json')
    require(licenses.get('schema_version') == 1 and licenses.get('determination') == 'compatible-for-public-redistribution-with-retained-component-licenses', 'public redistribution determination missing')
    license_components = {component['name']: component for component in licenses.get('components', [])}
    require(len(license_components) == 3, 'incomplete license determination')
    for dep in lock['dependencies']:
        require(dep['name'] not in names, 'duplicate dependency')
        names.add(dep['name'])
        require(re.fullmatch('[0-9a-f]{40}', dep['commit']) is not None, 'unpinned dependency')
        component = license_components.get(dep['name'], {})
        require(component.get('commit') == dep['commit'] and component.get('source') == dep['repository'] and component.get('license') == dep['license'], 'license provenance mismatch')
        license_path = safe_path(root, component.get('license_file'))
        require(license_path.is_file() and hashlib.sha256(license_path.read_bytes()).hexdigest() == component.get('license_sha256'), 'license text mismatch')
        dep_root = safe_path(root, dep['installed_path'])
        require(dep_root.is_relative_to(root / 'skills/ui-design/vendor'), 'dependency outside vendor root')
        for relative, digest in dep['files'].items():
            safe_path(dep_root, relative)
            require(re.fullmatch('[0-9a-f]{64}', digest) is not None, 'invalid dependency digest')
        require(inventory(dep_root) == dep['files'], 'dependency inventory mismatch: ' + dep['name'])
    for notice in ('UPSTREAM-NOTICE.md', 'MODERN-SCREENSHOT-LICENSE', 'PLATFORM-DESIGN-SKILLS-LICENSE'):
        require((root / 'skills/ui-design/vendor/impeccable' / notice).is_file(), 'missing bundled attribution: ' + notice)
    require(names == {'interface-design', 'ui-ux-pro-max', 'impeccable'}, 'dependency set mismatch')
    require({p.name for p in (root / 'skills/ui-design/vendor').iterdir()} == names, 'unexpected vendor resource')
    expected = read_json(root / 'package.files.json')
    require(expected.get('schema_version') == 1, 'unsupported package inventory')
    for relative in expected['files']:
        safe_path(root, relative)
    actual.pop('package.files.json', None)
    require(actual == expected['files'], 'package inventory mismatch (missing, extra, or modified file)')
    skill = (root / 'skills/ui-design/SKILL.md').read_text()
    require(skill.startswith('---\nname: ui-design\n') and '\ndescription:' in skill.split('---', 2)[1], 'invalid skill metadata')
    metadata = (root / 'skills/ui-design/agents/openai.yaml').read_text()
    require('allow_implicit_invocation: true' in metadata, 'implicit invocation unavailable')
    for path in (root / 'skills/ui-design').rglob('*.md'):
        if 'vendor' in path.relative_to(root).parts:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            require(not target.startswith('/') and '..' not in PurePosixPath(target).parts, 'nonportable reference')
            require((path.parent / target.split('#')[0]).is_file(), 'broken reference: ' + target)
    return {'plugin': PLUGIN, 'version': manifest['version'], 'intake_contract': INTAKE, 'files_verified': len(actual), 'plugin_root': str(root)}

def write_inventory(path):
    root = plugin_root(path)
    files = inventory(root)
    files.pop('package.files.json', None)
    (root / 'package.files.json').write_text(json.dumps({'schema_version': 1, 'files': files}, indent=2, sort_keys=True) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.path), sort_keys=True))
    except (VerificationError, KeyError, TypeError) as exc:
        print('Verification failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
