import time
import json

from datetime import datetime
from elasticsearch import Elasticsearch


def create_new_project(type_name, index_name):

	ES_HOST    = {"host" : "localhost", "port" : 9200}
	INDEX_NAME = 'measure_' + index_name
	TYPE_NAME  = type_name

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
						'operands': {'type': 'float'},
						'operands_pred': {'type': 'float'}
					}}}
		}

	es.indices.create(index = INDEX_NAME, body = request_body)


	es.index(index=INDEX_NAME, doc_type='metric', id=0, body={
		'id': 0,
		'insert_date': int(time.time() * 1000),
		'lcode': 0,
		'lcom': 0,
		'lcom_pred': 0,
		'operands': 0,
		'operands_pred': 0
	})

	print ("Project " + INDEX_NAME + " created!")

create_new_project('metric', 'gg')