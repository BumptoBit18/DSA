RED, BLACK = "RED", "BLACK"


class Node:
    # 1 node only has 6 slots, which help handles memory when dealing with millions of nodes
    __slots__ = ('key', 'data', 'color', 'left', 'right', 'parent')

    def __init__(self, key=None, data=None, color=BLACK):
        # key used to compare and arrange the position of nodes
        self.key, self.data, self.color = key, data, color
        self.left = self.right = self.parent = None


class RedBlackTree:
    def __init__(self, verbose=False):
        self.NIL = Node()
        self.root = self.NIL  # root is Null at the time of creation
        self.size = 0  # the total number of nodes
        self.verbose = verbose  # the flag to turn on/off activity log

    def log(self, msg):
        if self.verbose:
            print(" ->", msg)

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right is not self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self.NIL:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key, val=None):
        y, x = self.NIL, self.root
        while x is not self.NIL:
            y = x
            if key == x.key:
                x.val = val
                return False
            x = x.left if key < x.key else x.right
        z = Node(key, val, RED)
        z.left = z.right = self.NIL
        z.parent = y
        if y is self.NIL:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self.size += 1
        self._insert_fixup(z)
        return True

    def _insert_fixup(self, z):
        while z.parent.color == RED:
            gp = z.parent.parent
            if z.parent is gp.left:
                u = gp.right
                if u.color == RED:                         # TH1
                    self._log(
                        f"TH1 (chú đỏ): đổi màu cha {z.parent.key}, chú {u.key} -> ĐEN; ông {gp.key} -> ĐỎ")
                    z.parent.color = u.color = BLACK
                    gp.color = RED
                    z = gp
                else:
                    if z is z.parent.right:                # TH2
                        self._log(
                            f"TH2 (tam giác): xoay TRÁI tại {z.parent.key}")
                        z = z.parent
                        self._left_rotate(z)
                    self._log(
                        f"TH3 (đường thẳng): đổi màu cha {z.parent.key} -> ĐEN, ông {z.parent.parent.key} -> ĐỎ, xoay PHẢI tại {z.parent.parent.key}")
                    z.parent.color = BLACK                 # TH3
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:                                          # đối xứng
                u = gp.left
                if u.color == RED:
                    self._log(
                        f"TH1 (chú đỏ): đổi màu cha {z.parent.key}, chú {u.key} -> ĐEN; ông {gp.key} -> ĐỎ")
                    z.parent.color = u.color = BLACK
                    gp.color = RED
                    z = gp
                else:
                    if z is z.parent.left:
                        self._log(
                            f"TH2 (tam giác): xoay PHẢI tại {z.parent.key}")
                        z = z.parent
                        self._right_rotate(z)
                    self._log(
                        f"TH3 (đường thẳng): đổi màu cha {z.parent.key} -> ĐEN, ông {z.parent.parent.key} -> ĐỎ, xoay TRÁI tại {z.parent.parent.key}")
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _find(self, key):
        x = self.root
        while x is not self.NIL and key != x.key:
            x = x.left if key < x.key else x.right
        return x

    def search(self, key):
        n = self._find(key)
        return None if n is self.NIL else n

    def __contains__(self, key):
        return self._find(key) is not self.NIL

    def ceiling(self, key):
        """Khóa nhỏ nhất >= key (hoặc None)."""
        x, ans = self.root, None
        while x is not self.NIL:
            if x.key >= key:
                ans, x = x, x.left
            else:
                x = x.right
        return ans

    def floor(self, key):
        """Khóa lớn nhất <= key (hoặc None)."""
        x, ans = self.root, None
        while x is not self.NIL:
            if x.key <= key:
                ans, x = x, x.right
            else:
                x = x.left
        return ans

    def _transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x):
        while x.left is not self.NIL:
            x = x.left
        return x

    def delete(self, key):
        z = self._find(key)
        if z is self.NIL:
            return False
        y, y_color = z, z.color
        if z.left is self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        self.size -= 1
        if y_color == BLACK:
            self._log("Mất 1 nút ĐEN -> cần sửa 'double black'")
            self._delete_fixup(x)
        return True

    def _delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:                                   # TH1
                    self._log(
                        f"TH1 (anh đỏ {w.key}): đổi màu, xoay TRÁI tại {x.parent.key}")
                    w.color, x.parent.color = BLACK, RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:  # TH2
                    self._log(
                        f"TH2 (anh đen, 2 cháu đen): anh {w.key} -> ĐỎ, đẩy 'đen thừa' lên cha")
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:                       # TH3
                        self._log(
                            f"TH3 (cháu xa đen): xoay PHẢI tại anh {w.key}")
                        w.left.color, w.color = BLACK, RED
                        self._right_rotate(w)
                        w = x.parent.right
                    self._log(
                        f"TH4 (cháu xa đỏ): xoay TRÁI tại cha {x.parent.key}, xong")
                    w.color = x.parent.color                         # TH4
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:                                                    # đối xứng
                w = x.parent.left
                if w.color == RED:
                    self._log(
                        f"TH1 (anh đỏ {w.key}): đổi màu, xoay PHẢI tại {x.parent.key}")
                    w.color, x.parent.color = BLACK, RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    self._log(
                        f"TH2 (anh đen, 2 cháu đen): anh {w.key} -> ĐỎ, đẩy 'đen thừa' lên cha")
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        self._log(
                            f"TH3 (cháu xa đen): xoay TRÁI tại anh {w.key}")
                        w.right.color, w.color = BLACK, RED
                        self._left_rotate(w)
                        w = x.parent.left
                    self._log(
                        f"TH4 (cháu xa đỏ): xoay PHẢI tại cha {x.parent.key}, xong")
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK
