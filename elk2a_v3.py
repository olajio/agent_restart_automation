#!/usr/bin/env python3

'''
The program will pull data from the elastic inventory index and will pass the host down to Ansible to be started1
'''

import requests
import jmespath
import subprocess
import argparse
import os
import sys
import datetime
from pathlib import Path
import helpers.json_log_format as jlf



#Configurations
today_date= datetime.datetime.utcnow().strftime("%m%d%Y")
logfilename=f"logs/agent_automation-{today_date}.json"
jlf.service_name = Path(__file__).stem
jlf.service_type = 'monitoring-scripts'
jlf.json_logging.init_non_web(custom_formatter=jlf.CustomJSONLog, enable_json=True)
logger = jlf.logging.getLogger(__name__)
logger.setLevel(jlf.logging.DEBUG)
logger.addHandler(jlf.logging.FileHandler(logfilename))
#vars for the api call
apivars = {
    "systemtype" : {
        "win" : "windows",
        "lin" : "centos"
    },
    "uuid" : {
        "hst" : "mXqbzwdKSvSeNAJ1lM5oIw",
        "hsc" : "uXgaSKNVTnSv3BrGSmfmsQ"
    }
}

procvars = {
    "url" : {
        "hst" : ".hedgeservtest.com",
        "hsc" : ".hedgeservcustomers.com"
    }
}


def read_data_from_elk(systemtype, domain):
    print(datetime.datetime.utcnow().isoformat(), " API Call to ElasticSearch - CCS ...")
    logger.info(f" API Call to ElasticSearch - CCS ...")
    #elastic_api = f"ApiKey {os.environ['ELASTICAPI']}"
    elastic_api = "ApiKey U0QzLTBuWUJuZlVPVDlXQkE0a1c6YjFoS2VBQUpTVFd4YXFRZmxZY1YtQQ=="
    url = "https://de26459b90754aceb3234fe7969cb1ee.us-east-1.aws.found.io:9243/inventory/_search"
    querystring = {"":"","filter_path":"aggregations.uhosts.buckets"}
    #payload = "{\n  \"size\": 0,\n  \"sort\": [\n    {\n      \"_score\": {\n        \"order\": \"desc\"\n      }\n    }\n  ],\n  \"_source\": {\n        \"includes\": [ \"beats_state.beat.host\" ]\n  },\n  \"query\": {\n    \"bool\": {\n      \"must\": [\n\t\t\t\t{\n          \"bool\": {\n            \"must\": [\n              {\n                \"bool\": {\n                  \"must_not\": {\n                    \"bool\": {\n                      \"should\": [\n                        {\n                          \"query_string\": {\n                            \"fields\": [\n                              \"beats_state.beat.name.keyword\"\n                            ],\n                            \"query\": \"CS51*\"\n                          }\n                        }\n                      ],\n                      \"minimum_should_match\": 1\n                    }\n                  }\n                }\n              },\n              {\n                \"bool\": {\n                  \"must_not\": {\n                    \"bool\": {\n                      \"should\": [\n                        {\n                          \"query_string\": {\n                            \"fields\": [\n                              \"beats_state.beat.name.keyword\"\n                            ],\n                            \"query\": \"ip-*\"\n                          }\n                        }\n                      ],\n                      \"minimum_should_match\": 1\n                    }\n                  }\n                }\n              },\n              {\n                \"bool\": {\n                  \"must_not\": {\n                    \"bool\": {\n                      \"should\": [\n                        {\n                          \"query_string\": {\n                            \"fields\": [\n                              \"beats_state.beat.name.keyword\"\n                            ],\n                            \"query\": \"CW51-*\"\n                          }\n                        }\n                      ],\n                      \"minimum_should_match\": 1\n                    }\n                  }\n                }\n              }\n            ]\n          }\n        }\n\t\t\t],\n      \"filter\": [\n        {\n          \"range\": {\n            \"timestamp\": {\n              \"gte\": \"now-20d\",\n              \"lt\": \"now\"\n            }\n          }\n        },\n        {\n          \"bool\": {\n            \"should\": [\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"metricbeat\"\n                }\n              },\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"filebeat\"\n                }\n              }\n            ],\n            \"minimum_should_match\": 1\n          }\n        },\n\t\t\t\t{\n          \"match_phrase\": {\n            \"status\": \"down\"\n          }\t\t\t\t\t\n        },\n		{\n          \"exists\": {\n            \"field\": \"timestamp\"\n          }\n        }\n      ],\n      \"should\": [],\n      \"must_not\": []\n    }\n  },\n  \"aggs\": {\n    \"uhosts\": {\n      \"terms\": {\n        \"field\": \"beats_state.beat.name.keyword\",\n\t\t\t\t\"size\": 2000\n      }\n    }\n  }\n\n}"
    base_payload = "{\n  \"size\": 0,\n  \"sort\": [\n    {\n      \"_score\": {\n        \"order\": \"desc\"\n      }\n    }\n  ],\n  \"_source\": {\n        \"includes\": [ \"beats_state.beat.host\" ]\n  },\n  \"query\": {\n    \"bool\": {\n      \"must\": [\n\t\t\t\t{\n          \"bool\": {\n            \"must\": [\n              {\n                \"bool\": {\n                  \"must_not\": {\n                    \"bool\": {\n                      \"should\": [\n                        {\n                          \"query_string\": {\n                            \"fields\": [\n                              \"beats_state.beat.name.keyword\"\n                            ],\n                            \"query\": \"CS51*\"\n                          }\n                        }\n                      ],\n                      \"minimum_should_match\": 1\n                    }\n                  }\n                }\n              },\n              {\n                \"bool\": {\n                  \"must_not\": {\n                    \"bool\": {\n                      \"should\": [\n                        {\n                          \"query_string\": {\n                            \"fields\": [\n                              \"beats_state.beat.name.keyword\"\n                            ],\n                            \"query\": \"ip-*\"\n                          }\n                        }\n                      ],\n                      \"minimum_should_match\": 1\n                    }\n                  }\n                }\n              },\n              {\n                \"bool\": {\n                  \"must_not\": {\n                    \"bool\": {\n                      \"should\": [\n                        {\n                          \"query_string\": {\n                            \"fields\": [\n                              \"beats_state.beat.name.keyword\"\n                            ],\n                            \"query\": \"CW51-*\"\n                          }\n                        }\n                      ],\n                      \"minimum_should_match\": 1\n                    }\n                  }\n                }\n              }\n            ]\n          }\n        }\n\t\t\t],\n      \"filter\": [\n        {\n          \"range\": {\n            \"timestamp\": {\n              \"gte\": \"now-5d\",\n              \"lt\": \"now\"\n            }\n          }\n        },\n        {\n          \"bool\": {\n            \"should\": [\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"metricbeat\"\n                }\n              },\n              {\n                \"match_phrase\": {\n                  \"beats_state.beat.type\": \"filebeat\"\n                }\n              }\n            ],\n            \"minimum_should_match\": 1\n          }\n        },\n\t\t\t\t{\n          \"match_phrase\": {\n            \"status\": \"down\"\n          }\t\t\t\t\t\n        },\n\t\t\t\t{\n          \"match_phrase\": {\n            \"beats_state.state.host.os.platform\": \"%s\"\n          }\t\t\t\t\t\n        },   \n		{\n          \"exists\": {\n            \"field\": \"timestamp\"\n          }\n        }\n      ],\n      \"should\": [],\n      \"must_not\": []\n    }\n  },\n  \"aggs\": {\n    \"uhosts\": {\n      \"terms\": {\n        \"field\": \"beats_state.beat.name.keyword\",\n\t\t\t\t\"size\": 2000\n      }\n    }\n  }\n\n}"
    systemtype_map = {
        "lin":"centos",
        "win":"windows"
    }

    actual_systemtype = systemtype_map.get(systemtype)
    payload = base_payload %actual_systemtype.lower()
    headers = {
    'Authorization': elastic_api,
    'Content-Type': "application/json"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring, verify=False)
    print(datetime.datetime.utcnow().isoformat(), " API Call to ElasticSearch - CSS Done!!! Response Code: ", response.status_code)
    logger.info(f" API Call to ElasticSearch - CSS Done!!! Response Code: {response.status_code}")
    print("RAW DATA :")
    print(response.text)
    #print(payload)
    return response


def process_data(api_response, systemtype, domain):
    print (datetime.datetime.utcnow().isoformat(), " Starting data processing...")
    #Parsing the hostnames from thr Json object to a list
    list_host_down = jmespath.search("aggregations.uhosts.buckets[*].key", api_response)
    exitmessage = (datetime.datetime.utcnow().isoformat(), "No Alert !!!. Exiting...")
    logger.info(f"{exitmessage}")
    if len(list_host_down) == 0:
        sys.exit(exitmessage)


    print("VAR BEFORE PROCESSING")
    print(list_host_down)
    #Adding Domain URL
    #domain_name = procvars["url"][domain]
    domain_name = []
    if domain == 'hst':
        filtered_hosts = [host for host in list_host_down if host.lower().startswith('ts01') or host.lower().startswith('tw01')]
        domain_name = procvars["url"][domain]
    elif domain == 'hsc':
        filtered_hosts = [host for host in list_host_down if host.lower().startswith('cs01') or host.lower().startswith('ms01') or host.lower().startswith('es01')or host.lower().startswith('cw01')]
        for host in filtered_hosts:
            if host.lower().startswith('cs'):
                domain_name.append(host + ".hedgeservcustomers.com")
            elif host.lower().startswith('ms'):
                domain_name.append(host + ".hedgeservmgmt.com")
            elif host.lower().startswith('es'):
                domain_name.append(host + ".funddevelopmentservices.com")
            elif host.lower().startswith('cw'):
                domain_name.append(host + ".hedgeservweb.com")    


    print(f"Hosts that are filtered by domain {domain}")
    #print(filtered_hosts)
    print("============ENRICHED WITH DOMAIN =============")
    #print(domain_name)
    #print("===========================")

    print("Dropping DR hosts")
    #print(filtered_hosts)  
    if len(filtered_hosts) == 0:
        exitmessage = (datetime.datetime.utcnow().isoformat(), "No agents to activate in domain", domain)
        print(exitmessage)
        sys.exit()

    if domain == 'hst':
        list_host_down_domain = [hostname + domain_name for hostname in filtered_hosts]
    else:
        list_host_down_domain = domain_name    
    
    #Insert the Ansible var tag at the beggining
    list_host_down_domain.insert(0, f"[{systemtype}_{domain}]")
    print(datetime.datetime.utcnow().isoformat(), " Completed data processing.")
    print(datetime.datetime.utcnow().isoformat(), " Ansible Inventory File: ", list_host_down_domain)
    logger.info(f" Completed data processing. Ansible Inventory File contains the following hosts: {list_host_down_domain}")
    #print("VAR BEFORE PROCESSING")
    #print(list_host_down)
    print("HOST LIST AFTER PROCESSING : ================")
    print(list_host_down_domain)
    return list_host_down_domain


def write_data_to_file(modified_data, systemtype, domain):
    filename = f"/root/ansible/{systemtype}_{domain}"
    with open(filename, 'w') as inventory_file:
        for element in modified_data:
           inventory_file.write(element)
           inventory_file.write('\n')
    print(f"{datetime.datetime.utcnow().isoformat()}  File Result: Complete {filename}")
    return filename


def start_ansible(filename, systemtype, domain):
    logger.info("Starting ansible playbook ...")
    cmd = f"ansible-playbook /root/ansible/{systemtype}_start_services.yaml --inventory-file /root/ansible/{systemtype}_{domain} --vault-password-file /root/ansible/value.yml -e /root/ansible/vault.yml"
    #cmd = f"ansible-playbook /root/ansible/{systemtype}_start_services.yaml --inventory-file /root/ansible/{systemtype}_{domain}"
    print(datetime.datetime.utcnow().isoformat(), cmd)
    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    output = stdout.decode()
    formatted_output = output.replace('\\n', '\n')
    print(f"{formatted_output}")
    if stdout:
        logger.info("RESULT: "+ formatted_output)
    if stderr:
        logger.error("ERROR: "+stderr.decode())    


def main(systemtype, domain):
    data = read_data_from_elk(systemtype, domain)
    api_response = data.json()
    modified_data = process_data(api_response, systemtype, domain)
    filename = write_data_to_file(modified_data, systemtype, domain)
    start_ansible(filename, systemtype, domain)
    print("----------------------------------------------------------------------------------------------------------------------------------")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script will pull hostnames for stopped filebeat or metricbeat services and start them. Expects two arguments.')
    parser.add_argument('--systemtype', type=str, help = 'win -> Windows hosts; lin -> Linux hosts')
    parser.add_argument('--domain', type=str, help='hsc -> Hosts in hscustomers.com; hst -> Hosts in hedgeservcustomers.com')
    args = parser.parse_args()
    main(args.systemtype, args.domain)

