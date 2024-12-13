from dataclasses import dataclass, field
from typing import Self, Iterable


class NodeBase:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


@dataclass
class NodeDeg2:
    value: any
    parent: Self = field(init=False, default=None)
    child: Self = field(init=False, default=None)

    def append(self, node: Self):
        if self.child:
            node.child = self.child
            self.child.parent = node
        self.child = node
        node.parent = self
        return node

    def insertAfter(self, node: Self):
        return self.append(node)

    def prepend(self, node: Self):
        if self.parent:
            node.parent = self.parent
            self.parent.child = node
        self.parent = node
        node.child = self
        return node

    def delete(self):
        self.parent = self.child
        self.child = self.parent

    def findStart(self):
        n = self
        while n.parent is not None:
            n = n.parent
        return n

    def __iter__(self):
        n = self
        while n is not None:
            yield n
            n = n.child

    def __repr__(self):
        n_prev = getattr(self.parent, "value", "None")
        n_next = getattr(self.child, "value", "None")
        return f"[Node {self.value}, prev: {n_prev}, next: {n_next}]"


class NodeUndirected(NodeBase):
    def __init__(self, value, neighbors: Iterable = None):
        super().__init__(value)
        self.links: set[Self] = set(neighbors) if neighbors else set()

    def link(self, node: Self):
        self.links.add(node)
        node.links.add(self)
        return node

    def unlink(self, node: Self):
        self.links.remove(node)
        node.links.remove(self)
