"""Skybox object"""

import numpy as np

from core import Mesh
from texture import TextureCubeMap, Textured


class Skybox(Textured):
    """Skybox class"""

    def __init__(self, shader, faces):
        cubemap_texture = TextureCubeMap(faces)
        skybox_vertices = np.array(
            [
                # positions
                (-1.0, 1.0, -1.0),
                (-1.0, -1.0, -1.0),
                (1.0, -1.0, -1.0),
                (1.0, -1.0, -1.0),
                (1.0, 1.0, -1.0),
                (-1.0, 1.0, -1.0),
                (1.0, -1.0, -1.0),
                (1.0, -1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, 1.0, -1.0),
                (1.0, -1.0, -1.0),
                (-1.0, -1.0, 1.0),
                (-1.0, -1.0, -1.0),
                (-1.0, 1.0, -1.0),
                (-1.0, 1.0, -1.0),
                (-1.0, 1.0, 1.0),
                (-1.0, -1.0, 1.0),
                (-1.0, -1.0, 1.0),
                (-1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, -1.0, 1.0),
                (-1.0, -1.0, 1.0),
                (-1.0, 1.0, -1.0),
                (1.0, 1.0, -1.0),
                (1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (-1.0, 1.0, 1.0),
                (-1.0, 1.0, -1.0),
                (-1.0, -1.0, -1.0),
                (-1.0, -1.0, 1.0),
                (1.0, -1.0, -1.0),
                (1.0, -1.0, -1.0),
                (-1.0, -1.0, 1.0),
                (1.0, -1.0, 1.0),
            ],
            np.float32,
        )
        skybox = Mesh(shader, attributes=dict(position=skybox_vertices))
        super().__init__(skybox, skybox=cubemap_texture)
