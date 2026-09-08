"""Synthetic timestamps; no real backup paths or logs."""
import datetime as dt
import os
import runpy
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import subprocess

M = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'tmwatch'))


class TimezoneTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, TZ='Europe/Berlin')
        self.env.start()
        time.tzset()

    def tearDown(self):
        self.env.stop()
        time.tzset()

    def report(self, stamp, now, threshold=48):
        outputs = {'destinationinfo': 'Name : Test\nKind : Local',
                   'latestbackup': stamp, 'status': 'Running = 0;'}
        def probe(command):
            return subprocess.CompletedProcess(command, 0, outputs[command], '')
        with patch.dict(M['inspect'].__globals__, tmutil=probe):
            return M['inspect'](dt.datetime.fromisoformat(now), threshold)

    def test_winter_backup_summer_now(self):
        r = self.report('2026-01-02-120000', '2026-07-02T12:00:00+02:00')
        self.assertEqual(r['latest_backup_utc'], '2026-01-02T11:00:00Z')

    def test_summer_backup_winter_now(self):
        r = self.report('2026-07-02-120000', '2026-12-02T12:00:00+01:00')
        self.assertEqual(r['latest_backup_utc'], '2026-07-02T10:00:00Z')

    def test_spring_transition_elapsed_hours(self):
        r = self.report('2026-03-28-120000', '2026-03-29T12:00:00+02:00', 23)
        self.assertEqual(r['age_hours'], 23.0)
        self.assertEqual(r['status'], 'OK')

    def test_ambiguous_fall_time_unknown(self):
        r = self.report('2026-10-25-023000', '2026-10-25T06:00:00+01:00')
        self.assertEqual(r['status'], 'UNKNOWN')
        self.assertIsNone(r['age_hours'])

    def test_nonexistent_spring_time_unknown(self):
        r = self.report('2026-03-29-023000', '2026-03-29T06:00:00+02:00')
        self.assertEqual(r['status'], 'UNKNOWN')
        self.assertIsNone(r['latest_backup_utc'])


if __name__ == '__main__':
    unittest.main()
