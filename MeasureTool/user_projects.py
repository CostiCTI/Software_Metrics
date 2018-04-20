'''
	This file contains contains functions for elasticsearch operations
'''

import time
import json
import math

from datetime import datetime
from elasticsearch import Elasticsearch


def delete_project(project_name):
	'''
		This function delete an index in elasticsearch

	Parameters:
	-----------
	project_name	string, name of the index

	Returns:
	--------
	None
	'''
	
	es = Elasticsearch()
	es.indices.delete(index=project_name)


def get_projects():
	'''
		This function returns all indexes from elasticsearch that
	start with substring 'measure_'

	Parameters:
	-----------
	None

	Returns:
	--------
	list of indexes
	'''
	es = Elasticsearch()
	projects = []

	for index in es.indices.get('*'):
		if index.startswith("measure_"):
			projects.append(index[8:])

	return projects


def add_phase(index, code, comm, op):

	ES_HOST    = {"host" : "localhost", "port" : 9200}
	INDEX_NAME = index
	TYPE_NAME  = 'metric'
	
	es = Elasticsearch()

	MODELCOMM = load_model('../model_lr_codecomm')
	MODELOP = load_model('../model_lr_code_operands')

	data_dict['lcom_pred'] = (MODELCOMM.predict(data_dict['lcode']))[0][0]

	compred = math.floor((MODELCOMM.predict(data_dict['code']))[0][0])
	oppred  = math.floor((MODELOP.predict(data_dict['code']))[0][0])

	if compred < 0:
		compred = 0
	if oppred < 0:
		oppred = 0

	es.index(index=INDEX_NAME, doc_type='metric', body={
		'id': 1,
		'insert_date': int(time.time() * 1000),
		'lcode': code,
		'lcom': comm,
		'lcom_pred': compred,
		'operands': op,
		'operands_pred': oppred
	})


def get_project_data(index):

	ES_HOST    = {"host" : "localhost", "port" : 9200}
	INDEX_NAME = index
	TYPE_NAME  = 'metric'
	
	es = Elasticsearch()

	query = {
		'query': {
			'match_all' : {}
			}
		}

	res = es.search(index=INDEX_NAME, body=query)

	import pprint as pp
	for r in res['hits']['hits']:
		pp.pprint(r)



def create_new_project(index_name):
	'''
		Create a new index with a starting registration

	Parameters:
	-----------
	index_name	string, name of the new index

	Returns:
	--------
	None
	'''

	ES_HOST    = {"host" : "localhost", "port" : 9200}
	INDEX_NAME = 'measure_' + index_name
	TYPE_NAME  = 'metric'

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


#add_phase('measure_audi', 226, 63, 112, 318, 298)
#get_project_data('measure_audi')