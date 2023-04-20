#!/usr/bin/env python3
import math as Math
from itertools import cycle

import numpy as np  # all matrix manipulations & OpenGL args
import OpenGL.GL as GL  # standard Python OpenGL wrapper
from perlin_noise import PerlinNoise  # pip install perlin-noise

from core import Mesh
from texture import Texture, Textured

class Disk(Textured):
     """ Disk for inside the volcano """
     def __init__(self, shader, tex_file, tex_file2, radius, height):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        base_coords = [(0, 0, height)]
        tex_coords = [(0, 0)]

        for i in range(0, 40):
            base_coords.append((radius * np.cos(2 * np.pi * i / 40), radius * np.sin(2 * np.pi * i / 40), height))
            tex_coords.append((np.cos(2 * np.pi * i / 40), np.sin(2 * np.pi * i / 40)))


        # setup plane mesh to be textured
        scaled = np.array(base_coords, np.float32)
        indices = []

        for i in range(1, 40):
            indices.append(0)
            indices.append(i)
            indices.append(i + 1)
        
        indices.append(0)
        indices.append(40)
        indices.append(1)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=tex_coords), index=np.array(indices, np.uint32))

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture, tex2=texture2)