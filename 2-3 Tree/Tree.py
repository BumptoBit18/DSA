from Node import Node23
from Insertion import Insert
from InOrderTranversal import InOrderTranversal
from Deletion import Delete
from Search import Search


class TwoThreeTree(Search, Insert, Delete, InOrderTranversal):
    def __init__(self):
        self.root = None