#!/usr/bin/env python3

import sys

from arbre import AnimatedTree, Tree
from assets.Skybox.skybox import Skybox
from assets.Volcano.volcano import Volcano
from assets.Water.water import Water
from core import Node, Shader, Viewer, load
from floor import Floor
from transform import scale, translate
from Disk import Disk


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

    ##### Some trees #####
    trees = Node(children=[AnimatedTree(transform= translate((-200+120*i,((-1)**i)*(-200 + 140*i), 5))
                                    @scale((0.8,0.8,0.8))) for i in range(4)])
    trees2 = Node(children=[AnimatedTree(transform= translate((200-120*i,((-1)**i)*(200 - 120*i), 5))
                                    @scale((0.8,0.8,0.8))) for i in range(4)])

    floor = Node(children=[Floor(shader, "img/cayu.jpg", "img/terre.jpeg")])
    lava = Node(children = [Disk(shader, "img/lava.jpg", "img/lava.jpg", 20, 150)])
    volcano = Node(children=[Volcano(shader_volcano, "img/grass.png", "img/basalte.jpg"), lava])
    island = Node(children = [floor, volcano, trees, trees2])

    viewer.add(island)
    viewer.add(Water(water_shader))

    # start rendering loop
    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
