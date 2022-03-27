# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Takashi Menjo

import unittest


class TestPass(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(0, 0)


if __name__ == '__main__':
    gimp.message("calling unittest.main(argv=[__file__], exit=False)")

    # error!
    unittest.main(argv=[__file__], exit=False)

    gimp.message("cannot get here!")
