#!/usr/bin/env python3
"""
PreToolUse Hook: Blockiert git commit wenn Quality Gate fehlschlägt.
Läuft vor jedem 'git commit' — alle Stufen müssen grün sein.
"""
import sys, json, os, subprocess

try:
    d = json.load(sys.stdin)
    cmd = d.get('tool_input', {}).get('command', '')

    if not cmd.strip().startswith('git commit'):
        sys.exit(0)

    def find_root():
        p = os.getcwd()
        prev = None
        while p != prev:
            if os.path.exists(os.path.join(p, '.git')):
                return p
            prev = p
            p = os.path.dirname(p)
        return os.getcwd()

    root = find_root()
    check_sh = os.path.join(root, 'scripts', 'check.sh')
    makefile = os.path.join(root, 'Makefile')

    if os.path.exists(check_sh):
        r = subprocess.run(
            ['bash', check_sh],
            cwd=root, capture_output=True, text=True, timeout=180
        )
    elif os.path.exists(makefile):
        r = subprocess.run(
            ['make', 'check'],
            cwd=root, capture_output=True, text=True, timeout=180
        )
    else:
        sys.exit(0)  # Kein Gate-Script vorhanden — nicht blockieren

    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        print('COMMIT BLOCKIERT — Quality Gate fehlgeschlagen:\n' + out[-1200:])
        sys.exit(1)

    print('Quality Gate grün — Commit läuft.')

except Exception as e:
    print(f'COMMIT-GATE FEHLER (Hook abgestürzt): {e}')
    sys.exit(1)
