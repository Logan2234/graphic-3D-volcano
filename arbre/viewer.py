#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import sys                          # for system arguments

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
import glfw                         # lean window system wrapper for OpenGL

from core import Shader, Mesh, Viewer, Node, load
from transform import translate, identity, rotate, scale

class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """
    def __init__(self, shader):
        pos = ((0, 0, 0), (10, 0, 0), (0, 0, 0), (0, 10, 0), (0, 0, 0), (0, 0, 10))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

class Leaf(Node):
    """ Low poly leaf based on provided object"""
    def __init__(self, shader):
        super().__init__()
        self.add(*load('leaf.obj', shader, tex_file = 'leaf.jpg'))  # just load leaf from file

class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('cylinder.obj', shader, tex_file = 'wood.png'))  # just load cylinder from file

class Tree(Node):
    """ Hierchical element of the scene with a cylinder base, Round top with 3 leaves"""
    def __init__(self, shader_leaf, shader_wood):
        super().__init__()

        # --------------- Creation of the tree --------------------------
        cylinder = Cylinder(shader_wood)
        leaf = Leaf(shader_leaf)

        # --- make two long cylinders
        base_shape = Node(transform=scale((1,8,1)))
        base_shape.add(cylinder)

        second_cylinder = Node(transform=scale((1.5,8,1.5)))
        second_cylinder.add(cylinder)                    

        # --- make 4 leaves
        leaf_1 = Node(transform=scale((0.06,0.05,0.05))@(translate(-5041.9, 13,-1105)))
        leaf_1.add(leaf)    # the standard one

        leaf_2 = Node(transform=scale((0.04,0.06,0.06))@(translate(-5041.9, 13,-1105)))
        leaf_2.add(leaf)    # a bigger one

        leaf_3 = Node(transform=scale((0.05,0.03,0.03))@(translate(-5041.9, 13,-1105)))
        leaf_3.add(leaf)    # a curvier and smaller one

        leaf_4 = Node(transform=scale((0.05,0.08,0.05))@(translate(-5041.9, 13,-1105)))
        leaf_4.add(leaf)    # a longer and bigger one

        # --- hierarchy of the tree
        phi2 = 90.0        # second leaf angle
        phi3 = 180.0         # ...
        phi4 = 270.0         # ...

        transform_leaf4 = Node(transform=rotate((0,1,0), phi4))
        transform_leaf4.add(leaf_4)

        transform_leaf3 = Node(transform=rotate((0,1,0), phi3))
        transform_leaf3.add(transform_leaf4, leaf_2)

        transform_leaf2 = Node(transform=rotate((0,1,0), phi2))
        transform_leaf2.add(transform_leaf3, leaf_2)

        transform_leaf1 = Node(transform=translate(0,7.5,0) )
        transform_leaf1.add(transform_leaf2, leaf_1)

        transform_cyl = Node(transform=translate(0,12,0))
        transform_cyl.add(base_shape, transform_leaf1)

        transform_base = Node(transform=translate(0,8,0))
        transform_base.add(second_cylinder, transform_cyl) # notre arbre final

        self.add(transform_base)

def main():
    """ main """
    # TODO : transformer en une classe arbre

    viewer = Viewer()

    # default color shader
    shader = Shader("texture.vert", "texture.frag")


    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    if len(sys.argv) < 2:
        tree = Tree(shader, shader)
        axis = Axis(shader)

        viewer.add(tree)
        viewer.add(axis)

        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped