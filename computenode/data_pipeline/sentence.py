from .node import Node
from .edge import Edge, EdgeType, connect_next_nodes, connect_source_node
from .word import Word


class Sentence(Node):
    def __init__(self, text: str, word_tokenizer, id_gen, word_embedding):
        super().__init__(id_gen.get_id(), "Sentence")
        words = word_tokenizer(text)
        word_nodes = [Word(word, id_gen, word_embedding) for word in words]
        connect_next_nodes(word_nodes, EdgeType.NEXT_WORD)
        connect_source_node(self, word_nodes, EdgeType.SOURCE_SENT)

    def export_to_CNN(self, word_embeddings):
        for edge in self.edges:
            if edge.edge_type == EdgeType.SOURCE_SENT and edge.from_node != self:
                word_embeddings.append(edge.from_node.get_embedding())
        return word_embeddings
