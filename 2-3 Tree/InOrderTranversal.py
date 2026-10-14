from Node import Node23

class InOrderTranversal:
    
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


# Backward-compatible alias for the original misspelling.
InoderTranversal = InOrderTranversal