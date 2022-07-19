from typing import Any
from chain.node import ChainNode

class Chain:

    def __init__(self, root_node: ChainNode) -> None:
        self.state = root_node
        self.root_node = root_node

    def generate(self) -> Any:
        data = self.state.apply_transition().get_value()
        self.state = data.node
        return data.value
    
    def reset(self) -> None:
        self.state = self.root_node
