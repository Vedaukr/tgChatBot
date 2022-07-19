from abc import abstractclassmethod
from typing import List
from numpy.random import choice
from chain.chain import Chain
import random

class WordGenerator:

    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def generate(self) -> str:
        pass

    @abstractclassmethod
    def reset(self) -> None:
        pass

class CompositeWordGenerator(WordGenerator):

    def __init__(self) -> None:
        self.generators = []

    def add_generator(self, gen: WordGenerator):
        self.generators.append(gen)
        return self

    def reset(self) -> None:
        for gen in self.generators:
            gen.reset()

    def generate(self) -> None:
        for gen in self.generators:
            if res := gen.generate():
                return res

        return str("Fucked up")


class ListedWordsGenerator(WordGenerator):

    def __init__(self, gen_prob: float, words: List[str], word_probs: List[float]=None) -> None:
        self.words = words
        self.gen_prob = gen_prob
        self.word_probs = word_probs if word_probs else [1 / len(words)] * len(words)

    def generate(self) -> str:
        if random.random() < self.gen_prob:
            return choice(self.words, p=self.word_probs)
        return None

    def reset(self) -> None:
        pass

class ChainModelWordsGenerator(WordGenerator):

    def __init__(self, chain: Chain) -> None:
        self.chain = chain

    def generate(self) -> str:
        return self.chain.generate()

    def reset(self) -> None:
        self.chain.reset()