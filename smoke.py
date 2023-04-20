#!/usr/bin/env python3

from OpenGL import GL

import random
from core import Mesh, Node
from transform import identity
import numpy as np

# screen_width = 750
# screen_height = 650

# screen = pygame.display.set_mode((screen_width, screen_height))

# clock = pygame.time.Clock()
FPS = 60


class SmokeParticle(Mesh):
    """Particule de fumée seule"""
    def __init__(self, shader, position=-np.array(((1, 1, 1), (2, 1, 3), (3, 1, 2)), 'f'), 
                 velocity=np.array((0.,0.,0.02))):
        # ---------- Création du mesh -------
        #! TODO : faire une pseudo etoile
        self.position = position
        color = np.array(((0, 0, 0), (0, 0, 0), (0, 0, 0)), 'f')
        self.color = (0.5,0.5,0.5)


        self.scale_k = 1 #size of the particle
        self.alpha = 255 #oppacity of particule
        self.alpha_rate = 2 #how fast oppacity increases
        self.alive = True #if it should be drawn or not
        self.velocity = velocity
        self.k = 0.01 * random.random() * random.choice([-1,1]) #how fast x velocity changes and in which direction
        
        attributes = dict(position=self.position, color=color, alpha=self.alpha)
        super().__init__(shader, attributes=attributes)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        print(self.position)
        super().draw(primitives=primitives, global_color=self.color, 
                     attributes=dict(position=self.position) , **uniforms)

    def update(self):
        if self.alive == False:
            pass
        self.position += self.velocity
        # -- decrease alpha de alpha_rate
        self.alpha -= self.alpha_rate
        # -- if dead
        if self.alpha <= 0:
            self.alpha = 0
            self.alive = False
        # -- decrease alpha_rate
        # self.alpha_rate -= 0.1
        # if self.alpha_rate < 1.5:
        #     self.alpha_rate = 1.5
        # -- decsrease velosity
        # self.velocity[0] += self.k
        # self.velocity[1] += self.k
        # self.velocity*= 0.8
        #self.scale_k += 0.005
        #self.position *= self.scale_k

   
class Smoke():
    """Smoke with SmokeParticles héritant de Node pour faciliter la gestion des enfants"""
    def __init__(self, shader, position=-np.array(((1, 1, 1), (2, 1, 3), (3, 1, 2)),'f')):
        self.shader = shader
        self.position = position #départ des particules
        self.particles = []
        # self.frames = 0 #rate at which particles are added

    def update(self):
        self.particles.append(SmokeParticle(self.shader))
        self.particles = [i for i in self.particles if i.alive]
        # self.frames += 1
        # if self.frames % 2 == 0:
        #     self.frames = 0
        for i in self.particles:
            i.update()

    def draw(self, primitives=GL.GL_TRIANGLES, **other_uniforms):
        for i in self.particles:
            i.draw(primitives=primitives,**other_uniforms)
