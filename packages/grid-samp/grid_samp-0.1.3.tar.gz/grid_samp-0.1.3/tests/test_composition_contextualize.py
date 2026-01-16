# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:21:54 2023

@author: u0072088
"""

from image_aesthetic_maps.decomposition.quad_tree import QuadTree
from image_aesthetic_maps.composition.contextualize import Contextualize
from image_aesthetic_maps.Patch import Patch
from PIL import Image

import pytest

test_image = r"C:\Users\u0072088\OneDrive - KU Leuven\Documents\3-projects\image-aesthetic-map-toolbox\image-aesethic-map-toolbox\tests\test_image.jpg"

def test_contextualize_returns_image():
    """
    Generating a mozaique should return a PIL image object
    """
    # Arrange
    image = Image.open(test_image)
    root_patch = Patch.from_image(image)
    quadrants = root_patch.decompose(QuadTree)
    
    # Act
    result = Contextualize.generate(image, quadrants[1])
    
    # Assert
    assert isinstance(result, Image.Image), "Mozaique should generate an image"

