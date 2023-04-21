#!/usr/bin/env python3

from OpenGL import GL

import random
from core import Mesh, Shader
import numpy as np

# screen_width = 750
# screen_height = 650

# screen = pygame.display.set_mode((screen_width, screen_height))

# clock = pygame.time.Clock()
FPS = 60


class SmokeParticle(Mesh):
    """Particule de fumée seule"""
    def __init__(self, position=np.array((0,0,0)),
                 velocity=np.array((0,0,0.2 + random.randint(1,10)/10), 'f')):
        # ---------- Création du mesh -------
        # ---- Points de l'étoile ----
        A = (0,0,1)+position
        B = (1,0,0)+position
        C = (0,0,-1)+position
        D = (-1,0,0)+position
        E = (0,1,0)+position
        F = (0,-1,0)+position

        self.position = np.array((A,B,C, A,C,B,
                                A,F,C, A,C,F,
                                A,C,E, A,E,C,
                                A,D,C, A,C,D), 'f')
        color = np.full((24,3), .4,'f')
        self.color = (0.2,0.2,0.2)

        # --------- Init des autres champs --------------
        self.scale_k = 0.6 #size of the particle
        self.alpha = 255 #oppacity of particule
        self.alpha_rate = 1 #how fast oppacity increases => and how fast it will die
        self.alive = True #if it should be drawn or not
        self.velocity = velocity
        self.k = 0.01 * random.random() * random.choice([-1,1]) #how fast x velocity changes and in which direction
        
        attributes = dict(position=self.position, color=color, alpha=self.alpha)
        super().__init__(Shader("smoke.vert", "smoke.frag"), attributes=attributes)

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, 
                     attributes=dict(position=self.position), **uniforms)

    def update(self):
        """Evolution des particules"""
        if not self.alive:
            return
        self.position += self.velocity
        # -- decrease alpha de alpha_rate
        self.alpha -= self.alpha_rate
        # -- if dead
        if self.alpha <= 0:
            self.alpha = 0
            self.alive = False
        # -- decrease alpha_rate
        self.alpha_rate = max(1.5, self.alpha_rate - 0.1)

        # -- decrease velocity
        self.velocity = np.array((self.velocity[0] + self.k,
            self.velocity[1] + self.k,
            self.velocity[2]), 'f')
        # -- resize de la particule quand elle se déplace
        self.position *= self.scale_k
        self.scale_k += 0.0002 

   
class Smoke():
    """Smoke with SmokeParticles héritant de Node pour faciliter la gestion des enfants"""
    def __init__(self, position=-np.array((0,0,0),'f')):
        self.position = position #offset de sdépart des particules
        self.particles = []
        self.frames = 0 #current frame
        self.rate = 10 #rate at which particles are added (1 out of 5 frames)

    def update(self):
        """Evolution de la fumée"""
        self.particles = [i for i in self.particles if i.alive] #on fait le tri
        self.frames += 1 #on avance d'un frame
        if self.frames % self.rate == 0: #on rajoute une particule tous les rate
            self.frames = 0
            # print("+1", len(self.particles))
            self.particles.append(SmokeParticle(position=self.position.copy()))


    def draw(self, primitives=GL.GL_TRIANGLES, **other_uniforms):
        """Dessin de la fumée"""
        self.update() #mise à jour du nb de particules
        for i in self.particles:
            i.update() #mise à jour des particules restantes
            i.draw(primitives=primitives,**other_uniforms) #dessin des particules
