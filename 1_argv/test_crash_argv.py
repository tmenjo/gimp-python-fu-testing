# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Takashi Menjo

import tempfile
import unittest


class TestPass(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(0, 0)


if __name__ == '__main__':
    out = tempfile.TemporaryFile()
    runner = unittest.TextTestRunner(stream=out)

    gimp.message("calling unittest.main(testRunner=runner, exit=False)")

    # crash!
    unittest.main(testRunner=runner, exit=False)

    gimp.message("cannot get here!")

    out.seek(0)
    content = out.read()
    out.close()
    gimp.message(content)
