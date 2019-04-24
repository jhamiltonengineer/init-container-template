#!/usr/local/bin/python

"""request.template.py: Called from a Kubernetes init-container to get objects from RESTful service."""

__author__      = "Jesse Hamilton"
__version__     = "1.0.0"
__maintainer__  = "Jesse Hamilton"

import requests
import json
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Envrionment variables imported and env variables but derived from either configmap or secret
url=(os.environ.get('url'))
login=(os.environ.get('username'))
password=(os.environ.get('password'))
json.outfile=(os.environ.get('outfile'))

# Check the url and make sure we can get a 200 
request=(requests.get(url, auth=(login, password)))
if request.status_code == 200:
    logger.info('RESTful service is up: Status 200')
    # Since we got a 200, go ahead and get the content to use for the rest of the script
    payload=request.content
    # Example of case replacement prior to dumping the json to a file for final use.
    #payload = payload.replace('id', 'Id')
    #payload = payload.replace('string', 'String')
    output=json.loads(payload)
else:
    # Log what HTTP error so its viewable from Kubernetes logs
    logger.error(request.status_code) 
    sys.exit(1)

#Write the content out to text file for the init-container to utilize
with open(json.outfile, 'w') as outfile:
    json.dump(output, outfile, sort_keys=True, indent=4)

logger.info('File successfully created')
