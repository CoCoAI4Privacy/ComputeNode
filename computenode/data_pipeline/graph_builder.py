import sys
import io
from .segment import Segment
from .core_nlp import CoreNLP
from fastText import load_model


class GraphBuilder:
    def __init__(self, word_embedding_path, sentence_tokenizer=None, word_tokenizer=None, edge_selection=None):

        if sentence_tokenizer == None or word_tokenizer == None:
            if "nltk.tokenize" not in sys.modules:
                print("Loading nltk tokenizers...")
                from nltk.tokenize import sent_tokenize, word_tokenize
            if "sent_tokenize" not in sys.modules:
                print("Sent tokenize was not found!")
                from nltk.tokenize import sent_tokenize, word_tokenize
                if "sent_tokenize" not in sys.modules:
                    print("Sent tokenize is still not found!")

        if sentence_tokenizer == None:
            self.sentence_tokenizer = sent_tokenize
        else:
            self.sentence_tokenizer = sentence_tokenizer

        if word_tokenizer == None:
            self.word_tokenizer = word_tokenize
        else:
            self.word_tokenizer = word_tokenizer

        self.edge_selection = edge_selection
        self.nlp = CoreNLP()

        print("Loading fasttext model...")
        self.model = load_model(word_embedding_path)
        self.word_embedding = self.model.get_word_vector

    def build(self, text: str):
        return Segment(text, self.sentence_tokenizer, self.word_tokenizer, self.word_embedding, self.nlp.annotate, self.edge_selection)
