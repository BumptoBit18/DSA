from Node import Node23

class Delete: 
    
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
