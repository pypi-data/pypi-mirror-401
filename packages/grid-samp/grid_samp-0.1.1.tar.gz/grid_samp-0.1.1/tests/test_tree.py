# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:08:12 2023

@author: u0072088
"""
from PIL import Image

from image_aesthetic_maps.Node import Node
from image_aesthetic_maps.Tree import Tree
from image_aesthetic_maps.decomposition import QuadTree

test_image = r"C:\Users\u0072088\OneDrive - KU Leuven\Documents\3-projects\image-aesthetic-map-toolbox\image-aesethic-map-toolbox\tests\test_image.jpg"


def test_tree_initialization():
    """
    Initializing a tree with a default recursion level should produce a tree
    with one root node and no children
    """
    # Arrange
    image = Image.open(test_image)
    
    # Act
    tree = Tree(image)
    
    # Assert
    assert isinstance(tree._root_node, Node), "Tree has no root node"
    assert isinstance(tree._image, Image.Image), "Tree has no image"
    assert len(tree._root_node._children) == 0, "Default initialization produces no children"
    
def test_get_nodes_at_level():
    """
    Should return a list of nodes at the specified level
    """
    # Arrange
    LEVEL_2_NODES = 3
    LEVEL_3_NODES = 4
    
    image = Image.open(test_image)
    tree = Tree(image)
    
    for i in range(LEVEL_2_NODES):
        child_node = Node()
        tree._root_node.add_child(child_node)
        for j in range(LEVEL_3_NODES):
            child_node.add_child(Node())
            
    # Act
    level_1_nodes = tree._get_nodes_at_level(1)
    level_2_nodes = tree._get_nodes_at_level(2)
    level_3_nodes = tree._get_nodes_at_level(3)
    
    # Assert
    assert len(level_1_nodes) == 1, "Getting the nodes at level 1 should return the root node"
    assert len(level_2_nodes) == LEVEL_2_NODES, "Getting the nodes at level 1 should return the root node"
    assert len(level_3_nodes) == LEVEL_2_NODES * LEVEL_3_NODES, "Getting the nodes at level 1 should return the root node"
    
def test_tree_quad_decomposition():
    """
    Running the tree with a quad decomposition, should produce child nodes that are
    powers of 4
    """
    # Arrange
    image = Image.open(test_image)
    tree = Tree(image)
    
    # Act
    tree.decompose(QuadTree, 3)
    level_1_nodes = tree._get_nodes_at_level(1)
    level_2_nodes = tree._get_nodes_at_level(2)
    level_3_nodes = tree._get_nodes_at_level(3)
    
    # Assert
    assert len(level_1_nodes) == 1, "Getting the nodes at level 1 should return the root node"
    assert len(level_2_nodes) == 4, "Getting the nodes at level 1 should return the root node"
    assert len(level_3_nodes) == 16, "Getting the nodes at level 1 should return the root node"
    
    