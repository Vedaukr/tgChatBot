from datetime import datetime
from telethon import TelegramClient
import json, uuid, re

class WordTree:
    
    # constants
    max_word_length = 13
    top_chats = 20
    current_user = 'me'
    
    def __init__(self, client: TelegramClient) -> None:
        self.client = client
        self.tree = {}

    async def init(self, chats=None, depth=3, remove_duplicates=True):
        
        if not chats:
            chats = await self._get_chats()
        
        
        for chatId in chats:

            retrieved_messages = set()
            print("Retrieving messages from {} | {}".format(chatId, datetime.now()))
            
            async for message in self.client.iter_messages(chatId, from_user=self.current_user):
                
                if remove_duplicates:
                    if message.message in retrieved_messages:
                        continue
                    retrieved_messages.add(message.message)
                
                if not message.fwd_from and message.message:
                    words = list(filter(lambda w: w, map(self._normalize_word, re.split('\s', message.message))))
                    
                    if not self._check_message(words):
                        continue
            
                    for word_bunch in self._get_tree_iter(words, depth):
                        curr = self._get_or_add_counted(word_bunch[0])["next"]
                        for i, item in enumerate(word_bunch):
                            if i:
                                curr = self._get_or_add_counted(item, curr)["next"]
        
        return self

    def filter(self, word_list):
        self._filter_internal(word_list, self.tree)
        return self

    def sort(self):
        self.tree = self._sort_internal(self.tree)
        return self

    def save(self, output_file=None) -> None:
        
        print("Saving...")
        
        if not output_file:
            output_file = str(uuid.uuid4()) + '.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.tree, f, ensure_ascii=False, indent=2)
    
    
    # PRIVATE
    def _sort_internal(self, curr_tree):
        
        if not curr_tree:
            return
        
        for key, item in curr_tree.items():
            if "next" in item:
                item["next"] = self._sort_internal(item["next"])
        
        return dict(sorted(curr_tree.items(), key=lambda item: item[1]["count"], reverse=True))

    def _filter_internal(self, word_list, curr_tree):
        
        if not curr_tree:
            return
        
        for word in word_list:
            if word in curr_tree:
                del curr_tree[word]
        
        keys_to_delete = []
        for key, item in curr_tree.items():
            if len(key) > self.max_word_length:
                keys_to_delete.append(key)
            
            if 'http' in key:
                keys_to_delete.append(key)

            if "next" in curr_tree[key]:
                self._filter_internal(word_list, curr_tree[key]["next"])
        
        for key in keys_to_delete:
            if key in curr_tree:
                del curr_tree[key]

    def _normalize_word(self, word):
        return ''.join(filter(str.isalpha, word)).lower()

    def _check_message(self, words):
        return len(set(words)) >= len(words) / 5

    def _get_tree_iter(self, words, depth):
        result = []
        for i in range(len(words)):
            last = i + depth if i + depth < len(words) else len(words)
            result.append(words[i:last])
        return result
    
    def _get_or_add_counted(self, word, tree=None):
        if tree is None:
            tree = self.tree
        
        if not word in tree:
            tree[word] = {}
            tree[word]["count"] = 0
            tree[word]["next"]  = {}
        
        tree[word]["count"] += 1
        return tree[word]
            

    async def _get_chats(self):
        return [dialog.id async for dialog in self.client.iter_dialogs(limit=self.top_chats)]
