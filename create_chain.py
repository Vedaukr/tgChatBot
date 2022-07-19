from xmlrpc.client import Boolean
from telethon import TelegramClient
from word_tree.word_tree import WordTree
from chain.word_tree_adapter import WordTreeAdapter

dump_path = "./output/1000_dep5.json"
word_tree = WordTree.create_from_dump("./output/1000_dep8.json")
chain = WordTreeAdapter(word_tree).create_chain()

result = ""
for _ in range(50):
    result += chain.generate() + " "

print(result)