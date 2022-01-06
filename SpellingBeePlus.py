from collections import deque
from typing import List, Optional, Dict
from data import DATA_PATH


class BeeTree:
    letter: str
    is_word: bool
    children: Dict[str,'BeeTree']

    def __init__(self, ch: str):
        self.letter = ch
        self.is_word = False
        self.children = {}


def _index(tree: BeeTree, word:str):
    if len(word)==0:
        tree.is_word = True
    else:
        letter = word[0]
        if not letter in tree.children:
            child = BeeTree(letter)
            tree.children[letter] = child
            _index(child,word[1:])
        else:
            child = tree.children[letter]
            _index(child,word[1:])


def _search(tree:BeeTree, pattern:str, candidate:str, has_req:bool):
    if tree.letter == pattern[0]:
        has_req = True
    candidate += tree.letter
    if tree.is_word and has_req:
        yield candidate
    for letter,child in tree.children.items():
        if letter in pattern:
            yield from _search(child,pattern,candidate,has_req)

class SpellingBeePlus:
    _dictionary: Optional[BeeTree]

    def __init__(self):
        self._dictionary = None

    def get_words(self, pattern: str):
        pattern = pattern.lower()
        results = []
        for result in self._gen_words(pattern):
            results.append(result)
        results.sort(reverse=False, key=lambda t: t[0])
        results.sort(reverse=True, key=lambda t: t[1])
        return [t[0] for t in results]

    def dictionary(self):
        if not self._dictionary:
            dictionary = BeeTree('')
            with open(DATA_PATH / "dictionary.txt") as file:
                for word in file:
                    _index(dictionary,word[:-1])
            self._dictionary = dictionary
        return self._dictionary

    def _gen_words(self, pattern: str):
        required = pattern[0]

        for word in _search(self.dictionary(),pattern,'',False):
            pangram = set(pattern)
            for letter in word:
                if letter in pangram:
                    pangram.remove(letter)
            score = len(word)
            if score == 4:
                score = 1
            if len(pangram) == 0:
                score += 7
            yield (word, score)
