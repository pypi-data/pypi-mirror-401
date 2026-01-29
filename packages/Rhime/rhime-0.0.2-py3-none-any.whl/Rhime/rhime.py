# Create an Interface to find Different types of rhymes
import pathlib
import traceback

class Rhime():
    words = None
    def __init__(self):
        pass

    def load_words_frm_file(self, filepath: str) -> None:
        """"
        Adds words from a file to self.words list
        """

        path = pathlib.Path(filepath)
        if not path.exists(follow_symlinks=False):
            raise FileNotFoundError(filepath)
        
        try:
            with open(path, "r") as file:
                words = file.readlines()
        except Exception as error:
            print(traceback.format_exc())
        
        words = list(set(map(str.strip, words)))
        words = list(filter(lambda x: len(x) > 1, words))
        print(len(words),"Words loaded")
        if not self.words:
            self.words = words
            return
        self.words += words