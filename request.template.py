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
from os import path
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

# This version will take the auth method as an arguement.
# This way the script can handle the which ever auth method the RESTful service utilizes. 
parser.add_argument('-a,', action="store", dest='--auth', help='Token or Basic')

# Retrieve the env variables that we import from our Kubernetes configmap or secret.
# These are global
url = (os.environ.get('url'))
json.outfile = (os.environ.get('outfile'))

# Define our functions and set the variables to global so they can be called in the main logic.
def token_auth():
  global token
  global header
  global request
  token = (os.environ.get('token'))
  header = (os.environ.get('header'))
  if (token is None or header is None):
     logger.error(' ERROR: Missing enviornment variables for Token auth.')
     sys.exit(2)
  else:
      request = (requests.get(url, headers=header))

def basic_auth():
  global login
  global password
  global request
  login = (os.environ.get('username'))
  password = (os.environ.get('password'))
  if (login is None or password is None):
     logger.error(' ERROR: Missing enviornment variables for Basic auth.')
     sys.exit(2)    
  else:
     request = (requests.get(url, auth=(login, password)))

def payload_edit():
  global payload
  payload = payload.replace('example', 'Example')

# Perform some pre-flight checks
# Specifically, lets make sure we have the right argument syntax and output the help file if needed.
if len(sys.argv) == 1 or len(sys.argv) == 2:
    parser.print_help()
    sys.exit(1)

options = parser.parse_args()

if (sys.argv[2] == "Basic"):
   basic_auth()
else:
    if (sys.argv[2] == "Token"):
       token_auth()
    else:
       parser.print_help()
       sys.exit(1)

# Start the main program logic
def main():
  # Ensure that the url is responding to requests and returning a successful 200.
  if request.status_code == 200:
      logger.info(' CONNECTED: RESTful service is up: Status 200')
      # The url is responding so go ahead and load up the content. 
      payload = request.content
      #payload_edit() #Uncomment if we need to maniuplate the JSON payload in anyway
      output = json.loads(payload)
  else:
      # Log any HTTP error so its viewable from Kubernetes logs
      logger.error(request.status_code) 
      sys.exit(3)

  # Write the contents out to text file that the init-container will mount into the main pod.
  with open(json.outfile, 'w') as outfile:
      json.dump(output, outfile, sort_keys=True, indent=4)
  
  if path.exists(json.outfile):
      # Send a message to console signaling success
      logger.info(' SUCCESS: File created successfully.')
  else:
      logger.error(' FAILED: File failed to create.')
      sys.exit(4)

if __name__== "__main__":
     main()
