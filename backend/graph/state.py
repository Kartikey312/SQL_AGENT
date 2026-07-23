# graph/state.py

class GraphState:
    def __init__(self):
        self.current_node = None

    def set_current(self, node_id: str) -> None:
        self.current_node = node_id
