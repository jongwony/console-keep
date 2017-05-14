# -*- coding: utf-8 -*-
import json
import time
import getpass
from urllib import parse

from oauth2client.client import flow_from_clientsecrets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

scope = ['https://www.googleapis.com/auth/calendar']
redirect_uri = 'https://keep.google.com'

flow = flow_from_clientsecrets('client_secret.json', scope=scope, redirect_uri=redirect_uri)
auth_uri = flow.step1_get_authorize_url()

#######################

userID = input('Email: ')
passwd = getpass.getpass('Password: ')

driver = webdriver.Chrome(executable_path=r"E:\chromedriver_win32\chromedriver.exe")
driver.get(auth_uri)

page = driver.find_element_by_id('identifierId')
page.send_keys(userID)
page.send_keys(Keys.RETURN)

time.sleep(1)

page = driver.find_element_by_name("password")
page.send_keys(passwd)
page.send_keys(Keys.RETURN)

time.sleep(1)

# if len(scope) > 0:
#     page = driver.find_element_by_id('submit_approve_access')
#     page.send_keys(Keys.RETURN)
    
#     time.sleep(1)

code_url = driver.current_url

driver.close()

################

code = parse.parse_qs(parse.urlparse(code_url).query)['code'][0]
credentials = flow.step2_exchange(code)
print(credentials)