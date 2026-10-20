from node import Node, BLACK
from inserter import InserterMixin
from rotater import RotaterMixin
from deleter import Deleter
from searcher import Searcher


class RedBlackTree(InserterMixin, RotaterMixin, Deleter, Searcher):
    def __init__(self, verbose=False):
        self.NIL = Node()
        self.root = self.NIL  # root is Null at the time of creation
        self.size = 0  # the total number of nodes
        self.verbose = verbose  # the flag to turn on/off activity log

    def log(self, msg):
        if self.verbose:
            print(" ->", msg)


tree = RedBlackTree(verbose=True)
for key in [10, 20, 30, 15, 12]:
    print(f"insert({key})")
    success = tree.insert(key, data=f"Data_for_{key}")
    if success:
        print(f"Đã insert thành công key: {key}")
        print()
    else:
        print(f"Key {key} đã tồn tại trong cây!")
        print()

success = tree.delete(20)
if success:
    print(f"Đã xóa thành công key {20}")
    print()
else:
    print("Thất bại")
