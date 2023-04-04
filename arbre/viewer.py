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
from transform import translate, rotate, scale, identity, sincos, quaternion, quaternion_from_euler

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

# class Cylinder(Node):
#     """ Very simple cylinder based on provided load function """
#     def __init__(self, shader):
#         super().__init__()
#         self.add(*load('cylinder.obj', shader, tex_file = 'wood.png'))  # just load cylinder from file
# -------------- Deformable Cylinder Mesh  ------------------------------------
class SkinnedCylinder(KeyFrameControlNode):
    """ Deformable cylinder """
    def __init__(self, shader, sections=11, quarters=20):

        # this "arm" node and its transform serves as control node for bone 0
        # we give it the default identity keyframe transform, doesn't move
        super().__init__({0: (0, 0, 0)}, {0: quaternion()}, {0: 1})

        # we add a son "forearm" node with animated rotation for the second
        # part of the cylinder
        self.add(KeyFrameControlNode(
            {0: (0, 0, 0)},
            {0: quaternion(), 2: quaternion_from_euler(90), 4: quaternion()},
            {0: 1}))

        # there are two bones in this animation corresponding to above noes
        bone_nodes = [self, self.children[0]]

        # these bones have no particular offset transform
        bone_offsets = [identity(), identity()]

        # vertices, per vertex bone_ids and weights
        vertices, faces, bone_id, bone_weights = [], [], [], []
        for x_c in range(sections+1):
            for angle in range(quarters):
                # compute vertex coordinates sampled on a cylinder
                z_c, y_c = sincos(360 * angle / quarters)
                vertices.append((x_c - sections/2, y_c, z_c))

                bone_id.append((0, 1, 0, 0))

                weight = np.clip(1-(2*x_c/sections-1/2), 0, 1)
                bone_weights.append((weight, 1 - weight, 0, 0))


        # face indices
        faces = []
        for x_c in range(sections):
            for angle in range(quarters):

                # indices of the 4 vertices of the current quad, % helps
                # wrapping to finish the circle sections
                ir0c0 = x_c * quarters + angle
                ir1c0 = (x_c + 1) * quarters + angle
                ir0c1 = x_c * quarters + (angle + 1) % quarters
                ir1c1 = (x_c + 1) * quarters + (angle + 1) % quarters

                # add the 2 corresponding triangles per quad on the cylinder
                faces.extend([(ir0c0, ir0c1, ir1c1), (ir0c0, ir1c1, ir1c0)])

        # the skinned mesh itself. it doesn't matter where in the hierarchy
        # this is added as long as it has the proper bone_node table
        attributes = dict(position=vertices, normal=bone_weights,
                          bone_ids=bone_id, bone_weights=bone_weights, tex_file = 'wood.png')
        mesh = Mesh(shader, attributes=attributes, index=faces)
        self.add(Skinned(mesh, bone_nodes, bone_offsets))


class Tree(Node):
    """ Hierchical element of the scene with a cylinder base, Round top with 3 leaves"""
    def __init__(self):
        super().__init__()

        # --------------- Creation of the tree --------------------------
        cylinder = SkinnedCylinder(Shader("skinning.vert", "texture.frag"))
        leaf = Leaf(Shader("texture.vert", "texture.frag"))

        # # --- make two long cylinders
        # base_shape = Node(transform=scale((1,8,1)))
        # base_shape.add(cylinder)

        # second_cylinder = Node(transform=scale((1.5,8,1.5)))
        # second_cylinder.add(cylinder)                    

        base_shape = Node(transform=rotate((0,0,1),90) @ scale ((1.5,1,1)))
        base_shape.add(cylinder)

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

        transform_cyl = Node(transform=translate(0,6,0))
        transform_cyl.add(base_shape, transform_leaf1)

        # transform_base = Node(transform=translate(0,8,0))
        # transform_base.add(second_cylinder, transform_cyl) # notre arbre final


        self.add(transform_cyl)

def main():
    """ main """
    # TODO : transformer en une classe arbre

    viewer = Viewer()

    # default color shader
    shader = Shader("skinning.vert", "texture.frag")
    shader_color = Shader("color.vert", "color.frag")


    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    if len(sys.argv) < 2:
        tree = Tree()
        axis = Axis(shader_color)

        viewer.add(tree)
        viewer.add(axis)

        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped