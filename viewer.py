#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from transform import compute_normals

# -------------- Example textured plane class ---------------------------------


class Volcano(Textured):
    """ Simple first textured object """

    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file
        GL.glDisable(GL.GL_CULL_FACE)

        # setup mesh to be textured
        base_coords = [(np.cos(np.deg2rad(18+i*36)), np.sin(np.deg2rad(18+i*36)), 0)
                       for i in range(10)]  # vertex for the base
        base_coords += [(0.6*np.cos(np.deg2rad(i*45)), 0.6*np.sin(np.deg2rad(i*45)), 1)
                        for i in range(8)]  # vertex for the base
        base_coords += [(0, 0, 0), (0, 0, 1)]
        scaled = 1000 * np.array(base_coords, np.float32)

        # scaled = 100 * np.array(base_coords, np.float32)
        indices = [(i, (i+1) % 10, 18) for i in range(10)]
        # indices += [(10+i, 10+(i+1) % 8, 19) for i in range(8)]
        indices += [(0, 1, 11), (11, 1, 12), (1, 2, 12), (12, 2, 13), (2, 3, 13), (3, 4, 13), (13, 4, 14), (14, 4, 5), (14, 5, 15),
                    (15, 5, 6), (15, 6, 16), (16, 6, 7), (16, 7, 8), (16, 8, 17), (17, 8, 9), (10, 17, 9), (10, 9, 0), (0, 11, 10)]
        normal = compute_normals(base_coords, indices)

        mesh = Mesh(shader, attributes=dict(in_position=scaled, in_texcoord=(
            (1, 1), (0, 1), (0, 0), (0, 1)), in_normal=normal), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        # texture2 = Texture(tex_file2, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)


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
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        normal = compute_normals(base_coords, indices)
        mesh = Mesh(shader, attributes=dict(in_position=scaled, in_texcoord=(
            (1, 1), (0, 1), (0, 0), (0, 1)), in_normal=normal), index=indices, usage=GL.GL_STATIC_DRAW, )

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture, diffuse_map_2=texture2)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("fog.vert", "fog.frag")

    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    viewer.add(Volcano(shader, "basalte.jpg"))
    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))
        # viewer.add(TexturedPlane(shader, "grass.png", "flowers.png"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
