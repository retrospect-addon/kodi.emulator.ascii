# SPDX-License-Identifier: GPL-3.0
import os
import unittest

import xbmcvfs


class TestXbmcVfs(unittest.TestCase):

    def test_file(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'test.txt')

        # Create folder
        self.assertTrue(xbmcvfs.mkdirs(os.path.dirname(filename)))

        # Remove the file
        xbmcvfs.delete(filename)
        self.assertFalse(xbmcvfs.exists(filename))

        # Now we write to it
        f = xbmcvfs.File(filename, 'w')
        self.assertTrue(f.write(u'1234'))
        self.assertTrue(f.write('5678'))
        self.assertTrue(f.write(b'90'))
        f.close()
        self.assertTrue(xbmcvfs.exists(filename))

        # Now we want to read it
        with xbmcvfs.File(filename) as f:
            # Check filesize
            self.assertEqual(f.size(), 10)

            # Check full file
            self.assertEqual(f.read(), '1234567890')

            # Read parts of file
            self.assertEqual(f.seek(4), 4)
            self.assertEqual(f.seek(0), 0)
            self.assertEqual(f.read(4), '1234')
            self.assertEqual(f.readBytes(4), b'5678')
            self.assertEqual(f.tell(), 8)

    def test_dir(self):
        dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # add-on root

        (dirs, files) = xbmcvfs.listdir(dirname)
        self.assertTrue('sakee' in dirs)
        self.assertTrue('xbmcvfs.py' in files)
        self.assertTrue('.gitignore' in files)

    def test_stat(self):
        filename = __file__

        s = xbmcvfs.Stat(filename)
        self.assertIsNotNone(s.st_dev())
        self.assertIsNotNone(s.st_gid())
        self.assertIsNotNone(s.st_ino())
        self.assertIsNotNone(s.st_uid())
        self.assertIsNotNone(s.st_atime())
        self.assertIsNotNone(s.st_ctime())
        self.assertIsNotNone(s.st_mode())
        self.assertIsNotNone(s.st_mtime())
        self.assertIsNotNone(s.st_nlink())
        self.assertIsNotNone(s.st_size())
