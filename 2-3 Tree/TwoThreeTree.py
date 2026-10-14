class Node23:
    def __init__(self, key=None):
        self.keys = [] if key is None else [key]
        self.parent = None
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == 3


class TwoThreeTree:
    def __init__(self):
        self.root = None

    # ==================== SEARCH ====================
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False

        if key in node.keys:
            return True

        if node.is_leaf():
            return False

        if key < node.keys[0]:
            return self._search(node.children[0], key)

        if len(node.keys) == 1 or key < node.keys[1]:
            return self._search(node.children[1], key)

        return self._search(node.children[2], key)

    # ==================== INSERT ====================
    def insert(self, key):
        if self.root is None:
            self.root = Node23(key)
            return

        # Không chèn khóa trùng
        if self.search(key):
            return

        leaf = self._find_leaf(self.root, key)
        self._insert_into_leaf(leaf, key)

    def _find_leaf(self, node, key):
        if node.is_leaf():
            return node

        if key < node.keys[0]:
            return self._find_leaf(node.children[0], key)

        if len(node.keys) == 1 or key < node.keys[1]:
            return self._find_leaf(node.children[1], key)

        return self._find_leaf(node.children[2], key)

    def _insert_into_leaf(self, leaf, key):
        leaf.keys.append(key)
        leaf.keys.sort()

        if leaf.is_full():
            self._split(leaf)

    def _split(self, node):
        # node có 3 khóa: [a, b, c]
        left_key = node.keys[0]
        mid_key = node.keys[1]
        right_key = node.keys[2]

        left_node = Node23(left_key)
        right_node = Node23(right_key)

        # Nếu là nút trong, chia lại 4 cây con
        if not node.is_leaf():
            left_node.children = node.children[:2]
            right_node.children = node.children[2:]

            for child in left_node.children:
                child.parent = left_node

            for child in right_node.children:
                child.parent = right_node

        parent = node.parent

        # Tách nút gốc
        if parent is None:
            new_root = Node23(mid_key)
            new_root.children = [left_node, right_node]

            left_node.parent = new_root
            right_node.parent = new_root

            self.root = new_root
            return

        # Thay node bằng hai nút mới
        idx = parent.children.index(node)

        parent.children[idx] = left_node
        parent.children.insert(idx + 1, right_node)

        left_node.parent = parent
        right_node.parent = parent

        # Đưa khóa giữa lên cha
        parent.keys.append(mid_key)
        parent.keys.sort()

        # Sắp xếp các cây con theo thứ tự khóa
        parent.children.sort(
            key=lambda child: min(child.keys)
        )

        if parent.is_full():
            self._split(parent)

    # ==================== DELETE ====================
    def delete(self, key):
        node = self._find_node(self.root, key)

        if node is None:
            return False

        # Nếu là nút trong, thay bằng successor
        if not node.is_leaf():
            idx = node.keys.index(key)
            successor_leaf, successor_key = self._get_successor(
                node, idx
            )

            node.keys[idx] = successor_key
            node = successor_leaf
            key = successor_key

        node.keys.remove(key)

        if len(node.keys) == 0:
            self._fix_underflow(node)

        return True

    def _find_node(self, node, key):
        if node is None:
            return None

        if key in node.keys:
            return node

        if node.is_leaf():
            return None

        if key < node.keys[0]:
            return self._find_node(node.children[0], key)

        if len(node.keys) == 1 or key < node.keys[1]:
            return self._find_node(node.children[1], key)

        return self._find_node(node.children[2], key)

    def _get_successor(self, node, key_idx):
        curr = node.children[key_idx + 1]

        while not curr.is_leaf():
            curr = curr.children[0]

        return curr, curr.keys[0]

    def _fix_underflow(self, node):
        # Trường hợp nút gốc bị rỗng
        if node == self.root:
            if len(node.keys) == 0:
                if node.children:
                    self.root = node.children[0]
                    self.root.parent = None
                else:
                    self.root = None
            return

        parent = node.parent
        idx = parent.children.index(node)

        left_sib = (
            parent.children[idx - 1] if idx > 0 else None
        )
        right_sib = (
            parent.children[idx + 1]
            if idx + 1 < len(parent.children)
            else None
        )

        # 1. Mượn khóa từ anh em bên trái
        if left_sib is not None and len(left_sib.keys) == 2:
            node.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = left_sib.keys.pop()

            if left_sib.children:
                child = left_sib.children.pop()
                node.children.insert(0, child)
                child.parent = node

            return

        # 2. Mượn khóa từ anh em bên phải
        if right_sib is not None and len(right_sib.keys) == 2:
            node.keys.append(parent.keys[idx])
            parent.keys[idx] = right_sib.keys.pop(0)

            if right_sib.children:
                child = right_sib.children.pop(0)
                node.children.append(child)
                child.parent = node

            return

        # 3. Không mượn được: gộp với anh em bên trái
        if left_sib is not None:
            parent_key = parent.keys.pop(idx - 1)
            parent.children.pop(idx)

            left_sib.keys.append(parent_key)
            left_sib.keys.extend(node.keys)

            for child in node.children:
                child.parent = left_sib

            left_sib.children.extend(node.children)

        # 4. Không có anh em trái: gộp với anh em bên phải
        elif right_sib is not None:
            parent_key = parent.keys.pop(idx)
            parent.children.pop(idx + 1)

            node.keys.append(parent_key)
            node.keys.extend(right_sib.keys)

            for child in right_sib.children:
                child.parent = node

            node.children.extend(right_sib.children)

        # Nếu cha bị rỗng, xử lý tiếp từ cha
        if len(parent.keys) == 0:
            self._fix_underflow(parent)

    # ==================== IN-ORDER ====================
    def in_order(self):
        result = []
        self._traverse(self.root, result)
        return result

    def _traverse(self, node, result):
        if node is None:
            return

        if node.is_leaf():
            result.extend(node.keys)
            return

        for i, key in enumerate(node.keys):
            self._traverse(node.children[i], result)
            result.append(key)

        self._traverse(node.children[len(node.keys)], result)


# ==================== TEST ====================
if __name__ == "__main__":
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