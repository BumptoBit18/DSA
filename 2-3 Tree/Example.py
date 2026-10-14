from Tree import TwoThreeTree



tree = TwoThreeTree()

values = [30, 20, 10, 50, 40, 70, 60, 25, 35]

print("Inserted values:", values)
for v in values:
    tree.insert(v)

print("Tree traversal:", tree.in_order())
print("Search key 35:", tree.search(35))
print("Search key 99:", tree.search(99))

print("-" * 30)

print("Delete 25:", tree.delete(25))
print("After deleting 25:", tree.in_order())

print("Delete 30:", tree.delete(30))
print("After deleting 30:", tree.in_order())

print("Delete 10:", tree.delete(10))
print("Delete 20:", tree.delete(20))
print("After deleting 10 and 20:", tree.in_order())