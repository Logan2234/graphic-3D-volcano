#!/usr/bin/env python3
from texture import Texture, Textured
import math as Math
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
from core import Mesh
import numpy as np                  # all matrix manipulations & OpenGL args
from perlin_noise import PerlinNoise # pip install perlin-noise

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)

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

        for i in range(-120, 121): # Bord inférieur nord
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

        for i in range(-120, 121): # Bord supérieur sud
            if i < 0:
                positions.append((Math.floor(i*150/120), 180, 0))
                tex_coords.append(((150 + Math.floor(i*150/120)) * 3 / 150, 6.6))
            else :
                positions.append((Math.ceil(i*150/120), 180, 0))
                tex_coords.append(((150 + Math.ceil(i*150/120)) * 3 / 150, 6.6))

        for i in range(-120, 121): # Bord inférieur ouest
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

        if (tx + ty == 0):
            return 1
        
        t = np.sqrt(tx*tx + ty*ty)

        if t >= 1:
            return 0

        return 2 * Math.pow(t, 3) - 3 * Math.pow(t, 2) + 1
        
    def getAltitude(self, x, y, puissance):
        #return np.sin(x+np.cos(y))+0.5 * np.sin(2+y+np.cos(2 * x))+0.4
        nx = x/100
        ny = y/100
        out = 2*noise1([nx, ny])
        out += 0.5*noise2([nx, ny])
        out += 0.25*noise3([nx, ny])
        if out <= 0:
            return 0
        e = out / (1 + 0.5 + 0.25)
        return Math.pow(e, puissance)
