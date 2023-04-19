""" Volcano object """

import math as Math

import numpy as np
from OpenGL import GL
from perlin_noise import PerlinNoise

from core import Mesh
from texture import Texture, Textured
from transform import compute_normals, create_grid

noise0 = PerlinNoise(octaves=1, seed=1)
noise1 = PerlinNoise(octaves=3, seed=3)
noise2 = PerlinNoise(octaves=6, seed=2)


def get_altitude(x, y, puissance):
    """Returns the altitude computed with perlin noise"""
    nx = x / 100
    ny = y / 100
    out = 5 * noise0([nx, ny])
    out += 3 * noise1([nx, ny])
    out += 2 * noise2([nx, ny])
    if out <= 0:
        return out
    return Math.pow(out, puissance)


class Volcano(Textured):
    """Simple first textured object"""

    def __init__(self, shader, tex_file, tex_file2):
        self.taille = 50

        self.wrap = GL.GL_REPEAT
        self.filter = (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        self.file = tex_file
        self.file2 = tex_file2

        base_coords, indices = create_grid(self.taille)
        base_coords = 2 * base_coords

        for i, point in enumerate(base_coords):
            x_pos, y_pos = i % (2 * self.taille + 1), i // (2 * self.taille + 1)
            if x_pos == self.taille and y_pos == self.taille:
                point[2] = base_coords[i - 1][2]
            else:
                distance = (
                    0.4
                    * (np.sqrt((y_pos - self.taille) ** 2 + (x_pos - self.taille) ** 2))
                    ** 2
                )
                point[2] = 2000 * distance / (500 + distance**2)
                point[2] += 2 * get_altitude(x_pos, y_pos, 0.01)

        normal = compute_normals(base_coords, indices)

        mesh = Mesh(
            shader,
            attributes={
                "position": base_coords,
                "normal": normal,
                "tex_coord": [
                    (
                        (base_coords[i][0] + self.taille) / (2 * self.taille),
                        (base_coords[i][1] + self.taille) / (2 * self.taille),
                    )
                    for i in range(len(base_coords))
                ],
            },
            index=indices,
        )

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        texture3 = Texture("img/terre.jpeg", self.wrap, *self.filter)
        super().__init__(mesh, tex=texture, tex2=texture2, tex3=texture3)
