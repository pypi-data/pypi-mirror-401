# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:39:13 2023

@author: u0072088
"""

from image_aesthetic_maps.decomposition.tile_from_patch import TileFromPatch
from image_aesthetic_maps.Patch import Patch
from PIL import Image

test_image = r"C:\Users\u0072088\OneDrive - KU Leuven\Documents\3-projects\image-aesthetic-map-toolbox\image-aesethic-map-toolbox\tests\test_image.jpg"

def test_returns_list_of_patches():
    patch = Patch(40, 40, 50, 50)
    image = Image.open(test_image)
    
    patches = TileFromPatch.generate(patch, image)
    
    assert isinstance(patches, list), "Return value should be a list"
    for patch in patches:
        assert isinstance(patch, Patch), "List element is not a patch"

def test_subdivide_does_not_return_negative_patch_values():
    patch = Patch(230, 250, 150, 160)
    image = Image.open(test_image)
    
    patches = TileFromPatch.generate(patch, image)
    
    assert isinstance(patches, list), "Return value should be a list"
    for patch in patches:
        assert patch._x0 >= 0, "Value should >= 0"
        assert patch._y0 >= 0, "Value should >= 0"
        assert patch._width >= 0, "Value should >= 0"
        assert patch._height >= 0, "Value should >= 0"
    
def test_subdivide_returns_proper_subdivision_dimension_mismatch():
    """
    The test values should return the corresponding list of elements
    """
    result = TileFromPatch.subdivide(200, 50, 110)
    
    expected_result = [[0, 10], [10, 50], [60, 50], [110, 50], [160, 40]]
    
    assert len(result) == len(expected_result), "Result length does not match expected result"
    
    for idx, patch in enumerate(result):
        assert patch == expected_result[idx], "Result element " + str(patch) + " does not match expected result " + str(expected_result[idx])
        
def test_subdivide_returns_proper_subdivision_dimension_match():
    """
    The test values should return the corresponding list of elements
    """
    result = TileFromPatch.subdivide(200, 50, 100)
    
    expected_result = [[0, 50], [50, 50], [100, 50], [150, 50]]
    
    assert len(result) == len(expected_result), "Result length does not match expected result"
    
    for idx, patch in enumerate(result):
        assert patch == expected_result[idx], "Result element " + str(patch) + " does not match expected result " + str(expected_result[idx])
        
def test_patches_have_unique_grid_attributes():
    """
    The generated patches should have the _grid attribute, and each patch
    should have a unique combination of row and column indices
    """
    # Arrange
    patch = Patch(230, 250, 150, 160)
    image = Image.open(test_image)
    
    # Act
    patches = TileFromPatch.generate(patch, image)
    
    
    # Assert
    for patch in patches:
        assert hasattr(patch, '_grid'), "Patches returned from TileFromPatch have no grid attributes"

    grid_coordinates = [(patch._grid['row'], patch._grid['col']) for patch in patches]
    assert len(set(grid_coordinates)) == len(patches), "Number of unique grid coordinates does not match number of patches"