import os
import queue
import time
import traceback
from datetime import datetime
from threading import Thread

import requests

from typing import Dict, List
from app import constants


class Updater(Thread):

    def __init__(self, queue:queue.Queue):
        self.queue = queue
        self.synonyms_by_line : Dict[int, List[str]] = {}
        self.lines_by_synonyms : Dict[str, int] = {}
        self.lines = 0
        self.load_synonyms()
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                if not self.queue.empty():
                    self.process_synonyms(self.queue.get())
            except:
                print(datetime.now().isoformat() + " " + traceback.format_exc())
            time.sleep(constants.UPDATER_RUN_INTERVAL)

    #loads synonyms into memory, they load the synonyms by line numbers
    #they also store them as lines by synonyms
    def load_synonyms(self):
        with open(constants.SYNONYMS_PATH) as f:

            lines = f.read().splitlines()
            self.lines = len(lines)

            for idx, line in enumerate(lines):
                words = line.split(',')
                for word in words:

                    if word not in self.lines_by_synonyms:
                        self.lines_by_synonyms[word] = idx

                    if idx not in self.synonyms_by_line:
                        self.synonyms_by_line[idx] = []

                    self.synonyms_by_line[idx].append(word)

    def process_synonyms(self, synonym_list):

        #update in memory synonyms
        if self.lines == 0:
            self.process_first_synonyms(synonym_list)
        else:
            self.process_appending_synonyms(synonym_list)
        
        #update solr
        self.dump_synonyms()
        requests.get(f"http://{constants.SOLR_HOST}:8983/solr/admin/cores?action=RELOAD&core=mycore")

    def process_first_synonyms(self, synonym_list):
        self.synonyms_by_line[0] = synonym_list
        for synonym in synonym_list:
            self.lines_by_synonyms[synonym] = 0
        self.lines = 1

    def process_appending_synonyms(self, synonym_list):
            #check if there is a match on any synonym and append it
            for synonym in synonym_list:
                if synonym in self.lines_by_synonyms:
                    idx = self.lines_by_synonyms[synonym]
                    self.synonyms_by_line[idx] = list(dict.fromkeys(self.synonyms_by_line[idx] + synonym_list))
                    for synonym in synonym_list:
                        if synonym not in self.lines_by_synonyms:
                            self.lines_by_synonyms[synonym] = idx
                    return
                     
            #if its a new one then ...
            self.synonyms_by_line[self.lines] = list(dict.fromkeys(synonym_list))

            for synonym in synonym_list:
                if synonym not in self.lines_by_synonyms:
                    self.lines_by_synonyms[synonym] = self.lines
            self.lines = self.lines + 1


    def dump_synonyms(self):

        #cleanup leftover if exists
        if os.path.exists(f"{constants.CONF_PATH}synonyms2.txt"):
            os.remove(f"{constants.CONF_PATH}synonyms2.txt")

        #dump in memory synonyms to file
        with open(f"{constants.CONF_PATH}synonyms2.txt", "w") as textfile:
            for idx in self.synonyms_by_line:
                line = ','.join(self.synonyms_by_line[idx])
                line = line + "\n"
                textfile.write(line)

        #replace old synonyms with new synonyms making an atomic change
        os.replace(f"{constants.CONF_PATH}synonyms2.txt", constants.SYNONYMS_PATH)
        

