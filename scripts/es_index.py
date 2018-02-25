import pandas as pd
import pickle
import time
import json
import pprint

from datetime import datetime
from elasticsearch import Elasticsearch


def load_model(file_name): 
    # load the model
    filename = file_name + '.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    
    return loaded_model

MODEL = load_model('../Notebooks/model_lr_comm')

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'projectcti'
TYPE_NAME = 'metric'


es = Elasticsearch()

df = pd.read_csv('datep.csv')

#d = df.to_dict('records')

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

print ("creating new index...")
es.indices.create(index = INDEX_NAME, body = request_body)


print ("Importing data...")
bulk_data = []

for index, row in df.iterrows():
    data_dict = {}
    print("Index: " + str(index))
    time.sleep(1)
    for i in range(len(row)):
        data_dict[df.columns[i]] = row[i]
		
    op_dict = {
        "index": {
            "_index": INDEX_NAME,
            "_type": 'metrics'
        }
    }
    
    data_dict['lcom_pred'] = (MODEL.predict(data_dict['lcode']))[0][0]
    data_dict['insert_date'] = int(time.time() * 1000)
    data_dict['id'] = index

    bulk_data.append(op_dict)
    bulk_data.append(data_dict)

res = es.bulk(index = INDEX_NAME, body = bulk_data)

print ("Ready!")
# check data is in there, and structure in there
es.search(body={"query": {"match_all": {}}}, index = INDEX_NAME)
#es_indices.get_mapping(index = 'metrics1')
