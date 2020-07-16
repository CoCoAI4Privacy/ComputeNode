from .edge import EdgeType
import numpy as np


class Node:
    def __init__(self, id: int, label: str):
        self.id = id
        self.label = label
        self.edges = []
        self.features = None

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_features(self):
        if type(self.features) is not np.ndarray:
            features = []
            for edge in self.edges:
                if edge.edge_type in [EdgeType.SOURCE_SENT, EdgeType.SOURCE_SEG] and edge.to_node == self:
                    features.append(edge.from_node.get_features())
            self.features = np.asarray([sum(feature)
                                        for feature in zip(*features)])
        return self.features

    def add_to_nx_graph(self, G, node_labels: dict, edge_labels: dict):
        G.add_node(self.get_id(), features=self.get_features())
        node_labels[self.get_id()] = self.get_label()

        for edge in self.edges:
            edge.add_to_nx_graph(G, node_labels, edge_labels)
