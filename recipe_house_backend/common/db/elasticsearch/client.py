from django.conf import settings
from elasticsearch import Elasticsearch

from recipe_house_backend.common.utils.logger import get_logger


class ElasticSearchClient:
    """
    A singleton object for communicating with ES through REST
    """
    __es_client = None

    def __init__(self):
        self.__logger = get_logger()
        self.__create_client()

    @staticmethod
    def get_client():
        if ElasticSearchClient.__es_client is None:
            ElasticSearchClient()
        return ElasticSearchClient.__es_client

    def __create_client(self):
        """
        Initializes  ElasticSearch  Client
        :return : Elasticsearch client
        """
        __host_url = settings.ES_HOST_URL
        __timeout = settings.ES_TIMEOUT
        __max_retries = settings.ES_MAX_RETRIES
        __retry_on_timeout = settings.ES_RETRY_ON_TIMEOUT

        __ca_certs = None
        __verify_ca_certs = None
        __enable_auth = False
        __username = None
        __password = None

        self.__logger.info("Initializing the ElasticSearch Client")
        self.__logger.info("ElasticSearch Host:" + "".join(__host_url))

        __client = None
        print(__retry_on_timeout)
        __client = Elasticsearch(timeout=__timeout,
                                 hosts=__host_url,
                                 max_retries=__max_retries,
                                 retry_on_timeout=__retry_on_timeout
                                 )

        if self.__check_connection_status(__client):
            ElasticSearchClient.__es_client = __client
            self.__logger.info("ElasticSearch Client connected successfully")
        else:
            self.__logger.info("Not able to connect to ElasticSearch")
            raise Exception("Cannot Communicate with Elastic search , Pls check Connectivity")

    def __check_connection_status(self, client):
        """
        This  function will check the client
        :param client: Elastic search client  Object
        :return: bool: return the status of ES connection
        """
        return bool(client.ping())
