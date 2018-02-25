import time
import json

from datetime import datetime
from elasticsearch import Elasticsearch

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'projectx'
TYPE_NAME = 'metric'


es = Elasticsearch()

request_body = {
	    "settings" : {
	        "number_of_shards": 5,
	        "number_of_replicas": 1
	    },

	    'mappings': {
	        INDEX_NAME: {
	            'properties': {
                    'id': {'type': 'float'},
                    'insert_date': {'type': 'date'},
	                'lcode': {'type': 'float'},
                    'lcom': {'type': 'float'},
					'lcom_pred': {'type': 'float'},
                    'class': {'type': 'float'}
	            }}}
	}

es.indices.create(index = INDEX_NAME, body = request_body)
print ("Index " + INDEX_NAME + " created!")