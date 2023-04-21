#!/usr/bin/env python3
"""
Contains class for a cute animated tree
"""

from animation import KeyFrameControlNode
from core import Node, Shader, load
from transform import (identity, quaternion, quaternion_from_euler, rotate,
                       scale, translate, vec)


class Leaf(Node):
    """Low poly leaf based on provided object"""

    def __init__(self, shader):
        super().__init__()
        self.add(
            *load("arbre/leaf.obj", shader, tex_file="arbre/leaf.jpg")
        )  # just load leaf from file


class Cylinder(Node):
    """Cylinder based on provided object"""

    def __init__(self, shader):
        super().__init__()
        self.add(
            *load("arbre/cylinder.obj", shader, tex_file="arbre/wood.png")
        )  # just load cylinder from file


class Tree(Node):
    """Hierchical element with a static version"""

    def __init__(self, children=(), transform=identity()):
        super().__init__(children=children, transform=transform)

        # ------------------------------ Constants used --------------------------
        cylinder = Cylinder(Shader("tree.vert", "tree.frag"))
        leaf = Leaf(Shader("tree.vert", "tree.frag"))

        # --- Make two long cylinders
        base_shape = Node(transform=scale((1, 8, 1)))
        base_shape.add(cylinder)

        second_cylinder = Node(transform=scale((1.5, 8, 1.5)))
        second_cylinder.add(cylinder)

        # --- Make 4 leaves
        leaf_1 = Node(
            transform=scale((0.06, 0.05, 0.05)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_1.add(leaf)  # the standard one

        leaf_2 = Node(
            transform=scale((0.04, 0.06, 0.06)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_2.add(leaf)  # a bigger one

        leaf_3 = Node(
            transform=scale((0.05, 0.03, 0.03)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_3.add(leaf)  # a curvier and smaller one

        leaf_4 = Node(
            transform=scale((0.05, 0.08, 0.05)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_4.add(leaf)  # a longer and bigger one

        # ------------------------ Creation of items ---------------------------
        phi2 = 90.0  # second leaf angle
        phi3 = 180.0  # ...
        phi4 = 270.0  # ...

        # --- For leaf 4
        transform_leaf4 = Node(
            transform=rotate((0, 1, 0), phi4) @ translate(0, 7.2, 0), children=[leaf_4]
        )

        # -- For leaf 3
        transform_leaf3 = Node(
            transform=rotate((0, 1, 0), phi3) @ translate(0, 7.5, 0), children=[leaf_1]
        )

        # -- For leaf 2
        transform_leaf2 = Node(
            transform=rotate((0, 1, 0), phi2) @ translate(0, 7.5, 0), children=[leaf_2]
        )

        # -- For leaf 1
        transform_leaf1 = Node(transform=translate(0, 7.5, 0), children=[leaf_1])

        # ----------------------- Hierarchy of the tree -------------------------
        leaves = Node(
            children=[
                transform_leaf1,
                transform_leaf2,
                transform_leaf3,
                transform_leaf4,
            ]
        )

        transform_cyl = Node(transform=translate(0, 12, 0))
        transform_cyl.add(base_shape, leaves)

        transform_base = Node(transform=translate(0, 8, 0) @ rotate((1, 0, 0), 90))
        transform_base.add(second_cylinder, transform_cyl)  # notre arbre final

        self.add(transform_base)


class AnimatedTree(Node):
    """Hierchical element of the scene taht will be animated"""

    def __init__(self, children=(), transform=identity()):
        super().__init__(children=children, transform=transform)

        # ------------------------------ Constants used --------------------------
        cylinder = Cylinder(Shader("tree.vert", "tree.frag"))
        leaf = Leaf(Shader("tree.vert", "tree.frag"))

        # --- Make two long cylinders
        base_shape = Node(transform=scale((1, 8, 1)))
        base_shape.add(cylinder)

        second_cylinder = Node(transform=scale((1.5, 8, 1.5)))
        second_cylinder.add(cylinder)

        # --- Make 4 leaves
        leaf_1 = Node(
            transform=scale((0.06, 0.05, 0.05)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_1.add(leaf)  # the standard one

        leaf_2 = Node(
            transform=scale((0.04, 0.06, 0.06)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_2.add(leaf)  # a bigger one

        leaf_3 = Node(
            transform=scale((0.05, 0.03, 0.03)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_3.add(leaf)  # a curvier and smaller one

        leaf_4 = Node(
            transform=scale((0.05, 0.08, 0.05)) @ (translate(-5041.9, 13, -1105))
        )
        leaf_4.add(leaf)  # a longer and bigger one

        # ------------------------ Animation of items ---------------------------
        phi2 = 90.0  # second leaf angle
        phi3 = 180.0  # ...
        phi4 = 270.0  # ...

        # --- For leaf 4
        transform_leaf4 = Node(
            transform=rotate((0, 1, 0), phi4) @ translate(0, 7.2, 0), children=[leaf_4]
        )
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0), 5: vec(0, 0, 0)}
        rotate_keys = {
            0: quaternion(),
            2: quaternion_from_euler(0, -30, 0),
            3: quaternion_from_euler(0, 30, 0),
            4: quaternion(),
        }
        scale_keys = {0: 1, 3: 1, 5: 1}
        animated_leaf4 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf4.add(transform_leaf4)

        # -- For leaf 3
        transform_leaf3 = Node(
            transform=rotate((0, 1, 0), phi3) @ translate(0, 7.5, 0), children=[leaf_1]
        )
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0), 5: vec(0, 0, 0)}
        rotate_keys = {
            0: quaternion(),
            2: quaternion_from_euler(0, -40, 0),
            3: quaternion_from_euler(0, 40, 0),
            4: quaternion(),
        }
        scale_keys = {0: 1, 3: 1, 5: 1}
        animated_leaf3 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf3.add(transform_leaf3)

        # -- For leaf 2
        transform_leaf2 = Node(transform=rotate((0, 1, 0), phi2) @ translate(0, 7.5, 0))
        transform_leaf2.add(leaf_2)
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0), 5: vec(0, 0, 0)}
        rotate_keys = {
            0: quaternion(),
            2: quaternion_from_euler(0, -20, 0),
            3: quaternion_from_euler(0, 20, 0),
            4: quaternion(),
        }
        scale_keys = {0: 1, 3: 1, 5: 1}
        animated_leaf2 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf2.add(transform_leaf2)

        # -- For leaf 1
        transform_leaf1 = Node(transform=translate(0, 7.5, 0))
        transform_leaf1.add(leaf_1)
        translate_keys = {0: vec(0, 0, 0), 3: vec(0, -0.3, 0), 5: vec(0, 0, 0)}
        rotate_keys = {
            0: quaternion(),
            2: quaternion_from_euler(0, -30, 0),
            3: quaternion_from_euler(0, 30, 0),
            4: quaternion(),
        }
        scale_keys = {0: 1, 3: 1, 5: 1}
        animated_leaf1 = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        animated_leaf1.add(transform_leaf1)

        # ----------------------- Hierarchy of the tree -------------------------
        leaves = Node(
            children=[animated_leaf4, animated_leaf3, animated_leaf2, animated_leaf1]
        )

        transform_cyl = Node(transform=translate(0, 12, 0))
        transform_cyl.add(base_shape, leaves)

        transform_base = Node(transform=translate(0, 8, 0) @ rotate((1, 0, 0), 90))
        transform_base.add(second_cylinder, transform_cyl)  # notre arbre final

        # ----------------------- Animation of object ----------------------------------

        # --- For the whole tree
        translate_keys = {
            0: vec(0, 0, 0),
            2: vec(0, 0, 0),
            3: vec(0, -2, 0),
            4: vec(0, 0, 0),
        }
        rotate_keys = {
            0: quaternion(),
            2: quaternion_from_euler(180, 0, 0),
            3: quaternion_from_euler(280, 0, 0),
            4: quaternion_from_euler(360, 0, 0),
            5: quaternion(),
        }
        scale_keys = {0: 1, 1: 0.8, 2: 1, 5: 1}
        keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        keynode.add(transform_base)
        self.add(keynode)
