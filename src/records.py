import re
from numpy import exp
from dataclasses import dataclass
from typing import List, Dict
from aws_lambda_powertools import Logger

logger = Logger(service="redlie-data-proccesing")


def normalize(items: List[str]) -> List[str]:
    normalized_items = []
    for word in items:
        w = word.lower().strip()
        w = w.replace('á', 'a')
        w = w.replace('é', 'e')
        w = w.replace('í', 'i')
        w = w.replace('ó', 'o')
        w = w.replace('ú', 'u')
        normalized_word = re.sub(r'\W+', '', w)
        normalized_items.append(normalized_word)
    return normalized_items


@dataclass
class Record:
    ni: str
    ci: str
    items: list

    def __init__(self, ni, ci, items):
        self.ni = ni
        self.ci = ci
        self.items = normalize(items)

    def __str__(self):
        return f"NI: {self.ni}, CI: {self.ci}, Items: {self.items}"


class Records:
    def __init__(self, records: List[Dict], name):

        self.name = name
        self.all_records: List[Record] = []
        self.nis: List[str] = []
        self.cis: List[str] = []
        self.words: List[str] = []
        self.ni_records: Dict[str, List[str]] = {}
        self.ni_ci_records: Dict[str, Dict[str, List[str]]] = {}
        self.ci_ni_records: Dict[str, Dict[str, List[str]]] = {}
        self.ci_words: Dict[str, List[str]] = {}
        self.ci_words2: [dict] = []
        self.disp: [dict] = []

        self.process(records)

        self.total_words: int = len(self.words)
        self.total_cis: int = len(self.cis)
        self.total_nis: int = len(self.nis)
        self.stats = {"total_words": self.total_words, "total_cis": self.total_cis, "total_nis": self.total_nis}

        self.disposition_index()

    def process(self, records: List[Dict]):
        for r in records:
            try:
                ci, ni, items_str = r.get('CI'), r.get('NI'), r.get('ITEMS')
                if ci == 'CI' or ni == 'NI' or not isinstance(items_str, str):
                    continue

                items_list = items_str.split(',')
                self.add(Record(ni, ci, items_list))
            except Exception as e:
                print(f"[ERROR] Error parsing record: {r}")

        # Remove duplicates from self.ci_words
        for ci, words in self.ci_words.items():
            self.ci_words[ci]['words'] = sorted(list(filter(None, set(words['words']))))
            self.ci_words[ci]['total'] = len(self.ci_words[ci]['words'])
            self.ci_words2.append(self.ci_words[ci])

    def add(self, record: Record):
        if not record.items:
            return

        self.all_records.append(record.__dict__)
        if record.ci not in self.ci_words.keys():
            self.ci_words[record.ci] = {'words': [], 'total': 0, 'ci': record.ci}

        self.ci_words[record.ci]['words'].extend(record.items)

        if record.ni not in self.ni_records:
            self.ni_records[record.ni] = []

        if record.ni not in self.ni_ci_records:
            self.ni_ci_records[record.ni] = {}

        if record.ci not in self.ci_ni_records:
            try:
                self.ci_ni_records[record.ci][record.ni] = []
            except Exception as e:
                pass

        self.ni_records[record.ni].extend(record.items)

        if record.ci not in self.ni_ci_records[record.ni]:
            self.ni_ci_records[record.ni][record.ci] = []

        self.ni_ci_records[record.ni][record.ci].extend(record.items)
        # self.ci_ni_records[record.ci][record.ni].extend(record.items)

        if record.ni not in self.nis:
            self.nis.append(record.ni)
        if record.ci not in self.cis:
            self.cis.append(record.ci)

        self.words.extend(record.items)

    def disposition_index(self):
        for i in sorted(self.ci_words.keys()):
            disp = {}
            values = self.index(i)
            disp["ci"] = i
            disp["values"] = values
            self.disp.append(disp)

    def index(self, ci):
        words = [rec["items"] for rec in self.all_records
                 if rec["ci"] == str(ci) and isinstance(rec["items"], list)]
        # Parameters for the operation
        entries, max_list = len(words), max(len(lst) for lst in words)
        logger.info(f"[{self.name}] Number of entries and max length for one entry is: "
                    f"{str(entries)}, {str(max_list)} for ci: {str(ci)}")

        header = self.ci_words[str(ci)]["words"]
        # Create a matrix with the position of appearance for each different word
        evaluate = {}
        for head in header:
            indexes = []
            for word in words:
                if head in word:
                    indexes.append(word.index(head) + 1)
            evaluate[head] = sorted(indexes)
        # Store and make the sum for all the different words to obtain the lexical index
        lexical_index = {}
        for head in header:
            value = 0
            for i in set(evaluate[head]):
                # Count frequency and sum value for each word position
                freq = evaluate[head].count(i)
                value += exp(-2.3 * (i - 1) / (max_list - 1)) * freq / entries
            # Calculate value for lexical index
            lexical_index[head] = round(value, 8)
        # Sort the lexical_index dictionary by values in descending order
        lexical_index = dict(sorted(lexical_index.items(), key=lambda item: item[1], reverse=True))
        top10 = {key: lexical_index[key] for key in list(lexical_index.keys())[:10]}
        logger.info(f"[{self.name}] Top 10 lexical index for ci {ci} are: {top10}")
        return lexical_index

