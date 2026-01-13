from tinydb import where
from tinydb.table import Document, Table


class TinyModelController:

    def __init__(self, table: Table):
        self.table = table

    def list(self, **kwargs) -> list[Document]:
        result = []
        query_options = []
        for k, v in kwargs:
            query_options.append(where(k) == v)
        for r in self.table.search(*query_options):
            r['doc_id'] = r.doc_id
            result.append(r)
        return result

    def create(self, data: dict) -> Document:
        doc_id = self.table.insert(data)
        return self.table.get(doc_id=doc_id)
