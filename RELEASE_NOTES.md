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
