#!/usr/bin/env python3
"""
SessionStart Hook: Laedt Memory-Files tiered + prueft ob Selftest/Techstack-Check faellig.
Immer: standards.md + workflow.md + checklists.md
Projekt-spezifisch: scannt ~/.claude/memory/projects/*.md dynamisch
"""
import sys, json, os, datetime, glob, re, subprocess
from pathlib import Path

memory_dir = Path.home() / '.claude' / 'memory'
log_dir = Path.home() / '.claude' / 'logs'
scripts_dir = Path.home() / '.claude' / 'scripts'
log_dir.mkdir(parents=True, exist_ok=True)

# --- Settings validieren ---
settings_file = Path.home() / '.claude' / 'settings.json'
try:
    with open(settings_file) as f:
        settings = json.load(f)
    required_keys = ['permissions', 'hooks']
    missing_keys = [k for k in required_keys if k not in settings]
    if missing_keys:
        backup = settings_file.with_suffix('.json.backup')
        if backup.exists():
            with open(backup) as f:
                restored = json.load(f)
            with open(settings_file, 'w') as f:
                json.dump(restored, f, indent=2)
except Exception:
    pass

# --- Memory Files laden ---
files = [
    memory_dir / 'standards.md',
    memory_dir / 'workflow.md',
    memory_dir / 'checklists.md',
]

# Dynamische Projekt-Erkennung
cwd = os.getcwd()
projects_dir = memory_dir / 'projects'
if projects_dir.is_dir():
    for mem_file in sorted(projects_dir.glob('*.md')):
        try:
            content_fm = mem_file.read_text(encoding='utf-8')[:512]
            match = re.search(r'^project_path:\s*(.+)$', content_fm, re.MULTILINE)
            if match:
                project_path = match.group(1).strip()
                if cwd.startswith(project_path):
                    files.append(mem_file)
                    break
        except Exception:
            pass

content = ''
for f in files:
    if f.exists():
        try:
            content += f.read_text(encoding='utf-8') + '\n'
        except Exception:
            pass

# --- Techstack-Check Faelligkeit (woechtentlich) ---
techstack_ts_file = log_dir / 'last-techstack-check.txt'
techstack_due = True

if techstack_ts_file.exists():
    try:
        last = datetime.datetime.fromisoformat(techstack_ts_file.read_text().strip())
        days_since = (datetime.datetime.now() - last).days
        if days_since < 7:
            techstack_due = False
    except Exception:
        pass

if techstack_due:
    # Techstack-Check ausfuehren
    check_script = scripts_dir / 'techstack-check.py'
    if check_script.exists():
        try:
            # Verwende den gleichen Python-Interpreter der dieses Script ausfuehrt
            result = subprocess.run(
                [sys.executable, str(check_script)],
                capture_output=True, text=True, timeout=60
            )
            if result.stdout.strip():
                try:
                    check_result = json.loads(result.stdout.strip())
                    msg = check_result.get('systemMessage', '')
                    if msg:
                        content += f'\nTECHSTACK-CHECK: {msg}\n'
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            content += f'\nTECHSTACK-CHECK FEHLER: {e}\n'

# --- Ausgabe ---
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': content
    }
}))
