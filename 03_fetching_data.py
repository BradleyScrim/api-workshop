# -*- coding: utf-8 -*-
"""03 Fetching data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IYGWv5misDPAulnG_jfYOCtx5hxKl3Fr

# Accessing and downloading Data



*   Finding the route to get hold of the data
*   Converting spreadsheets to CSV
"""

import requests
import json
import string

import io

# Importing the libraries we need to format the data in a more readable way. 
import pandas as pd
from pandas.io.json import json_normalize

from IPython.display import HTML

base_url = 'https://fairdomhub.org'

def json_for_resource(type, id):    

  headers = {"Accept": "application/vnd.api+json",
           "Accept-Charset": "ISO-8859-1"}
  r = requests.get(base_url + "/" + type + "/" + str(id), headers=headers)
  r.raise_for_status()
  return r.json()

"""Fetch the JSON for the Data file resource at https://fairdomhub.org/data_files/1049

We print out title to be sure we have the correct item.
"""

data_file_id = 1049

result = json_for_resource('data_files',data_file_id)

title = result['data']['attributes']['title']

title

"""The attributes contain a 'content_blobs' block. Content Blob is the name we use in SEEK for the entity that corresponds to a file or URL.

Note that content_blobs is always an array. Models can currently contain multiple content blobs (multiple files), and we plan to provide the same support to Data files and other assets in the future.
"""

result['data']['attributes']

"""Here we focus on the details about a single content blob:

* **content_type** - this is the mime type of the file, or the whatever the URL points to
*  **link** - this is the link that describes the content blob route
*  **md5sum** - an MD5 checksum of the contents
* **sha1sum** - a SHA1 based checksum of the contents. These checksums are useful for checking the file downloaded is correct, and there hasn't been an error or has been modified since being registered with SEEK.
* **original_filename** - the filename if the file, as it was when registered with SEEK
* **size** - the size of the file in bytes
* **url** - url to an external resource, if the item was registered with SEEK using a URL rather than a direct upload

In this case, this is an *Excel XLSX* file, called *1205 amino acid omission pyogenes.xlsx*, and is about 59k
"""

blob = result['data']['attributes']['content_blobs'][0]

blob

"""The route to directly download a file is the content blob route, with the */download* action appended. This is always the case for anything downloadable in SEEK.

In this example we display the URL to download the content blob for generete a HTML hyperlink for it.

Although in this case we download the content blob itself directly, it is also possible to download with https://fairdomhub.org/data_files/1049/download . Other than Models, this currently results in downloading a single file. For models, a ZIP file is generated that contains all files. To be future proof, we recommend downloading individual files through the content-blob route.
"""

link = blob['link']
filename = blob['original_filename']

download_link = link+"/download"

print("Download link is: " + download_link + "\n")

HTML("<a href='"+ download_link + "'>Download + " + filename + "</a>")

"""As we saw earlier. this Data file is an Excel spreadsheet. Where data is an Excel spreadsheet, it can be converted to a Comma Seperated File (CSV), by requesting this format through content negotiation. 

In this case, we request a GET to https://fairdomhub.org/data_files/1049/content_blobs/1518, but instead of requesting JSON we use an Accept: header of 'text/csv'. A parameter 'sheet' can be included to access different sheets, which if missed always defaults to the first sheet.

Here we request CSV and display the first sheet in a table using the Pandas module. (NaN is just a blank cell in the spreadsheet).
"""

headers = { "Accept": "text/csv" }
r = requests.get(link, headers=headers, params={'sheet':'1'})
r.raise_for_status()

csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))

csv

"""# Exercise 3



*   Update the notebook to display the content blob details and CSV for sheet 2 of https://fairdomhub.org/data_files/2222
*   Update and look at the multiple model file content blobs for https://fairdomhub.org/models/308 (don't worry if the csv step fails)
"""