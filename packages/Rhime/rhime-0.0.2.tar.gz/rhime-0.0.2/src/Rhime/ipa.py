from .ipa_trie import IPATrie
import epitran

class IpaRhyme:
    def __init__(self, rhyme) -> None:
        self.ipa_translits = {}

        self.__rhyme = rhyme
        self.__epi = epitran.Epitran("hin-Deva")
        self.__buildTrie()

    def __buildTrie(self):
        self.IPATrie = IPATrie()

        for word in self.__rhyme.words:
            try:
                ipa_list = self.__epi.trans_list(word)
            except Exception as error:
                print("Failed to transliterate word %s into IPA".format(word))
                ipa_list = None

            if ipa_list:
                self.IPATrie.add_word(ipa_list, word)

    def __get_suffix_match_len(self, target_ipa: str, candidate_ipa: str) -> int:

        match_len = 0
        len_word = min(len(target_ipa), len(candidate_ipa))

        for ch in range(1, len_word  + 1):
            if target_ipa[-ch] == candidate_ipa[-ch]:
                match_len += 1
            else:
                break
        return match_len
    
    def get_ipa_rhyme(self, target):
        return self.IPATrie.search(self.__epi.trans_list(target))
