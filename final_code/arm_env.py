import math
import numpy as np
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
    def __init__(self, length, width, color, angle=0, origin=None, parent=None, constraints=[0,math.pi]):
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
        return self.point_at(self.global_angle)

    @property
    def global_angle(self):
        return self._gangle


    @global_angle.setter
    def global_angle(self, angle):
        tmp = self.remove_offset_angle(angle)
        if tmp<self.constraints[0]:
            tmp = self.constraints[0]
        if tmp>self.constraints[1]:
            tmp = self.constraints[1]
        self._angle = tmp
        self._gangle = self.get_offset_angle(self._angle)

        #update the origin position
        if self.parent:
            # X = (xcosθ + ysinθ) and and Y = (−xsinθ+ycosθ).
            self.origin = self.parent.point_at(self.parent.global_angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        #print(angle)
        if angle<self.constraints[0]:
            angle = self.constraints[0]
        if angle>self.constraints[1]:
            angle = self.constraints[1]

        self._angle = angle
        self._gangle = self.get_offset_angle(self._angle)

        #update the origin position
        if self.parent:
            # X = (xcosθ + ysinθ) and and Y = (−xsinθ+ycosθ).
            self.origin = self.parent.point_at(self.parent.global_angle)

    def get_offset_angle(self, angle):
        # computes the offset
        # from the parent and returns
        if self.parent is not None:
            offset = angle - math.pi/2 + self.parent.global_angle
            return offset % (2*math.pi)
        else:
            return angle

    def remove_offset_angle(self, angle):
        if self.parent:
            offset = angle - self.parent.global_angle + math.pi/2
            return offset % (2*math.pi)
        else:
            return angle

    def angle_to(self, point):
        """
        Returns the angle to the specified point.
        :param point:
        :return:
        """
        return math.atan2(point.y - self.origin.y, point.x - self.origin.x)


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
        point = Point2D(point[0],point[1])
        end = self.point_at(self.global_angle)
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
            self.origin = self.parent.point_at(self.parent.global_angle)
        look_at = self.point_at(self.global_angle)
        pyglet.gl.glLineWidth(self.width)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (self.origin.x, self.origin.y, look_at.x, look_at.y)), ('c3B', self.color * 2))
        self.draw_grid()
        self.draw_axis()


class Arm(object):
    def __init__(self, origin,env_size, link_width=1, goal=None):
        self.origin = origin
        self.links = []
        self.link_width = link_width
        self.goal_len = 30
        self.gloal = goal if goal else [500,500,self.goal_len]
        self.on_goal = 0
        self.state_dim = 9
        self.action_dim = 2
        self.action_bound=[-1,+1]
        self.env_size = env_size
        self.step_size = 0.05 # granularity


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

        self.action_dim = len(self.links)
        self.state_dim = 4*self.action_dim + 1 # total number of observations


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

    def get_observation(self,goal):
        observation = []
        for link in self.links:
            observation.append(link.endpoint.x/self.env_size.x) #normalize
            observation.append(link.endpoint.y/self.env_size.y) #normalize
        
        for link in self.links:
            observation.append((goal[0]-link.endpoint.x)/self.env_size.x)   #normalize
            observation.append((goal[1]-link.endpoint.y)/self.env_size.y)   #normalize

        return observation

    def get_reward(self, goal):
        return -self.head().distance_to(goal)/max(self.env_size.x,self.env_size.y)


    def step(self, action):
        done = False
        for i in range(len(action)):
            self.links[i].angle += np.clip(action[i],-1,1)*self.step_size

        r = self.get_reward(self.goal)

        # done and reward
        if self.goal[0] - self.goal[2]/2 < self.head().endpoint.x < self.goal[0] + self.goal[2]/2:
            if self.goal[1] - self.goal[2]/2 < self.head().endpoint.y < self.goal[1] + self.goal[2]/2:
                r += 1.
                self.on_goal += 1
                if self.on_goal > 50:       # if it is over the goal for 50 times
                    done = True
        else:
            self.on_goal = 0

        observations = self.get_observation(self.goal)
        s = np.concatenate((observations, [1. if self.on_goal else 0.]))

        return s, r, done

    def reset(self):
        # set the goal approximately withing the arm's range
        while(1):
            self.goal = [np.random.rand()*self.env_size.x,np.random.rand()*self.env_size.y,self.goal_len]
            if math.sqrt((self.goal[0]-self.origin.x)**2+(self.goal[1]-self.origin.y)**2)> self.links[0].length:
                break
        
        # check if on goal
        if self.goal[0] - self.goal[2]/2 < self.head().endpoint.x < self.goal[0] + self.goal[2]/2:
            if self.goal[1] - self.goal[2]/2 < self.head().endpoint.y < self.goal[1] + self.goal[2]/2:
                self.on_goal = 1
        else:
            self.on_goal = 0

        for link in self.links: # randomize arm angles
            link.angle = math.pi * np.random.rand(1)[0]

        observations = self.get_observation(self.goal)

        s = np.concatenate((observations, [1. if self.on_goal else 0.]))
        return s

    def setenv(self,goal):
        
        self.goal = goal
        # check if on goal
        if self.goal[0] - self.goal[2]/2 < self.head().endpoint.x < self.goal[0] + self.goal[2]/2:
            if self.goal[1] - self.goal[2]/2 < self.head().endpoint.y < self.goal[1] + self.goal[2]/2:
                self.on_goal = 1
        else:
            self.on_goal = 0

        #for link in self.links: # randomize arm angles
        #    link.angle = math.pi * np.random.rand(1)[0]

        observations = self.get_observation(self.goal)

        s = np.concatenate((observations, [1. if self.on_goal else 0.]))
        return s 

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
    def __init__(self, arm, model):
        super(ArmSimViewer, self).__init__(
            width=300, height=300, resizable=True, caption="Arm", vsync=False
        )
        
        self.arm = arm
        self.env_size = arm.env_size # max spawn of the arm
        self.model = model
        arm.set_angles(0,90)
        self.target = ArmTarget(Point2D(150, 150), (0, 0, 255))
       
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
            pt = head.point_at(head.global_angle)
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
        #self.arm.head().global_angle = self.arm.head().angle_to(Point2D(x, y))
        #self.target.origin = Point2D(x, y)
        goal = [x, y, self.arm.goal_len]
        self.target.origin = Point2D(x,y)
        s = self.arm.setenv(goal)
        tolerance_counter = 0
        max_steps = 200
        while True:
            a = self.model.choose_action(s)
            s, r, done = self.arm.step(a)

            tolerance_counter += 1

            if done or tolerance_counter>max_steps:    # check if reached or saturated
                print('reward:',r)
                for i, link in enumerate(self.arm.links):
                    print('angle of link ',i,rad2deg(link.angle))
                break



if __name__ == "__main__":
    viewer = ArmSimViewer()
    pyglet.app.run()
