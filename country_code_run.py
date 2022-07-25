#import sqlite3
import yaml
import datetime
import json
import os
import requests
import sys
import random
import glob
from helpers import db_ops
import logging
import pandas as pd


logging.basicConfig(level=logging.INFO, filename=os.path.dirname(os.path.abspath('country_code_run.py'))
                                                 + '/logs/countryCodeRun_'
                                                 + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt',
                    format='%(process)d--%(asctime)s--%(levelname)s--%(message)s')

# filePath = os.path.dirname(os.path.abspath('country_code_run.py')) + '/helpers'
# filePath = os.path.abspath('..') + '/helpers'
filePath = sys.path[0]


def fetch_api_env():
    logging.info('Loading the api environment parameters...')
    with open(filePath + '/helpers/env.yaml') as file:
        params = yaml.load(file, Loader=yaml.FullLoader)
    return params


def fetch_country_codes():
    logging.info('Loading the country codes...')
    with open(filePath + '/helpers/country_codes.yaml') as file:
        country_codes = yaml.load(file, Loader=yaml.FullLoader)
    return country_codes


def fetch_payload_params():
    logging.info('Fetching the api POST method payload parameters...')
    with open(filePath + '/helpers/payload_parameters.yaml') as file:
        payload_params = yaml.load(file, Loader=yaml.FullLoader)
    return payload_params



def build_payload():
    """Build out the structure of the payload to be used for the POST request to the api endpoint"""
    orig = random.choice(fetch_country_codes()['iso_code'])
    dest = random.choice(fetch_country_codes()['iso_code'])
    logging.info('Running build_payload with orig: %s and dest: %s', orig, dest)
    depart_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return_ = datetime.datetime.strptime(depart_date, '%Y-%m-%d') + datetime.timedelta(days=random.randint(3, 9))
    return_date = return_.strftime('%Y-%m-%d')
    payload = json.dumps({
        "data": {
            "type": "TRIP",
            "attributes": {
                "category": fetch_payload_params()['parameters']['category'][1],
                "travellers": [
                    {
                        "vaccinations": [
                            {
                                "type": "COVID-19",
                                "status": random.choice(fetch_payload_params()['parameters']['vax_status'])
                            }
                        ],
                        "nationality": orig
                    }
                ],
                "segments": [
                    {
                        "segmentType": "OUTBOUND",
                        "origin": {
                            "countryCode": orig
                        },
                        "destination": {
                            "countryCode": dest
                        },
                        "travelMode": "AIR",
                        "departureDate": depart_date,
                        "departureTime": "12:59",
                        "arrivalDate": return_date,
                        "arrivalTime": "12:59"
                    }
                ]
            }
        }
    })
    return payload


def query_api():
    logging.info('Running query_api against /tripsV2 api endpoint...')
    baseurl = fetch_api_env()['sandbox']['mainUrl']
    date_of_extraction = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    affId = fetch_api_env()['sandbox']['affiliateId']
    key = fetch_api_env()['sandbox']['apiKey']
    include = fetch_api_env()['sandbox']['includes']
    url = baseurl + '?affiliateId=' + affId + '&key=' + key + '&language=en-US&include=' + include[0] + ',' + include[1]
    payload = build_payload()
    headers = {'Content-Type': 'application/json'}
    retries = 0
    while retries < 6:
        resp = requests.request("POST", url, headers=headers, data=payload)
        if len(resp.content) <= 1434:
            logging.warning('Response invalid, querying endpoint again...')
            # requests.request("POST", url, headers=headers, data=payload)
            retries += 1
        else:
            response = resp.json()
            response = json.dumps(response, indent=4)
            filename = 'v2tripsResponse_' + date_of_extraction + str('.json')
            with open(filename, "w") as outfile:
                outfile.write(response)
            # orig = json.loads(build_payload())['data']['attributes']['segments'][0]['origin']['countryCode']
            # dest = json.loads(build_payload())['data']['attributes']['segments'][0]['destination']['countryCode']
            return response


# print(query_api())


def read_json_file():
    """Convert the api response data to a pandas df"""
    # file = glob.glob(filePath + '/v2trips*')[0].split('/')[-1]
    file = glob.glob(filePath + '/v2trips*')[0]
    with open(file) as f:
        json_file = json.load(f)
    return json_file


# print(extract_values_from_response('category'))
if __name__ == '__main__':
    query_api()
