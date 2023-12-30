from typing import List
from .ingestor_interface import IngestorInterface, QuoteModel
import pandas


class CSVIngestor(IngestorInterface):
    """
    Parsing the contents of a csv file.
    """
    
    allowed_extensions = ['csv']
    
    @classmethod
    def parse(cls, path:str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception')
        
        quotes = []
        c = pandas.read_csv(path, header=0)
        
        for _, row in c.iterrows():
            new_quote = QuoteModel(row['body'], row['author'])
            quotes.append(new_quote)
        return quotes