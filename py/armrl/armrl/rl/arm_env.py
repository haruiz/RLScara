import math

import pyglet
from pyglet import shapes

class Point2D(object):
    """2D point class"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

def rad2deg(rad):
    return rad * 180 / math.pi

def deg2rad(deg):
    return deg * math.pi / 180

class ArmLink(object):
    """Arm link class"""
    def __init__(self, length, width, color, angle=0, origin=None, parent=None):
        self.length = length
        self.width = width
        self.color = color
        self._angle = angle
        self.origin = origin or Point2D(0, 0)
        self.parent = parent


    @property
    def endpoint(self):
        return self.point_at(self.angle)

    @property
    def global_angle(self):
        raise NotImplementedError


    @global_angle.setter
    def global_angle(self, angle):
        raise NotImplementedError

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = self.get_offset_angle(angle)

    def get_offset_angle(self, angle):
        # computes the offset
        # from the parent and returns
        if self.parent:
            offset = angle - self.parent.angle - math.pi/2
            return offset % (2*math.pi)
        else:
            return angle

    def remove_offset_angle(self, angle):
        if self.parent:
            offset = angle - self.parent.angle - math.pi/2

    def angle_to(self, point):
        """
        Returns the angle to the specified point.
        :param point:
        :return:
        """
        return self.get_offset_angle(math.atan2(point.y - self.origin.y, point.x - self.origin.x))+math.pi


    # X=(xcosθ+ysinθ) and and Y=(−xsinθ+ycosθ).

    def point_at(self, angle):
        """
        Returns the point at the specified angle.
        :param angle:
        :return:
        """
        #angle = self.remove_offset_angle()
        return Point2D(self.origin.x + self.length * math.cos(angle), self.origin.y + self.length * math.sin(angle))

    def distance_to(self, point):
        """
        Returns the distance to the specified point.
        :param point:
        :return:
        """
        end = self.point_at(self.angle)
        return math.sqrt((point.x - end.x) ** 2 + (point.y - end.y) ** 2)

    def draw_axis(self):
        """
        Draws the arm link axis.
        :return:
        """
        pyglet.gl.glLineWidth(2)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (self.origin.x, self.origin.y, self.origin.x + 100, self.origin.y)), ('c3B', (255, 0, 0) * 2))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (self.origin.x, self.origin.y, self.origin.x, self.origin.y + 100)), ('c3B', (0, 255, 0) * 2))

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
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (self.origin.x, self.origin.y, point.x, point.y)), ('c3B', (255, 255, 255) * 2))


    def draw(self):
        """
        Draws the arm link.
        :return:
        """
        if self.parent:
            # X = (xcosθ + ysinθ) and and Y = (−xsinθ+ycosθ).
            self.origin = self.parent.point_at(self.parent.angle)
        look_at = self.point_at(self.angle)
        pyglet.gl.glLineWidth(self.width)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (self.origin.x, self.origin.y, look_at.x, look_at.y)), ('c3B', self.color * 2))
        self.draw_grid()
        self.draw_axis()


class Arm(object):
    def __init__(self, origin, link_width=1):
        self.origin = origin
        self.links = []
        self.link_width = link_width


    def head(self):
        return self.links[-1] if len(self.links) > 0 else None

    def tail(self):
        return self.links[0] if len(self.links) > 0 else None

    def add_link(self, length, color):
        """
        Adds a link to the arm.
        :param length:
        :param width:
        :param color:
        :return:
        """
        if len(self.links) == 0:
            self.links.append(ArmLink(length, self.link_width, color, origin=self.origin))
        else:
            self.links.append(ArmLink(length, self.link_width, color, parent=self.links[-1]))


    def draw(self):
        """
        Draws the arm.
        :return:
        """
        for link in self.links:
            link.draw()

    def set_angles(self, *angles):
        """
        Sets the angles of the arm links.
        :param angles:
        :return:
        """
        if len(angles) != len(self.links):
            raise ValueError("Invalid number of angles specified.")
        for i, angle in enumerate(angles):
            self[i].angle = deg2rad(angle)

    def __getitem__(self, item):
        return self.links[item] if item < len(self.links) else None


class ArmTarget(object):
    """Arm target class"""
    def __init__(self, origin, color):
        self.origin = origin
        self.color = color

    def draw(self):
        """
        Draws the arm target.
        :return:
        """
        self.shape = shapes.Circle(self.origin.x, self.origin.y, 10, color=self.color)
        self.shape.draw()


class ArmSimViewer(pyglet.window.Window):
    def __init__(self):
        super(ArmSimViewer, self).__init__(
            width=600, height=600, resizable=True, caption="Arm", vsync=False
        )
        self.arm = Arm(self.center(), link_width=20)

        self.arm.add_link(100,(255, 0, 0))
        self.arm.add_link(100,(0, 255, 0))
        self.arm.add_link(100,(0, 0, 255))
        #self.arm.add_link(100, (0, 255, 0))
        #self.arm.add_link(100, (0, 0, 255))

        self.arm.set_angles(0, 45, 90)

        self.target = ArmTarget(Point2D(300, 300), (0, 0, 255))

    def center(self):
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
            pt = head.point_at(head.angle)
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (pt.x, pt.y, point.x, point.y)), ('c3B', (255, 255, 255) * 2))

    def on_draw(self):
        self.clear()
        self.arm.draw()
        self.target.draw()

        # Draw trajectory to target
        self.draw_trajectory_to_point(self.target.origin)

        # get distance
        print(",".join([f"{rad2deg(link.angle):0.2f}" for link in self.arm.links]))


    def on_mouse_motion(self, x, y, dx, dy):
        # self.arm.head().angle = self.arm.head().angle_to(Point2D(x, y))
        self.target.origin = Point2D(x, y)

        print(self.arm.head().endpoint)


if __name__ == "__main__":
    viewer = ArmSimViewer()
    pyglet.app.run()
