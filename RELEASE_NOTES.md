# v0.3.1

- Fix historical daylight-saving offsets when interpreting backup path timestamps.
- Calculate freshness correctly across seasonal clock transitions.
- Report ambiguous/nonexistent local timestamps as UNKNOWN with null age and UTC timestamp.
- Add five deterministic Europe/Berlin regressions; 17 unit tests total plus CLI smoke tests.
- No new dependencies, probes, JSON fields, system changes, or telemetry.
- Original backup timezone cannot be recovered from an offset-free path; timezone changes remain a limitation.

# v0.3.0

- Correctly parse tmutil's Running = 1; assignment syntax.
- Report failed required probes and future backup timestamps as UNKNOWN.
- JSON compatibility note: backup_running can now be null when unknown.
- Reject non-finite thresholds; compare exact age before display rounding.
- Handle invalid dates and process launch permission errors without tracebacks.
- Add 12 regression tests alongside existing CLI smoke tests.
- Remains strictly read-only; no scheduling, notification, or backup changes.

# v0.2.0

- Adds `--redact` for share-safer text and JSON reports.
- Replaces a parsed Time Machine destination label with `[redacted]` before output.
- Adds deterministic tests proving the original destination name does not leak in redacted output.
- Remains strictly read-only: no backup, destination, schedule, or notification changes.

# v0.1.0

Initial public release.

- Read-only Time Machine destination, latest-backup, and current-status inspection.
- Configurable freshness threshold with automation-friendly exit codes.
- Human-readable and JSON output.
- No backup mutation, sudo, network, telemetry, persistence, or notifications.

Time Machine Watchdog reports a health clue, not restore-integrity proof. Test real restores separately.
