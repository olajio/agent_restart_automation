#!/usr/bin/env python3

'''
 inventory script for Ansible, in Python.
'''

import requests
import json
import jmespath

url = "https://de26459b90754aceb3234fe7969cb1ee.us-east-1.aws.found.io:9243/inventory/_search"

querystring = {"":"","filter_path":"aggregations.uhosts.buckets"}

payload = "{\n  \"size\": 500,\n  \"sort\": [\n    {\n      \"_score\": {\n        \"order\": \"desc\"\n      }\n    }\n  ],\n  \"_source\": {\n        \"includes\": [ \"beats_state.beat.host\" ]\n  },\n  \"query\": {\n    \"bool\": {\n      \"must\": [],\n      \"filter\": [\n        {\n          \"match_all\": {}\n        },\n        {\n          \"bool\": {\n            \"should\": [\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"metricbeat\"\n                }\n              },\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"filebeat\"\n                }\n              }\n            ],\n            \"minimum_should_match\": 1\n          }\n        },\n        {\n          \"match_phrase\": {\n            \"beats_state.beat.version\": \"windows\"\n          }\t\t\t\t\t\n        },\n\t\t\t\t{\n\t\t\t\t\t\"match_phrase\": {\n            \"cluster_uuid\": \"mXqbzwdKSvSeNAJ1lM5oIw\"\n          }\n\t\t\t\t}\n      ],\n      \"should\": [],\n      \"must_not\": []\n    }\n  },\n  \"aggs\": {\n    \"uhosts\": {\n      \"terms\": {\n        \"field\": \"beats_state.beat.host.keyword\"\n      }\n    }\n  }\n\n}"
headers = {
    'Authorization': "ApiKey U0QzLTBuWUJuZlVPVDlXQkE0a1c6YjFoS2VBQUpTVFd4YXFRZmxZY1YtQQ==",
    'Content-Type': "application/json"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring, verify=False)

print("API Response Code:", response.status_code)


api_response_json = response.json()

#Parsing the hostnames from thr Json object to a list
list_host_down = jmespath.search("aggregations.uhosts.buckets[*].key", api_response_json)

print("Jmespath Result:", list_host_down)
list_host_down_domain = [s + ".hedgeservtest.com" for s in list_host_down]
print("Adding Domain URL", list_host_down_domain)
#Insert the Ansible var tag at the beggining 
list_host_down_domain.insert(0, "[win_hst]")
print("Adding Ansible variable tag", list_host_down_domain)

#Writing the hostnames to a file
MyFile=open('win_hst','w')
for element in list_host_down_domain:
     MyFile.write(element)
     MyFile.write('\n')
MyFile.close()
print("File Result: Complete")






'''
print("encoding Result:")
print(response.encoding)

print("Raise Status:")
print(response.raise_for_status())


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



#print("JSON Result:")
#print(api_response_json)

# Write API response to file
#with open('api_response.json', 'w') as fd: 
#    fd.write(api_response_json)

# Write API response to file
#with open('api_response.txt', 'w') as fd: 
#    fd.write(api_response_text)
'''