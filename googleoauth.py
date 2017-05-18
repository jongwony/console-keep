# -*- coding: utf-8 -*-
import os
from oauth2client import file, client, tools

class GoogleOAuth:
    def __init__(self, project_dir):
        scope = ['https://www.googleapis.com/auth/drive']
        redirect_uri = 'https://keep.google.com'
        self.store = file.Storage(os.path.join(project_dir,'storage.json'))
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(os.path.join(project_dir, 'client_secret.json'), scope=scope, redirect_uri=redirect_uri)
            self.creds = tools.run(self.flow, self.store)