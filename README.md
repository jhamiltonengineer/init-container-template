# init-container-template
Template for calling RESTful API from a Kubernetes init-container and adding the content to a main pod via emptydir() volume mounts.

# Motivation
The goal is to always keep the primary application pods lean and the attack surface to a minimum. However, there are times that on pod startup, we need to get various objects from
A RESTful service for proper pod initialization. Enter init-containers which are used to run code or tooling that we otherwise do not want in the main pod.  Here is a template for utilizing an init-container to defer all the required packages and commands for requesting data from a RESTful service away from the primary pod.

# Instructions
1) Edit the secret.yml to include your base64 encoded values for the following keys. (echo -n 'something' | base64)
   * username
   * password
2) Create a configmap to contain the following values if you do not wish to store them in a secret.
   * url
   * outfile
3) Apply the secret and or configmap. (kubectl apply -f secret.yml -n namespace)
4) Adjust the deployment manifest to include an init-container spec.

# Task List
- [x] Create python template script 
- [x] Add functionality allowing to pass different auth methods to python script
- [x] Add logging and error checking to python script
- [ ] Add Detailed instructions to README for executing container from docker command line
- [ ] Create deployment manifest that includes mounting output file to main pod from init-container
- [ ] Add Helm charts

