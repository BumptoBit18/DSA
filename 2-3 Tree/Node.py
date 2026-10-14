class Node23:
    
    def __init__(self, key=None):
        self.keys = [] if key is None else [key]
        self.parent = None
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == 3