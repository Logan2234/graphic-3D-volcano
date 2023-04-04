#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured, TextureCubeMap
from PIL import Image               # load texture maps
from transform import compute_normals

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


class Skybox(Textured):

    def __init__(self, shader, faces):
        cubemap_texture = TextureCubeMap(faces)
        skybox_vertices = np.array([
            # positions
            (-1.0,  1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0,  1.0, -1.0),
            (-1.0,  1.0, -1.0),

            (1.0, -1.0, -1.0),
            (1.0, -1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0, -1.0),
            (1.0, -1.0, -1.0),

            (-1.0, -1.0,  1.0),
            (-1.0, -1.0, -1.0),
            (-1.0,  1.0, -1.0),
            (-1.0,  1.0, -1.0),
            (-1.0,  1.0,  1.0),
            (-1.0, -1.0,  1.0),

            (-1.0, -1.0,  1.0),
            (-1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0, -1.0,  1.0),
            (-1.0, -1.0,  1.0),

            (-1.0,  1.0, -1.0),
            (1.0,  1.0, -1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (-1.0,  1.0,  1.0),
            (-1.0,  1.0, -1.0),

            (-1.0, -1.0, -1.0),
            (-1.0, -1.0,  1.0),
            (1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0,  1.0),
            (1.0, -1.0,  1.0)
        ], np.float32)
        skybox = Mesh(shader, attributes=dict(position=skybox_vertices))
        super().__init__(skybox, skybox=cubemap_texture)

# -------------- main program and scene setup --------------------------------

def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")
    skybox_shader = Shader("skybox.vert", "skybox.frag")
    
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])

    viewer.add(Skybox(skybox_shader, ["cubemaps/right.png", "cubemaps/left.png",
                                      "cubemaps/top.png", "cubemaps/bottom.png", "cubemaps/front.png", "cubemaps/back.png"]))

    if len(sys.argv) != 2:
        print(
            'Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in format supported by assimp.' % (sys.argv[0],))
        viewer.add(TexturedPlane(shader, "grass.png", "flowers.png"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
