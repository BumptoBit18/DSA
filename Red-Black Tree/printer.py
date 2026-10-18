from node import RED, BLACK


class Printer:
    def height(self, n=None):
        """Calculate the height of the tree or from any nodes"""
        n = self.root if n is None else n
        if n == self.NIL:
            return 0

        return 1 + max(self.height(n.left), self.height(n.right))

    def is_valid(self):
        """Check if the tree maintains all red-black tree properties 
            - the root must be black 
            - a red node cannot have a red child 
            - black-height
            - it must satisfy the properties of a BST
            - the integrity of the parent pointers must be maintained 
        """

        if self.root is self.NIL:
            return True  # Empty tree is valid

        if self.root.color is RED:
            return False

        def check(node, low, high):
            if node is self.NIL:
                return 1

            # Ktra the property of BST (low < key < high)
            if (low is not None and node.key <= low) or (high is not None and node.key >= high):
                return -1

            if node.color == RED and (node.left.color == RED or node.right.color == RED):
                return -1

            for c in (node.left, node.right):
                if c is not self.NIL and c.parent is not node:
                    return -1

            l = check(node.left, low, node.key)
            r = check(node.right, node.key, high)

            # check if the black height of branches are equal
            if l == -1 or r == -1 or l != r:
                return -1

            # return black height of the current branch
            return l + (1 if node.color == BLACK else 0)

        return check(self.root, None, None) != -1

    def pretty(self):
        if self.root is self.NIL:
            return "(Empty tree)"

        lines = []

        def build_strings(node, prefix, is_left):
            if node is not self.NIL:
                color_str = 'R' if node.color == RED else 'B'

                # Add left branch or right branch
                pointer = "├── " if is_left else "└── "
                lines.append(prefix + pointer + f"{node.key} {color_str}")

                # Recursion for children with modified prefix
                extension = "|   " if is_left else "   "
                build_strings(node.left, prefix + extension, True)
                build_strings(node.right, prefix + extension, False)

        # Add the root first
        root_color = "R" if self.root.color == RED else "B"
        lines.append(f"{self.root.key} {root_color}")

        if self.root.left is not self.NIL:
            build_strings(self.root.left, "", True)

        if self.root.right is not self.NIL:
            build_strings(self.root.right, "", False)

        return "\n".join(lines)
