import datetime as dt
import os
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'tmwatch'
M = runpy.run_path(str(SCRIPT))
NOW = dt.datetime(2026, 1, 3, tzinfo=dt.timezone.utc)


class HealthTests(unittest.TestCase):
    def report(self, stamp='2026-01-02-000000', running='Running = 1;', fail=None, destination='Name : Test Backup\nKind : Local'):
        outputs = {'destinationinfo': destination, 'latestbackup': '/Volumes/Test/' + stamp + '.backup', 'status': running}
        def probe(command):
            return subprocess.CompletedProcess(command, 1 if command == fail else 0, outputs[command], '')
        with patch.dict(M['inspect'].__globals__, tmutil=probe):
            return M['inspect'](NOW, 48)

    def test_active_assignment(self):
        self.assertIs(self.report()['backup_running'], True)

    def test_inactive_assignment(self):
        self.assertIs(self.report(running='Running = 0;')['backup_running'], False)

    def test_colon_format(self):
        self.assertIs(self.report(running='Running : 1')['backup_running'], True)

    def test_status_unknown(self):
        for kwargs in ({'fail': 'status'}, {'running': 'unrecognized'}):
            self.assertIsNone(self.report(**kwargs)['backup_running'])

    def test_required_probe_failure(self):
        for command in ('destinationinfo', 'latestbackup'):
            self.assertEqual(self.report(fail=command)['status'], 'UNKNOWN')

    def test_future_not_healthy(self):
        self.assertEqual(self.report(stamp='2099-01-01-000000')['status'], 'UNKNOWN')

    def test_invalid_date_no_crash(self):
        self.assertEqual(self.report(stamp='2026-99-99-000000')['status'], 'NO_BACKUP')

    def test_unrecognized_date(self):
        self.assertEqual(self.report(stamp='unknown')['status'], 'NO_BACKUP')

    def test_no_destination(self):
        self.assertEqual(self.report(destination='')['status'], 'NO_DESTINATION')

    def test_exact_threshold(self):
        self.assertEqual(self.report(stamp='2026-01-01-000000')['status'], 'OK')
        self.assertEqual(self.report(stamp='2025-12-31-235959')['status'], 'STALE')

    def test_invalid_thresholds_rejected_before_probe(self):
        for value in ('nan', 'inf', '-inf', '0', '-1'):
            p = subprocess.run([sys.executable, str(SCRIPT), '--threshold-hours=' + value], capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)
            self.assertIn('finite and greater than zero', p.stderr)

    def test_probe_errors_are_contained(self):
        with patch('subprocess.run', side_effect=PermissionError('denied')):
            self.assertEqual(M['tmutil']('status').returncode, 127)


if __name__ == '__main__':
    unittest.main()
