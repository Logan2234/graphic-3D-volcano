""" Volcano object """

import math as Math

import numpy as np
from OpenGL import GL
from perlin_noise import PerlinNoise

from core import Mesh
from texture import Texture, Textured
from transform import compute_normals, create_grid

noise1 = PerlinNoise(octaves=3, seed=3)
noise2 = PerlinNoise(octaves=6, seed=2)


def get_altitude(x, y, puissance, taille):
    """Returns the altitude computed with perlin noise"""
    if (
        x - taille >= taille - 1
        or y - taille >= taille - 1
        or x - taille <= -taille + 1
        or y - taille <= -taille + 1
    ):
        return 0
    nx = x / 100
    ny = y / 100
    out = 4 * noise1([nx, ny])
    out += 3 * noise2([nx, ny])
    if out <= 0:
        return out
    return Math.pow(out, puissance)


def smooth(points, size):
    """Applique une fonction de lissage sur un ensemble de points 3D."""
    for i in range(2 * size + 1, len(points) - (2 * size + 1)):
        if i % (2 * size + 1) == 0:
            continue
        if i % (2 * size + 1) == 2 * size:
            continue

        voisins_directs = 2 * np.array(
            [
                2 * points[i],
                points[i - 1],
                points[i + 1],
                points[i + (2 * size + 1)],
                points[i - (2 * size + 1)],
            ]
        )
        voisins_diagonale = np.array(
            [
                points[i - (2 * size)],
                points[i - (2 * size + 2)],
                points[i + (2 * size)],
                points[i + (2 * size + 2)],
            ]
        )

        points[i] = (
            np.sum(np.concatenate((voisins_diagonale, voisins_directs)), axis=0) / 16
        )


class Volcano(Textured):
    """Simple first textured object"""

    def __init__(self, shader, tex_file, tex_file2):
        self.taille = 80

        self.wrap = GL.GL_REPEAT
        self.filter = (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        self.file = tex_file
        self.file2 = tex_file2

        def formula(x_pos, y_pos):
            distance = 0.4 * (np.sqrt(y_pos**2 + x_pos**2)) ** 2
            return 5000 * distance / (1500 + distance**2) + 2 * get_altitude(
                x_pos + self.taille, y_pos + self.taille, 0.01, self.taille
            )

        base_coords, indices = create_grid(self.taille, formula=formula)
        base_coords = 2.5 * base_coords
        smooth(base_coords, self.taille)

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
