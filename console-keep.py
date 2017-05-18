# -*- coding: utf-8 -*-
import json
import os
import re
from collections import OrderedDict

# virtualenv
current_dir = os.path.realpath(os.path.dirname(__file__))
try:
    from googleoauth import GoogleOAuth
    from bs4 import BeautifulSoup
    import httplib2
except ImportError:
    venv_name = '_ck'
    osdir = 'Scripts' if os.name is 'nt' else 'bin'
    venv = os.path.join(venv_name, osdir, 'activate_this.py')
    activate_this = (os.path.join(current_dir, venv))
    # Python 3: exec(open(...).read()), Python 2: execfile(...)
    exec(open(activate_this).read(), dict(__file__=activate_this))

    from googleoauth import GoogleOAuth
    from bs4 import BeautifulSoup
    import httplib2

class ConnectKeep:
    """connect to google keep by usnig WITH context manager"""
    def __enter__(self):
        keep = GoogleOAuth(current_dir)
        http = httplib2.Http()
        http = keep.creds.authorize(http)
        return http.request('https://keep.google.com')

    def __exit__(self, exc_ty, exc_val, tb):
        pass

# class Unit:
#     def __init__(self):

def text_mining(i, e):
    anno_ = e['annotationsGroup']['annotations']
    anno_query = ''
    for w in anno_:
        if 'webLink' in w:
            w_url = w['webLink']['url']
            anno_query = w_url
        else:
            anno_query = ''

    ts_ = e['timestamps']['created']
    
    title_ = e['title']
    title_query = title_ if title_ else ''
    text_ = e['text']
    text_query = text_ if text_ else ''
    type_ = e['type']
    query = '{:<2} {} {:<10s} {:<20s} {:>4s} \n   {}'.format(i, ts_, title_query, text_query, type_, anno_query)
    return query

def getKeepJSON():
    with ConnectKeep() as http:
        response, contents = http

        # (.*?) shortest matching
        datapat = re.compile(rb"JSON.parse\('(.*?)'\)")
        info = datapat.findall(contents)

        # Hex decoding byte code -> Preserve literal byte(latin1) -> Unicode mapping
        # http://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python3?answertab=votes#tab-top
        # component lists info[-1]
        decode_comp = info[-1].decode('unicode_escape').encode('latin1').decode('utf-8')
        return json.loads(decode_comp, object_pairs_hook=OrderedDict)

## TODO: Argparse?

print('Welcome Console Keep!')
print('Type help!')
flag = 'ROOT'
while True:
    state = input(flag + '> ')

    if state in ['ls', 'l']:
        # TODO: Unit State Class
        i = 1
        for element in getKeepJSON():
            # value equality
            if element['parentId'] == 'root':
                print(text_mining(i, element))
                i += 1
    elif state is ['put', 'p']:
        pass
    elif state is ['cd']:
        # parentId <-> id
        pass
    elif state in ['help', 'h']:
        pass
    elif state in ['exit', 'q']:
        print('Bye!')
        break

# with open('source.html', 'wb') as f:
#     f.write(contents)

