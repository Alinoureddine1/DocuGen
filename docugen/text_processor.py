from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import random

def get_synonyms(word, tag):
    if tag.startswith('NN'):
        synsets = wn.synsets(word, pos=wn.NOUN)
    elif tag.startswith('VB'):
        synsets = wn.synsets(word, pos=wn.VERB)
    elif tag.startswith('JJ'):
        synsets = wn.synsets(word, pos=wn.ADJ)
    elif tag.startswith('RB'):
        synsets = wn.synsets(word, pos=wn.ADV)
    else:
        return []

    synonyms = []
    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma.name() != word:
                synonyms.append(lemma.name())
    return list(set(synonyms))

def paraphrase(text):
    words = word_tokenize(text)
    tagged = pos_tag(words)
    
    result = []
    for word, tag in tagged:
        synonyms = get_synonyms(word, tag)
        if synonyms and random.random() < 0.3:  # 30% chance to replace with synonym, might change it
            replacement = random.choice(synonyms)
            result.append(replacement)
        else:
            result.append(word)
    
    return ' '.join(result)