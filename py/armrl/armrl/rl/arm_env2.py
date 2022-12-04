import math

import pyglet
from pyglet import shapes

class Point2D(object):
    """2D point class"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

def rad2deg(rad):
    return rad * 180 / math.pi

def deg2rad(deg):
    return deg * math.pi / 180

def point_at(origin, length, angle):
    """
    Returns the point at the specified angle.
    :param angle:
    :return:
    """
    return Point2D(origin.x + length * math.cos(angle), origin.y + length * math.sin(angle))

def distance_to(origin, point):
    """
    Returns the distance to the specified point.
    :param point:
    :return:
    """
    return math.sqrt((point.x - origin.x) ** 2 + (point.y - origin.y) ** 2)

def angle_to(origin, point):
    """
    Returns the angle to the specified point.
    :param point:
    :return:
    """
    return math.atan2(point.y - origin.y, point.x - origin.x)


def project_axes(origin, length, angle):
    """
    Returns the point at the specified angle.
    :param angle:
    :return:
    """
    return Point2D(origin.x + length * math.cos(angle), origin.y + length * math.sin(angle))

def set_origin(x, y, angle, x_shift=0, y_shift=0, units="DEGREES"):
    """
    Rotates a point in the xy-plane counterclockwise through an angle about the origin
    https://en.wikipedia.org/wiki/Rotation_matrix
    :param x: x coordinate
    :param y: y coordinate
    :param x_shift: x-axis shift from origin (0, 0)
    :param y_shift: y-axis shift from origin (0, 0)
    :param angle: The rotation angle in degrees
    :param units: DEGREES (default) or RADIANS
    :return: Tuple of rotated x and y
    """

    # Shift to origin (0,0)
    x = x - x_shift
    y = y - y_shift

    # Convert degrees to radians
    if units == "DEGREES":
        angle = math.radians(angle)

    # Rotation matrix multiplication to get rotated x & y
    xr = (x * math.cos(angle)) - (y * math.sin(angle)) + x_shift
    yr = (x * math.sin(angle)) + (y * math.cos(angle)) + y_shift

    return Point2D(xr, yr)


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
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle

    def draw(self):
        """
        Draws the arm link.
        :return:
        """
        if self.parent:
            self.origin = set_origin(self.parent.origin.x, self.parent.origin.y, self.parent.angle, units="RADIANS")


        end = point_at(self.origin, self.length, self.angle)
        shapes.Line(self.origin.x, self.origin.y, end.x, end.y, width=self.width, color=self.color).draw()



class ArmSimViewer(pyglet.window.Window):
    def __init__(self):
        super(ArmSimViewer, self).__init__(
            width=600, height=600, resizable=True, caption="Arm", vsync=False
        )
        self.link1 = ArmLink(100, width=10, color=(255, 0, 0), angle=deg2rad(45), origin= self.center())
        self.link2 = ArmLink(100, width=10, color=(0, 255, 0), angle=deg2rad(90), parent=self.link1)

    def center(self):
        return Point2D(self.width / 2, self.height / 2)

    def on_draw(self):
        self.clear()
        self.link1.draw()
        self.link2.draw()


    def on_mouse_motion(self, x, y, dx, dy):
        #self.link1.angle = angle_to(self.link1.origin, Point2D(x, y))
        self.link2.angle = angle_to(self.link2.origin, Point2D(x, y))
        print(rad2deg(self.link2.angle))

if __name__ == "__main__":
    viewer = ArmSimViewer()
    pyglet.app.run()
