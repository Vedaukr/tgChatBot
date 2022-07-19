from word_tree.word_tree import WordTree
import settings

dump_path = settings.output
output_path = "../output/filtered.json"

WordTree.create_from_dump(dump_path).filter(settings.word_black_list).save(output_path)