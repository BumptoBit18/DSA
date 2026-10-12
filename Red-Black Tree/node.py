RED, BLACK = "RED", "BLACK"


class Node:
    # 1 node only has 6 slots, which help handles memory when dealing with millions of nodes
    __slots__ = ('key', 'data', 'color', 'left', 'right', 'parent')

    def __init__(self, key=None, data=None, color=BLACK):
        # key used to compare and arrange the position of nodes
        self.key, self.data, self.color = key, data, color
        self.left = self.right = self.parent = None
