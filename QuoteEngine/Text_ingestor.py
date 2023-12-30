from .ingestor_interface import IngestorInterface, QuoteModel
from typing import List


class TextIngestor(IngestorInterface):
    """
    Parsing the contents of a txt file.
    """
    
    allowed_extensions = ['txt']
    
    @classmethod
    def parse(cls, path:str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception')

        quotes = []

        with open(path, "r", encoding='utf-8-sig') as t:
            for _, line in enumerate(t):
                parsed = line.strip().split('-')
                new_quote = QuoteModel(parsed[0], parsed[1])
                quotes.append(new_quote)
        return quotes