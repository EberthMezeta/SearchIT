from nltk import word_tokenize
from nltk.corpus import stopwords
import unidecode


class tokenizer:

    def get_tokenz(self, text):
        # Remove accents
        text = unidecode.unidecode(text)
        # To Lower Case
        text = text.lower()
        # Tokenizer
        tokens = word_tokenize(text)
        # Remove punctuations, other formalities of grammar
        tokens = [word for word in tokens if word.isalpha()]
        # Remove white spaces and StopWords
        tokens = [
            word for word in tokens if not word in stopwords.words("spanish")]
        return tokens
