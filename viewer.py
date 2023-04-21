#!/usr/bin/env python3

""" Main file """

from arbre import AnimatedTree
from assets.Skybox.skybox import Skybox
from assets.Volcano.volcano import Volcano
from assets.Water.water import Water
from core import Node, Shader, Viewer
from disk import Disk
from floor import Floor
from transform import scale, translate

#from smoke import Smoke, SmokeParticle

def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()

    shader = Shader("fog.vert", "fog.frag")
    floor_shader = Shader("floor.vert", "floor.frag")
    lava_shader = Shader("lava.vert", "lava.frag")
    water_shader = Shader(
        "assets/Water/shaders/water.vert", "assets/Water/shaders/water.frag"
    )

    skybox_shader = Shader(
        "assets/Skybox/shaders/skybox.vert", "assets/Skybox/shaders/skybox.frag"
    )

    volcano_shader = Shader(
        "assets/Volcano/shaders/volcano.vert", "assets/Volcano/shaders/volcano.frag"
    )

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
    trees = Node(
        children=[
            AnimatedTree(
                transform=translate((-200 + 150 * i, ((-1) ** i) * (-200 + 120 * i),10))
                @ scale((0.8, 0.8, 0.8))
            )
            for i in range(4)
        ]
    )
    trees2 = Node(
        children=[
            AnimatedTree(
                transform=translate((200 - 120 * i, ((-1) ** i) * (200 - 50 * i), 10))
                @ scale((0.8, 0.8, 0.8))
            )
            for i in range(4)
        ]
    )

    lava = Node(children=[Disk(lava_shader, "img/lava.jpg", 20, 150)])
    volcano = Node(
        children=[Volcano(volcano_shader, "img/grass.png", "img/basalte.jpg"), lava]
    )

    floor = Node(
        children=[
            Floor(floor_shader, "img/rock.png", "img/terre.jpeg", "img/grass.png"),
            volcano
        ]
    )

    island = Node(children=[floor, trees, trees2])
    viewer.add(island)
    viewer.add(Water(water_shader))

    # smoke = Smoke()
    # viewer.add(smoke)

    # start rendering loop
    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
