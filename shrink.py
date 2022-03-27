# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Takashi Menjo

from gimpfu import *


def half(length):
    return length / 2


def shrink(image, drawable):
    new_width = half(image.width)
    new_height = half(image.height)
    pdb.gimp_image_undo_group_start(image)
    pdb.gimp_context_push()
    try:
        pdb.gimp_context_set_interpolation(INTERPOLATION_CUBIC)
        pdb.gimp_image_scale(image, new_width, new_height)
    finally:
        pdb.gimp_context_pop()
        pdb.gimp_image_undo_group_end(image)


if __name__ == '__main__':
    register(shrink.__name__,
             "TODO MENU LABEL",
             "TODO DESCRIPTION",
             "Takashi Menjo",
             "Copyright (c) 2022 Takashi Menjo",
             "Mar 27, 2022",
             "<Image>/Python-Fu/{:s}".format(shrink.__name__),
             "*",
             [],
             [],
             shrink)
    main()
