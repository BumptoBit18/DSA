
class Node:
    def __init__(self, s, e):
        self.s, self.e = s, e
        self.red = True
        self.left = self.right = self.parent = None


class MyCalendar:
    def __init__(self):
        self.root = None

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix(self, z):
        while z.parent and z.parent.red:
            p = z.parent
            g = p.parent
            if p == g.left:
                u = g.right
                if u and u.red:
                    p.red = u.red = False
                    g.red = True
                    z = g
                else:
                    if z == p.right:
                        z = p
                        self.rotate_left(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.rotate_right(z.parent.parent)
            else:
                u = g.left
                if u and u.red:
                    p.red = u.red = False
                    g.red = True
                    z = g
                else:
                    if z == p.left:
                        z = p
                        self.rotate_right(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.rotate_left(z.parent.parent)
        self.root.red = False

    def book(self, startTime, endTime):
        p = None
        cur = self.root

        while cur:
            p = cur
            if endTime <= cur.s:
                cur = cur.left
            elif startTime >= cur.e:
                cur = cur.right
            else:
                return False

        z = Node(startTime, endTime)
        z.parent = p

        if not p:
            self.root = z
        elif startTime < p.s:
            p.left = z
        else:
            p.right = z

        self.fix(z)
        return True
