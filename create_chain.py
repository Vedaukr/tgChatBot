from xmlrpc.client import Boolean
from telethon import TelegramClient
from word_tree.word_tree import WordTree
from chain.word_tree_adapter import WordTreeAdapter
from chain.word_generator import CompositeWordGenerator, ListedWordsGenerator, ChainModelWordsGenerator

dump_path = "./output/1000_dep5.json"
word_tree = WordTree.create_from_dump("./output/10000_dep5.json")
chain = WordTreeAdapter(word_tree).create_chain()

listedWordsGen = ListedWordsGenerator(0.1, ["это самое", "крч", "ну как его", "короче", "это"])
chainGen = ChainModelWordsGenerator(chain)
wordGenerator = CompositeWordGenerator().add_generator(chainGen)

result = ""
for _ in range(50):
    result += wordGenerator.generate() + " "

print(result)