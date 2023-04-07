"""Camera module redefining our own camera"""

import numpy as np
import glfw                         # lean window system wrapper for OpenGL
from transform import lookat, normalized, perspective, vec


class Camera:
    """New camera class because apparently trackball wasn't... good enough :P"""

    def __init__(self):
        # camera Attributes
        self.position = vec(-3.0, 0.0, 3.0)
        self.front = vec(0.0, 0.0, 0.0)
        self.up = vec(0.0, 0.0, 0.0)
        self.right = vec(0.0, 0.0, 0.0)
        self.world_up = vec(0.0, 0.0, 1.0)
        # euler Angles
        self.yaw = 0
        self.pitch = 0
        # camera options
        self.movement_speed = 1
        self.mouse_sensitivity = 0.1
        self.zoom = 50
        self.update_camera_vectors()

    def camera_position(self):
        """Returns the camera position"""
        return self.position

    def get_view_matrix(self):
        """Returns the view matrix"""
        return lookat(self.position, self.position + self.front, self.up)

    def projection_matrix(self, win_size):
        """Returns the projection matrix"""
        return perspective(self.zoom, win_size[0] / win_size[1], 0.1, 1000)

    def process_mouvement(self, win):
        """Allows the camera translate"""
        if glfw.get_key(win, glfw.KEY_W):
            self.position += self.front * self.movement_speed
        if glfw.get_key(win, glfw.KEY_S):
            self.position -= self.front * self.movement_speed
        if glfw.get_key(win, glfw.KEY_A):
            self.position -= self.right * self.movement_speed
        if glfw.get_key(win, glfw.KEY_D):
            self.position += self.right * self.movement_speed
        if glfw.get_key(win, glfw.KEY_SPACE):
            self.position += self.world_up * self.movement_speed
        if glfw.get_key(win, glfw.KEY_C):
            self.position -= self.world_up * self.movement_speed

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        """Allows the camera to rotate around"""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        # make sure that when pitch is out of bounds, screen doesn't get flipped
        if constrain_pitch:
            if self.pitch > 90:
                self.pitch = 90
            if self.pitch < -90:
                self.pitch = -90

        # update Front, Right and Up Vectors using the updated Euler angles
        self.update_camera_vectors()

    def process_mouse_scroll(self, yoffset):
        """Zoom effect using mouse scroll"""
        self.zoom -= float(yoffset)
        if self.zoom < 1.0:
            self.zoom = 1.0
        if self.zoom > 50.0:
            self.zoom = 50.0

    def update_camera_vectors(self):
        """Compute all the vectors after a rotation"""
        # calculate the new Front vector
        self.front = vec(
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            -np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)))
        self.front = normalized(self.front)
        # also re-calculate the Right and Up vector
        self.right = normalized(np.cross(self.front, self.world_up))
        self.up = normalized(np.cross(self.right, self.front))
