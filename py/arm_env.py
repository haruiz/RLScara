from __future__ import annotations
import math
import typing

import numpy as np
import pyglet
from pyglet import shapes

from arm_controller import ArmController
from math_utils import Point2D, Size2D, rad2deg, deg2rad


DEBUG = False


class ArmLink(object):
    """Arm link class, based on our implementation a single arm could have multiple links."""

    def __init__(
        self,
        length: int,
        width: int,
        color: tuple,
        angle: int = 0,
        origin: Point2D = None,
        parent: ArmLink = None,
        constraints: typing.List[int] = [0, math.pi],
    ):
        self.length = length
        self.width = width
        self.color = color
        self._angle = angle
        self.origin = origin or Point2D(0, 0)
        self.parent = parent
        self._gangle = self.get_offset_angle(angle)
        self.constraints = constraints

    @property
    def endpoint(self):
        """get the endpoint of the arm link"""
        return self.point_at(self.global_angle)

    @property
    def global_angle(self):
        """get the global angle of the arm link"""
        return self._gangle

    @global_angle.setter
    def global_angle(self, angle: int):
        """ "set the global angle making sure that it falls into the 0, math.pi range
        :param angle:
        :return:
        """

        tmp = self.remove_offset_angle(angle)
        if tmp < self.constraints[0]:
            tmp = self.constraints[0]
        if tmp > self.constraints[1]:
            tmp = self.constraints[1]
        self._angle = tmp
        self._gangle = self.get_offset_angle(self._angle)

        # update the origin position
        if self.parent:
            # X = (xcosθ + ysinθ) and and Y = (−xsinθ+ycosθ).
            self.origin = self.parent.point_at(self.parent.global_angle)

    @property
    def angle(self):
        """get the local angle of the arm link"""
        return self._angle

    @angle.setter
    def angle(self, angle: int):
        """set the local angle making sure that it falls into the 0, math.pi range
        :param angle:
        :return:
        """
        if angle < self.constraints[0]:
            angle = self.constraints[0]
        if angle > self.constraints[1]:
            angle = self.constraints[1]

        self._angle = angle
        self._gangle = self.get_offset_angle(self._angle)

        # update the origin position
        if self.parent:
            # X = (xcosθ + ysinθ) and and Y = (−xsinθ+ycosθ).
            self.origin = self.parent.point_at(self.parent.global_angle)

    def get_offset_angle(self, angle) -> float:
        """
        Returns the angle with the offset from the parent.
        :param angle:
        :return:
        """
        # from the parent and returns
        if self.parent is not None:
            offset = angle - math.pi / 2 + self.parent.global_angle
            return offset % (2 * math.pi)
        else:
            return angle

    def remove_offset_angle(self, angle) -> float:
        """
        Removes the offset from the parent and returns
        :param angle:
        :return:
        """
        if self.parent:
            offset = angle - self.parent.global_angle + math.pi / 2
            return offset % (2 * math.pi)
        else:
            return angle

    def angle_to(self, point: Point2D) -> float:
        """
        Returns the angle between the arm link origin and a point.
        :param point:
        :return:
        """
        return math.atan2(point.y - self.origin.y, point.x - self.origin.x)

    # X=(xcosθ+ysinθ) and and Y=(−xsinθ+ycosθ).

    def point_at(self, angle: typing.Union[float, int]) -> Point2D:
        """
        get the coordinates of a point at the specified angle and distance from the link's origin,
        this function is mainly used to compute the endpoint of the link
        :param angle:
        :return:
        """
        # angle = self.remove_offset_angle()
        return Point2D(
            self.origin.x + self.length * math.cos(angle),
            self.origin.y + self.length * math.sin(angle),
        )

    def distance_to(self, point: typing.Union[typing.List, Point2D]) -> float:
        """
        Returns the distance for the link endpoint to a given point.
        :param point:
        :return:
        """
        if isinstance(point, list):
            point = Point2D(point[0], point[1])
        end = self.point_at(self.global_angle)
        return math.sqrt((point.x - end.x) ** 2 + (point.y - end.y) ** 2)

    def draw_axis(self):
        """
        Draws the arm link axis.
        :return:
        """
        pyglet.gl.glLineWidth(2)
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ("v2f", (self.origin.x, self.origin.y, self.origin.x + 100, self.origin.y)),
            ("c3B", (255, 0, 0) * 2),
        )
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ("v2f", (self.origin.x, self.origin.y, self.origin.x, self.origin.y + 100)),
            ("c3B", (0, 255, 0) * 2),
        )

    def draw_grid(self):
        """
        Draws the arm link grid.
        :return:
        """
        self.draw_axis()
        pyglet.gl.glLineWidth(0.1)
        for i in range(0, 360, 10):
            angle = deg2rad(i)
            point = self.point_at(angle)
            pyglet.graphics.draw(
                2,
                pyglet.gl.GL_LINES,
                ("v2f", (self.origin.x, self.origin.y, point.x, point.y)),
                ("c3B", (255, 255, 255) * 2),
            )


    def draw_angles(self):
        """
        Draws the arm link angles.
        :return:
        """
        pyglet.gl.glLineWidth(1)
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ("v2f", (self.origin.x, self.origin.y, self.origin.x + 100, self.origin.y)),
            ("c3B", (255, 0, 0) * 2),
        )
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ("v2f", (self.origin.x, self.origin.y, self.origin.x, self.origin.y + 100)),
            ("c3B", (0, 255, 0) * 2),
        )

    def draw(self):
        """
        Draws the arm link.
        :return:
        """
        if self.parent:
            # X = (xcosθ + ysinθ) and and Y = (−xsinθ+ycosθ).
            self.origin = self.parent.point_at(self.parent.global_angle)
        look_at = self.point_at(self.global_angle)
        pyglet.gl.glLineWidth(self.width)
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ("v2f", (self.origin.x, self.origin.y, look_at.x, look_at.y)),
            ("c3B", self.color * 2),
        )
        
        self.draw_angles()
        if DEBUG:
            self.draw_grid()
            self.draw_axis()
        


class Arm(object):
    """A class to represent an arm, based on our implementation a single arm could
    have multiple links"""

    def __init__(
        self, origin: Point2D, env_size: Size2D, link_width: int = 1, goal=typing.List
    ):
        """
        :param origin: the origin of the arm
        :param env_size: the size of the environment
        :param link_width: the width of the arm link
        :param goal: the goal point
        """
        # arm
        self.origin = origin
        self.links = []
        self.link_width = link_width
        # goal
        self.goal_len = 30
        self.goal = goal if goal else [500, 500, self.goal_len]
        self.on_goal = 0
        # env attributes
        self.state_dim = 9
        self.action_dim = 2
        self.action_bound = [-1, +1]
        self.env_size = env_size

        self.step_size = 0.05  # granularity

    def head(self):
        """returns the last link of the arm"""
        return self.links[-1] if len(self.links) > 0 else None

    def tail(self):
        """returns the first link of the arm"""
        return self.links[0] if len(self.links) > 0 else None

    def add_link(self, length: int, color: tuple = (255, 255, 255)):
        """
        Adds a link to the arm.
        :param length:
        :param width:
        :param color:
        :return:
        """
        if len(self.links) == 0:
            self.links.append(
                ArmLink(length, self.link_width, color, origin=self.origin)
            )
        else:
            self.links.append(
                ArmLink(length, self.link_width, color, parent=self.links[-1])
            )

        self.action_dim = len(self.links)
        self.state_dim = 4 * self.action_dim + 1  # total number of observations

    def draw(self):
        """
        Draws the arm.
        :return:
        """
        for link in self.links:
            link.draw()

    def set_angles(self, *angles: int):
        """
        Sets the angles of the arm links.
        :param angles:
        :return:
        """
        if len(angles) != len(self.links):
            raise ValueError("Invalid number of angles specified.")
        for i, angle in enumerate(angles):
            self[i].angle = deg2rad(angle)

    def get_observation(self, goal: typing.List = None) -> typing.List:
        """
        Returns the observation of the arm.
        :param goal: the goal point
        :return: the observation of the arm
        """
        observation = []
        for link in self.links:
            observation.append(link.endpoint.x / self.env_size.width)  # normalize
            observation.append(link.endpoint.y / self.env_size.height)  # normalize

        for link in self.links:
            observation.append(
                (goal[0] - link.endpoint.x) / self.env_size.width
            )  # normalize
            observation.append(
                (goal[1] - link.endpoint.y) / self.env_size.height
            )  # normalize

        return observation

    def get_reward(self, goal: typing.List) -> float:
        """
        Returns the reward of the arm.
        """
        return -self.head().distance_to(goal) / max(
            self.env_size.width, self.env_size.height
        )

    def step(self, action: typing.List) -> typing.Tuple:
        """
        Performs a step in the environment.
        :param action: the action to perform defined as the angle of each link
        """
        done = False
        for i in range(len(action)):
            self.links[i].angle += np.clip(action[i], -1, 1) * self.step_size

        r = self.get_reward(self.goal)

        # done and reward
        if (
            self.goal[0] - self.goal[2] / 2
            < self.head().endpoint.x
            < self.goal[0] + self.goal[2] / 2
        ):
            if (
                self.goal[1] - self.goal[2] / 2
                < self.head().endpoint.y
                < self.goal[1] + self.goal[2] / 2
            ):
                r += 1.0
                self.on_goal += 1
                if self.on_goal > 50:  # if it is over the goal for 50 times
                    done = True
        else:
            self.on_goal = 0

        observations = self.get_observation(self.goal)
        s = np.concatenate((observations, [1.0 if self.on_goal else 0.0]))

        return s, r, done

    def reset(self):
        # set the goal approximately withing the arm's range
        while 1:
            self.goal = [
                np.random.rand() * self.env_size.width,
                np.random.rand() * self.env_size.height,
                self.goal_len,
            ]
            if (
                math.sqrt(
                    (self.goal[0] - self.origin.x) ** 2
                    + (self.goal[1] - self.origin.y) ** 2
                )
                > self.links[0].length
            ):
                break

        # check if on goal
        if (
            self.goal[0] - self.goal[2] / 2
            < self.head().endpoint.x
            < self.goal[0] + self.goal[2] / 2
        ):
            if (
                self.goal[1] - self.goal[2] / 2
                < self.head().endpoint.y
                < self.goal[1] + self.goal[2] / 2
            ):
                self.on_goal = 1
        else:
            self.on_goal = 0

        for link in self.links:  # randomize arm angles
            link.angle = math.pi * np.random.rand(1)[0]

        observations = self.get_observation(self.goal)

        s = np.concatenate((observations, [1.0 if self.on_goal else 0.0]))
        return s

    def setenv(self, goal) -> np.ndarray:

        self.goal = goal
        # check if on goal
        if (
            self.goal[0] - self.goal[2] / 2
            < self.head().endpoint.x
            < self.goal[0] + self.goal[2] / 2
        ):
            if (
                self.goal[1] - self.goal[2] / 2
                < self.head().endpoint.y
                < self.goal[1] + self.goal[2] / 2
            ):
                self.on_goal = 1
        else:
            self.on_goal = 0

        # for link in self.links: # randomize arm angles
        #    link.angle = math.pi * np.random.rand(1)[0]

        observations = self.get_observation(self.goal)

        s = np.concatenate((observations, [1.0 if self.on_goal else 0.0]))
        return s

    def __getitem__(self, item):
        return self.links[item] if item < len(self.links) else None


class ArmTarget(object):
    """Arm target class"""

    def __init__(self, origin: Point2D, color: typing.Tuple, size: float = 10):
        self.origin = origin
        self.color = color
        self.size = size

    def draw(self):
        """
        Draws the arm target.
        :return:
        """
        shape = shapes.Circle(self.origin.x, self.origin.y, self.size, color=self.color)
        shape.draw()


class ArmSimViewer(pyglet.window.Window):
    """
    Pyglet based simulation viewer.
    """

    def __init__(self, arm: Arm, model: "DDPG", env_size: Size2D, *args, **kwargs):
        config = pyglet.gl.Config(sample_buffers=1, samples=8, double_buffer=False)
        super(ArmSimViewer, self).__init__(
            width=env_size.width,
            height=env_size.height,
            resizable=True,
            config=config,
            caption="Arm",
            *args,
            **kwargs,
        )
        """
        :param arm: the arm to be simulated
        :param model: the model to be used
        :param env_size: the size of the environment
        """

        self.arm = arm
        self.env_size = arm.env_size  # max spawn of the arm
        self.model = model
        self.target = None
        self.target_coords = None

    def center(self):
        """return the center of the window"""
        return Point2D(self.width / 2, self.height / 2)

    def draw_trajectory_to_point(self, point):
        """
        Draws the trajectory to the specified point.
        :param point:
        :return:
        """
        head = self.arm.head()
        if head:
            pyglet.gl.glLineWidth(1)
            pt = head.point_at(head.global_angle)
            pyglet.graphics.draw(
                2,
                pyglet.gl.GL_LINES,
                ("v2f", (pt.x, pt.y, point.x, point.y)),
                ("c3B", (255, 255, 255) * 2),
            )

    def on_draw(self):
        """
        Called when the window is drawn.
        """
        self.clear()
        self.arm.draw()
        pyglet.gl.glFlush()
        if self.target:
            self.target.draw()
            # Draw trajectory to target
            self.draw_trajectory_to_point(self.target.origin)
            pyglet.gl.glFlush()
            self.update_arm_controller()

    def update_arm_controller(self):
        """
        Updates the arm controller.
        """
        if self.target_coords:
            # with ArmController() as arm_controller:
            #     if arm_controller.is_connected():
            #         arm_controller.move_to(*self.target_coords)
            self.target_coords = None

    def get_predicted_action(self, target_x, target_y):
        """
        Gets the predicted action from the model.
        :param target_x: the target x coordinate
        :param target_y: the target y coordinate
        :return:
        """
        goal = [target_x, target_y, self.arm.goal_len]
        s = self.arm.setenv(goal)
        tolerance_counter = 0
        max_steps = 200
        predicted_action = None
        while True:
            a = self.model.choose_action(s)
            s, r, done = self.arm.step(a)
            tolerance_counter += 1
            if done or tolerance_counter > max_steps:  # check if reached or saturated
                for i, link in enumerate(self.arm.links):
                    print("angle of link ", i, rad2deg(link.angle))
                predicted_action = [rad2deg(link.angle) for link in self.arm.links]
                break
        return predicted_action

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.target is None:
                self.target = ArmTarget(Point2D(x, y), color=(255, 0, 0))
            self.target.origin = Point2D(x, y)
            self.target_coords = self.get_predicted_action(x, y)
            self.arm.set_angles(*self.target_coords)
