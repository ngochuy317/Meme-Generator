from typing import List
from abc import ABCMeta, abstractmethod


class QuoteModel(object):
    
    def __init__(self, body: str, author: str):
        self.body = body
        self.author = author
    
    def __repr__(self):
        return f'"{self.body}" - {self.author}'


class IngestorInterface(metaclass=ABCMeta):

    @classmethod
    def can_ingest(cls, path:str) -> bool:
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass