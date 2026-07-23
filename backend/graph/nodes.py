# graph/nodes.py

class Node:
    def __init__(self, node_id: str, data: dict | None = None):
        self.node_id = node_id
        self.data = data or {}
