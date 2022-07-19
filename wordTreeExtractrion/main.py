from xmlrpc.client import Boolean
from telethon import TelegramClient
from word_tree import WordTree
import settings

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

client = TelegramClient(settings.session_name, settings.api_id, settings.api_hash)



async def main():
    
    await client.connect()
    word_tree = WordTree(client)
    await word_tree.init(settings.chats)
    word_tree.filter(settings.word_black_list).sort().save()


client.loop.run_until_complete(main())

