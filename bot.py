import os
import telebot
from chain.word_generator import ChainModelWordsGenerator, CompositeWordGenerator, ListedWordsGenerator
from chain.word_tree_adapter import WordTreeAdapter
from word_tree.word_tree import WordTree

bot_token = os.environ.get('BOT_TOKEN', None)
webhook = os.environ.get('WEBHOOK', None)

dump_path = "./output/1000_dep5.json"
word_tree = WordTree.create_from_dump("./output/10000_dep5.json")
chain = WordTreeAdapter(word_tree).create_chain()

chainGen = ChainModelWordsGenerator(chain)

wordGenerator = CompositeWordGenerator().add_generator(chainGen)

listedWordsGen = ListedWordsGenerator(0.25, ["это самое", "крч", "ну как его", "короче", "это"])
bidloWordGen = CompositeWordGenerator().add_generator(listedWordsGen).add_generator(chainGen)

bot = telebot.TeleBot(bot_token, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hello")

@bot.message_handler(commands=['generate'])
def generate(message):
	bot.reply_to(message, generate(wordGenerator))

@bot.message_handler(commands=['generate_bidlo'])
def generate(message):
	bot.reply_to(message, generate(bidloWordGen))

def generate(gen, count=30):
    result = ""
    for _ in range(count):
        result += gen.generate() + " "
    return result

bot.set_webhook(webhook)
bot.infinity_polling()