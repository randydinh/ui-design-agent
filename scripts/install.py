#!/usr/bin/env python3
"""Install a reviewed Git revision through the Codex plugin CLI, then verify discovery."""
import argparse
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import tempfile
import threading
from urllib.parse import urlparse
from verify import VerificationError, require, verify, inventory

SOURCE = 'https://github.com/randydinh/ui-design-agent'
MARKETPLACE = 'ui-design-agents'
IDENTITY = 'ui-design-agent@' + MARKETPLACE

class InstallError(RuntimeError):
    pass

def run(args, env, timeout=90):
    try:
        # Spool output to anonymous files so noisy subprocesses cannot fill Python memory.
        with tempfile.TemporaryFile(mode='w+t') as stdout, tempfile.TemporaryFile(mode='w+t') as stderr:
            result = subprocess.run(args, env=env, text=True, stdout=stdout, stderr=stderr, timeout=timeout, check=False)
            if result.returncode:
                raise InstallError('command failed: ' + ' '.join(args[:3]) + ' (exit ' + str(result.returncode) + ')')
            require(stdout.tell() <= 8_000_000 and stderr.tell() <= 8_000_000, 'command output exceeds limit')
            stdout.seek(0)
            return stdout.read(8_000_001)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InstallError('command unavailable or timed out: ' + args[0]) from exc

def source_url(source):
    parsed = urlparse(source)
    require(parsed.scheme == 'https' and parsed.netloc == 'github.com' and not parsed.query and not parsed.fragment, 'source must be an HTTPS github.com repository URL without credentials or query')
    require(re.fullmatch(r'/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?', parsed.path) is not None, 'invalid GitHub repository URL')
    return source

def resolve_ref(source, ref, env):
    require(isinstance(ref, str) and re.fullmatch(r'[0-9a-f]{40}|v\d+\.\d+\.\d+', ref) is not None, 'use an immutable 40-character commit or exact vMAJOR.MINOR.PATCH tag; branches and HEAD are rejected')
    if re.fullmatch('[0-9a-f]{40}', ref):
        return ref
    output = run(['git', 'ls-remote', '--tags', source, 'refs/tags/' + ref, 'refs/tags/' + ref + '^{}'], env)
    found = {}
    for line in output.splitlines():
        commit, name = line.split('\t', 1)
        require(re.fullmatch('[0-9a-f]{40}', commit) is not None, 'invalid remote commit')
        found[name] = commit
    commit = found.get('refs/tags/' + ref + '^{}') or found.get('refs/tags/' + ref)
    require(commit is not None, 'version tag not found')
    return commit

def discover(codex, env, cwd, expected_skill):
    """Fresh app-server JSON-RPC session, without starting an agent/model turn."""
    process = subprocess.Popen([codex, 'app-server', '--stdio'], env=env, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
    messages = queue.Queue()
    def reader():
        for line in process.stdout:
            if len(line) > 8_000_000:
                messages.put(InstallError('app-server response exceeds size limit'))
                break
            try:
                messages.put(json.loads(line))
            except ValueError:
                messages.put(InstallError('app-server returned invalid JSON'))
                break
        messages.put(None)
    threading.Thread(target=reader, daemon=True).start()
    def send(message):
        process.stdin.write(json.dumps(message) + '\n')
        process.stdin.flush()
    def response(identifier):
        # Bound total wait even if server streams unrelated notifications.
        import time
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                item = messages.get(timeout=max(.01, deadline - time.monotonic()))
            except queue.Empty:
                break
            if item is None:
                raise InstallError('app-server stopped before discovery')
            if isinstance(item, InstallError):
                raise item
            require(isinstance(item, dict), 'app-server returned a non-object message')
            if item.get('id') == identifier:
                require('error' not in item, 'app-server discovery RPC failed')
                result = item.get('result')
                require(isinstance(result, dict), 'app-server returned a non-object result')
                return result
        raise InstallError('app-server discovery timed out')
    try:
        send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'ui-design-agent-verifier', 'version': '0.1.0'}, 'capabilities': {'experimentalApi': True}}})
        response(1)
        send({'method': 'initialized'})
        send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(cwd)], 'forceReload': True}})
        result = response(2)
        entries = result.get('data')
        require(isinstance(entries, list), 'skills/list data must be an array')
        skills = []
        for entry in entries:
            require(isinstance(entry, dict), 'skills/list entry must be an object')
            require(isinstance(entry.get('errors'), list), 'skills/list errors must be an array')
            require(not entry['errors'], 'fresh skill discovery returned errors')
            entry_skills = entry.get('skills')
            require(isinstance(entry_skills, list), 'skills/list skills must be an array')
            for skill in entry_skills:
                require(isinstance(skill, dict), 'skills/list skill must be an object')
                require(isinstance(skill.get('name'), str) and isinstance(skill.get('path'), str) and isinstance(skill.get('enabled'), bool), 'skills/list skill metadata has invalid types')
            skills.extend(entry_skills)
        matches = [s for s in skills if s.get('name') in ('ui-design', 'ui-design-agent:ui-design') and Path(s.get('path', '')).resolve() == expected_skill.resolve()]
        require(len(matches) == 1 and matches[0].get('enabled') is True, 'installed UI Design skill missing, disabled, duplicated, or path mismatch')
        return matches[0]['name']
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        if process.stdin:
            process.stdin.close()
        if process.stdout:
            process.stdout.close()

def enabled_plugin(data):
    require(isinstance(data, dict), 'plugin list must return an object')
    installed = data.get('installed')
    require(isinstance(installed, list), 'plugin list installed must be an array')
    for item in installed:
        require(isinstance(item, dict), 'plugin list entry must be an object')
        require(isinstance(item.get('name'), str) and isinstance(item.get('enabled'), bool), 'plugin list entry metadata has invalid types')
    matches = [item for item in installed if item['name'] == 'ui-design-agent' and item['enabled']]
    require(len(matches) <= 1, 'plugin list contains duplicate enabled UI Design entries')
    return matches[0] if matches else None

def install(source, ref, codex='codex', codex_home=None):
    source_url(source)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if codex_home:
        target_home = Path(codex_home).resolve()
        target_home.mkdir(parents=True, exist_ok=True)
        env['CODEX_HOME'] = str(target_home)
    else:
        target_home = Path(env.get('CODEX_HOME', str(Path.home() / '.codex'))).resolve()
    commit = resolve_ref(source, ref, env)
    registration_started = False
    try:
        with tempfile.TemporaryDirectory(prefix='ui-design-agent-inspect-') as temporary:
            checkout = Path(temporary) / 'repo'
            run(['git', '-c', 'core.hooksPath=/dev/null', 'clone', '--no-checkout', '--', source, str(checkout)], env)
            run(['git', '-C', str(checkout), '-c', 'core.hooksPath=/dev/null', 'checkout', '--detach', commit], env)
            require(run(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], env).strip() == commit, 'checkout commit mismatch')
            package = checkout / 'plugins/ui-design-agent'
            checked = verify(package)
            marketplace = json.loads((checkout / '.agents/plugins/marketplace.json').read_text())
            require(isinstance(marketplace, dict), 'marketplace must be an object')
            require(isinstance(marketplace.get('plugins'), list), 'marketplace plugins must be an array')
            require(marketplace.get('name') == MARKETPLACE and len(marketplace['plugins']) == 1, 'unexpected marketplace')
            item = marketplace['plugins'][0]
            require(isinstance(item, dict), 'marketplace entry must be an object')
            require(item.get('name') == 'ui-design-agent' and item.get('source') == {'source': 'local', 'path': './plugins/ui-design-agent'}, 'unexpected marketplace source')
            registration_started = True
            run([codex, 'plugin', 'marketplace', 'add', source, '--ref', commit, '--json'], env)
            added = json.loads(run([codex, 'plugin', 'add', IDENTITY, '--json'], env))
            require(isinstance(added, dict), 'plugin add must return an object')
            require(isinstance(added.get('installedPath'), str) and added['installedPath'], 'plugin add omitted installed path')
            listing = json.loads(run([codex, 'plugin', 'list', '--marketplace', MARKETPLACE, '--json'], env))
            enabled = enabled_plugin(listing)
            require(enabled is not None and enabled.get('pluginId', IDENTITY) == IDENTITY, 'plugin list did not confirm enabled installation')
            # The cache is host-owned; accept only the single byte-identical package.
            cache = target_home / 'plugins/cache' / MARKETPLACE / 'ui-design-agent'
            installed = Path(added['installedPath']).resolve()
            require(installed.is_relative_to(cache.resolve()), 'installed path outside expected cache')
            verify(installed)
            require(inventory(installed) == inventory(package), 'installed cache differs from the chosen Git commit')
            name = discover(codex, env, temporary, installed / 'skills/ui-design/SKILL.md')
            return {'source': source, 'commit': commit, 'version': checked['version'], 'installed_path': str(installed), 'discovered_skill': name, 'enabled': True}
    except (InstallError, VerificationError, ValueError, OSError, KeyError) as exc:
        suffix = ' Registration may remain; inspect codex plugin list before retrying. No atomic rollback is claimed.' if registration_started else ' Nothing was registered.'
        raise InstallError(str(exc) + suffix) from exc

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=SOURCE)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--codex-home', help='Separate Codex home for installation tests; default is the current user host')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.source, args.ref, args.codex, args.codex_home), sort_keys=True))
    except (InstallError, VerificationError) as exc:
        print('Installation failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
