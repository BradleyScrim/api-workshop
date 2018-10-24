# -*- coding: utf-8 -*-
"""07 Upload a model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZaM-sNR9_6vqGBpRobWjTq7gkm4t9bbW

# 7 Uploading Model files

Demonstrates uploading a file (rather than registering a URL). This requires multiple steps, first creating content blob "placeholders", and then updating the content blobs with the data to be uploaded.
"""

import requests
import json
import string

import getpass

import urllib.request

base_url = 'https://sandbox3.fairdomhub.org'

headers = {"Content-type": "application/vnd.api+json",
           "Accept": "application/vnd.api+json",
           "Accept-Charset": "ISO-8859-1"}

session = requests.Session()
session.headers.update(headers)
session.auth = (input('Username:'), getpass.getpass('Password'))

def json_for_resource(type, id):    

  
  r = session.get(base_url + "/" + type + "/" + str(id), headers=headers)
  
  if (r.status_code != 200):
    print(r.json())
  
  r.raise_for_status()
  return r.json()

containing_project_id = 1

"""This defines the placeholder information for the content blob. For now just the filename and mime type are provided."""

local_blob = {'original_filename' : 'RoboKoD.xml', 'content_type' : 'text/xml'}

"""Set up the attributes for the model and include the content blob details. This also shows the intent that content blobs will be provided. Although in this case there is only one content blob, for Models there could potentially be more which can be described."""

model = {}
model['data'] = {}
model['data']['type'] = 'models'
model['data']['attributes'] = {}
model['data']['attributes']['title'] = 'iNS142 RobOKoD Redesigned Butanol Producing.'
model['data']['attributes']['policy'] = {'access':'download'}
model['data']['relationships'] = {}
model['data']['relationships']['projects'] = {}
model['data']['relationships']['projects']['data'] = [{'id' : containing_project_id, 'type' : 'projects'}]

model['data']['attributes']['content_blobs'] = [local_blob]

"""Register the Model. The resulting JSON contains the content blob element, but this is currently blank."""

r = session.post(base_url + '/models', json=model)
r.raise_for_status()

populated_model = r.json()
populated_model

"""Now upload the file. Normally it would come from a local file, but we simulate this here by fetching from a URL (notice how the SEEK API is being used to fetch a model file!)

*data* contains the data for an SBML model.
"""

url = 'https://fairdomhub.org/models/159/content_blobs/1986/download'
response = urllib.request.urlopen(url)
data = response.read()

"""Now with a PUT update the content blob with the data. The url for the content blob was provided by the Model creation JSON response.

The *headers={'Content-Type': 'application/octet-stream'}* is currently required, otherwise in this case SEEK tries to process it as an invalid XML request resulting i an error.
"""

blob_url = populated_model['data']['attributes']['content_blobs'][0]['link']

upload = session.put(blob_url, data=data, headers={'Content-Type': 'application/octet-stream'})
upload.raise_for_status()

"""Fetch the JSON for the model again, and look at the content blob attributes.

The size and checksums have now been updated with the new content.
"""

model_json = json_for_resource('models',populated_model['data']['id'])
model_json['data']['attributes']['content_blobs']

"""# Exercice 7



*   Update the notebook to register a Model with 2 content blobs. You can use a URL to a resource on the web, or use the link to the FAIRDOM logo in the previous example
* More details about the API can be found at https://docs.seek4science.org/help/user-guide/api.html which is constantly updated. This includes a link to the [API Overview](https://docs.seek4science.org/tech/api/index.html)
"""