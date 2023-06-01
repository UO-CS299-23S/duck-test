"""Example of how a hypothetical test harness might be applied.
This is a module that we will test with another module.
"""

class Tree:
    def count(self) -> int:
        raise NotImplementedError(f"No implementation of count in {self.__class__.__name__}")

class Branch(Tree):
    def __init__(self, left: Tree, right: Tree):
        self.left = left
        self.right = right

    def count(self) -> int:
        return self.left.count() + self.right.count()

class Leaf(Tree):
    def __init__(self, v: str):
        self.value = v

    def count(self) -> int:
        return 1

class Empty(Tree):
    def count(self) -> int:
        return 0

def nonsense():
    """A sample function that we don't cover with tests"""
    return





