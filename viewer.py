#!/usr/bin/env python3

import math as Math
import sys

import numpy as np  # all matrix manipulations & OpenGL args
from OpenGL import GL  # standard Python OpenGL wrapper
from perlin_noise import PerlinNoise  # pip install perlin-noise

from assets.Skybox.skybox import Skybox
from assets.Volcano.volcano import Volcano
from assets.Water.water import Water
from core import Mesh, Shader, Viewer, load
from texture import Texture, Textured
from transform import compute_normals

from floor import Floor



# -------------- Example textured plane class ---------------------------------

class TexturedPlane(Textured):
    """ Simple first textured object """

    def __init__(self, shader, tex_file, tex_file2):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100*np.array(base_coords, np.float32)
        indices = np.array(((0, 1, 2), (0, 2, 3)), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=((1, 1), (0, 1), (0, 0), (0, 1))), index=indices, usage=GL.GL_STATIC_DRAW, )

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture, diffuse_map2=texture2)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)
            


# -------------- main program and scene setup --------------------------------


def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()
    shader_color = Shader("fog.vert", "fog.frag")
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

    viewer.add(Volcano(shader_volcano, "img/grass.png", "img/basalte.jpg"))
    viewer.add(Water(water_shader))
    # viewer.add(Floor(shader, "img/cayu.jpg", "img/flowers.png"))

    # start rendering loop
    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
