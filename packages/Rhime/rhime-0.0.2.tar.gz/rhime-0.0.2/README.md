# Rhime
A simple python library to find rhymes of hindi words

## Usage

Import the following modules to your project
```python
from Rhime.rhime import Rhime
from Rhime.ipa import IpaRhyme
```

Load the words from a file
```python
rhyme = Rhime()
rhyme.load_words_frm_file('path/to/file1.txt') # Creates a list Rhyme.words
rhyme.load_words_frm_file('path/to/file2.txt') # Appends words from file2.txt to Rhyme.words
```
For IPA based rhyme:
```python
word = "तुकांत"
ipa = IpaRhyme(rhyme)
print(ipa.get_ipa_rhyme(word))
```