"""Camera module redefining our own camera"""

import glfw  # lean window system wrapper for OpenGL
import numpy as np

from transform import lookat, normalized, perspective, vec

CAMERA_NORMAL_MOVE = 0
CAMERA_ROTATE_MOVE = 1
CAMERA_PAN_MOVE = 2


class Camera:
    """New camera class because apparently trackball wasn't... good enough :P"""

    def __init__(self):
        # camera Attributes
        self.position = vec(-150, 200, 300)
        self.front = vec(0, 0, 0)
        self.up = vec(0, 0, 0)
        self.right = vec(0, 0, 0)
        # self.position = vec(-910.0, -1050.0, 0)
        # self.front = vec(0.6, 0.76, -0.2)
        # self.up = vec(0.14, 0.17, 0.97)
        # self.right = vec(0.78, -0.6, 0.0)
        self.world_up = vec(0.0, 0.0, 1.0)
        # euler Angles
        self.yaw = 60
        self.pitch = -25
        # camera options
        self.movement_speed = 20
        self.mouse_sensitivity = 0.1
        self.zoom = 50
        self.update_camera_vectors()

    def camera_position(self):
        """Returns the camera position"""
        return self.position

    def get_view_matrix(self):
        """Returns the view matrix"""
        # print(f"{self.position},{self.front},{self.up},{self.right}\n")
        return lookat(self.position, self.position + self.front, self.up)

    def projection_matrix(self, win_size):
        """Returns the projection matrix"""
        return perspective(self.zoom, win_size[0] / win_size[1], 0.1, 100000)

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

    def process_mouse_movement(self, xoffset, yoffset, move_mode, constrain_pitch=True):
        """Allows the camera to rotate around"""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        if move_mode == CAMERA_ROTATE_MOVE:
            #     TODO
            return
        elif move_mode == CAMERA_PAN_MOVE:
            self.position = np.add(
                self.position,
                vec(
                    -xoffset * np.sin(np.radians(self.yaw)),
                    -xoffset * np.cos(np.radians(self.yaw)),
                    yoffset,
                ),
            )
        else:
            self.yaw += xoffset
            self.pitch += yoffset

            # make sure that when pitch is out of bounds, screen doesn't get flipped
            if constrain_pitch:
                self.pitch = min(self.pitch, 90)
                self.pitch = max(self.pitch, -90)

            # update Front, Right and Up Vectors using the updated Euler angles
            self.update_camera_vectors()

    def process_mouse_scroll(self, yoffset):
        """Zoom effect using mouse scroll"""
        self.zoom -= float(yoffset)
        self.zoom = max(self.zoom, 1.0)
        self.zoom = min(self.zoom, 50.0)

    def update_camera_vectors(self):
        """Compute all the vectors after a rotation"""
        # calculate the new Front vector
        self.front = vec(
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            -np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
        )
        self.front = normalized(self.front)
        # also re-calculate the Right and Up vector
        self.right = normalized(np.cross(self.front, self.world_up))
        self.up = normalized(np.cross(self.right, self.front))

    def change_speed(self, win):
        """Change the speed of the camera accordding to the key pressed"""
        if glfw.get_key(win, glfw.KEY_KP_ADD):
            self.movement_speed += 1
        elif glfw.get_key(win, glfw.KEY_KP_SUBTRACT):
            self.movement_speed -= 1
        print("Speed changed to " + str(self.movement_speed))
