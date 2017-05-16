# -*- coding: utf-8 -*-
import json
import os
from urllib import parse
from bs4 import BeautifulSoup
import re

venv_name = '_ck'
osdir = 'Scripts' if os.name is 'nt' else 'bin'
current_dir = os.path.realpath(os.path.dirname(__file__))
venv = os.path.join(venv_name, osdir, 'activate_this.py')
activate_this = (os.path.join(current_dir, venv))
# Python 3: exec(open(...).read()), Python 2: execfile(...)
exec(open(activate_this).read(), dict(__file__=activate_this))

from oauth2client import file, client, tools

# TODO: argument parsing
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

scope = ['https://www.googleapis.com/auth/drive']
redirect_uri = 'https://keep.google.com'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', scope=scope, redirect_uri=redirect_uri)
    creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

###################

import httplib2

http = httplib2.Http()
http = creds.authorize(http)

resp, contents = http.request('https://keep.google.com')

# (.*?) shortest matching
datapat = re.compile(rb"JSON.parse\('(.*?)'\)")
info = datapat.findall(contents)

# Hex decoding byte code -> Preserve literal byte(latin1) -> Unicode mapping
# http://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python3?answertab=votes#tab-top
for i in info:
    convert = i.decode('unicode_escape').encode('latin1').decode('utf-8')
    print(json.loads(convert))

## TODO: JSON parsing

# with open('source.html', 'wb') as f:
#     f.write(contents)

