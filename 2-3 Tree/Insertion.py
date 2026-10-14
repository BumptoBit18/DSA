from Node import Node23

class Insert:
    
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