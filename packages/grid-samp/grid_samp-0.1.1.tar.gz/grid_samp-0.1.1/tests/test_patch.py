# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:21:54 2023

@author: u0072088
"""

from image_aesthetic_maps.Patch import Patch
from PIL import Image

test_image = r"C:\Users\u0072088\OneDrive - KU Leuven\Documents\3-projects\image-aesthetic-map-toolbox\image-aesethic-map-toolbox\tests\test_image.jpg"

def test_patch_get_center():
    """
    The function should return the center coordinate of a patch
    """
    # Arrange
    even_dimensions   = Patch(0, 0, 100, 100)
    uneven_dimensions = Patch(0, 0, 101, 101) 
    
    # Act
    patch_center_1 = even_dimensions.get_center()
    patch_center_2 = uneven_dimensions.get_center()
    
    # Assert
    assert patch_center_1[0] == 50 and patch_center_1[1] == 50, "Does not return the correct center for even dimensions"
    assert patch_center_2[0] == 50 and patch_center_1[1] == 50, "Does not return the correct center for uneven dimensions"
    

def test_patch_scale():
    """
    The function should return a new patch by scaling the width and height
    according to the scale factor

    """
    # Arrange
    root_patch = Patch(40, 40, 30, 30)
    
    # Act
    new_patch = root_patch.scale(2)
    
    # Assert
    assert isinstance(new_patch, Patch), "scale() should return a Patch object"
    assert new_patch._width == 60, "Scale should change the width of the new patch"
    assert new_patch._height == 60, "Scale should change the height of the new patch"
    assert new_patch.get_center() == root_patch.get_center(), "Old and new patch should have same center"
    
def test_patch_extract_from_image():
    """
    The function should return an image region from an image.
    

    """
    # Arrange
    root_patch = Patch(40, 40, 30, 30)
    boundary_patch = Patch(-20, -20, 50, 50)
    image = Image.open(test_image)
    
    # Act
    image_patch_1 = root_patch.extract_from_image(image)
    image_patch_2 = boundary_patch.extract_from_image(image)
    
    # Assert
    assert isinstance(image_patch_1, Image.Image), "extract_from_image() should return an Image"
    assert image_patch_1.size == (30, 30), "image size should be equal to patch size"
    assert image_patch_2.size != (50, 50), "Image size should not be equal to patch size"
    
def test_patch_set_grid_data():
    """
    The function should add a _grid attribute to the patch. 
    
    The _grid attribute is a dictionary with a 'col' and 'row' key
    """
    # Arrange 
    patch = Patch(0, 0, 10, 10)
    
    # Act
    patch.set_grid_data(3, 3)
    
    # Assert
    assert hasattr(patch, '_grid'), "The patch does not have a grid attribute"
    assert 'col' in patch._grid, "The _grid dictionary does not have a 'col' property"
    assert 'row' in patch._grid, "The _grid dictionary does not have a 'row' property"
    