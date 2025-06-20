#!/usr/bin/env python3

'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import requests
import json
import jmespath

url = "https://de26459b90754aceb3234fe7969cb1ee.us-east-1.aws.found.io:9243/inventory/_search"

querystring = {"":"","filter_path":"hits.hits._source"}

payload = "{\n  \"size\": 500,\n  \"sort\": [\n    {\n      \"_score\": {\n        \"order\": \"desc\"\n      }\n    }\n  ],\n  \"query\": {\n    \"bool\": {\n      \"must\": [],\n      \"filter\": [\n        {\n          \"match_all\": {}\n        },\n        {\n          \"match_phrase\": {\n            \"status\": \"down\"\n          }\n        },\n        {\n          \"bool\": {\n            \"should\": [\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"metricbeat\"\n                }\n              },\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"filebeat\"\n                }\n              }\n            ],\n            \"minimum_should_match\": 1\n          }\n        }\n      ],\n      \"should\": [],\n      \"must_not\": []\n    }\n  }\n}"
headers = {
    'Authorization': "ApiKey U0QzLTBuWUJuZlVPVDlXQkE0a1c6YjFoS2VBQUpTVFd4YXFRZmxZY1YtQQ==",
    'Content-Type': "application/json"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring, verify=False)


#print(response.content)
# Write API response to file
with open('api_response.json', 'w') as fd: 
    fd.write(response.text)

#input file
fin = open("api_response.json", "rt")
#output file to write the result to
fout = open("api_response_mod.json", "wt")
#for each line in the input file
for line in fin:
	#read replace the string and write to output file
	fout.write(line.replace('.', '_'))
#close input and output files
fin.close()
fout.close()


#dataset = (json.loads(response.content))

#print(dataset)

print("Jmespath Result:")
#search_string = jmespath.search("hits.hits[*]._source[?beats_state.beat.version == 'windows'].beats_state.beat.host", dataset)
#search_string = jmespath.search("*", dataset)
#print(search_string)