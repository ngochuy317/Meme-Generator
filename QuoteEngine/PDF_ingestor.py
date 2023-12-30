from .ingestor_interface import IngestorInterface, QuoteModel
from typing import List
import random
import subprocess


class PDFIngestor(IngestorInterface):
    """
    Parsing the contents of a pdf file.
    """
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest Exception')

        tmp = f'./tmp/{random.randint(0,1000000)}.txt'
        cmd = f"./pdftotext -layout -nopgbrk {path} {tmp}"
        call = subprocess.call(['pdftotext', '-layout', path, tmp])

        quotes = []
        with open(tmp, "r", encoding='utf-8-sig') as t:
            for _, line in enumerate(t):
                parsed = line.strip().split('-')
                if parsed != ['']:
                    new_quote = QuoteModel(parsed[0], parsed[1])
                    quotes.append(new_quote)
        return quotes