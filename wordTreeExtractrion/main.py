from xmlrpc.client import Boolean
from telethon import TelegramClient
from word_tree import WordTree
import settings

client = TelegramClient(settings.session_name, settings.api_id, settings.api_hash)

async def main():
    await client.connect()
    word_tree = await WordTree().init(client, settings.chats)
    word_tree.filter(settings.word_black_list).sort().save(settings.output)

client.loop.run_until_complete(main())

