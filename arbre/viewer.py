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
        pos = ((0, 0, 0), (100, 0, 0), (0, 0, 0), (0, 100, 0), (0, 0, 0), (0, 0, 100))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

class Leaf(Node):
    """ Low poly leaf based on provided object"""
    def __init__(self, shader):
        super().__init__()
        self.add(*load('leaf.obj', shader))  # just load leaf from file

class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('cylinder.obj', shader))  # just load cylinder from file

def main():
    """ Hierchical element of the scene with a cylinder base, Round top with 3 leaves"""

    viewer = Viewer()

    # default color shader
    shader = Shader("color.vert", "color.frag")

    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    if len(sys.argv) < 2:
        cylinder = Cylinder(shader)
        leaf = Leaf(shader)
        axis = Axis(shader)

        # make a long cylinder
        base_shape = Node(transform=scale((10,190,10)))
        base_shape.add(cylinder)                    # shape of robot base

        # make 4 leaves
        leaf_1 = Node(transform=scale((0.5,0.5,0.5))@(translate(-5031.9, 13,-1105)))
        leaf_1.add(leaf)    # the standard one

        leaf_2 = Node(transform=scale((0.6,0.6,0.6))@(translate(-5031.9, 13,-1105)))
        leaf_2.add(leaf)    # a bigger one

        leaf_3 = Node(transform=scale((0.5,0.3,0.3))@(translate(-5031.9, 13,-1105)))
        leaf_3.add(leaf)    # a curvier and smaller one

        leaf_4 = Node(transform=scale((0.5,0.7,0.5))@(translate(-5031.9, 13,-1105)))
        leaf_4.add(leaf)    # a longer and bigger one

        # ---- construct our robot arm hierarchy ---------------------------
        phi2 = 90.0        # second leaf angle
        phi3 = 180.0         # ...
        phi4 = 270.0         # 

        transform_leaf4 = Node(transform=rotate((0,1,0), phi4))
        transform_leaf4.add(leaf_4)

        transform_leaf3 = Node(transform=rotate((0,1,0), phi3))
        transform_leaf3.add(transform_leaf4, leaf_2)

        transform_leaf2 = Node(transform=rotate((0,1,0), phi2))
        transform_leaf2.add(transform_leaf3, leaf_2)

        transform_leaf1 = Node(transform=translate(0,190,0) )
        transform_leaf1.add(transform_leaf2, leaf_1)

        transform_base = Node(transform=translate(0,190,0))
        transform_base.add(base_shape, transform_leaf1)

        # transform_arm = Node(transform=translate(0,1,0) @ rotate((0,0,1), phi1))
        # transform_arm.add(arm_shape, transform_forearm)

        # transform_base = Node(transform=rotate((0,1,0), theta))
        # transform_base.add(base_shape, transform_arm)

        viewer.add(transform_base)
        #viewer.add(leaf_1)
        viewer.add(axis)

        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped