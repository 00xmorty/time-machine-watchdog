# Time Machine Watchdog

A tiny, dependency-free CLI that checks whether macOS Time Machine has a configured destination and whether its latest reported backup is fresh.

## Run

Requires macOS, Python 3.9+, and the built-in `tmutil` command.

```sh
curl -LO https://github.com/00xmorty/time-machine-watchdog/releases/latest/download/tmwatch
chmod +x tmwatch
./tmwatch
```

The default stale threshold is 48 hours. Customize it or emit JSON:

```sh
./tmwatch --threshold-hours 72
./tmwatch --json
```

Destination labels can contain names or other private context. Use the share-safe
mode before pasting a report into an issue or chat:

```sh
./tmwatch --redact
./tmwatch --redact --json
```

`--redact` replaces the destination name with `[redacted]` before output. It does
not alter Time Machine or the destination itself.

Exit code is `0` when the latest reported backup is within the threshold and `2` for stale, missing-backup, missing-destination, or `UNKNOWN` states. Invalid CLI arguments also exit `2` (with an error on stderr, not a JSON report).

### v0.3.0: uncertainty is not health

Failed destination/latest-backup probes and future timestamps now report `UNKNOWN`,
not a healthy backup or a definitive missing destination. `Running = 1;` from
`tmutil status` is correctly recognized. JSON `backup_running` is now `true`,
`false`, or `null` (unknown); consumers must handle the new nullable value.
Status-probe failure alone does not invalidate independently observed freshness.
Non-finite thresholds are rejected, invalid dates do not crash, and freshness
uses exact seconds rather than the rounded display age.

## Safety

- Strictly read-only: only runs `tmutil destinationinfo`, `tmutil latestbackup`, and `tmutil status`.
- Never starts, stops, deletes, repairs, configures, mounts, or changes a backup or destination.
- No `sudo`, network requests, telemetry, persistence, or notifications.
- Destination names can be personal. Review output before sharing it, or use `--redact`.

## Limitations

- macOS only for real checks; Linux CI exercises deterministic fixture data.
- A recent timestamp is a health clue, not proof that every expected file is recoverable. Test restores separately.
- Time Machine output is not a stable API; an unknown or invalid timestamp format in successful output is reported as `NO_BACKUP` rather than guessed. This is not proof that no backup exists.
- Backup path timestamps are interpreted in the Mac's current local timezone; changing timezones can introduce a timezone-sized age offset.
- Network destination availability and free space are not independently probed.
- Redaction covers the parsed destination name; it is not a general-purpose log scrubber.
- This release does not install a LaunchAgent or send notifications. Scheduling is intentionally left to the user.

## Development

```sh
bash tests/test.sh
```

## License

MIT
