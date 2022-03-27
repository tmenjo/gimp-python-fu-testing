# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Takashi Menjo

import tempfile
import unittest

from gimpfu import *

from shrink import *


class TestShrink(unittest.TestCase):
    def test_shrink_rgb_fhd(self):
        # create a new image
        image =  pdb.gimp_image_new(1920, 1080, RGB)
        self.assertIsNotNone(image)
        try:
            self.assertEqual(1920, image.width)
            self.assertEqual(1080, image.height)
            self.assertEqual(RGB, pdb.gimp_image_base_type(image))

            # no layer nor channel yet
            self.assertEqual(0, pdb.gimp_image_get_layers(image)[0])
            self.assertEqual(0, pdb.gimp_image_get_channels(image)[0])
            self.assertIsNone(pdb.gimp_image_get_active_layer(image))

            # create a new layer
            layer = pdb.gimp_layer_new(image,
                                       image.width,
                                       image.height,
                                       RGB_IMAGE,
                                       "RGB-FHD",
                                       100.0,
                                       LAYER_MODE_NORMAL)
            self.assertIsNotNone(layer)
            self.assertEqual(image.width, layer.width)
            self.assertEqual(image.height, layer.height)
            self.assertEqual(RGB_IMAGE, layer.type)
            self.assertEqual("RGB-FHD", layer.name)
            self.assertEqual(100.0, layer.opacity)
            self.assertEqual(LAYER_MODE_NORMAL, layer.mode)
            self.assertTrue(pdb.gimp_item_is_layer(layer))
            self.assertTrue(pdb.gimp_item_is_drawable(layer))

            # insert the layer to the image
            pdb.gimp_image_insert_layer(image, layer, None, -1)
            self.assertEqual(1, pdb.gimp_image_get_layers(image)[0])
            self.assertIsNotNone(pdb.gimp_image_get_active_layer(image))

            # call my Python-fu function!
            shrink(image, layer)

            # after that the image and the layer should be ...
            self.assertEqual(960, image.width)
            self.assertEqual(540, image.height)
            self.assertEqual(RGB, pdb.gimp_image_base_type(image))
            self.assertEqual(image.width, layer.width)
            self.assertEqual(image.height, layer.height)
            self.assertEqual(RGB_IMAGE, layer.type)
            self.assertEqual("RGB-FHD", layer.name)
            self.assertEqual(100.0, layer.opacity)
            self.assertEqual(LAYER_MODE_NORMAL, layer.mode)

        finally:
            pdb.gimp_image_delete(image)

    def test_shrink_gray_4k(self):
        # create a new image
        image =  pdb.gimp_image_new(4000, 2000, GRAY)
        self.assertIsNotNone(image)
        try:
            self.assertEqual(4000, image.width)
            self.assertEqual(2000, image.height)
            self.assertEqual(GRAY, pdb.gimp_image_base_type(image))

            # no layer nor channel yet
            self.assertEqual(0, pdb.gimp_image_get_layers(image)[0])
            self.assertEqual(0, pdb.gimp_image_get_channels(image)[0])
            self.assertIsNone(pdb.gimp_image_get_active_layer(image))

            # create a new layer
            layer = pdb.gimp_layer_new(image,
                                       image.width,
                                       image.height,
                                       GRAY_IMAGE,
                                       "GRAY-4K",
                                       100.0,
                                       LAYER_MODE_NORMAL)
            self.assertIsNotNone(layer)
            self.assertEqual(image.width, layer.width)
            self.assertEqual(image.height, layer.height)
            self.assertEqual(GRAY_IMAGE, layer.type)
            self.assertEqual("GRAY-4K", layer.name)
            self.assertEqual(100.0, layer.opacity)
            self.assertEqual(LAYER_MODE_NORMAL, layer.mode)
            self.assertTrue(pdb.gimp_item_is_layer(layer))
            self.assertTrue(pdb.gimp_item_is_drawable(layer))

            # insert the layer to the image
            pdb.gimp_image_insert_layer(image, layer, None, -1)
            self.assertEqual(1, pdb.gimp_image_get_layers(image)[0])
            self.assertIsNotNone(pdb.gimp_image_get_active_layer(image))

            # call my Python-fu function!
            shrink(image, layer)

            # after that the image and the layer should be ...
            self.assertEqual(2000, image.width)
            self.assertEqual(1000, image.height)
            self.assertEqual(GRAY, pdb.gimp_image_base_type(image))
            self.assertEqual(image.width, layer.width)
            self.assertEqual(image.height, layer.height)
            self.assertEqual(GRAY_IMAGE, layer.type)
            self.assertEqual("GRAY-4K", layer.name)
            self.assertEqual(100.0, layer.opacity)
            self.assertEqual(LAYER_MODE_NORMAL, layer.mode)

        finally:
            pdb.gimp_image_delete(image)


class TestHalf(unittest.TestCase):
    def test_half_even(self):
        self.assertEqual(0, half(0))
        self.assertEqual(1, half(2))
        self.assertEqual(2, half(4))
        self.assertEqual(540, half(1080))
        self.assertEqual(960, half(1920))
        self.assertEqual(1000, half(2000))
        self.assertEqual(2000, half(4000))

    def test_half_odd(self):
        self.assertEqual(0, half(1))
        self.assertEqual(1, half(3))
        self.assertEqual(2, half(5))


if __name__ == '__main__':
    content = None
    with tempfile.TemporaryFile() as out:
        runner = unittest.TextTestRunner(stream=out)
        unittest.main(argv=[__file__], testRunner=runner, exit=False)
        out.seek(0)
        content = out.read()
    gimp.message(content)
