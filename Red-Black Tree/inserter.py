from node import Node, RED, BLACK


class Inserter:
    def insert(self, key, data=None):
        # y, following x, is parent of x --> When x is NIL, y will be parent of the new node
        y, x = self.NIL, self.root
        while x is not self.NIL:
            y = x
            if key == x.key:
                x.data = data
                return False
            x = x.left if key < x.key else x.right
        z = Node(key, data, RED)
        z.left = z.right = self.NIL
        z.parent = y

        # Insert z into the right side of y
        if y is self.NIL:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z

        self.size += 1
        self.insert_fixup(z)
        return True

    def insert_fixup(self, z):
        while z.parent.color == RED:
            grandparent = z.parent.parent
            if z.parent is grandparent.left:
                uncle = grandparent.right
                if uncle.color == RED:
                    self.log(
                        f"TH1: Đổi màu cha {z.parent.key} và chú {uncle.key} --> BLACK, ông {grandparent.key} --> RED")
                    uncle.color = z.parent.color = BLACK
                    grandparent.color = RED
                    z = grandparent
                else:
                    # Triangle-shaped subtree
                    if z is z.parent.right:
                        self.log(
                            f"TH2 (triangle): Xoay trái tại {z.parent.key}")
                        z = z.parent
                        self.left_rotate(z)
                    self.log(
                        f"TH3 (line): đổi màu cha {z.parent.key} --> BLACK, ông {z.parent.parent.key} --> RED, rotate right tại {z.parent.parent.key}")
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_right(z.parent.parent)
            else:
                uncle = grandparent.left
                if uncle.color == RED:
                    self.log(
                        f"TH1: đổi màu cha {z.parent.key}, chú {uncle.key} -> BLACK; ông {grandparent.key} -> RED")
                    z.parent.color = uncle.color = BLACK
                    grandparent.color = RED
                    z = grandparent
                else:
                    if z is z.parent.left:
                        self.log(
                            f"TH2 (triangle): xoay PHẢI tại {z.parent.key}")
                        z = z.parent
                        self.right_rotate(z)
                    self.log(
                        f"TH3 (line): đổi màu cha {z.parent.key} -> BLACK, ông {z.parent.parent.key} -> RED, rotate left tại {z.parent.parent.key}")
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK
