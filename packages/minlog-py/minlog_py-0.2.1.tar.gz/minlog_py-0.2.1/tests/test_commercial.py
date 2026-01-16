import json
import logging
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Adjust path to import MinLog
sys.path.append(str(Path(__file__).parent.parent / "src"))

import minlog.core
from minlog.core import AsyncHandler, JSONFormatter

# Save original load_config
original_load_config = minlog.core.load_config


class TestCommercialFeatures(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "async_test.log")
        minlog.core.load_config = self.mock_load_config_async

    def tearDown(self):
        minlog.core.load_config = original_load_config
        shutil.rmtree(self.test_dir)

    def mock_load_config_async(self):
        return {
            "log_dir": self.test_dir,
            "log_level": "INFO",
            "async": True,
            "enable_color": False,
            "rotation": {"max_bytes": 10000, "backup_count": 1},
        }

    def test_async_handler_performance(self):
        """Verify that AsyncHandler works and logs are written"""

        # Manually create AsyncHandler for testing to avoid setup_logging complexity with global state
        target_handler = logging.FileHandler(self.log_file)
        async_handler = AsyncHandler(target_handler)

        logger = logging.getLogger("AsyncPerfTest")
        logger.setLevel(logging.INFO)
        logger.addHandler(async_handler)

        start_time = time.time()
        for i in range(100):
            logger.info(f"Message {i}")
        duration = time.time() - start_time

        # Just ensure it runs without error and is fast
        self.assertLess(duration, 1.0)

        # Wait for flush (worker thread to process)
        time.sleep(1.5)
        async_handler.shutdown()

        # Verify file content
        with open(self.log_file, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 100)
            self.assertIn("Message 0", lines[0])

    def test_json_formatter(self):
        formatter = JSONFormatter()
        record = logging.LogRecord("test", logging.INFO, "path", 1, "Hello JSON", None, None)
        json_str = formatter.format(record)

        data = json.loads(json_str)
        self.assertEqual(data["message"], "Hello JSON")
        self.assertEqual(data["level"], "INFO")
        self.assertIn("timestamp", data)
        self.assertEqual(data["logger"], "test")


if __name__ == "__main__":
    unittest.main()
