from pydoc import cli
from xmlrpc.client import Boolean
from telethon import TelegramClient
from word_tree.word_tree import WordTree
import settings

client = TelegramClient(settings.session_name, settings.api_id, settings.api_hash).start()

DEPTH = 5
MSG_LIMIT = 5000

async def main():
    await client.connect()
    word_tree = WordTree()
    await word_tree.init(client, chats=settings.chats, depth=DEPTH, msg_limit=MSG_LIMIT)
    word_tree.filter(settings.word_black_list).sort().save(settings.output)

client.loop.run_until_complete(main())

