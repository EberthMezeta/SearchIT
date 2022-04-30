from utils.pdfDataExtractor import pdfDataExtractor
from utils.tokenizer import tokenizer
import pysolr
import os
import json
import requests


class clientSorl:

    run_interval = .5  # seconds
    solr_host = os.getenv("SOLR_HOST", "host.docker.internal")
    synonym_api = os.getenv("SOLR_HOST", "host.docker.internal")
    synonym_updater = os.getenv("SOLR_HOST", "host.docker.internal")
    solr = pysolr.Solr(
        f'http://{solr_host}:8983/solr/mycore/', always_commit=True)

    def submit_document(self, Path_File):

        pdfextractor = pdfDataExtractor()

        tokenize = tokenizer()
        content = pdfextractor.get_text_content(Path_File)

        tokenz = tokenize.get_tokenz(content)
        metadata = pdfextractor.get_meta_data(Path_File)
        print(metadata)
        title = "pez"

        for token in tokenz:
            self.updateSynonyms(token)

        metadata = pdfextractor.get_meta_data(Path_File)
        textUnWhiteSPace = pdfextractor.get_text_content_no_white_space(
            Path_File)
        snipped = textUnWhiteSPace[0:50]
        size = len(tokenz)
        textClean = " ".join(tokenz)

        document = {
            "title": title,
            "_title_": title,
            "text": textClean,
            "_text_": textClean,
            "_snippet_": snipped,
            "size": size,
            "url": "wwww.h3docs.com/gfgdfgdf",
            "base_url": "wwww.h3docs.com"
        }
        self.solr.add([document])

    pass

    def updateSynonyms(self, word):
        try:
            synonyms = requests.get(
                f"http://{self.synonym_api}:8091/spa?word={word}").json()
            synonyms.append(word)  # in case the synonyms didn't return it
            if len(set(synonyms)) > 1:
                print("sending synonym list " + json.dumps(synonyms))
                update_response = requests.post(
                    f"http://{self.synonym_updater}:8092/update", data=json.dumps(synonyms))
                update_response.raise_for_status()
        except:
            print('error updating synonyms for ' + word)
        pass
