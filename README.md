# init-container-rest
Template for calling RESTful API from a Kubernetes init-container.

# Motivation
We want to keep the primary long-running pods as lean as possible and the attack surface to a minimum. However, there are times that on pod startup, we need to get various objects from
a RESTful service for proper intialization. This is a template for utilizing an init-container to defer all the needed packages and commands away from the primary pod.

# Instructions
1) Edit the secret.yml to include your base64 encoded values for the following keys. (echo -n 'something' | base64)
   * url
   * username
   * password
   * outfile
2) Apply the secret (kubectl apply -f secret.yml -n somenamespace)
