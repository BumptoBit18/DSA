class Searcher:
    def search(self, key):
        x = self.root
        while x is not self.NIL and key != x.key:
            x = x.key if key < x.key else x.right

        return None if x is self.NIL else x

    def ceiling(self, key):
        """Find the mininum >= key (or None)"""
        x, ans = self.root, None
        while x is not self.NIL:
            if x.key >= key:
                x, ans = x.left, x
            else:
                x = x.right

        return ans

    def floor(self, key):
        """Find the maxinum <= key (or None)"""
        x, ans = self.root, None
        while x is not self.NIL:
            if x.key <= key:
                x, ans = x.right, x
            else:
                x = x.left

        return ans
