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

class FixedGrid:
    
    N_ROWS = 2
    N_COLS = 2
    STRICT_DIMENSIONS = True
    
    def __init__(self, image: Image.Image, n_rows: int = 2, n_cols: int = 2, strict_dimensions: bool = False):
        """
        Initialize a FixedGrid for partitioning an image into a regular grid.

        This class divides an input image into a fixed number of rows and
        columns, producing a set of equally sized image regions. The grid
        can optionally enforce strict divisibility of the image dimensions.

        Parameters
        ----------
        image : PIL.Image.Image
            Input image to be partitioned into a fixed grid.
        n_rows : int, optional
            Number of rows in the grid. Must be a positive integer.
            The default is 2.
        n_cols : int, optional
            Number of columns in the grid. Must be a positive integer.
            The default is 2.
        strict_dimensions : bool, optional
            If True, the image width and height must be exactly divisible
            by the number of columns and rows, respectively. If False,
            image regions may have slightly varying dimensions to account
            for remainder pixels. The default is False.

        Raises
        ------
        ValueError
            If `n_rows` or `n_cols` is not a positive integer.
        ValueError
            If `strict_dimensions` is True and the image dimensions are not
            divisible by the specified number of rows and columns.

        Notes
        -----
        The computed image regions are stored internally and can be accessed
        through the grid's image region interface. The grid is immutable
        after creation.

        Examples
        --------
        >>> from PIL import Image
        >>> from grid_samp.grids.fixed_grid import FixedGrid
        >>> img = Image.open("image.png")
        >>> grid = FixedGrid(img, n_rows=4, n_cols=4)
        """
        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of PIL.Image.Image")
        
        if not all(isinstance(variable, int) for variable in (n_rows, n_cols)):
            raise TypeError("n_rows and n_cols must be integers")

        if n_rows <= 0 or n_cols <= 0:
            raise ValueError("n_rows and n_cols must be positive integers")
        
        if not isinstance(strict_dimensions, bool):
            raise TypeError("strict_dimensions must be a boolean value")

        FixedGrid.validate_dimensions(image, n_rows, n_cols, strict_dimensions)
        
        self._image = image
        self._n_rows = n_rows
        self._n_cols = n_cols
        
        self._image_regions = FixedGrid.calculate_image_region_coordinates(image, n_rows, n_cols)
        
    
    @property
    def image_regions(self):
        sorted_list = sorted(self._image_regions, key = lambda image_region : image_region._grid['row'])
        return ImageRegionList(sorted_list)
    
    def get_image_region(self, region_index):
        assert region_index < len(self._image_regions), "Region index out of bounds"
        
        return self._image_regions[region_index]
    

    @staticmethod
    def generate(image, n_cols = None, n_rows = None):
        """
        Provides an Image_Region object by decomposing the image in Image_Region
        using the idea of subdivision (the image is divided in HORIZONTAL_PARTS
        along the horizontal dimension and VERTICAL_PARTS along the vertical
        dimension)

        Parameters
        ----------
        image : PIL Image
            PIL Image Object
        n_cols : int
            The number of columns in the image grid
        n_rows : int
            The number of rows in the image grid. Defaults to

        Returns
        -------
        Image_Region collection.

        """
        
        FixedGrid.validate_dimensions(image, n_rows, n_cols)
        
        image_regions = FixedGrid.calculate_image_region_coordinates(image, n_rows, n_cols)
        
        return ImageRegionList(image_regions)

        
    @staticmethod
    def validate_dimensions(image, target_rows, target_columns, strict_dimensions = True):
        """
        Checks if the dimensions of the image are consistent with the 
        HORIZONTAL_PARTS and VERTICAL_PARTS of the Fixed_Grid class

        Parameters
        ----------
        image : PIL Image
            The image for which to check the dimensions.

        Returns
        -------
        None.

        """
        if strict_dimensions:
            assert image.width % target_rows == 0, "Image width needs to be a multiple of %d (currently %d)"%(target_rows, image.width)
            assert image.height % target_columns == 0, "Image height needs to be a multiple of %d (currently %d)"%(target_columns, image.height)
            
        
    @staticmethod
    def calculate_image_region_coordinates(image, n_rows, n_cols):
        """
        Calculates the top left locations and the dimensions for each Image_Region
        when it is split in the configured number of HORIZONTAL_PARTS and 
        VERTICAL_PARTS

        Parameters
        ----------
        image : PIL Image
            A PIL Image object.

        Returns
        -------
        A list with dictionaries with Image_Region data (x, y, width and height)

        """
        # Calculate the Image_Region width and height based on the required number of subdivions
        target_width = image.width//n_cols
        target_height = image.height//n_rows
        
        image_regions = []
        for x in range(n_cols):
            for y in range(n_rows):
                # Calculate the top left corner position of the Image_Region
                x_0 = x * target_width
                y_0 = y * target_height
                
                # Calculate the actual Image_Region width and height, constrained by the actual image size
                region_width = image.width - x_0 if x_0 + target_width > image.width else target_width
                region_height = image.height - y_0 if y_0 + target_height > image.height else target_height
                
                # Create new Image_Region
                image_region = ImageRegion(x_0, y_0, region_width, region_height)
                
                image_region._grid = {
                    "row": y,
                    "col": x,
                    "x": x_0,
                    "y": y_0
                }

                image_regions.append(image_region)
                
                
        return image_regions