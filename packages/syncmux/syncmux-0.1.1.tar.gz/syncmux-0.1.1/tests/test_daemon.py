"""
Basic tests for syncmux daemon
"""

import unittest
from pathlib import Path
from syncmux.daemon import SyncHandler


class TestSyncHandler(unittest.TestCase):
    def test_should_sync_skips_git(self):
        config = {'debounce_time': 2.0, 'batch_threshold': 5}
        handler = SyncHandler(
            Path.home(), 
            "localhost", 
            "/tmp", 
            "/tmp/control",
            config
        )
        
        git_file = Path.home() / ".git" / "config"
        self.assertFalse(handler.should_sync(git_file))


if __name__ == '__main__':
    unittest.main()
