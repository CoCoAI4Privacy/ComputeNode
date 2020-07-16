import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from .id_generator import IDGenerator
from .sentence import Sentence
from .node import Node
from .edge import Edge, EdgeType, connect_next_nodes, connect_source_node


class Segment(Node):
    def __init__(self, text: str, sentence_tokenizer, word_tokenizer, word_embedding, annotate, edge_selection=None):
        node_id_gen = IDGenerator()
        super().__init__(node_id_gen.get_id(), "Segment")
        paragraphs = text.split("\n")
        sentences = []
        for paragraph in paragraphs:
            sentences.extend(sentence_tokenizer(paragraph))

        sentence_nodes = [Sentence(sentence, word_tokenizer, node_id_gen, word_embedding)
                          for sentence in sentences]
        connect_source_node(self, sentence_nodes, EdgeType.SOURCE_SEG)

        if edge_selection != None:
            if "NEXT" in edge_selection:
                connect_next_nodes(sentence_nodes, EdgeType.NEXT_SENTENCE)
            if "DEPENDENCY" in edge_selection or "COREF" in edge_selection or "Relation" in edge_selection:
                #annotation = annotate(text)
                pass

    def export_to_NX(self):
        G = nx.MultiDiGraph()
        G.graph["features"] = self.get_features()
        node_labels = {}
        edge_labels = {}
        self.add_to_nx_graph(G, node_labels, edge_labels)
        return G, node_labels, edge_labels

    def export_to_CNN(self):
        word_embeddings = []
        for edge in self.edges:
            if edge.edge_type == EdgeType.SOURCE_SEG:
                word_embeddings = edge.from_node.export_to_CNN(word_embeddings)
        return word_embeddings

    def visualise(self):
        G, node_labels, edge_labels = self.export_to_NX()
        pos = nx.nx_pydot.graphviz_layout(
            G, prog="C:/Program Files (x86)/Graphviz2.38/bin/twopi.exe")
        plt.figure()
        nx.draw(G, pos, labels=node_labels, with_labels=True, arrowsize=13)
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color="red")
        plt.axis("off")
        plt.show()
