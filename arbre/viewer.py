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
from transform import *

from animation import KeyFrameControlNode, Skinned

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
    def __init__(self, shader):
        
        super().__init__()
        self.add(*load('cylinder.obj', shader, tex_file = 'wood.png'))  # just load cylinder from file


class AnimatedTree(Node):
    """ Hierchical element of the scene taht will be animated"""
    def __init__(self):
        super().__init__()

        # ------------------------------ Constants used --------------------------
        cylinder = Cylinder(Shader("texture.vert", "texture.frag"))
        leaf = Leaf(Shader("texture.vert", "texture.frag"))

        # --- Make two long cylinders
        base_shape = Node(transform=scale((1,8,1)))
        base_shape.add(cylinder)

        second_cylinder = Node(transform=scale((1.5,8,1.5)))
        second_cylinder.add(cylinder)   


        # --- Make 4 leaves
        leaf_1 = Node(transform=scale((0.06,0.05,0.05))@(translate(-5041.9, 13,-1105)))
        leaf_1.add(leaf)    # the standard one

        leaf_2 = Node(transform=scale((0.04,0.06,0.06))@(translate(-5041.9, 13,-1105)))
        leaf_2.add(leaf)    # a bigger one

        leaf_3 = Node(transform=scale((0.05,0.03,0.03))@(translate(-5041.9, 13,-1105)))
        leaf_3.add(leaf)    # a curvier and smaller one

        leaf_4 = Node(transform=scale((0.05,0.08,0.05))@(translate(-5041.9, 13,-1105)))
        leaf_4.add(leaf)    # a longer and bigger one

        # ------------------------ Animation of items ---------------------------
        phi2 = 90.0        # second leaf angle
        phi3 = 180.0         # ...
        phi4 = 270.0         # ...

        # --- For leaf 4
        transform_leaf4 = Node(transform=rotate((0,1,0), phi4)@translate(0,7.2,0), children=[leaf_4])
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0) , 5: vec(0,0,0)}
        rotate_keys = {0: quaternion(), 2: quaternion_from_euler(0, -30, 0),
                    3: quaternion_from_euler(0, 30, 0), 4: quaternion()}
        scale_keys = {0: 1, 3:1, 5:1 }
        animated_leaf4 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf4.add(transform_leaf4)

        # -- For leaf 3
        transform_leaf3 = Node(transform=rotate((0,1,0), phi3)@translate(0,7.5,0), children=[leaf_1])
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0) , 5: vec(0,0,0)}
        rotate_keys = {0: quaternion(), 2: quaternion_from_euler(0, -40, 0),
                    3: quaternion_from_euler(0, 40, 0), 4: quaternion()}
        scale_keys = {0: 1, 3:1, 5:1 }
        animated_leaf3 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf3.add(transform_leaf3)

        # -- For leaf 2
        transform_leaf2 = Node(transform=rotate((0,1,0), phi2)@translate(0,7.5,0))
        transform_leaf2.add(leaf_2)
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0) , 5: vec(0,0,0)}
        rotate_keys = {0: quaternion(), 2: quaternion_from_euler(0, -20, 0),
                    3: quaternion_from_euler(0, 20, 0), 4: quaternion()}
        scale_keys = {0: 1, 3:1, 5:1 }
        animated_leaf2 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf2.add(transform_leaf2)

        # -- For leaf 1
        transform_leaf1 = Node(transform=translate(0,7.5,0) )
        transform_leaf1.add(leaf_1)
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0) , 5: vec(0,0,0)}
        rotate_keys = {0: quaternion(), 2: quaternion_from_euler(0, -30, 0),
                    3: quaternion_from_euler(0,30, 0), 4: quaternion()}
        scale_keys = {0: 1, 3:1, 5:1 }
        animated_leaf1 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf1.add(transform_leaf1)

        # ----------------------- Hierarchy of the tree -------------------------
        leaves = Node(children=[animated_leaf4, animated_leaf3, animated_leaf2, animated_leaf1])

        transform_cyl = Node(transform=translate(0,12,0))
        transform_cyl.add(base_shape, leaves)

        transform_base = Node(transform=translate(0,8,0))
        transform_base.add(second_cylinder, transform_cyl) # notre arbre final


        # ----------------------- Animation of object ----------------------------------

        # --- For the whole tree
        translate_keys = {0: vec(0, 0, 0), 2: vec(0, 0, 0), 3: vec(0, -2, 0) , 4: vec(0, 0, 0)}
        rotate_keys = {0: quaternion(), 2: quaternion_from_euler(0, 180, 0),
                    3: quaternion_from_euler(0, 280, 0), 4: quaternion_from_euler(0,360,0), 5: quaternion()}
        scale_keys = {0: 1, 1:0.8, 2:1, 5:1 }
        keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        keynode.add(transform_base)
        self.add(keynode)


def main():
    """ main """
    viewer = Viewer()

    # default color shader
    # TODO: faire de meilleures textures ?
    shader = Shader("skinning.vert", "texture.frag")
    shader_color = Shader("color.vert", "color.frag")


    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    if len(sys.argv) < 2:
        tree = AnimatedTree()
        axis = Axis(shader_color)

        viewer.add(tree)
        viewer.add(axis)

        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped