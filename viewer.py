#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, VertexArray, Viewer, Mesh, load
from skybox import Skybox
from texture import Texture, Textured
import math as Math
from perlin_noise import PerlinNoise

from transform import compute_normals  # pip install perlin-noise


noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)

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
        base_coords = [(np.cos(np.deg2rad(18+i*36)), np.sin(np.deg2rad(18+i*36)), 1)
                       for i in range(10)]  # vertex for the base
        base_coords += [(0.6*np.cos(np.deg2rad(i*45)), 0.6*np.sin(np.deg2rad(i*45)), 2)
                        for i in range(8)]  # vertex for the base
        base_coords += [(0, 0, 1), (0, 0, 2)]
        scaled = 10 * np.array(base_coords, np.float32)

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
        scaled = 100*np.array(base_coords, np.float32)
        indices = np.array(((0, 1, 2), (0, 2, 3)), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=(
            (1, 1), (0, 1), (0, 0), (0, 1))), index=indices, usage=GL.GL_STATIC_DRAW, )

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


class Floor(Textured):
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
        positions = []
        for i in range(-150, 151):
            for j in range(-150, 151):
                positions.append(
                    (i, j, 10 * self.getAltitude(i, j, 0.33) * self.smoothStep(130, 150, i, j)))

        longueur_base = len(positions)

        # Rectangles extérieurs supérieurs

        for i in range(150, 181):
            for j in range(-150, 151):
                positions.append((i, j, 0))

        longueur_rectangle = len(positions) - longueur_base

        for i in range(-180, -149):
            for j in range(-150, 151):
                positions.append((i, j, 0))

        for i in range(-150, 151):
            for j in range(-180, -149):
                positions.append((i, j, 0))

        for i in range(-150, 151):
            for j in range(150, 181):
                positions.append((i, j, 0))

        # Coins supérieurs

        positions.append((150, 150, 0))
        for i in range(20):
            positions.append((150 + 30 * np.cos(2 * np.pi * i / 40),
                             150 + 30 * np.sin(2 * np.pi * i / 40), 0))
            positions.append((150 + 30 * np.cos(2 * np.pi * (i + 1) / 40),
                             150 + 30 * np.sin(2 * np.pi * (i + 1) / 40), 0))

        positions.append((-150, 150, 0))
        for i in range(20):
            positions.append((-150 + 30 * np.cos(2 * np.pi * (i + 20) / 40),
                             150 - 30 * np.sin(2 * np.pi * (i + 20) / 40), 0))
            positions.append((-150 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40),
                             150 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40), 0))

        positions.append((-150, -150, 0))
        for i in range(20):
            positions.append((-150 - 30 * np.cos(2 * np.pi * i / 40), -
                             150 - 30 * np.sin(2 * np.pi * i / 40), 0))
            positions.append((-150 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -
                             150 - 30 * np.sin(2 * np.pi * (i + 1) / 40), 0))

        positions.append((150, -150, 0))
        for i in range(20):
            positions.append((150 + 30 * np.cos(2 * np.pi * i / 40), -
                             150 - 30 * np.sin(2 * np.pi * i / 40), 0))
            positions.append((150 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -
                             150 - 30 * np.sin(2 * np.pi * (i + 1) / 40), 0))

        # Coins inférieurs

        positions.append((120, 120, -30))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40),
                             120 + 30 * np.sin(2 * np.pi * i / 40), -30))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40),
                             120 + 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))

        positions.append((-120, 120, -30))
        for i in range(20):
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20) / 40),
                             120 - 30 * np.sin(2 * np.pi * (i + 20) / 40), -30))
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40),
                             120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40), -30))

        positions.append((-120, -120, -30))
        for i in range(20):
            positions.append((-120 - 30 * np.cos(2 * np.pi * i / 40), -
                             120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            positions.append((-120 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -
                             120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))

        positions.append((120, -120, -30))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -
                             120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -
                             120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))

        # Bords inférieurs

        for i in range(-120, 121):  # Bord inférieur nord
            positions.append((i, -150, -30))

        for i in range(-120, 121):  # Bord supérieur nord
            if i < 0:
                positions.append((Math.floor(i*150/120), -180, 0))
            else:
                positions.append((Math.ceil(i*150/120), -180, 0))

        for i in range(-120, 121):  # Bord inférieur est
            positions.append((150, i, -30))

        for i in range(-120, 121):  # Bord supérieur est
            if i < 0:
                positions.append((180, Math.floor(i*150/120), 0))
            else:
                positions.append((180, Math.ceil(i*150/120), 0))

        for i in range(-120, 121):  # Bord inférieur sud
            positions.append((i, 150, -30))

        for i in range(-120, 121):  # Bord supérieur sud
            if i < 0:
                positions.append((Math.floor(i*150/120), 180, 0))
            else:
                positions.append((Math.ceil(i*150/120), 180, 0))

        for i in range(-120, 121):  # Bord inférieur ouest
            positions.append((-150, i, -30))

        for i in range(-120, 121):  # Bord supérieur ouest
            if i < 0:
                positions.append((-180, Math.floor(i*150/120), 0))
            else:
                positions.append((-180, Math.ceil(i*150/120), 0))

        # Rocher inférieur
        for i in range(-120, 121):
            for j in range(-120, 121):
                positions.append(
                    (i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))

        # Rectangles extérieurs inférieurs

        for i in range(120, 151):
            for j in range(-120, 121):
                positions.append(
                    (i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))

        longueur_petit_rectangles = len(positions)

        for i in range(-150, -119):
            for j in range(-120, 121):
                positions.append(
                    (i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))

        for i in range(-120, 121):
            for j in range(-150, -119):
                positions.append(
                    (i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))

        for i in range(-120, 121):
            for j in range(120, 151):
                positions.append(
                    (i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))

        # Coins inférieurs

        positions.append((120, 120, -30))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40),
                             120 + 30 * np.sin(2 * np.pi * i / 40), -30))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40),
                             120 + 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))

        positions.append((-120, 120, -30))
        for i in range(20):
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20) / 40),
                             120 - 30 * np.sin(2 * np.pi * (i + 20) / 40), -30))
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40),
                             120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40), -30))

        positions.append((-120, -120, -30))
        for i in range(20):
            positions.append((-120 - 30 * np.cos(2 * np.pi * i / 40), -
                             120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            positions.append((-120 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -
                             120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))

        positions.append((120, -120, -30))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -
                             120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -
                             120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))

        scaled = 100 * np.array(positions, np.float32)
        indices = []
        for i in range(300):
            for j in range(300):
                indices.append(i*301+j)
                indices.append((i+1)*301+j+1)
                indices.append(i*301+j+1)
                indices.append(i*301+j)
                indices.append((i+1)*301+j)
                indices.append((i+1)*301+j+1)

        # Rectangles extérieurs supérieurs

        for i in range(30):
            for j in range(300):
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + (i+1)*301+j+1)
                indices.append(longueur_base + i*301+j+1)
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + (i+1)*301+j)
                indices.append(longueur_base + (i+1)*301+j+1)

        longueur_base += longueur_rectangle
        for i in range(30):
            for j in range(300):
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + (i+1)*301+j+1)
                indices.append(longueur_base + i*301+j+1)
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + (i+1)*301+j)
                indices.append(longueur_base + (i+1)*301+j+1)

        longueur_base += longueur_rectangle
        for i in range(300):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)

        longueur_base += longueur_rectangle
        for i in range(300):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)

        # Coins supérieurs
        longueur_base += longueur_rectangle
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i+1)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i+1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i+1)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i+1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i - 164)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i - 164)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i - 164)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i - 164)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i)

        longueur_base += 41

        for i in range(240):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 + 241)

        longueur_base += 241 * 2
        for i in range(240):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 + 241)

        longueur_base += 241 * 2
        for i in range(240):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)

        longueur_base += 241 * 2
        for i in range(240):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1 + 241)
        longueur_base += 241 * 2

        for i in range(240):
            for j in range(240):
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + i*241+j+1)
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + (i+1)*241+j)

        longueur_base += 241 * 241
        longueur_petit_rectangles -= longueur_base

        # Rectangles extérieurs inférieurs

        for i in range(30):
            for j in range(240):
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + i*241+j+1)
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + (i+1)*241+j)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)

        longueur_base += longueur_petit_rectangles
        for i in range(30):
            for j in range(240):
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + i*241+j+1)
                indices.append(longueur_base + (i+1)*241+j)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)

        longueur_base += longueur_petit_rectangles
        for i in range(240):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + (i+1)*31+j)

        longueur_base += longueur_petit_rectangles
        for i in range(240):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + (i+1)*31+j)

        longueur_base += longueur_petit_rectangles

        # Coins inférieurs
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i+1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i+1)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i+1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i+1)

        longueur_base += 41

        indices = np.array(indices, np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=(
            (1, 1), (0, 1), (0, 0), (0, 1))), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def smoothStep(self, edgeLeft, edgeRight, x, y):
        x, y = abs(x), abs(y)
        if x < edgeLeft:
            x = edgeLeft
        if x > edgeRight:
            x = edgeRight
        if y < edgeLeft:
            y = edgeLeft
        if y > edgeRight:
            y = edgeRight

        tx = (x - edgeLeft) / (edgeRight - edgeLeft)
        ty = (y - edgeLeft) / (edgeRight - edgeLeft)

        if (tx + ty == 0):
            return 1

        t = np.sqrt(tx*tx + ty*ty)

        if t >= 1:
            return 0

        return 2 * Math.pow(t, 3) - 3 * Math.pow(t, 2) + 1

    def getAltitude(self, x, y, puissance):
        # return np.sin(x+np.cos(y))+0.5 * np.sin(2+y+np.cos(2 * x))+0.4
        nx = x/100
        ny = y/100
        out = 2*noise1([nx, ny])
        out += 0.5*noise2([nx, ny])
        out += 0.25*noise3([nx, ny])
        if out <= 0:
            return 0
        e = out / (1 + 0.5 + 0.25)
        return Math.pow(e, puissance)


class WaterPlane(Textured):
    """ Simple first textured object """

    def __init__(self, shader):
        # setup plane mesh to be textured
        carre_de_base = np.array(
            ((0, 0, 0), (0.25, 0, 0), (0.25, 0.25, 0), (0, 0.25, 0)))
        indices_de_base = np.array(((0, 1, 2), (0, 2, 3)), np.uint32)
        positions = []
        indices = []
        self.shader = shader
        self.tex = Texture("water.jpg", GL.GL_REPEAT,
                           GL.GL_NEAREST, GL.GL_NEAREST)
        TAILLE = 50
        for i in range(-TAILLE, TAILLE + 1):
            for j in range(-TAILLE, TAILLE + 1):
                for elemt in carre_de_base:
                    positions.append(np.add(elemt, (j*0.25, i*0.25, 0)))
                indices.append(
                    np.add(indices_de_base[0], (4*(2*TAILLE+1)*(i+TAILLE) + 4*(j+TAILLE))))
                indices.append(
                    np.add(indices_de_base[1], (4*(2*TAILLE+1)*(i+TAILLE) + 4*(j+TAILLE))))
        self.positions = np.array(positions)
        self.indices = np.array(indices)
        self.normal = compute_normals(self.positions, self.indices)
        self.mesh = Mesh(shader, attributes=dict(position=self.positions, tex_coord=(
            (1, 1), (0, 1), (0, 0), (0, 1)), normal=self.normal), index=self.indices, usage=GL.GL_DYNAMIC_DRAW, )
        super().__init__(self.mesh, tex=self.tex)

# -------------- main program and scene setup --------------------------------


def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader_color = Shader("fog.vert", "fog.frag")
    water_shader = Shader("water.vert", "water.frag")
    shader = Shader("texture.vert", "texture.frag")
    skybox_shader = Shader("skybox.vert", "skybox.frag")

    viewer.add(*[mesh for file in sys.argv[1:]
               for mesh in load(file, shader_color)])
    viewer.add(Skybox(skybox_shader, ["cubemaps/right.png", "cubemaps/left.png",
                                      "cubemaps/top.png", "cubemaps/bottom.png", "cubemaps/front.png", "cubemaps/back.png"]))

    viewer.add(WaterPlane(water_shader))
    # viewer.add(Volcano(shader_color, "basalte.jpg"))
    # viewer.add(TexturedPlane(shader, "grass.png", "flowers.png"))

    if len(sys.argv) != 2:
        print(
            'Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in format supported by assimp.' % (sys.argv[0],))
        # viewer.add(Floor(shader, "grass.png", "flowers.png"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
