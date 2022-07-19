from abc import abstractclassmethod
from numpy.random import choice
from __future__ import annotations
from typing import Any, List, Tuple

class NodeData:

    def __init__(self, value: Any, node: ChainNode) -> None:
        self.value = value
        self.node = node

class ChainNode:

    def __init__(self, childProbs: List[Tuple[ChainNode, float]]) -> None:
        self.childs = [p[0] for p in childProbs]
        self.probs = [p[1] for p in childProbs]

    def apply_transition(self) -> ChainNode:
        return choice(self.childs, p=self.probs)
    
    @abstractclassmethod
    def get_value(self) -> NodeData:
        pass

class ValueNode(ChainNode):

    def __init__(self, childProbs, value) -> None:
        super().__init__(childProbs)
        self.data = NodeData(value, self)

    def get_value(self) -> NodeData:
        return self.data
        
class TransitionNode(ChainNode):

    def __init__(self, childProbs) -> None:
        super().__init__(childProbs)

    def get_value(self) -> NodeData:
        return self.apply_transition().get_value()