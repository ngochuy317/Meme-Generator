from .ingestor_interface import IngestorInterface, QuoteModel
from typing import List
import docx


class DocxIngestor(IngestorInterface):
    """
    Parsing the contents of a docx file.
    """
    
    allowed_extensions = ['docx']
    
    @classmethod
    def parse(cls, path:str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception')
        
        quotes = []
        d = docx.Document(path)
      
        for para in d.paragraphs:
            if para.text != '':
                parse = para.text.split('-')
                new_quote = QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)
        return quotes