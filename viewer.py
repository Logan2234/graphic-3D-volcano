#!/usr/bin/env python3
import math as Math
import sys
from itertools import cycle

import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
import OpenGL.GL as GL  # standard Python OpenGL wrapper
from perlin_noise import PerlinNoise

from core import Mesh, Shader, Viewer, load
from skybox import Skybox
from texture import Texture, Textured
from transform import compute_normals  # pip install perlin-noise

noise0 = PerlinNoise(octaves=1)
noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)

class Volcano(Textured):
    """Simple first textured object"""

    def __init__(self, shader, tex_file, tex_file2):
        TAILLE = 40

        self.wrap, self.filter = GL.GL_REPEAT, (
            GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        self.file = tex_file
        self.file2 = tex_file2

        base_coords, indices = create_grid(TAILLE)
        scaled = np.array(base_coords)

        def getAltitude(x, y, puissance):
            # return np.sin(x+np.cos(y))+0.5 * np.sin(2+y+np.cos(2 * x))+0.4
            nx = x / 100
            ny = y / 100
            out = 2 * noise1([nx, ny])
            out += 1 * noise2([nx, ny])
            out += 0.5 * noise3([nx, ny])
            if out <= 0:
                return out
            e = out / (2 + 1 + 0.5)
            return Math.pow(e, puissance)

        for i in range(len(scaled)):
            x, y = i % (2 * TAILLE + 1), i // (2 * TAILLE + 1)
            if x == TAILLE and y == TAILLE:
                scaled[i][2] = scaled[i - 1][2]
            else:
                distance = 0.4 * \
                    (np.sqrt((y - TAILLE) ** 2 + (x - TAILLE) ** 2)) ** 2
                scaled[i][2] = 1500 * distance / (400 + distance ** 2)
                scaled[i][2] += 2 * getAltitude(x, y, 0.01)

        normal = compute_normals(scaled, indices)

        mesh = Mesh(
            shader,
            attributes=dict(
                position=scaled,
                texcoord=((1, 1), (0, 1), (0, 0), (0, 1)),
                normal=normal,
            ),
            index=indices,
        )

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        super().__init__(mesh, tex=texture, tex2=texture2)


class TexturedPlane(Textured):
    """Simple first textured object"""

    def __init__(self, shader, tex_file, tex_file2):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle(
            [
                GL.GL_REPEAT,
                GL.GL_MIRRORED_REPEAT,
                GL.GL_CLAMP_TO_BORDER,
                GL.GL_CLAMP_TO_EDGE,
            ]
        )
        self.filters = cycle(
            [
                (GL.GL_NEAREST, GL.GL_NEAREST),
                (GL.GL_LINEAR, GL.GL_LINEAR),
                (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR),
            ]
        )
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array(((0, 1, 2), (0, 2, 3)), np.uint32)
        mesh = Mesh(
            shader,
            attributes=dict(
                position=scaled, tex_coord=((1, 1), (0, 1), (0, 0), (0, 1))
            ),
            index=indices,
            usage=GL.GL_STATIC_DRAW,
        )

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
    """Simple first textured object"""

    def __init__(self, shader, tex_file, tex_file2):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle(
            [
                GL.GL_REPEAT,
                GL.GL_MIRRORED_REPEAT,
                GL.GL_CLAMP_TO_BORDER,
                GL.GL_CLAMP_TO_EDGE,
            ]
        )
        self.filters = cycle(
            [
                (GL.GL_NEAREST, GL.GL_NEAREST),
                (GL.GL_LINEAR, GL.GL_LINEAR),
                (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR),
            ]
        )
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        positions = []
        tex_coords = []
        for i in range(-150, 151):
            for j in range(-150, 151):
                positions.append((i, j, 10 * self.getAltitude(i, j, 0.33) * self.smoothStep(130, 150, i, j)))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        longueur_base = len(positions)

        # Rectangles extérieurs supérieurs

        for i in range(150, 181):
            for j in range(-150, 151):
                positions.append((i, j, 0))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))
        
        longueur_rectangle = len(positions) - longueur_base

        for i in range(-180, -149):
            for j in range(-150, 151):
                positions.append((i, j, 0))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        for i in range(-150, 151):
            for j in range(-180, -149):
                positions.append((i, j, 0))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        for i in range(-150, 151):
            for j in range(150, 181):
                positions.append((i, j, 0))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        # Coins supérieurs

        positions.append((150, 150, 0))
        tex_coords.append((6, 6))
        for i in range(20):
            positions.append((150 + 30 * np.cos(2 * np.pi * i / 40), 150 + 30 * np.sin(2 * np.pi * i / 40), 0))
            tex_coords.append(((150 + 150 + 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + 150 + 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((150 + 30 * np.cos(2 * np.pi * (i + 1) / 40), 150 + 30 * np.sin(2 * np.pi * (i + 1) / 40), 0))
            tex_coords.append(((150 + 150 + 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + 150 + 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        positions.append((-150, 150, 0))
        tex_coords.append((0, 6))
        for i in range(20):
            positions.append((-150 + 30 * np.cos(2 * np.pi * (i + 20) / 40), 150 - 30 * np.sin(2 * np.pi * (i + 20) / 40), 0))
            tex_coords.append(((150 + -150 + 30 * np.cos(2 * np.pi * (i + 20) / 40)) * 3 / 150, (150 + 150 - 30 * np.sin(2 * np.pi * (i + 20) / 40)) * 3 / 150))
            positions.append((-150 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40), 150 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40), 0))
            tex_coords.append(((150 + -150 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40)) * 3 / 150, (150 + 150 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40)) * 3 / 150))

        positions.append((-150, -150, 0))
        tex_coords.append((0, 0))
        for i in range(20):
            positions.append((-150 - 30 * np.cos(2 * np.pi * i / 40), -150 - 30 * np.sin(2 * np.pi * i / 40), 0))
            tex_coords.append(((150 + -150 - 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + -150 - 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((-150 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -150 - 30 * np.sin(2 * np.pi * (i + 1) / 40), 0))
            tex_coords.append(((150 + -150 - 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + -150 - 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        positions.append((150, -150, 0))
        tex_coords.append((6, 0))
        for i in range(20):
            positions.append((150 + 30 * np.cos(2 * np.pi * i / 40), -150 - 30 * np.sin(2 * np.pi * i / 40), 0))
            tex_coords.append(((150 + 150 + 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + -150 - 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((150 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -150 - 30 * np.sin(2 * np.pi * (i + 1) / 40), 0))
            tex_coords.append(((150 + 150 + 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + -150 - 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        # Coins inférieurs

        positions.append((120, 120, -30))
        tex_coords.append((5.4, 5.4))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), 120 + 30 * np.sin(2 * np.pi * i / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + 120 + 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), 120 + 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + 120 + 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        positions.append((-120, 120, -30))
        tex_coords.append((0.6, 5.4))
        for i in range(20):
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20) / 40), 120 - 30 * np.sin(2 * np.pi * (i + 20) / 40), -30))
            tex_coords.append(((150 + -120 + 30 * np.cos(2 * np.pi * (i + 20) / 40)) * 3 / 150, (150 + 120 - 30 * np.sin(2 * np.pi * (i + 20) / 40)) * 3 / 150))
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40), 120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40), -30))
            tex_coords.append(((150 + -120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40)) * 3 / 150, (150 + 120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40)) * 3 / 150))

        positions.append((-120, -120, -30))
        tex_coords.append((0.6, 0.6))
        for i in range(20):
            positions.append((-120 - 30 * np.cos(2 * np.pi * i / 40), -120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            tex_coords.append(((150 + -120 - 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((-120 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))
            tex_coords.append(((150 + -120 - 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        positions.append((120, -120, -30))
        tex_coords.append(((150 + 5.4) * 3 / 150, (150 + 0.6) * 3 / 150))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        # Bords inférieurs

        for i in range(-120, 121):  # Bord inférieur nord
            positions.append((i, -150, -30))
            tex_coords.append(((150 + i) * 3 / 150, 0))

        
        for i in range(-120, 121): # Bord supérieur nord
            if i < 0:
                positions.append((Math.floor(i*150/120), -180, 0))
                tex_coords.append(((150 + Math.floor(i*150/120)) * 3 / 150, -0.6))
            else :
                positions.append((Math.ceil(i*150/120), -180, 0))
                tex_coords.append(((150 + Math.ceil(i*150/120)) * 3 / 150, -0.6))
            
        for i in range(-120, 121): # Bord inférieur est
            positions.append((150, i, -30))
            tex_coords.append((6, (150 + i) * 3 / 150))
        
        for i in range(-120, 121): # Bord supérieur est
            if i < 0:
                positions.append((180, Math.floor(i*150/120), 0))
                tex_coords.append((6.6, (150 + Math.floor(i*150/120)) * 3 / 150))
            else :
                positions.append((180, Math.ceil(i*150/120), 0))
                tex_coords.append((6.6, (150 + Math.ceil(i*150/120)) * 3 / 150))
            
        for i in range(-120, 121): # Bord inférieur sud
            positions.append((i, 150, -30))
            tex_coords.append(((150 + i) * 3 / 150, 6))

        for i in range(-120, 121):  # Bord supérieur sud
            if i < 0:
                positions.append((Math.floor(i*150/120), 180, 0))
                tex_coords.append(((150 + Math.floor(i*150/120)) * 3 / 150, 6.6))
            else :
                positions.append((Math.ceil(i*150/120), 180, 0))
                tex_coords.append(((150 + Math.ceil(i*150/120)) * 3 / 150, 6.6))

        for i in range(-120, 121):  # Bord inférieur ouest
            positions.append((-150, i, -30))
            tex_coords.append((0, (150 + i) * 3 / 150))
        
        for i in range(-120, 121): # Bord supérieur ouest
            if i < 0:
                positions.append((-180, Math.floor(i*150/120), 0))
                tex_coords.append((-0.6, (150 + Math.floor(i*150/120)) * 3 / 150))
            else :
                positions.append((-180, Math.ceil(i*150/120), 0))
                tex_coords.append((-0.6, (150 + Math.ceil(i*150/120)) * 3 / 150))

        # Rocher inférieur
        for i in range(-120, 121):
            for j in range(-120, 121):
                positions.append((i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        # Rectangles extérieurs inférieurs

        for i in range(120, 151):
            for j in range(-120, 121):
                positions.append((i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        longueur_petit_rectangles = len(positions)

        for i in range(-150, -119):
            for j in range(-120, 121):
                positions.append((i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        for i in range(-120, 121):
            for j in range(-150, -119):
                positions.append((i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))

        for i in range(-120, 121):
            for j in range(120, 151):
                positions.append((i, j, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j)))
                tex_coords.append(((150 + i) * 3 / 150, (150 + j) * 3 / 150))
        
        # Coins inférieurs

        positions.append((120, 120, -30))
        tex_coords.append((5.4, 5.4))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), 120 + 30 * np.sin(2 * np.pi * i / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + 120 + 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), 120 + 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + 120 + 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        positions.append((-120, 120, -30))
        tex_coords.append((0.6, 5.4))
        for i in range(20):
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20) / 40), 120 - 30 * np.sin(2 * np.pi * (i + 20) / 40), -30))
            tex_coords.append(((150 + -120 + 30 * np.cos(2 * np.pi * (i + 20) / 40)) * 3 / 150, (150 + 120 - 30 * np.sin(2 * np.pi * (i + 20) / 40)) * 3 / 150))
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40), 120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40), -30))
            tex_coords.append(((150 + -120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40)) * 3 / 150, (150 + 120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40)) * 3 / 150))

        positions.append((-120, -120, -30))
        tex_coords.append((0.6, 0.6))
        for i in range(20):
            positions.append((-120 - 30 * np.cos(2 * np.pi * i / 40), -120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            tex_coords.append(((150 + -120 - 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((-120 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))
            tex_coords.append(((150 + -120 - 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))

        positions.append((120, -120, -30))
        tex_coords.append((5.4, 0.6))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -120 - 30 * np.sin(2 * np.pi * i / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * i / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * i / 40)) * 3 / 150))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40), -30))
            tex_coords.append(((150 + 120 + 30 * np.cos(2 * np.pi * (i + 1) / 40)) * 3 / 150, (150 + -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)) * 3 / 150))
        
        scaled = 100 * np.array(positions, np.float32)
        indices = []
        for i in range(300):
            for j in range(300):
                indices.append(i * 301 + j)
                indices.append((i + 1) * 301 + j + 1)
                indices.append(i * 301 + j + 1)
                indices.append(i * 301 + j)
                indices.append((i + 1) * 301 + j)
                indices.append((i + 1) * 301 + j + 1)

        # Rectangles extérieurs supérieurs

        for i in range(30):
            for j in range(300):
                indices.append(longueur_base + i * 301 + j)
                indices.append(longueur_base + (i + 1) * 301 + j + 1)
                indices.append(longueur_base + i * 301 + j + 1)
                indices.append(longueur_base + i * 301 + j)
                indices.append(longueur_base + (i + 1) * 301 + j)
                indices.append(longueur_base + (i + 1) * 301 + j + 1)

        longueur_base += longueur_rectangle
        for i in range(30):
            for j in range(300):
                indices.append(longueur_base + i * 301 + j)
                indices.append(longueur_base + (i + 1) * 301 + j + 1)
                indices.append(longueur_base + i * 301 + j + 1)
                indices.append(longueur_base + i * 301 + j)
                indices.append(longueur_base + (i + 1) * 301 + j)
                indices.append(longueur_base + (i + 1) * 301 + j + 1)

        longueur_base += longueur_rectangle
        for i in range(300):
            for j in range(30):
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)
                indices.append(longueur_base + i * 31 + j + 1)
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)

        longueur_base += longueur_rectangle
        for i in range(300):
            for j in range(30):
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)
                indices.append(longueur_base + i * 31 + j + 1)
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)

        # Coins supérieurs
        longueur_base += longueur_rectangle
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
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
                indices.append(longueur_base + i * 241 + j)
                indices.append(longueur_base + i * 241 + j + 1)
                indices.append(longueur_base + (i + 1) * 241 + j + 1)
                indices.append(longueur_base + i * 241 + j)
                indices.append(longueur_base + (i + 1) * 241 + j + 1)
                indices.append(longueur_base + (i + 1) * 241 + j)

        longueur_base += 241 * 241
        longueur_petit_rectangles -= longueur_base

        # Rectangles extérieurs inférieurs

        for i in range(30):
            for j in range(240):
                indices.append(longueur_base + i * 241 + j)
                indices.append(longueur_base + i * 241 + j + 1)
                indices.append(longueur_base + (i + 1) * 241 + j + 1)
                indices.append(longueur_base + (i + 1) * 241 + j)
                indices.append(longueur_base + i * 241 + j)
                indices.append(longueur_base + (i + 1) * 241 + j + 1)

        longueur_base += longueur_petit_rectangles
        for i in range(30):
            for j in range(240):
                indices.append(longueur_base + (i + 1) * 241 + j + 1)
                indices.append(longueur_base + i * 241 + j)
                indices.append(longueur_base + i * 241 + j + 1)
                indices.append(longueur_base + (i + 1) * 241 + j)
                indices.append(longueur_base + i * 241 + j)
                indices.append(longueur_base + (i + 1) * 241 + j + 1)

        longueur_base += longueur_petit_rectangles
        for i in range(240):
            for j in range(30):
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + i * 31 + j + 1)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)
                indices.append(longueur_base + (i + 1) * 31 + j)

        longueur_base += longueur_petit_rectangles
        for i in range(240):
            for j in range(30):
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + i * 31 + j + 1)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)
                indices.append(longueur_base + i * 31 + j)
                indices.append(longueur_base + (i + 1) * 31 + j + 1)
                indices.append(longueur_base + (i + 1) * 31 + j)

        longueur_base += longueur_petit_rectangles

        # Coins inférieurs
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i)

        longueur_base += 41
        for i in range(20):
            indices.append(longueur_base)
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)

        longueur_base += 41

        normal = compute_normals(positions, indices)

        indices = np.array(indices, np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=tex_coords), index=indices)

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

        if tx + ty == 0:
            return 1

        t = np.sqrt(tx * tx + ty * ty)

        if t >= 1:
            return 0

        return 2 * Math.pow(t, 3) - 3 * Math.pow(t, 2) + 1

    def getAltitude(self, x, y, puissance):
        # return np.sin(x+np.cos(y))+0.5 * np.sin(2+y+np.cos(2 * x))+0.4
        nx = x / 100
        ny = y / 100
        out = 2 * noise1([nx, ny])
        out += 0.5 * noise2([nx, ny])
        out += 0.25 * noise3([nx, ny])
        if out <= 0:
            return 0
        e = out / (1 + 0.5 + 0.25)
        return Math.pow(e, puissance)


def create_grid(size):
    """Create grid for terrain generation"""
    positions = []
    indices = []

    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            positions.append((i, j, 0))
            current = (i + size) * (2 * size + 1) + j + size
            if i > -size and j == -size:
                indices.append((current - (2 * size + 1),
                               current, current - 2 * size))
            elif i > -size and j == size:
                indices.append(
                    (current, current - (2 * size + 1), current - 1))
            elif i > -size:
                indices.append(
                    (current - 1, current, current - (2 * size + 1)))
                indices.append((current, current - 2 * size,
                               current - (2 * size + 1)))
    return (positions, indices)


class WaterPlane(Textured):
    """Water textured object"""

    def __init__(self, shader):
        # setup plane mesh to be textured

        self.shader = shader
        self.tex = Texture("water.jpg", GL.GL_REPEAT,
                           GL.GL_NEAREST, GL.GL_NEAREST)

        self.positions, self.indices = np.array(create_grid(50), dtype=tuple)
        self.normal = compute_normals(self.positions, self.indices)
        self.mesh = Mesh(
            shader,
            attributes=dict(
                position=self.positions,
                tex_coord=[((self.positions[i][0] + 50)/100, (self.positions[i][1] + 50)/100)
                           for i in range(len(self.positions))],
                normal=self.normal,
            ),
            index=self.indices,
            usage=GL.GL_DYNAMIC_DRAW,
        )
        super().__init__(self.mesh, tex=self.tex)


# -------------- main program and scene setup --------------------------------


def main():
    """create a window, add scene objects, then run rendering loop"""
    viewer = Viewer()
    shader_color = Shader("fog.vert", "fog.frag")
    water_shader = Shader("water.vert", "water.frag")
    shader = Shader("texture.vert", "texture.frag")
    shader_color = Shader("color.vert", "color.frag")
    skybox_shader = Shader("skybox.vert", "skybox.frag")
    shader_volcano = Shader("volcano.vert", "volcano.frag")

    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])

    viewer.add(Skybox(skybox_shader, ["cubemaps/right.png", "cubemaps/left.png",
                                      "cubemaps/top.png", "cubemaps/bottom.png", "cubemaps/front.png", "cubemaps/back.png"]))
    viewer.add(Floor(shader, "cayu.jpg", "flowers.png"))
    viewer.add(Volcano(shader, "cayu.jpg", "flowers.png"))
    if len(sys.argv) != 2:
        print(
            "Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in format supported by assimp."
            % (sys.argv[0],)
        )
    # start rendering loop
    viewer.run()


if __name__ == "__main__":
    main()  # main function keeps variables locally scoped
