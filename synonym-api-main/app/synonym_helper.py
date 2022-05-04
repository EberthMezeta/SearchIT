import traceback
from nltk.corpus import wordnet

def get_synonyms(word:str, lang:str):
    try:
        results = []
        for syn in wordnet.synsets(word, lang=(lang)):
            for name in syn.lemma_names(lang):
                results.append(name)
        return results
    except BaseException as ex:
        print(traceback.format_exc())
        return []