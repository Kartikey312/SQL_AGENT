# graph/graph.py

from backend.graph.nodes import Node


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)
