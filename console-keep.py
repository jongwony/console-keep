# -*- coding: utf-8 -*-
import actvenv
import argparse
import json
import re
import manage_data
import googleoauth

def getKeepJSON():
    with googleoauth.ConnectKeep(actvenv.SCRIPTDIR) as http:
        response, contents = http

        # (.*?) shortest matching
        datapat = re.compile(rb"JSON.parse\('(.*?)'\)")
        info = datapat.findall(contents)

        # Hex decoding byte code -> Preserve literal byte(latin1) -> Unicode mapping
        # http://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python3?answertab=votes#tab-top
        # component lists info[-1]
        decode_comp = info[-1].decode('unicode_escape').encode('latin1').decode('utf-8')
        return json.loads(decode_comp)

def initializing():
    flag = manage_data.State('root')
    data = manage_data.UnitGroup(getKeepJSON())
    data.refresh(flag.current)
    return flag

if __name__ == '__main__':
    print('Welcome to Console Keep!')
    print('Initializing...')
    flag = initializing()
    print('Initial data fetched.')
    print('Type help!')


    while True:
        args_parser = argparse.ArgumentParser(prog='COMMAND')

        state = input(flag.current + '> ')
        cmd, *options = state.split()

        # SystemError: continue

        if cmd in ['exit', 'q']:
            print('Bye!')
            break

        # refresh
        print('Data Refreshing...')
        data = manage_data.UnitGroup(getKeepJSON())
        data.refresh(flag.current)

        if cmd == 'cd':
            # parentId <-> id
            if options:
                try:
                    [opt] = options
                    if opt == 'root':
                        flag.parents = 'root'
                        flag.current = 'root'
                    elif opt == '..':
                        # TODO: specify parents
                        flag.current = flag.parents
                        flag.parents = 'root'
                    else:
                        if isinstance(int(opt), int):
                            flag.parents = flag.current
                            flag.current = data.dicts[int(opt)].id
                            flag.idx = int(opt)
                except ValueError:
                    # keep current state
                    print('Wrong Options')
            else:
                flag.current = 'root'

        if cmd == 'ls':
            # TODO: path
            # args_parser.add_argument('element', help='Show list')
            # args_parser.add_argument('-d', action='store_true')
            args_parser.add_argument('-n', '--number', type=int)

            filtered = args_parser.parse_args(options)

            data.ls(flag.current, num=filtered.number)

        if cmd == 'put':
            pass

    # with open('source.html', 'wb') as f:
    #     f.write(contents)
