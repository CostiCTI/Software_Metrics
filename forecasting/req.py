import requests
import json
import pprint as pp


def get_pro():
    #url = 'http://194.2.241.244/measure/api/projects/42'
    #response = requests.get(url)
    #return response.json()

    url = 'http://194.2.241.244/measure/api/measurement/find'
    d = {
        "measureInstance": "RandomInstance",
        "page": 0,
        "pageSize": 5,
        "query": ""
        }
    r = requests.post(url, data=d)
    print (r.text)
    print(r.status_code) 
    print(r.reason)

#pp.pprint (get_pro())
get_pro()