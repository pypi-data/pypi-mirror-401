import unittest
import os
import shutil
from assumeless.core.cache import FileHashCache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.test_dir = "temp_test_cache"
        os.makedirs(self.test_dir, exist_ok=True)
        self.cache = FileHashCache(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_cache_lifecycle(self):
        fpath = os.path.join(self.test_dir, "test.py")
        content = "print('hello')"
        
        # 1. New file -> Changed
        self.assertTrue(self.cache.check_changed(fpath, content))
        
        # 2. Update cache
        self.cache.update(fpath, content)
        self.cache.save()
        
        # 3. Reload
        new_cache = FileHashCache(self.test_dir)
        new_cache.load()
        
        # 4. Same content -> Not Changed
        self.assertFalse(new_cache.check_changed(fpath, content))
        
        # 5. Modified content -> Changed
        self.assertTrue(new_cache.check_changed(fpath, "print('modified')"))

if __name__ == '__main__':
    unittest.main()
