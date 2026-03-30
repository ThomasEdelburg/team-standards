#!/usr/bin/env python3
"""
Techstack Health-Check fuer Claude Code.
Prueft alle benoetigten Tools + Versionen, gibt JSON systemMessage aus.
Teamweit nutzbar: Requirements aus techstack-requirements.json.
"""
import json, os, re, subprocess, sys
from datetime import datetime
from pathlib import Path

CLAUDE_DIR = Path.home() / '.claude'
REQ_FILE = CLAUDE_DIR / 'techstack-requirements.json'
LOG_DIR = CLAUDE_DIR / 'logs'
REPORT_FILE = LOG_DIR / 'techstack-report.txt'
TIMESTAMP_FILE = LOG_DIR / 'last-techstack-check.txt'

LOG_DIR.mkdir(parents=True, exist_ok=True)


def version_gte(actual: str, required: str) -> bool:
    """True wenn actual >= required (semver-aehnlich)."""
    def to_ints(v):
        return [int(x) for x in re.findall(r'\d+', v)]
    a, r = to_ints(actual), to_ints(required)
    for i in range(max(len(a), len(r))):
        av = a[i] if i < len(a) else 0
        rv = r[i] if i < len(r) else 0
        if av > rv:
            return True
        if av < rv:
            return False
    return True


def check_tool(name: str, command: str, min_version: str, alt_commands: list = None, timeout: int = 10) -> dict:
    """Prueft ob ein Tool verfuegbar ist und die Mindestversion erfuellt.
    Probiert altCommands falls der primaere Command fehlschlaegt."""
    commands_to_try = [command] + (alt_commands or [])
    result = {'name': name, 'version': None, 'status': 'FEHLT', 'min': min_version}

    for cmd in commands_to_try:
        try:
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            output = proc.stdout + proc.stderr
            # Erste Versionsnummer extrahieren
            match = re.search(r'(\d+\.\d+(?:\.\d+)?)', output)
            if match:
                ver = match.group(1)
                result['version'] = ver
                if version_gte(ver, min_version):
                    result['status'] = 'OK'
                else:
                    result['status'] = 'VERALTET'
                return result
            elif proc.returncode == 0:
                result['status'] = 'OK'
                result['version'] = '?'
                return result
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            continue

    return result


def load_requirements() -> dict:
    """Lade Requirements aus JSON oder verwende Defaults."""
    if REQ_FILE.exists():
        with open(REQ_FILE) as f:
            return json.load(f)
    # Defaults wenn keine JSON existiert
    return {
        'tools': {
            'required': [
                {'name': 'git', 'command': 'git --version', 'minVersion': '2.40.0', 'purpose': 'Versionskontrolle'},
                {'name': 'node', 'command': 'node --version', 'minVersion': '20.0.0', 'purpose': 'Frontend Runtime'},
                {'name': 'npm', 'command': 'npm --version', 'minVersion': '10.0.0', 'purpose': 'Package Manager'},
                {'name': 'docker', 'command': 'docker --version', 'minVersion': '24.0.0', 'purpose': 'Container Runtime'},
                {'name': 'docker-compose', 'command': 'docker compose version', 'minVersion': '2.20.0', 'purpose': 'Container Orchestrierung'},
                {'name': 'dotnet', 'command': 'dotnet --version', 'minVersion': '8.0.0', 'purpose': 'Backend Runtime'},
                {'name': 'curl', 'command': 'curl --version', 'minVersion': '7.0.0', 'purpose': 'HTTP Client'},
            ],
            'recommended': [
                {'name': 'python', 'command': 'python --version', 'minVersion': '3.10.0', 'purpose': 'Scripting', 'install': 'choco install python -y'},
                {'name': 'gh', 'command': 'gh --version', 'minVersion': '2.40.0', 'purpose': 'GitHub CLI', 'install': 'choco install gh -y'},
                {'name': 'jq', 'command': 'jq --version', 'minVersion': '1.6', 'purpose': 'JSON Processing', 'install': 'choco install jq -y'},
                {'name': 'make', 'command': 'make --version', 'minVersion': '4.0', 'purpose': 'Build Tool', 'install': 'choco install make -y'},
                {'name': 'pnpm', 'command': 'pnpm --version', 'minVersion': '8.0.0', 'purpose': 'Package Manager', 'install': 'npm install -g pnpm'},
            ]
        }
    }


def main():
    reqs = load_requirements()
    report_lines = [
        '=' * 50,
        ' Techstack Health-Check',
        f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        '=' * 50,
        '',
    ]

    total = 0
    ok_count = 0
    missing_req = 0
    missing_rec = 0
    outdated = 0

    # Required
    report_lines.append('--- REQUIRED ---')
    for tool in reqs['tools']['required']:
        r = check_tool(tool['name'], tool['command'], tool['minVersion'], tool.get('altCommands'))
        total += 1
        if r['status'] == 'OK':
            ok_count += 1
            report_lines.append(f"  {r['name']:<18} {r['version']:<14} OK")
        elif r['status'] == 'VERALTET':
            outdated += 1
            report_lines.append(f"  {r['name']:<18} {r['version']:<14} VERALTET (min: {r['min']})")
        elif r['status'] == 'TIMEOUT':
            missing_req += 1
            report_lines.append(f"  {r['name']:<18} {'-':<14} TIMEOUT")
        else:
            missing_req += 1
            report_lines.append(f"  {r['name']:<18} {'-':<14} FEHLT!")

    # Recommended
    report_lines.append('')
    report_lines.append('--- RECOMMENDED ---')
    for tool in reqs['tools']['recommended']:
        r = check_tool(tool['name'], tool['command'], tool['minVersion'], tool.get('altCommands'))
        total += 1
        install = tool.get('install', '')
        if r['status'] == 'OK':
            ok_count += 1
            report_lines.append(f"  {r['name']:<18} {r['version']:<14} OK")
        elif r['status'] == 'VERALTET':
            outdated += 1
            report_lines.append(f"  {r['name']:<18} {r['version']:<14} VERALTET ({install})")
        else:
            missing_rec += 1
            report_lines.append(f"  {r['name']:<18} {'-':<14} FEHLT ({install})")

    # Zusammenfassung
    report_lines.extend([
        '',
        '--- ZUSAMMENFASSUNG ---',
        f'  Gesamt: {total} | OK: {ok_count} | Veraltet: {outdated} | Fehlt required: {missing_req} | Fehlt recommended: {missing_rec}',
    ])

    # Report schreiben
    REPORT_FILE.write_text('\n'.join(report_lines) + '\n', encoding='utf-8')

    # Timestamp
    TIMESTAMP_FILE.write_text(datetime.now().isoformat() + '\n', encoding='utf-8')

    # JSON-Ausgabe fuer Hook
    summary = f'Techstack: {ok_count}/{total} OK'
    if missing_req > 0:
        summary += f', {missing_req} required FEHLEN'
    if outdated > 0:
        summary += f', {outdated} veraltet'
    if missing_rec > 0:
        summary += f', {missing_rec} empfohlene fehlen'
    summary += '. Report: ~/.claude/logs/techstack-report.txt'

    print(json.dumps({'systemMessage': summary}))


if __name__ == '__main__':
    main()
