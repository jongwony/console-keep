# -*- coding: utf-8 -*-
from datetime import datetime

class Unit:
    def __init__(self, element):
        self.annotations = element['annotationsGroup']['annotations']
        self.id = element['id']
        self.parentId = element['parentId']
        self.title = element['title'] if 'title' in element else ''
        self.text = element['text'] if 'text' in element else ''
        self.sortValue = element['sortValue'] if 'sortValue' in element else 0
        self.reminders = element['reminders']
        self.type = element['type']
        self.to_datetime(element['timestamps'])

    def to_datetime(self, timestamps):
        result = dict()
        for k, v in timestamps.items():
            if k != 'kind':
                result[k] = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.timestamps = result

class State:
    def __init__(self, current):
        self.parents = 'root'
        self.current = current

class UnitGroup:
    def __init__(self, data):
        self.data = data
        num = sum(1 for _ in self.gen_lists())
        self.total_lists = [_ for _ in zip(range(num), self.gen_lists())]
        self.dicts = dict()

    def gen_lists(self):
        for element in self.data:
            yield Unit(element)

    def refresh(self, flag):
        self.dicts = dict()
        idx = 0
        for e in self.gen_lists():
            if e.parentId == flag:
                idx += 1
                self.dicts[idx] = e
        return idx

    def ls(self, flag, **options):
        idx = self.refresh(flag)
        num = options['num']
        if num is not None:
            idx = num if idx > num else idx

        self.gen_print(idx)

    def gen_print(self, num):
        for i, e in self.dicts.items():
            if i > num:
                break

            anno_ = e.annotations
            anno_query = ''
            for w in anno_:
                if 'webLink' in w:
                    w_url = w['webLink']['url']
                    anno_query = w_url
                else:
                    anno_query = ''

            ts_ = datetime.strftime(e.timestamps['created'], '%Y-%m-%d %H:%M %p')

            print('{:<2} {} {:<10s} {:<20s} {:>4s} \n   {}'.format(i, ts_, e.title, e.text, e.type, anno_query))