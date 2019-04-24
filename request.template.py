#!/usr/local/bin/python

"""request.template.py: Called from a Kubernetes init-container to get objects from RESTful service."""

__author__      = "Jesse Hamilton"
__version__     = "1.0.0"
__maintainer__  = "Jesse Hamilton"

import requests
import json
import os
import argparse
import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

parser.add_argument('-a', action="store", dest='--auth', help='Token or Basic')

if len(sys.argv) == 2:
    parser.print_help()
    sys.exit(1)
else:
   if sys.argv[2] == 'Basic':
      print(sys.argv[2])
      options = parser.parse_args()
      login=(os.environ.get('username'))
      password=(os.environ.get('password'))
   else:
      options = parser.parse_args()

# Config imported as env variables but derived from either a configmap or secret
url=(os.environ.get('url'))
json.outfile=(os.environ.get('outfile'))

# Check the url and make sure we can get a 200 
request=(requests.get(url, auth=(login, password))) #Add functionality for token arg here.
if request.status_code == 200:
    logger.info('RESTful service is up: Status 200')
    # Since we got a 200, go ahead and get the content to use for the rest of the script
    payload=request.content
    # Example of case replacement prior to dumping the json to a file for final use.
    #payload = payload.replace('id', 'Id')
    #payload = payload.replace('string', 'String')
    output=json.loads(payload)
else:
    # Log any HTTP error so its viewable from Kubernetes logs
    logger.error(request.status_code) 
    sys.exit(2)

# Write the content out to text file for the init-container to utilize
with open(json.outfile, 'w') as outfile:
    json.dump(output, outfile, sort_keys=True, indent=4)

# Send a message to console signaling success
logger.info('File successfully created')
