import time
import json

from datetime import datetime
from elasticsearch import Elasticsearch

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'prox'
TYPE_NAME = 'metric'

es = Elasticsearch()


lcode = int(input('Enter lines of code: '))
lcom = int(input('Enter lines of comment: '))
classes = int(input('Enter number od classes: '))


es.index(index=INDEX_NAME, doc_type='metric', id=3, body={
    'id': 3,
    'insert_date': int(time.time() * 1000),
    'lcode': lcode,
    'lcom': lcom,
    'lcom_pred': lcom + lcom / 10,
    'class': classes
})

print ("Data inserted!")