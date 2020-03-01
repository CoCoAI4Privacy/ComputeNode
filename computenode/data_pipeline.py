import os
import re
import subprocess
# import fastText

from bs4 import BeautifulSoup, Comment, NavigableString
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from nltk.tokenize import sent_tokenize


# Simple implementation to get a MVP
# Will need to be replaced for tracing segments back to their original text
class DataPipeline:
    MODEL_PATH = ""
    GRAPHSEG_INPUT = "graphseg_in"
    GRAPHSEG_OUTPUT = "graphseg_out"

    trash_name = re.compile(
        r"(script|header|head|svg|iframe|footer|nav|img|meta)")
    extract_name = re.compile(
        r"(strong|^a$|span)")
    empty_string = re.compile(r"(^\s*$|^$)")

    def __init__(self):
        if not os.path.exists(self.GRAPHSEG_INPUT):
            os.makedirs(self.GRAPHSEG_INPUT)
        if not os.path.exists(self.GRAPHSEG_OUTPUT):
            os.makedirs(self.GRAPHSEG_OUTPUT)

        self.regex_html = re.compile(r"<[a-z][\s\S]*>")
        print("Loading fasttext model...")
        # self.ft = fastText.load_model(self.MODEL_PATH)
        print("Fasttext model loaded")
        print("Loading Selenium and Chrome")
        options = Options()
        options.headless = True
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(binary_path, options=options)
        print("Selenium and Chrome loaded")

    def process_url(self, url: str):
        self.driver.get(url)
        html = self.driver.page_source
        self.driver.close()
        clean_text, segments, vector_segments = self.process_html(html)
        return (html, clean_text, segments, vector_segments)

    def process_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        self.extract_body(soup)
        self.handle_lists(soup, soup)
        self.extract_data(soup)

        text = soup.get_text("\n", False)
        clean_text, segments, vector_segments = self.process_text(text)

        return (clean_text, segments, vector_segments)

    def extract_body(self, soup: BeautifulSoup):
        trash_list = soup.find_all(self.trash_name)
        for entry in trash_list:
            entry.decompose()

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    def extract_data(self, soup: BeautifulSoup):
        extract_list = soup.find_all(self.extract_name)
        for entry in extract_list:
            entry.replaceWith(entry.get_text(" ", True))

    def handle_lists(self, soup: BeautifulSoup, origin: BeautifulSoup, outer_header=""):
        if outer_header != "":
            inner_header = self._get_first_child(soup)
            if inner_header is not None:
                outer_header = outer_header + " " + inner_header

        lists = self._find_recursive(soup, "ul")
        lists.reverse()
        all_tags = []
        for cur_list in lists:
            list_header = self._get_list_header(cur_list, outer_header)
            if list_header is not None:
                prev_tag = origin.new_tag("p")
                prev_tag.string = list_header
                insert_prev_tag = False
                new_tags = []

                entries = self._find_recursive(cur_list, "li")
                entries.reverse()
                for entry in entries:
                    entry_is_navstr = type(entry) is NavigableString
                    if not entry_is_navstr and entry is not None:
                        new_tags.extend(
                            self.handle_lists(entry, origin, list_header))

                    entry_text = self._get_string(entry)

                    num_words = len(entry_text.split())
                    if num_words > 20:
                        new_tag = origin.new_tag("p")
                        new_tag.string = list_header + " " + entry_text
                        new_tags.append(new_tag)
                    else:
                        insert_prev_tag = True
                        prev_tag.string += " " + entry_text

                if insert_prev_tag:
                    new_tags.append(prev_tag)

                if outer_header == "":
                    for tag in new_tags:
                        cur_list.insert_after(tag)
                else:
                    all_tags.extend(new_tags)

                cur_list.decompose()
        return all_tags

    def process_text(self, text: str):
        text = self.clean_text(text)
        segments = self.create_segments(text)
        vectors = self.vectorize_segments(segments)
        return (text, segments, vectors)

    def clean_text(self, text: str):
        # Remove non-ascii characters
        # text = text.encode("ascii", errors="ignore").decode()

        # Remove duplicate whitespace
        text = re.sub(r"[\r\t\f\v ]{2,}", " ", text)
        text = re.sub(r"\n{3,}", r"\n", text)

        # Remove newlines surrounded by spaces
        text = re.sub(r"( +\n)|(\n +)", " ", text)

        # Replace whitespaces after colons with spaces
        text = re.sub(r":\n", r": ", text)

        # Remove whitespace before punctuation
        text = re.sub(r'\s+([?.,!"])', r'\1',
                      text)

        # Replace newlines that do not come after punctuation with spaces
        text = re.sub(r'([^?.!;"])\n', r'\1 ',
                      text)

        # Remove duplicate whitespace
        text = re.sub(r"[\r\t\f\v ]{2,}", " ", text)
        text = re.sub(r"\n{3,}", r"\n", text)

        return text

    def create_segments(self, text: str):
        return text.splitlines()

    # This method has to preserve segment order
    def split_large_segments(self, text: str):
        with open(os.path.join(self.GRAPHSEG_INPUT, "tmp"), "w") as f:
            f.write(text)

        returncode = subprocess.call(["java", "-jar", "graphseg.jar",
                                      self.GRAPHSEG_INPUT, self.GRAPHSEG_OUTPUT, "0.25", "3"])

        print("Return code:", returncode)

        return text

    def vectorize_segments(self, segments: list):
        return segments

    def close(self):
        self.driver.quit()

    # Private helper methods
    def _find_recursive(self, root: BeautifulSoup, name: str):
        children = []

        if type(root) is not NavigableString and type(root) is not Comment:
            for child in root.children:
                if type(child) is not NavigableString:
                    if child.name == name:
                        children.append(child)
                    else:
                        children.extend(self._find_recursive(child, name))
        return children

    def _get_first_child(self, section: BeautifulSoup):
        first = section.findChild()
        text = self._get_string(first)
        while first is not None and bool(self.empty_string.match(text)):
            first = first.next_sibling
            text = self._get_string(first)

        if first is None:
            return None

        sentences = sent_tokenize(text)
        header = sentences[0]

        return header

    def _get_list_header(self, cur_list: BeautifulSoup, outer_header: str):
        prev = cur_list.previous_sibling
        text = self._get_string(prev)
        while prev is not None and bool(self.empty_string.match(text)):
            prev = prev.previous_sibling
            text = self._get_string(prev)

        if prev is None:
            return None

        sentences = sent_tokenize(text)
        header = sentences[-1]

        return header if outer_header == "" else outer_header + " " + header

    def _get_string(self, soup: BeautifulSoup):
        if soup is None:
            return ""

        if type(soup) is NavigableString:
            return soup
        else:
            return soup.get_text(" ", True)


# spotify: https://www.spotify.com/no/legal/privacy-policy/
# amazon: https://aws.amazon.com/privacy/
# google: https://policies.google.com/privacy?hl=en-US
# linkedin: https://www.linkedin.com/legal/privacy-policy
if __name__ == "__main__":
    pipeline = DataPipeline()
    result = pipeline.process_url(
        "https://aws.amazon.com/privacy/")
    # print(result[0])
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write(result[1])
    pipeline.close()
