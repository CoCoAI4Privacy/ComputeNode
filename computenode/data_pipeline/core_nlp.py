from stanfordnlp.server import CoreNLPClient

import json


class CoreNLP:
    def __init__(self, annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref', 'relation', 'openie', 'entitylink', 'kbp']):
        print("Loading Stanford CoreNLP server...")
        self.client = CoreNLPClient(start_server=False,
                                    annotators=annotators, timeout=300000, memory="16G", be_quiet=False)

    def annotate(self, text):
        return self.client.annotate(text)

    def close(self):
        self.client.stop()


if __name__ == "__main__":
    cnlp = CoreNLP()
    print("Annotating...")
    result = cnlp.annotate("My cat is called David.\nHe is 5 years old.")
    print("Done!")
    print(result)
    cnlp.close()
