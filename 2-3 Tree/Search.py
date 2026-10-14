from Node import Node23

class Search:
    
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