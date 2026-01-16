# grid_samp - Grid-based image sampling toolbox
# Copyright (C) 2026 Maarten Leemans, Crhrisophe Bossens, Johan Wagemans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from PIL import Image

from grid_samp import ImageRegion
from grid_samp import ImageRegionList

class RecursiveGrid:
    
    def __init__(self, image: Image.Image | ImageRegion, recursion_depth: int):
        """
        Initialize a RecursiveGrid for recursively subdividing an image or image region.

        This grid subdivides an image into progressively smaller regions according
        to the specified recursion depth. The recursion tree is stored internally,
        with each level containing a list of ImageRegion objects generated from the
        previous level.

        Parameters
        ----------
        image : PIL.Image.Image or ImageRegion
            Source image or an existing ImageRegion to be recursively subdivided.
        recursion_depth : int
            Number of recursive subdivisions to perform. Must be >= 1.

        Raises
        ------
        TypeError
            If `image` is not a PIL.Image.Image or an ImageRegion.
            If `recursion_depth` is not an integer.
        ValueError
            If `recursion_depth` is less than 1.

        Notes
        -----
        If a PIL Image is provided, the first-level ImageRegion is created
        automatically covering the entire image. For each recursion level, the
        `generate` method is used to subdivide the regions from the previous level.

        The resulting tree is stored in `self._tree`, with keys `'level_1'`,
        `'level_2'`, ..., `'level_n'` corresponding to each recursion level.

        Examples
        --------
        >>> from PIL import Image
        >>> from grid_samp.image_region import ImageRegion
        >>> from grid_samp.grids.recursive_grid import RecursiveGrid
        >>> img = Image.open("example.png")
        >>> grid = RecursiveGrid(img, recursion_depth=3)
        >>> grid._recursion_depth
        3
        >>> grid._tree['level_1']  # first-level ImageRegions
        [<ImageRegion>, <ImageRegion>, ...]
        """

        if not isinstance(image, (Image.Image, ImageRegion)):
            raise TypeError("image must be of type PIL.Image.Image or ImageRegion")
        
        if not isinstance(recursion_depth, int):
            raise TypeError("recursion_depth must be of type int")
        
        if recursion_depth < 1:
            raise ValueError("recursion_depth must be at least 1")
        
        self._recursion_depth = recursion_depth
        self._tree = {}

        if isinstance(image, ImageRegion):
            self._source_image = image
        else:
            self._source_image = ImageRegion(0, 0, image.width, image.height)
            self._source_image._grid = {'x': 0, 'y': 0, 'row': 0, 'col': 0, 'depth': 0}
            self._source_image._quadrant = 0

        self._tree['level_1'] = RecursiveGrid.generate(self._source_image)
        for recursion_index in range(2, recursion_depth + 1):
            self._tree[f'level_{recursion_index}'] = []

            for current_level_element in self._tree[f'level_{recursion_index - 1}']:
                self._tree[f'level_{recursion_index}'].extend(RecursiveGrid.generate(current_level_element))

    def get_recursion_level_images(self, recursion_level):
        image_region_list = ImageRegionList(self._tree[f'level_{recursion_level}'])
        sorted_list = sorted(image_region_list, key=lambda image_region: image_region._grid['row'])
        return sorted_list

    @staticmethod
    def generate(image_region):
        width, start_x  = RecursiveGrid.split_length(image_region._width)
        height, start_y = RecursiveGrid.split_length(image_region._height)

        quadrant_1 = ImageRegion(image_region._x0, image_region._y0, width, height)
        quadrant_2 = ImageRegion(image_region._x0 + start_x, image_region._y0, width, height)
        quadrant_3 = ImageRegion(image_region._x0, image_region._y0 + start_y, width, height)
        quadrant_4 = ImageRegion(image_region._x0 + start_x, image_region._y0 + start_y, width, height)

        quadrant_1._quadrant = 1
        quadrant_2._quadrant = 2
        quadrant_3._quadrant = 3
        quadrant_4._quadrant = 4

        src_row = -1
        src_col = -1
        src_depth = 1
        if hasattr(image_region, '_grid'):
            src_row = image_region._grid['row']
            src_col = image_region._grid['col']
            src_depth = image_region._grid['depth']

        quadrant_1._grid = {
            'x': quadrant_1._x0,
            'y': quadrant_1._y0,
            'row': 2 * max(0, src_row) + 0,
            'col': 2 * max(0, src_col) + 0,
            'depth': src_depth + 1
        }

        quadrant_2._grid = {
            'x': quadrant_2._x0,
            'y': quadrant_2._y0,
            'row': 2 * max(0, src_row) + 0,
            'col': 2 * max(0, src_col) + 1,
            'depth': src_depth + 1
        }

        quadrant_3._grid = {
            'x': quadrant_3._x0,
            'y': quadrant_3._y0,
            'row': 2 * max(0, src_row) + 1,
            'col': 2 * max(0, src_col) + 0,
            'depth': src_depth + 1
        }

        quadrant_4._grid = {
            'x': quadrant_4._x0,
            'y': quadrant_4._y0,
            'row': 2 * max(0, src_row) + 1,
            'col': 2 * max(0, src_col) + 1,
            'depth': src_depth + 1
        }

        return [quadrant_1, quadrant_2, quadrant_3, quadrant_4]

    @staticmethod
    def split_length(length):
        """
        For a dimension of 'length' pixels, calculates the width and the starting point
        of the second part when the dimension is split in two.
                
        In the case of even dimensions this works out in two equal sized
        non-overlapping parts
                
        In the case of uneven dimensions, the midlle pixel overlaps in each part.

        Parameters
        ----------
        length : INT
            Number of pixels 

        Returns
        -------
        width : TYPE
            DESCRIPTION.
        start : TYPE
            DESCRIPTION.
        """
        if length % 2 == 0:
            width = length // 2
            start_2 = width
        else:
            width = (length + 1) // 2
            start_2 = width - 1
        return width, start_2
