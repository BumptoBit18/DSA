from node import Node, BLACK
from inserter import Inserter
from rotater import Rotater
from deleter import Deleter
from searcher import Searcher
from printer import Printer


class RedBlackTree(Inserter, Rotater, Deleter, Searcher, Printer):
    def __init__(self, verbose=False):
        self.NIL = Node()
        self.root = self.NIL  # root is Null at the time of creation
        self.size = 0  # the total number of nodes
        self.verbose = verbose  # the flag to turn on/off activity log

    def log(self, msg):
        if self.verbose:
            print(" ->", msg)


# ---------- INSERT ---------------
tree = RedBlackTree(verbose=True)
for key in [10, 20, 30, 15, 12, 23, 9]:
    print(f"insert({key})")
    success = tree.insert(key, data=f"Data_for_{key}")
    if success:
        print(f"Đã insert thành công key: {key}")
        print()
    else:
        print(f"Key {key} đã tồn tại trong cây!")
        print()
print("-------------------------------")
print("Tree after inserting element: ")
print(tree.pretty())
print("-------------------------------")

# ---------- DELETE ----------------
success = tree.delete(20)
if success:
    print(f"Đã xóa thành công node {20}")
    print()
else:
    print("Thất bại")
    print()

print("-------------------------------")
print(f"Tree after deleting element {20}: ")
print(tree.pretty())
print("-------------------------------")


# ----------- SEARCH ----------------
print(f"Found {30}" if tree.search(30) is not tree.NIL else "Not found")
print()

# ----------- ROTATE ----------------
node_to_use = tree.right_rotate(12)

print("-------------------------------")
print(f"Tree after right rotating {12}: ")
print(tree.pretty())
print("-------------------------------")
