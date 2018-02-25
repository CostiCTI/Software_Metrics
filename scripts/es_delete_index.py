import sys

from elasticsearch import Elasticsearch

es = Elasticsearch()

if len(sys.argv) != 2:
    print("Wrong number of args!")
else:
    index = sys.argv[1]
    es.indices.delete(index=index)

    print("Index " + index + " deleted!")