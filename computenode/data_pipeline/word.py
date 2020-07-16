from .node import Node


class Word(Node):
    def __init__(self, text: str, id_gen, word_embedding):
        super().__init__(id_gen.get_id(), text)

        self.raw_text = text
        self.embedding = word_embedding(text.lower())

    def get_text(self) -> str:
        return self.raw_text

    def get_embedding(self):
        return self.embedding

    def get_features(self):
        return self.embedding
