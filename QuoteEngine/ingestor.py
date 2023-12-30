from .ingestor_interface import IngestorInterface, QuoteModel
from typing import List
from .Docx_ingestor import DocxIngestor
from .Text_ingestor import TextIngestor
from .CSV_ingestor import CSVIngestor
from .PDF_ingestor import PDFIngestor

class Ingestor(IngestorInterface):
    
    importers = [
        DocxIngestor,
        TextIngestor,
        CSVIngestor,
        PDFIngestor,
    ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for importer in cls.importers:
            if importer.can_ingest(path):
                return importer.parse(path)
