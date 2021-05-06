from abc import ABC, abstractmethod
from typing import Iterator


class Node:
    def __init__(self, parent):
        self.parent = parent
        self.lchild = None
        self.rchild = None
        self.traversed = False

    def put(self, value):
        if self.rchild:
            if self.lchild:
                self.lchild.put(value)
            else:
                self.lchild = Node(value)
        elif self.lchild:
            if self.rchild:
                self.rchild.put(value)
            else:
                self.rchild = Node(value)
        else:
            self.lchild = Node(value)

    def __iter__(self):
        return NodePostOrderIterator(node_obj=self)

    def __next__(self):
        return self.__iter__().__next__()

    def __str__(self):
        return f'{self.lchild}-{self.parent}-{self.rchild}'


class NodePostOrderIterator(Iterator):
    def __init__(self, node_obj: Node):
        self.node = node_obj
        self.cursor = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.node.lchild:
            if not self.node.lchild.traversed:
                self.cursor = self.node.lchild
            elif self.node.rchild and not self.node.rchild.traversed:
                self.cursor = self.node.rchild
            elif self.node.traversed:
                raise StopIteration()
            else:
                self.node.traversed = True
                self.cursor = self.node.parent
        else:
            if self.node.traversed:
                raise StopIteration()
            else:
                self.cursor = self.node.parent
                self.node.traversed = True
        try:
            return self.cursor.__next__()
        except AttributeError:
            return self.cursor


class Tree(ABC):
    def __init__(self, root: Node = None):
        self.root = root

    def add(self, value):
        if self.root:
            self.root.put(value)
        else:
            self.root = Node(value)

    @abstractmethod
    def __iter__(self):
        # appropriate iterator. There are only one PostOrderIterator
        pass


class PostOrderTree(Tree):
    def __init__(self, root: Node = None):
        super().__init__(root)

    def __iter__(self):
        return NodePostOrderIterator(node_obj=self.root)


if __name__ == '__main__':
    node = PostOrderTree(Node(10))
    node.add(11)
    node.add(12)
    node.add(13)
    node.add(14)
    for el in node:
        print(el)
