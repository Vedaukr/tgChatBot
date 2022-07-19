from ast import List, Tuple
from platform import node
from xmlrpc.client import Boolean
from word_tree.word_tree import WordTree
from chain.chain import Chain
from chain.node import ChainNode, ValueNode, TransitionNode

class WordTreeAdapter:

    SW_LENGTH = 4
    SW_NORMALIZATION_FACTOR = 0.25
    ROOT_NORMALIZATION_FACTOR = 0.75

    def __init__(self, word_tree: WordTree) -> None:
        self.word_tree = word_tree
        self.root_node = TransitionNode()

    def create_chain(self) -> Chain:
        self.root_node.init_props(self._get_nodes(self.word_tree.tree, True, True))
        return Chain(self.root_node)
    

    # PRIVATE
    def _get_nodes(self, tree, normalize_sw: bool = False, is_root: bool = False):

        if not tree:
            return [self._get_transition_to_root()]

        nodes = []
        key_count_map = {}
        for key, value in tree.items():
            child_prob_map = self._get_nodes(value["next"])
            key_count_map[key] = self._apply_normalize(key, value["count"]) if normalize_sw else value["count"]
            nodes.append(ValueNode(child_prob_map, key))
        
        total_count = sum(key_count_map.values())
        if is_root:
            return [(node, key_count_map[node.data.value] / total_count) for node in nodes]
        else:
            root_link_diff = min(key_count_map.values()) * self.ROOT_NORMALIZATION_FACTOR
            total_count += root_link_diff
            result = [(node, key_count_map[node.data.value] / total_count) for node in nodes]
            result.append(self._get_transition_to_root(root_link_diff / total_count))
            return result
        
        
    def _apply_normalize(self, word:str, count:int) -> int:
        return count * self.SW_NORMALIZATION_FACTOR if len(word) < self.SW_LENGTH else count
    
    def _get_transition_to_root(self, prob: float=1.0):
        return (self.root_node, prob)
