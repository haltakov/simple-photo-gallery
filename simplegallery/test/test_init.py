import unittest
import sys
import os
from testfixtures import TempDirectory
import simplegallery.gallery_init as gallery_init


class SPGInitTestCase(unittest.TestCase):
    def test_nonexisting_gallery_path(self):
        with TempDirectory() as tmp_dir:
            with self.assertRaises(SystemExit) as cm:
                sys.argv=['gallery_init', '-p', os.path.join(tmp_dir.path, 'aaaa')]
                gallery_init.main()

            self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
