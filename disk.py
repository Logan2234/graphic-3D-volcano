""" Disk used to create the lava """

import numpy as np  # all matrix manipulations & OpenGL args
import OpenGL.GL as GL  # standard Python OpenGL wrapper

from core import Mesh
from texture import Texture, Textured
from transform import compute_normals


class Disk(Textured):
    """Disk for inside the volcano"""

    def __init__(self, shader, tex_file, radius, height):
        self.wrap, self.filter = GL.GL_REPEAT, (
            GL.GL_LINEAR,
            GL.GL_LINEAR_MIPMAP_LINEAR,
        )
        self.file = tex_file

        base_coords = [(0, 0, height)]
        tex_coords = [(0, 0)]

        for i in range(0, 40):
            base_coords.append(
                (
                    radius * np.cos(2 * np.pi * i / 40),
                    radius * np.sin(2 * np.pi * i / 40),
                    height,
                )
            )
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

        mesh = Mesh(
            shader,
            attributes=dict(
                position=scaled,
                tex_coord=tex_coords,
                normal=compute_normals(scaled, indices),
            ),
            index=np.array(indices, np.uint32),
        )

        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, tex=texture)
