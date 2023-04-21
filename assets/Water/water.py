""" Water object """

from OpenGL import GL

from core import Mesh
from texture import Texture, Textured
from transform import compute_normals, create_grid


class Water(Textured):
    """Water textured object"""

    def __init__(self, shader):
        # setup plane mesh to be textured
        self.taille = 75
        self.scale = 15
        self.shader = shader
        self.tex = Texture("img/water.jpg", GL.GL_REPEAT, GL.GL_NEAREST, GL.GL_NEAREST)

        self.positions, self.indices = create_grid(self.taille, True, -40)
        self.positions = self.positions * self.scale
        self.normal = compute_normals(self.positions, self.indices)
        self.mesh = Mesh(
            shader,
            attributes={
                "position": self.positions,
                "tex_coord": [
                    (
                        (self.positions[i][0] + self.scale * self.taille)
                        / (2 * self.scale * self.taille),
                        (self.positions[i][1] + self.scale * self.taille)
                        / (2 * self.scale * self.taille),
                    )
                    for i in range(len(self.positions))
                ],
                "normal": self.normal,
            },
            index=self.indices,
            usage=GL.GL_DYNAMIC_DRAW,
        )
        super().__init__(self.mesh, tex=self.tex)
