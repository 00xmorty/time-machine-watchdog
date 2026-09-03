#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/tmutil" <<'SH'
#!/usr/bin/env bash
case "$1" in
  destinationinfo) printf 'Name : Test Backup\nKind : Local\n' ;;
  latestbackup) printf '/Volumes/Test/Backups.backupdb/Mac/2020-01-01-000000.backup\n' ;;
  status) printf 'Backup session status:\n{\n Running = 0;\n}\n' ;;
  *) exit 64 ;;
esac
SH
chmod +x "$tmp/tmutil" "$root/tmwatch"
python3 -m py_compile "$root/tmwatch"
TZ=UTC TMWATCH_TMUTIL="$tmp/tmutil" python3 "$root/tmwatch" --threshold-hours 100000 > "$tmp/ok.txt"
grep -q '^OK:' "$tmp/ok.txt"
grep -q 'read-only' "$tmp/ok.txt"
set +e
TZ=UTC TMWATCH_TMUTIL="$tmp/tmutil" python3 "$root/tmwatch" --threshold-hours 1 --json > "$tmp/stale.json"
code=$?
set -e
[ "$code" -eq 2 ]
python3 - "$tmp/stale.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
assert r["status"] == "STALE"
assert r["read_only"] is True
assert r["destination_name"] == "Test Backup"
assert r["latest_backup_utc"] == "2020-01-01T00:00:00Z"
PY
python3 "$root/tmwatch" --version | grep -q '0.1.0'
python3 "$root/tmwatch" --help | grep -q 'Time Machine destination'
echo 'PASS: syntax, fresh/stale fixtures, JSON, safety, help/version'
