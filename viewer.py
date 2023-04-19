#!/usr/bin/env python3

import sys

from arbre import Tree
from assets.Skybox.skybox import Skybox
from assets.Volcano.volcano import Volcano
from assets.Water.water import Water
from core import Node, Shader, Viewer, load
from floor import Floor
from transform import scale, translate


def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()
    shader_fog = Shader("fog.vert", "fog.frag")
    shader = Shader("texture.vert", "texture.frag")
    shader_color = Shader("color.vert", "color.frag")

    water_shader = Shader("assets/Water/shaders/water.vert", "assets/Water/shaders/water.frag")

    skybox_shader = Shader(
        "assets/Skybox/shaders/skybox.vert", "assets/Skybox/shaders/skybox.frag"
    )
    shader_volcano = Shader(
        "assets/Volcano/shaders/volcano.vert", "assets/Volcano/shaders/volcano.frag"
    )

    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])

    viewer.add(
        Skybox(
            skybox_shader,
            [
                "img/cubemaps/right.png",
                "img/cubemaps/left.png",
                "img/cubemaps/top.png",
                "img/cubemaps/bottom.png",
                "img/cubemaps/front.png",
                "img/cubemaps/back.png",
            ],
        )
    )
    tree0 = Tree(transform=translate((-200,-100,100))@scale((0.3,0.3,0.3)))
    floor = Node(children=[Floor(shader, "img/cayu.jpg", "img/flowers.png")])
    volcano = Node(children=[Volcano(shader_volcano, "img/grass.png", "img/basalte.jpg"), floor, tree0])
    viewer.add(volcano)
    viewer.add(Water(water_shader))

    # start rendering loop
    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
