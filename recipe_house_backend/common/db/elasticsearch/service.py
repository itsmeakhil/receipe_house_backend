from elasticsearch import helpers

from blue_agilis_backend.common.db.elasticsearch.client import ElasticSearchClient
from blue_agilis_backend.common.utils.logger import get_logger


class ElasticSearchService(object):
    """
    This Class will provide basic CRUD operations for ES as functions
    """

    def __init__(self):
        self.__logger = get_logger()
        self.es_client = ElasticSearchClient.get_client()

    def _insert_document(self, index, doc_type, doc_id, body, parent):
        res = self.es_client.index(index=index, doc_type=doc_type, body=body, parent=parent)
        self.__logger.debug(
            "ElasticSearchService | insert document| success | id :" + doc_id)
        return res

    def _perform_bulk_operation(self, actions):
        return helpers.bulk(self.es_client, actions, request_timeout=200)

    def _insert_document_without_id(self, index, body):
        # Insert a document with id of the document
        res = self.es_client.index(index=index, body=body)
        self.__logger.debug(f'Data insertion response- {res}')
        return res

    def index(self, index, body):
        # Function to index document to elastic search
        res = self.es_client.index(index=index, body=body)
        self.__logger.debug(f'Data insertion response- {res}')
        return res

    def delete(self, index, id):
        # Function to delete document from elastic search passing id
        res = self.es_client.delete(index=index, id=id)
        self.__logger.debug(f'Data delete response- {res}')
        return res

    def get_all(self, index, body=None):
        # Function to fetch all the details from elastic search
        res = self.es_client.search(index=index, body=body)
        data = []
        for hit in res['hits']['hits']:
            hit['_source']['_id'] = hit['_id']
            data.append(hit['_source'])
        self.__logger.debug(f'Data fetch response- {res}')
        return data
