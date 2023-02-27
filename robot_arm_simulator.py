import os
import sys
import copy
import math
from collections import deque

import pygame
from pygame.locals import *

import array_math as np
import game.kinematics
from game.ui_text_button import UTTextButton
from robot_arm_routine import robot_arm_routine


def identity_matrix():
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def rotate_x_matrix(radians):
    """Return matrix for rotating about the x-axis by 'radians' radians"""

    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])


def rotate_y_matrix(radians):
    """Return matrix for rotating about the y-axis by 'radians' radians"""

    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


def rotate_z_matrix(radians):
    """Return matrix for rotating about the z-axis by 'radians' radians"""

    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def translation_matrix(dx=0, dy=0, dz=0):
    """Return matrix for translation along vector (dx, dy, dz)."""

    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]])


def rotate2d(pos, radian):
    x, y = pos
    s, c = math.sin(radian), math.cos(radian)
    return x * c - y * s, y * c + x * s


class Cam:
    def __init__(self, panel_dimensions, pos=(0, 0, 0), rot=(0, 0)):
        self.panel_dimensions = panel_dimensions
        self.pos = list(pos)
        self.rot = list(rot)
        self.rot[1] = math.pi / 4

        self.camera_control_active = False

    def events(self, event: pygame.event.Event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if (
                    mouse_pos[0] < self.panel_dimensions[0]
                    and mouse_pos[1] < self.panel_dimensions[1]
                ):
                    self.camera_control_active = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1 and self.camera_control_active:
                self.camera_control_active = False
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
        if self.camera_control_active:
            if event.type == MOUSEMOTION:
                self.calculate_camera_movement(event.rel)

    def calculate_camera_movement(self, mouse_move):
        x, y = mouse_move
        speed = 3.0
        dist_from_origin = math.sqrt(self.pos[0] ** 2 + self.pos[2] ** 2)
        move_length = x * speed
        angle = 0
        if abs(move_length) > 0.0:
            a = dist_from_origin
            c = dist_from_origin
            b = move_length
            angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        comp_x, comp_y = math.sin(self.rot[0] + angle), math.cos(self.rot[0] + angle)
        self.pos[0] += move_length * comp_x
        self.pos[2] += move_length * comp_y
        self.rot[0] = math.atan2(-self.pos[0], -self.pos[2])

    def update(self, dt: float, key):
        s = dt * 1000

        if key[K_q]:
            self.pos[1] += s
        if key[K_e]:
            self.pos[1] -= s

        if key[K_w]:
            self.pos[0] += s
            self.pos[2] += s
        if key[K_s]:
            self.pos[0] -= s
            self.pos[2] -= s
        if key[K_a]:
            self.pos[0] -= s
            self.pos[2] += s
        if key[K_d]:
            self.pos[0] += s
            self.pos[2] -= s


class Cube:
    vertices = (
        (-0.5, -0.5, -0.5),
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, 0.5, 0.5),
        (-0.5, 0.5, 0.5),
    )
    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    )
    faces = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 3, 7, 4),
        (1, 2, 6, 5),
    )
    colours = (
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (255, 255, 255),
        (0, 0, 255),
        (0, 255, 0),
    )

    def __init__(
        self, idx, pos=(0, 0, 0), scale=(1, 1, 1), initial_heirarchy_pos=(0, 0, 0)
    ):
        self.id = idx
        self.parent = None
        self.x, self.y, self.z = pos
        self.original_vertices = [
            (X * scale[0], Y * scale[1], Z * scale[2], 1.0) for X, Y, Z in self.vertices
        ]
        self.half_dimensions = [scale[0] / 2, scale[1] / 2, scale[2] / 2]

        self.initial_translation_matrix = translation_matrix(
            initial_heirarchy_pos[0], initial_heirarchy_pos[1], initial_heirarchy_pos[2]
        )

        self.rotate_x_matrix = identity_matrix()
        self.rotate_y_matrix = identity_matrix()
        self.rotate_z_matrix = identity_matrix()
        self.translation_matrix = translation_matrix(pos[0], pos[1], pos[2])

        self.local_transform = identity_matrix()
        self.final_transform = identity_matrix()
        self.final_vertices = []
        self.update_local_transform()
        self.apply_final_transform()
        self.shouldUpdateLocalTransform = False

    def get_half_dimensions(self):
        return self.half_dimensions

    def get_position(self):
        return [
            self.final_transform[3][0],
            self.final_transform[3][1],
            self.final_transform[3][2],
        ]

    def set_position(self, pos):
        if self.parent is None:
            self.translation_matrix = translation_matrix(pos[0], pos[1], pos[2])
            self.shouldUpdateLocalTransform = True
        else:
            print("Can't set position of an object with parents in skeletal hierarchy")

    def set_rotation(self, x=0, y=0, z=0):
        self.rotate_x_matrix = rotate_x_matrix(x)
        self.rotate_y_matrix = rotate_y_matrix(y)
        self.rotate_z_matrix = rotate_z_matrix(z)
        self.shouldUpdateLocalTransform = True

    def update(self):
        if self.shouldUpdateLocalTransform:
            self.shouldUpdateLocalTransform = False
            self.update_local_transform()

    def update_local_transform(self):
        rotation = self.rotate_x_matrix * self.rotate_y_matrix * self.rotate_z_matrix
        self.local_transform = rotation * self.translation_matrix

    def apply_parent_transform(self, final_transform):
        if self.parent.parent is not None:
            step_transform = final_transform * self.parent.local_transform
            return self.parent.apply_parent_transform(step_transform)
        else:
            return final_transform * self.parent.local_transform

    def apply_final_transform(self):
        if self.parent is not None:
            self.final_transform = copy.deepcopy(self.local_transform)
            self.final_transform = (
                self.initial_translation_matrix
                * self.apply_parent_transform(self.final_transform)
            )
        else:
            self.final_transform = (
                self.initial_translation_matrix * self.local_transform
            )
        self.final_vertices = np.dot(self.original_vertices, self.final_transform).list


class ArmSimulator:
    def __init__(self, cubes):
        self.cubes = cubes
        self.z_offset_for_base = 33.5  # 36
        self.gripper_half_depth = 7.5
        self.current_angles = [0, math.pi / 6, 0]
        self.start_move_angles = [0, math.pi / 6, 0]
        self.current_target_angles = [0, math.pi / 6, 0]

        self.target_angles_queue = deque([])
        self.current_lerps = [0.0, 0.0, 0.0]
        self.speed = 0.5
        self.total_rotation_dist = 0.0
        self.total_distance = 0.0
        self.speed_factor = 1.0

        self.held_cube = None

        self.next_command = None

        # arm heirarchy
        self.cubes[1].parent = self.cubes[0]
        self.cubes[2].parent = self.cubes[1]
        self.cubes[3].parent = self.cubes[2]
        self.cubes[4].parent = self.cubes[3]
        self.cubes[5].parent = self.cubes[4]

        self.reset()

    def reached_target(self):
        a0 = self.current_angles[0] == self.current_target_angles[0]
        a1 = self.current_angles[1] == self.current_target_angles[1]
        a2 = self.current_angles[2] == self.current_target_angles[2]

        return a0 and a1 and a2

    def move_to(self, x, y, z):
        adjusted_z = z - self.z_offset_for_base
        new_target_angles = [0, 0, 0]
        if not game.kinematics.solve(y, x, adjusted_z, new_target_angles):
            print("Failed to find solution")

        self.target_angles_queue.append(["move_target", new_target_angles, [x, y, z]])

    @staticmethod
    def point_distance(point_a, point_b):
        x_dist = (point_a[0] - point_b[0]) ** 2
        y_dist = (point_a[1] - point_b[1]) ** 2
        z_dist = (point_a[2] - point_b[2]) ** 2
        return math.sqrt(x_dist + y_dist + z_dist)

    def cube_distance(self, cube_a, cube_b):
        return self.point_distance(cube_a.get_position(), cube_b.get_position())

    def activate_gripper(self):
        self.target_angles_queue.append(["activate_gripper", None])

    def deactivate_gripper(self):
        self.target_angles_queue.append(["deactivate_gripper", None])

    def actually_activate_gripper(self):
        nearby_cube = None
        closest_cube_dist = 10000.0
        for i in range(6, 9):
            cube = self.cubes[i]
            cube_dist = self.cube_distance(cube, self.cubes[5])
            if cube_dist < 60.0:
                if cube_dist < closest_cube_dist:
                    closest_cube_dist = cube_dist
                    nearby_cube = cube

        if nearby_cube is not None:
            self.held_cube = nearby_cube
            self.held_cube.set_position([-22.5, 0, 0])
            self.held_cube.parent = self.cubes[5]

    def actually_deactivate_gripper(self):
        if self.held_cube is not None:
            held_position = self.held_cube.get_position()
            self.held_cube.parent = None
            if -held_position[1] < 15.0:
                held_position[1] = -15
            self.held_cube.set_position(held_position)

    def reset(self):
        self.actually_deactivate_gripper()
        self.current_angles = [0, math.pi / 6, 0]
        self.current_target_angles = [0, math.pi / 6, 0]
        self.current_lerps = [0.0, 0.0, 0.0]
        self.target_angles_queue = deque([])

        angle4 = math.pi / 2 - (self.current_angles[2] + self.current_angles[1])
        self.cubes[1].set_rotation(0, self.current_angles[0], 0)
        self.cubes[2].set_rotation(0, 0, self.current_angles[1])
        self.cubes[3].set_rotation(0, 0, self.current_angles[2])
        self.cubes[4].set_rotation(0, 0, angle4)

    def update(self, dt):
        if self.reached_target() and len(self.target_angles_queue) != 0:
            self.next_command = self.target_angles_queue.popleft()
            if self.next_command[0] == "move_target":
                self.current_target_angles = self.next_command[1]
                x_dist = (
                    self.next_command[2][0] - (-self.cubes[5].get_position()[0])
                ) ** 2
                y_dist = (
                    self.next_command[2][1] - (-self.cubes[5].get_position()[2])
                ) ** 2
                z_dist = (
                    self.next_command[2][2] - (-self.cubes[5].get_position()[1])
                ) ** 2
                self.total_distance = math.sqrt(x_dist + y_dist + z_dist)
                self.total_rotation_dist = (
                    abs(self.current_target_angles[0] - self.current_angles[0])
                    + abs(self.current_target_angles[1] - self.current_angles[1])
                    + abs(self.current_target_angles[2] - self.current_angles[2])
                )
                self.speed_factor = 300.0 / self.total_distance
                self.current_lerps[0] = 0.0
                self.current_lerps[1] = 0.0
                self.current_lerps[2] = 0.0
                self.start_move_angles = [
                    self.current_angles[0],
                    self.current_angles[1],
                    self.current_angles[2],
                ]
            elif self.next_command[0] == "activate_gripper":
                self.actually_activate_gripper()
            elif self.next_command[0] == "deactivate_gripper":
                self.actually_deactivate_gripper()

        if not self.reached_target():
            self.current_lerps[0] += dt * self.speed * self.speed_factor
            if self.current_lerps[0] > 1.0:
                self.current_lerps[0] = 1.0
            self.current_lerps[1] += dt * self.speed * self.speed_factor
            if self.current_lerps[1] > 1.0:
                self.current_lerps[1] = 1.0
            self.current_lerps[2] += dt * self.speed * self.speed_factor
            if self.current_lerps[2] > 1.0:
                self.current_lerps[2] = 1.0

            self.current_angles[0] = self.lerp(
                self.start_move_angles[0],
                self.current_target_angles[0],
                self.current_lerps[0],
            )
            self.current_angles[1] = self.lerp(
                self.start_move_angles[1],
                self.current_target_angles[1],
                self.current_lerps[1],
            )
            self.current_angles[2] = self.lerp(
                self.start_move_angles[2],
                self.current_target_angles[2],
                self.current_lerps[2],
            )
            angle4 = math.pi / 2 - (self.current_angles[2] + self.current_angles[1])
            self.cubes[1].set_rotation(0, self.current_angles[0], 0)
            self.cubes[2].set_rotation(0, 0, self.current_angles[1])
            self.cubes[3].set_rotation(0, 0, self.current_angles[2])
            self.cubes[4].set_rotation(0, 0, angle4)

    @staticmethod
    def lerp(a, b, c):
        return (c * b) + ((1.0 - c) * a)


class SimulatorApp:
    def __init__(self):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        screen_width, screen_height = 1000, 600
        self.window_panel = pygame.display.set_mode((screen_width, screen_height))

        self.w, self.h = 800, 500
        pygame.display.set_caption("Robot Arm Simulator")
        self.cx, self.cy = self.w // 2, self.h // 2
        self.fov = min(self.w, self.h)
        self.screen = pygame.Surface((self.w, self.h))

        self.clock = pygame.time.Clock()
        self.cam = Cam((self.w, self.h), (0, -600, -600))
        pygame.event.get()
        pygame.mouse.get_rel()

        self.cubes = [
            Cube("Square Base", (0, -22.5, 0), (110, 45, 110), (0, 0, 0)),
            Cube("Rotating Base", (0, 0, 0), (80, 35, 80), (0, -40, 0)),  # -40
            Cube(
                "Upper Arm", (0, -40, 0), (25, 150, 15), (0, -107, 0)
            ),  # -40 then offset -107
            Cube("Lower Arm", (-23, -187.5, 0), (190, 15, 15), (-59, 0, 0)),
            Cube("Wrist", (-162, 0, 0), (15, 60, 15), (0, -22.5, 0)),
            Cube("Gripper", (-15, -45, 0), (15, 15, 15), (0, 0, 0)),
            Cube("stackable_cube_1", (-282, -15, -82), (30, 30, 30)),
            Cube("stackable_cube_2", (-251, -15, 52), (30, 30, 30)),
            Cube("stackable_cube_3", (-112, -15, 82), (30, 30, 30)),
            Cube("target", (-200, 0, 0), (10, 1, 10)),
        ]

        self.fonts = [
            pygame.font.Font(pygame.font.match_font("gillsanscondensed"), 24),
            pygame.font.Font(pygame.font.match_font("gillsanscondensed"), 16),
        ]

        self.frame_average_range = 10
        self.last_three_frames = deque([1000.0] * self.frame_average_range)

        self.ui_buttons = []
        self.play_button = UTTextButton((25, 525, 100, 50), "Play", self.fonts, 0)
        self.ui_buttons.append(self.play_button)
        self.reset_button = UTTextButton((150, 525, 100, 50), "Reset", self.fonts, 0)
        self.ui_buttons.append(self.reset_button)

        self.optimise_arm_info_button = UTTextButton(
            (275, 525, 200, 50), "Optimise Arm Len.", self.fonts, 0
        )
        self.ui_buttons.append(self.optimise_arm_info_button)

        self.arm = ArmSimulator(self.cubes)

        self.gravity = 100.0

        self.playing = False

    @staticmethod
    def check_cube_collisions(cube_a, cube_b):
        # check the X axis
        if (
            abs(cube_a.get_position()[0] - cube_b.get_position()[0])
            < cube_a.get_half_dimensions()[0] + cube_b.get_half_dimensions()[0]
        ):
            # check the Y axis
            if (
                abs(cube_a.get_position()[1] - cube_b.get_position()[1])
                < cube_a.get_half_dimensions()[1] + cube_b.get_half_dimensions()[1]
            ):
                # check the Z axis
                if (
                    abs(cube_a.get_position()[2] - cube_b.get_position()[2])
                    < cube_a.get_half_dimensions()[2] + cube_b.get_half_dimensions()[2]
                ):
                    return True

        return False

    @staticmethod
    def try_optimise_arm_info(arm, cubes):
        found_base = 0
        found_l1 = 0
        found_l2 = 0
        found_l3 = 0

        # Final Total Error: 26.62675167617352
        # Base Offset: 36
        # L1: 179
        # L2: 162
        # L3: 69

        # Final Total Error: 27.91442848959052
        # Base Offset: 40
        # L1: 175
        # L2: 163
        # L3: 70

        # Base Range tested so far
        # 25 -> 40

        test_positions = [
            [82, 282, 30],
            [-52, 251, 30],
            [-82, 112, 30],
            [82, 282, 100],
            [-52, 251, 100],
            [-82, 112, 50],
        ]
        min_total_error = 100000000.0

        for base_offset in range(36, 37):
            arm.z_offset_for_base = base_offset
            for L1 in range(165, 181):
                for L2 in range(150, 171):
                    for L3 in range(60, 71):
                        total_error = 0
                        for position in test_positions:
                            x, y, z = position
                            adjusted_z = z - arm.z_offset_for_base
                            angles = [0, 0, 0]
                            if not game.kinematics.adj_length_solve(
                                L1, L2, L3, x, y, adjusted_z, angles
                            ):
                                print("Failed to find solution")
                            angle4 = math.pi / 2 - (angles[2] + angles[1])
                            cubes[1].set_rotation(0, angles[0], 0)
                            cubes[2].set_rotation(0, 0, angles[1])
                            cubes[3].set_rotation(0, 0, angles[2])
                            cubes[4].set_rotation(0, 0, angle4)

                            for obj in cubes:
                                obj.update()
                                obj.apply_final_transform()

                            found_x = -cubes[5].get_position()[2]
                            found_y = -cubes[5].get_position()[0]
                            found_z = (
                                -cubes[5].get_position()[1] - arm.gripper_half_depth
                            )
                            total_error += (
                                abs(x - found_x) + abs(y - found_y) + abs(z - found_z)
                            )
                        if total_error < min_total_error:
                            min_total_error = total_error
                            found_l1 = L1
                            found_l2 = L2
                            found_l3 = L3
                            found_base = base_offset
                            print("Min Total Error: " + str(min_total_error))
                            print("Base Offset: " + str(found_base))
                            print("L1: " + str(found_l1))
                            print("L2: " + str(found_l2))
                            print("L3: " + str(found_l3))

        print("Final Total Error: " + str(min_total_error))
        print("Base Offset: " + str(found_base))
        print("L1: " + str(found_l1))
        print("L2: " + str(found_l2))
        print("L3: " + str(found_l3))

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.arm.update(dt)
            if self.play_button.was_pressed():
                if not self.playing:
                    self.playing = True
                    robot_arm_routine(self.arm)

                else:
                    self.playing = False
                    self.arm.reset()
                    self.cubes[6].set_position([-282, -15, -82])
                    self.cubes[7].set_position([-251, -15, 52])
                    self.cubes[8].set_position([-112, -15, 82])
            if self.reset_button.was_pressed():
                self.playing = False
                self.arm.reset()
                self.cubes[6].set_position([-282, -15, -82])
                self.cubes[7].set_position([-251, -15, 52])
                self.cubes[8].set_position([-112, -15, 82])

            if self.optimise_arm_info_button.was_pressed():
                self.playing = False
                self.try_optimise_arm_info(self.arm, self.cubes)

            for i in range(6, 9):
                cube_a = self.cubes[i]
                collided_with_ground_or_cube = True
                if cube_a.parent is None:  # don't collide if we are on the arm
                    if (-cube_a.get_position()[1]) - cube_a.get_half_dimensions()[
                        1
                    ] > 0.0:
                        collided = False
                        for j in range(6, 9):
                            cube_b = self.cubes[j]
                            if cube_a != cube_b:
                                if self.check_cube_collisions(cube_a, cube_b):
                                    collided = True
                        if not collided:
                            collided_with_ground_or_cube = False

                if not collided_with_ground_or_cube:
                    current_position = cube_a.get_position()
                    current_position[1] += self.gravity * dt
                    cube_a.set_position(current_position)

                    # subject to gravity

            for obj in self.cubes:
                obj.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                self.cam.events(event)

                for button in self.ui_buttons:
                    button.handle_input_event(event)

            self.window_panel.fill((128, 128, 128))
            self.screen.fill((0, 0, 0))

            face_list = []
            face_colour = []
            depth = []

            for obj in self.cubes:
                obj.apply_final_transform()
                vert_list = []
                screen_coords = []
                for x, y, z, q in obj.final_vertices:
                    x -= self.cam.pos[0]
                    y -= self.cam.pos[1]
                    z -= self.cam.pos[2]
                    x, z = rotate2d((x, z), self.cam.rot[0])
                    y, z = rotate2d((y, z), self.cam.rot[1])
                    vert_list += [[x, y, z]]
                    f = self.fov / z
                    x, y = x * f, y * f
                    screen_coords += [(self.cx + int(x), self.cy + int(y))]

                for f in range(len(obj.faces)):
                    face = obj.faces[f]

                    on_screen = False
                    for i in face:
                        x, y = screen_coords[i]
                        if vert_list[i][2] > 0 and 0 < x < self.w and 0 < y < self.h:
                            on_screen = True
                            break

                    if on_screen:
                        coords = [screen_coords[i] for i in face]
                        face_list += [coords]
                        face_colour += [obj.colours[f]]
                        depth += [
                            sum(
                                sum(vert_list[j][i] / len(face) for j in face) ** 2
                                for i in range(3)
                            )
                        ]

            # drawing of all faces
            order = sorted(range(len(face_list)), key=lambda k: depth[k], reverse=True)
            for i in order:
                pygame.draw.polygon(self.screen, face_colour[i], face_list[i])

            # frames per second calculation
            if dt > 0.0:
                self.last_three_frames.popleft()
                self.last_three_frames.append(1.0 / dt)
            average_fps = sum(self.last_three_frames) / self.frame_average_range
            fps_string = "FPS: " + "{:.2f}".format(average_fps)
            fps_text_render = self.fonts[0].render(
                fps_string, True, pygame.Color(255, 255, 255)
            )
            self.screen.blit(
                fps_text_render,
                fps_text_render.get_rect(centerx=self.w - 60, centery=24),
            )

            self.window_panel.blit(self.screen, (0, 0))

            for button in self.ui_buttons:
                button.update()
                button.draw(self.window_panel)

            cube1_pos_title_str = "Cube 1"
            cube1_pos_str = "Pos: [{:.0f}, {:.0f}, {:.0f}]".format(
                -self.cubes[6].get_position()[0],
                -self.cubes[6].get_position()[2],
                -self.cubes[6].get_position()[1],
            )
            cube1_dimensions_str = "Dimensions: [30,30,30]"
            cube1_pos_title_render = self.fonts[0].render(
                cube1_pos_title_str, True, pygame.Color(255, 255, 255)
            )
            cube1_pos_str_render = self.fonts[0].render(
                cube1_pos_str, True, pygame.Color(255, 255, 255)
            )
            cube1_dimensions_str_render = self.fonts[0].render(
                cube1_dimensions_str, True, pygame.Color(255, 255, 255)
            )
            self.window_panel.blit(
                cube1_pos_title_render,
                cube1_pos_title_render.get_rect(centerx=900, centery=32),
            )
            self.window_panel.blit(
                cube1_pos_str_render,
                cube1_pos_str_render.get_rect(centerx=900, centery=58),
            )
            self.window_panel.blit(
                cube1_dimensions_str_render,
                cube1_dimensions_str_render.get_rect(centerx=900, centery=84),
            )

            cube2_pos_title_str = "Cube 2"
            cube2_pos_str = "Pos: [{:.0f}, {:.0f}, {:.0f}]".format(
                -self.cubes[7].get_position()[0],
                -self.cubes[7].get_position()[2],
                -self.cubes[7].get_position()[1],
            )
            cube2_dimensions_str = "Dimensions: [30,30,30]"
            cube2_pos_title_render = self.fonts[0].render(
                cube2_pos_title_str, True, pygame.Color(255, 255, 255)
            )
            cube2_pos_str_render = self.fonts[0].render(
                cube2_pos_str, True, pygame.Color(255, 255, 255)
            )
            cube2_dimensions_str_render = self.fonts[0].render(
                cube2_dimensions_str, True, pygame.Color(255, 255, 255)
            )
            self.window_panel.blit(
                cube2_pos_title_render,
                cube2_pos_title_render.get_rect(centerx=900, centery=142),
            )
            self.window_panel.blit(
                cube2_pos_str_render,
                cube2_pos_str_render.get_rect(centerx=900, centery=168),
            )
            self.window_panel.blit(
                cube2_dimensions_str_render,
                cube2_dimensions_str_render.get_rect(centerx=900, centery=194),
            )

            cube3_pos_title_str = "Cube 3"
            cube3_pos_str = "Pos: [{:.0f}, {:.0f}, {:.0f}]".format(
                -self.cubes[8].get_position()[0],
                -self.cubes[8].get_position()[2],
                -self.cubes[8].get_position()[1],
            )
            cube3_dimensions_str = "Dimensions: [30,30,30]"
            cube3_pos_title_render = self.fonts[0].render(
                cube3_pos_title_str, True, pygame.Color(255, 255, 255)
            )
            cube3_pos_str_render = self.fonts[0].render(
                cube3_pos_str, True, pygame.Color(255, 255, 255)
            )
            cube3_dimensions_str_render = self.fonts[0].render(
                cube3_dimensions_str, True, pygame.Color(255, 255, 255)
            )
            self.window_panel.blit(
                cube3_pos_title_render,
                cube3_pos_title_render.get_rect(centerx=900, centery=252),
            )
            self.window_panel.blit(
                cube3_pos_str_render,
                cube3_pos_str_render.get_rect(centerx=900, centery=278),
            )
            self.window_panel.blit(
                cube3_dimensions_str_render,
                cube3_dimensions_str_render.get_rect(centerx=900, centery=304),
            )

            target_pos_title_str = "Stack Target"
            target_pos_str = "Pos: [{:.0f}, {:.0f}, {:.0f}]".format(
                -self.cubes[9].get_position()[0],
                -self.cubes[9].get_position()[2],
                -self.cubes[9].get_position()[1],
            )
            target_pos_title_render = self.fonts[0].render(
                target_pos_title_str, True, pygame.Color(255, 255, 255)
            )
            target_pos_str_render = self.fonts[0].render(
                target_pos_str, True, pygame.Color(255, 255, 255)
            )
            self.window_panel.blit(
                target_pos_title_render,
                target_pos_title_render.get_rect(centerx=900, centery=362),
            )
            self.window_panel.blit(
                target_pos_str_render,
                target_pos_str_render.get_rect(centerx=900, centery=388),
            )

            instructions_str = "Left click view panel and move mouse to rotate view"
            instructions_str_render = self.fonts[1].render(
                instructions_str, True, pygame.Color(255, 255, 255)
            )
            self.window_panel.blit(
                instructions_str_render,
                instructions_str_render.get_rect(centerx=800, centery=525),
            )

            pygame.display.flip()

            key = pygame.key.get_pressed()
            self.cam.update(dt, key)


if __name__ == "__main__":
    simulator_app = SimulatorApp()
    simulator_app.run()
