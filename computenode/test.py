from data_pipeline.document_parser import DocumentParser

parser = DocumentParser()
print(parser.parse_url(
    "https://www.spotify.com/au/legal/privacy-policy/")[2])
