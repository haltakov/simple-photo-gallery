import unittest
from unittest import mock
import sys
import os
import json
import simplegallery.logic.gallery_logic as gallery_logic


class SPGInitTestCase(unittest.TestCase):

    def test_get_gallery_type(self):
        link_type_mapping = [
            # OneDrive
            ('https://onedrive.live.com/?authkey=%21ABCDabcd123456789&id=12345678ABCDEFGH%12345&cid=ABCDEFGH12345678', 'onedrive'),
            ('https://1drv.ms/u/s!Abc7fg--123abcdefgHUJK-0abcdEFGH1124', 'onedrive'),
            # Google Photos
            ('https://photos.app.goo.gl/12345abcdeABCDEFG', 'google'),
            ('https://photos.google.com/share/ABCDEFGHIJabcdefg123456789_ABCDEFGHIJKLMNOPabcdefghijklmnopqr123456789?key=ABCDEFGHIJKLMNabcdefghijklmnopq123456789', 'google'),
            # Amazon
            ('https://www.amazon.de/photos/share/ABCDEFGHIJKLabcdefghijklmnopqrstuvw12345678', ''),
            # iCloud
            ('https://share.icloud.com/photos/01234567ABCDabc-abcdABCDE#Home', ''),
            # DropBox
            ('https://www.dropbox.com/sh/abcdefghi123456/ABCDEFGHIabcdefghi1234567?dl=0', ''),
            # Other
            ('https://test.com/test', ''),
        ]

        for link_type in link_type_mapping:
            self.assertEqual(link_type[1], gallery_logic.get_gallery_type(link_type[0]))


if __name__ == '__main__':
    unittest.main()