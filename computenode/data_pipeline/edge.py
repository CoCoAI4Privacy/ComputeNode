import numpy as np


class EdgeType:
    NEXT_SENTENCE = "Next Sentence"
    NEXT_WORD = "Next Word"
    SOURCE_SENT = "Source Sentence"
    SOURCE_SEG = "Source Segment"

    features = {
        NEXT_SENTENCE: np.asarray([1, 0, 0, 0], dtype=np.float64),
        NEXT_WORD: np.asarray([0, 1, 0, 0], dtype=np.float64),
        SOURCE_SENT: np.asarray([0, 0, 1, 0], dtype=np.float64),
        SOURCE_SEG: np.asarray([0, 0, 0, 1], dtype=np.float64)
    }


class Edge:
    def __init__(self, from_node, to_node, edge_type: str, bidirectional: bool):
        self.from_node = from_node
        from_node.add_edge(self)
        self.to_node = to_node
        to_node.add_edge(self)
        self.edge_type = edge_type
        self.features = EdgeType.features[edge_type]
        self.bidirectional = bidirectional
        self.id = (self.from_node.get_id(),
                   self.edge_type, self.to_node.get_id())

    def get_id(self):
        return self.id

    def get_features(self):
        return self.features

    def print(self):
        arrow = "<" if self.bidirectional else ""
        print(
            f"{self.edge_type}: {self.from_node.get_text()} {arrow}-> {self.to_node.get_text()}")

    def add_to_nx_graph(self, G, node_labels: dict, edge_labels: dict):
        edge_id = self.get_id()
        if edge_id in edge_labels:
            return

        # !!! THIS MAY CAUSE PROBLEMS WHEN HAVING MULTIPLE EDGES BETWEEN THE SAME NODES
        G.add_edge(edge_id[0], edge_id[2], features=self.get_features())
        edge_labels[edge_id] = self.edge_type
        if self.from_node.get_id() not in node_labels:
            self.from_node.add_to_nx_graph(G, node_labels, edge_labels)
        if self.to_node.get_id() not in node_labels:
            self.to_node.add_to_nx_graph(G, node_labels, edge_labels)


def connect_next_nodes(nodes: list, edge_type: str):
    edges = []
    prev_node = None
    for node in nodes:
        if prev_node != None:
            edges.append(Edge(prev_node, node, edge_type, True))
        prev_node = node

    return edges


def connect_source_node(source, nodes: list, edge_type: str):
    edges = []
    for node in nodes:
        edges.append(Edge(node, source, edge_type, False))

    return edges
