import unidecode
import traceback
from nltk import word_tokenize
from nltk.corpus import stopwords


class tokenizer:
    def get_clean_query(self, query):
        try:
            # lower case
            clean_query = query.lower()
            # remove accents
            clean_query = unidecode.unidecode(clean_query)
            # tokenize
            tokens = word_tokenize(clean_query, language="spanish")
            # Remove punctuations, other formalities of grammar
            tokens = [word for word in tokens if word.isalpha()]
            # Remove white spaces and StopWords
            tokens = [
                word for word in tokens if not word in stopwords.words("spanish")]

            clean_query = ""
            for token in tokens:
                word = str(token)
                if word != 'not' and word != 'and' and word != 'or':
                    clean_query = clean_query + word + '~ '
                else:
                    clean_query = clean_query + word + ' '
            if len(tokens) == 0:
                clean_query = '*:*'

            return clean_query
        except BaseException as ex:
            print(traceback.format_exc())
            '''
        Si hay algun error en el procesamiento de la consulta, 
        no hay que fallar, hay que presentar resultados
        '''
            return '*:*'
