import re
import urllib
from .graph_builder import GraphBuilder
from pathlib import Path


def training_extractor(text: str) -> str:
    new_text = text
    new_text = re.sub(r"<(?:script|style|header|nav|noscript|iframe|svg|path|head).*?</(?:script|style|header|nav|noscript|iframe|svg|path|head)>",
                      "", new_text, flags=re.S)
    new_text = re.sub(r"<br>(\s*<br>)*", "\n", new_text)
    new_text = re.sub(r"<.*?>", "", new_text)
    new_text = re.sub(r"\s{2,}", "\n", new_text)
    return new_text


def training_segmenter(text: str) -> list:
    segments = text.split("|||")
    for index, segment in enumerate(segments):
        segments[index] = segment.strip()
    return segments


class DocumentParser:
    def __init__(self, embedding="..\\data\\policies_model_300.bin", text_extractor=training_extractor, text_segmenter=training_segmenter, edge_selection=None):
        self.graph_builder = GraphBuilder(
            embedding, edge_selection=edge_selection)
        self.text_extractor = text_extractor
        self.text_segmenter = text_segmenter

    def parse_file(self, path):
        text = Path(path).read_text()
        return self.parse_text(text)

    def parse_url(self, url):
        try:
            with urllib.request.urlopen(url) as page:
                downloaded = page.read()
                text = downloaded.decode("utf8")
                return self.parse_text(text)
        except Exception as e:
            print("An error occurred:", type(e).__name__, e.args)
            print(e)
            return None

    def parse_text(self, text):
        extracted = self.text_extractor(text)
        print(extracted)
        segments = self.text_segmenter(extracted)
        graphs = [self.graph_builder.build(segment) for segment in segments]
        return (text, extracted, segments, graphs)
