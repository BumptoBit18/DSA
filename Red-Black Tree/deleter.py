from node import BLACK, RED


class Deleter:
    def transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = u
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def find_minimum(self, x):
        while x.left is not self.NIL:
            x = x.left

        return x

    def delete(self, key):
        z = self.search(key)
        if z is self.NIL:
            return False
        y, y_color = z, z.color
        if z.left is self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right is self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.find_minimum(z.right)
            y_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        self.size -= 1
        if y_color == BLACK:
            self.log("Mất 1 nút BLACK -> cần sửa 'double black'")
            self.delete_fixup(x)
        return True

    def delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    self.log(
                        f"TH1 (anh đỏ {w.key}): đổi màu, xoay TRÁI tại {x.parent.key}")
                    w.color, x.parent.color = BLACK, RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    self.log(
                        f"TH2 (anh đen, 2 cháu đen): anh {w.key} -> RED, đẩy 'đen thừa' lên cha")
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        self.log(
                            f"TH3 (cháu xa đen): xoay PHẢI tại anh {w.key}")
                        w.left.color, w.color = BLACK, RED
                        self.right_rotate(w)
                        w = x.parent.right
                    self.log(
                        f"TH4 (cháu xa đỏ): xoay TRÁI tại cha {x.parent.key}, xong")
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    self.log(
                        f"TH1 (anh đỏ {w.key}): đổi màu, xoay PHẢI tại {x.parent.key}")
                    w.color, x.parent.color = BLACK, RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    self.log(
                        f"TH2 (anh đen, 2 cháu đen): anh {w.key} -> ĐỎ, đẩy 'đen thừa' lên cha")
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        self.log(
                            f"TH3 (cháu xa đen): xoay TRÁI tại anh {w.key}")
                        w.right.color, w.color = BLACK, RED
                        self.left_rotate(w)
                        w = x.parent.left
                    self.log(
                        f"TH4 (cháu xa đỏ): xoay PHẢI tại cha {x.parent.key}, xong")
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK
