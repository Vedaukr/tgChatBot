from word_tree import WordTree
import settings

dump_path = settings.output
WordTree.create_from_dump(dump_path).filter(settings.word_black_list).save("../output/filtered.json")