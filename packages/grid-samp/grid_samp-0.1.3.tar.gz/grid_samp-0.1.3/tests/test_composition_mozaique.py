# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:21:54 2023

@author: Christophe Bossens
"""

from image_aesthetic_maps.decomposition.quad_tree import QuadTree
from image_aesthetic_maps.composition.mozaique import Mozaique
from image_aesthetic_maps.Patch import Patch
from PIL import Image

import pytest

test_image = r"C:\Users\u0072088\OneDrive - KU Leuven\Documents\3-projects\image-aesthetic-map-toolbox\image-aesethic-map-toolbox\tests\test_image.jpg"

def test_mozaique_returns_image():
    """
    Generating a mozaique should return a PIL image object
    """
    # Arrange
    image = Image.open(test_image)
    root_patch = Patch.from_image(image)
    quadrants = root_patch.decompose(QuadTree)
    
    # Act
    result = Mozaique.generate(image, quadrants)
    
    # Assert
    assert isinstance(result, Image.Image), "Mozaique should generate an image"


def test_mozaique_validates_patches():
    """
    The mozaique function raises an attribute error when patches do not
    have a grid attribute
    """
    # Arrange
    no_attribute_patches = []
    attribute_patches    = []
    for row_index in range(1, 5):
        for col_index in range(1, 5):
            no_attribute_patches.append(Patch(10, 10, 20, 20))
            
            attribute_patch = Patch(10, 10, 30, 30)
            attribute_patch.set_grid_data(row_index, col_index)
            attribute_patches.append(attribute_patch)
            
    # Assert
    with pytest.raises(AttributeError):
        Mozaique.validate_patch_attributes(no_attribute_patches)
        
    assert Mozaique.validate_patch_attributes(attribute_patches) == None, "Should not raise an error"

def test_get_grid_dimensions():
    """
    The mozaique function returns the maximum column and row index for 
    a list of patches

    """
    # Arrange
    MAX_COLUMN_VALUE = 10
    MAX_ROW_VALUE    = 7
    
    patches = []
    for row_index in range(1, MAX_ROW_VALUE + 1):
        for col_index in range(1, MAX_COLUMN_VALUE + 1):
            patch = Patch(10, 10, 30, 30)
            patch.set_grid_data(row_index, col_index)
            patches.append(patch)
            
    # Act
    max_row, max_col = Mozaique.get_maximum_grid_values(patches)
    
    # Assert
    assert max_col == MAX_COLUMN_VALUE, "Maximum column value does not match expected value, %d != %d"%(max_col, MAX_COLUMN_VALUE)
    assert max_row == MAX_ROW_VALUE, "Maximum row value does not match expected value, %d != %d"%(max_row, MAX_ROW_VALUE)
    
    
def test_calculate_new_image_size():
    """
    Should return the appropriate image size
    """
    # Arrange
    original_width = 300
    original_height = 400
    
    n_rows = 5
    n_columns = 7
    
    margin = 10
    
    expected_width = original_width + ((n_columns + 1) * margin)
    expected_height = original_height + ((n_rows + 1) * margin)
    
    # Act 
    new_width, new_height = Mozaique.calculate_new_image_size(original_width, original_height, n_columns, n_rows, margin)
    
    # Assert
    assert new_width == expected_width, "New width does not match expected width: %d != %d"%(new_width, expected_width)
    assert new_height == expected_height, "New height does not match expected width: %d != %d"%(new_height, expected_height)