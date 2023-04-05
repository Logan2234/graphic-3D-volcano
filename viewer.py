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
                positions.append((i, 10 * self.getAltitude(i, j, 0.33) * self.smoothStep(130, 150, i, j), j))

        longueur_base = len(positions)

        # Rectangles extérieurs supérieurs

        for i in range(150, 181):
            for j in range(-150, 151):
                positions.append((i, 0, j))
        
        longueur_rectangle = len(positions) - longueur_base
        
        for i in range(-180, -149):
            for j in range(-150, 151):
                positions.append((i, 0, j))

        for i in range(-150, 151):
            for j in range(-180, -149):
                positions.append((i, 0, j))

        for i in range(-150, 151):
            for j in range(150, 181):
                positions.append((i, 0, j))

        # Coins supérieurs
                
        positions.append((150, 0, 150))
        for i in range(20):
            positions.append((150 + 30 * np.cos(2 * np.pi * i / 40), 0, 150 + 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((150 + 30 * np.cos(2 * np.pi * (i + 1) / 40), 0, 150 + 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        positions.append((-150, 0, 150))
        for i in range(20):
            positions.append((-150 + 30 * np.cos(2 * np.pi * (i + 20) / 40), 0, 150 - 30 * np.sin(2 * np.pi * (i + 20) / 40)))
            positions.append((-150 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40), 0, 150 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40)))

        positions.append((-150, 0, -150))
        for i in range(20):
            positions.append((-150 - 30 * np.cos(2 * np.pi * i / 40), 0, -150 - 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((-150 - 30 * np.cos(2 * np.pi * (i + 1) / 40), 0, -150 - 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        positions.append((150, 0, -150))
        for i in range(20):
            positions.append((150 + 30 * np.cos(2 * np.pi * i / 40), 0, -150 - 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((150 + 30 * np.cos(2 * np.pi * (i + 1) / 40), 0, -150 - 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        # Coins inférieurs
                
        positions.append((120, -30, 120))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -30, 120 + 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -30, 120 + 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        positions.append((-120, -30, 120))
        for i in range(20):
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20) / 40), -30, 120 - 30 * np.sin(2 * np.pi * (i + 20) / 40)))
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40), -30, 120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40)))

        positions.append((-120,-30, -120))
        for i in range(20):
            positions.append((-120 - 30 * np.cos(2 * np.pi * i / 40), -30, -120 - 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((-120 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -30, -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        positions.append((120, -30, -120))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -30, -120 - 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -30, -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        # Bords inférieurs

        for i in range(-120, 121): # Bord inférieur nord
            positions.append((i, -30, -150))
        
        for i in range(-120, 121): # Bord supérieur nord
            if i < 0:
                positions.append((Math.floor(i*150/120), 0, -180))
            else :
                positions.append((Math.ceil(i*150/120), 0, -180))
            
        for i in range(-120, 121): # Bord inférieur est
            positions.append((150, -30, i))
        
        for i in range(-120, 121): # Bord supérieur est
            if i < 0:
                positions.append((180, 0, Math.floor(i*150/120)))
            else :
                positions.append((180, 0, Math.ceil(i*150/120)))
            
        for i in range(-120, 121): # Bord inférieur sud
            positions.append((i, -30, 150))

        for i in range(-120, 121): # Bord supérieur sud
            if i < 0:
                positions.append((Math.floor(i*150/120), 0, 180))
            else :
                positions.append((Math.ceil(i*150/120), 0, 180))

        for i in range(-120, 121): # Bord inférieur ouest
            positions.append((-150, -30, i))
        
        for i in range(-120, 121): # Bord supérieur ouest
            if i < 0:
                positions.append((-180, 0, Math.floor(i*150/120)))
            else :
                positions.append((-180, 0, Math.ceil(i*150/120)))

        # Rocher inférieur
        for i in range(-120, 121):
            for j in range(-120, 121):
                positions.append((i, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j), j))

        # Rectangles extérieurs inférieurs
 
        for i in range(120, 151):
            for j in range(-120, 121):
                positions.append((i, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j), j))

        longueur_petit_rectangles = len(positions)
        
        for i in range(-150, -119):
            for j in range(-120, 121):
                positions.append((i, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j), j))

        for i in range(-120, 121):
            for j in range(-150, -119):
                positions.append((i, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j), j))

        for i in range(-120, 121):
            for j in range(120, 151):
                positions.append((i, -30 - 150 * self.getAltitude(i, j, 0.15) * self.smoothStep(0, 150, i, j), j))
        
        # Coins inférieurs
                
        positions.append((120, -30, 120))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -30, 120 + 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -30, 120 + 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        positions.append((-120, -30, 120))
        for i in range(20):
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20) / 40), -30, 120 - 30 * np.sin(2 * np.pi * (i + 20) / 40)))
            positions.append((-120 + 30 * np.cos(2 * np.pi * (i + 20 + 1) / 40), -30, 120 - 30 * np.sin(2 * np.pi * (i + 20 + 1) / 40)))

        positions.append((-120,-30, -120))
        for i in range(20):
            positions.append((-120 - 30 * np.cos(2 * np.pi * i / 40), -30, -120 - 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((-120 - 30 * np.cos(2 * np.pi * (i + 1) / 40), -30, -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)))

        positions.append((120, -30, -120))
        for i in range(20):
            positions.append((120 + 30 * np.cos(2 * np.pi * i / 40), -30, -120 - 30 * np.sin(2 * np.pi * i / 40)))
            positions.append((120 + 30 * np.cos(2 * np.pi * (i + 1) / 40), -30, -120 - 30 * np.sin(2 * np.pi * (i + 1) / 40)))
        
        scaled = 100 * np.array(positions, np.float32)
        indices = []
        for i in range(300):
            for j in range(300):
                indices.append(i*301+j)
                indices.append(i*301+j+1)
                indices.append((i+1)*301+j+1)
                indices.append(i*301+j)
                indices.append((i+1)*301+j+1)
                indices.append((i+1)*301+j)

        # Rectangles extérieurs supérieurs

        for i in range(30):
            for j in range(300):
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + i*301+j+1)
                indices.append(longueur_base + (i+1)*301+j+1)
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + (i+1)*301+j+1)
                indices.append(longueur_base + (i+1)*301+j)

        longueur_base += longueur_rectangle
        for i in range(30):
            for j in range(300):
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + i*301+j+1)
                indices.append(longueur_base + (i+1)*301+j+1)
                indices.append(longueur_base + i*301+j)
                indices.append(longueur_base + (i+1)*301+j+1)
                indices.append(longueur_base + (i+1)*301+j)

        longueur_base += longueur_rectangle
        for i in range(300):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + (i+1)*31+j)

        longueur_base += longueur_rectangle
        for i in range(300):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + (i+1)*31+j)

        # Coins supérieurs
        longueur_base += longueur_rectangle
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
        for i in range(20):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i - 164)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 - 164)
            indices.append(longueur_base + i)

        longueur_base += 41

        for i in range(240):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1 + 241)

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
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 + 241)
            indices.append(longueur_base + i + 241)

        longueur_base += 241 * 2
        for i in range(240):
            indices.append(longueur_base + i)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 241)
            indices.append(longueur_base + i + 1)
            indices.append(longueur_base + i + 1 + 241)
            indices.append(longueur_base + i + 241)
        longueur_base += 241 * 2

        for i in range(240):
            for j in range(240):
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + i*241+j+1)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)

        longueur_base += 241 * 241
        longueur_petit_rectangles -= longueur_base

        # Rectangles extérieurs inférieurs

        for i in range(30):
            for j in range(240):
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + i*241+j+1)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)

        longueur_base += longueur_petit_rectangles
        for i in range(30):
            for j in range(240):
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)
                indices.append(longueur_base + i*241+j+1)
                indices.append(longueur_base + i*241+j)
                indices.append(longueur_base + (i+1)*241+j)
                indices.append(longueur_base + (i+1)*241+j+1)

        longueur_base += longueur_petit_rectangles
        for i in range(240):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)

        longueur_base += longueur_petit_rectangles
        for i in range(240):
            for j in range(30):
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)
                indices.append(longueur_base + i*31+j+1)
                indices.append(longueur_base + i*31+j)
                indices.append(longueur_base + (i+1)*31+j)
                indices.append(longueur_base + (i+1)*31+j+1)

        longueur_base += longueur_petit_rectangles

        # Coins inférieurs
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

        

        indices = np.array(indices, np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=((1, 1), (0, 1), (0, 0), (0, 1))), index=indices)

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
