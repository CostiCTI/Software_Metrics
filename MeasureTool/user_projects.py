'''
	This file contains contains functions for elasticsearch operations
'''

import time
import json
import math
import pickle

from datetime import datetime
from elasticsearch import Elasticsearch


def delete_last_phase(index, event_date):

	ES_HOST = {"host" : "localhost", "port" : 9200}
	es = Elasticsearch()
	project_name = 'measure_' + index

	query = {
		"query": { 
			"match": {
				"insert_date": event_date
			}
		}
	}

	es.delete_by_query(index=project_name, doc_type='metric', body=query)


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


def load_model(file_name): 
    # load the model
    filename = file_name + '.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    
    return loaded_model


def get_score(lcode, lcome, oper, option):

	MODELCOMM = load_model('models/model_lr_codecomm')
	MODELOP = load_model('models/model_lr_code_operands')

	compred = math.floor((MODELCOMM.predict(lcode))[0][0])
	oppred  = math.floor((MODELOP.predict(lcode))[0][0])

	if compred < 0:
		compred = 0
	if oppred < 0:
		oppred = 0

	#with open('cfg/score_rules.json') as json_data:
    #	d = json.load(json_data)

	if option == "comments":
		m = lcome
		mp = compred
	else:
		m = oper
		mp = oppred
	score = 0
	dif = abs(m - mp)
	if mp != 0:
		p = dif * 100 / mp
	else:
		# no data, new project
		p = 100
	if p <= 10:
		score = 5
	elif p <= 20:
		score = 4
	elif p <= 35:
		score = 3
	elif p <= 50:
		score = 2
	else:
		score = 1

	return score


def add_phase(index, code, comm, op):

	print ('aici')

	ES_HOST    = {"host" : "localhost", "port" : 9200}
	INDEX_NAME = 'measure_' + index
	TYPE_NAME  = 'metric'
	
	es = Elasticsearch()

	MODELCOMM = load_model('models/model_lr_codecomm')
	MODELOP = load_model('models/model_lr_code_operands')

	compred = math.floor((MODELCOMM.predict(code))[0][0])
	oppred  = math.floor((MODELOP.predict(code))[0][0])

	if compred < 0:
		compred = 0
	if oppred < 0:
		oppred = 0

	x = es.index(index=INDEX_NAME, doc_type='metric', body={
		'id': 1,
		'insert_date': int(time.time() * 1000),
		'lcode': code,
		'lcom': comm,
		'lcom_pred': compred,
		'operands': op,
		'operands_pred': oppred
	})

	print (x)

def get_project_data(index):

	ES_HOST    = {"host" : "localhost", "port" : 9200}
	INDEX_NAME = 'measure_' + index
	TYPE_NAME  = 'metric'
	
	es = Elasticsearch()

	query = {
		'size': 1000,
		'query': {
			'match_all' : {}
			}
		}

	res = es.search(index=INDEX_NAME, body=query)

	result = []
	for r in res['hits']['hits']:
		d = r['_source']
		result.append(d)

	return result




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
#get_project_data('zet')