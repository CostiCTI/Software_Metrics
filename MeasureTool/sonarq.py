
import requests
import pprint as pp
 
URL = "http://localhost:9000/api/resources?metrics=ncloc,coverage"
 
# location given here
location = "delhi technological university"
 
# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}
 
# sending get request and saving the response as response object
r = requests.get(url = URL)
 
# extracting data in json format
data = r.json()

pp.pprint(data)