from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests
import time
DEBUG = True

user= ####### FILL IN BC HYDRO PASSWORD HERE #######
pword= ###### FILL IN USERNAME HERE ########
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

def initialize():
    #Login via Selenium/PhantomJS
    if DEBUG:
        print('initialize: Loading PhantomJS from selenium.webdriver')
    jsdrive = webdriver.PhantomJS()
    return jsdrive

def bchydro_login(jsdrive):
    try:
        if DEBUG:
            print('bchydro_login: Loading BC hydro main page')
        jsdrive.get("https://www.bchydro.com/BCHCustomerPortal/web/login.html")
    except WebDriverException:
        jsdrive.save_screenshot('logging/selenium_screenshots/error.png')
        print('bchydro_login: ERROR: Could not load the BC hydro page!\
                Error string = {}'.format(error))
    try:
        if DEBUG:
            print('bchydro_login: Submitting username and password')
        jsdrive.find_element_by_name('IDToken1').send_keys(user)
        jsdrive.find_element_by_name('IDToken2').send_keys(pword)
        jsdrive.find_element_by_name('Login.Submit').click()
    except WebDriverException as error:
        jsdrive.save_screenshot('logging/selenium_screenshots/error.png')
        print('bchydro_login: ERROR: Could not find elements and send username and password tokens.\
                Error string = {}'.format(error))
    #TODO: put in something here to confirm we are actually logged in.
    time.sleep(2)
    try:
        if DEBUG:
            print('bchydro_login: Going to download centre page')
        jsdrive.get('https://app.bchydro.com/datadownload/web/download-centre.html')
    except WebDriverException as error:
        jsdrive.save_screenshot('logging/selenium_screenshots/error.png')
        print('bchydro_login: ERROR: Could not go to the download page.\
                Error string = {}'.format(error))
    time.sleep(0.2)

jsdrive = initialize()
bchydro_login(jsdrive)

#Transfer session to python requests library and download data
headers = {
    "User-Agent":user_agent}
s = requests.session()
s.headers.update(headers)

for cookie in jsdrive.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)

form = {
    'accountId':'',
    "fromDate": "Jan 21, 2016",
    'toDate': 'Jun 5, 2017',
    'downloadInterval': 'MONTHLY',
    'downloadType': 'BILLHSTRY',
    'downloadFormat': 'CSVFILE'}


r = s.get('https://app.bchydro.com/datadownload/web/download-centre.html')
print('Download centre page GET: '+r.reason)

#TODO: Add bchydro param, referrers, and crsf tokens to the header. That's probably why this next post doesn't work.
headers = {
        "User-Agent":user_agent,
        "Referer":'https://app.bchydro.com/datadownload/web/download-centre.html',
        'X-CSRF-Token':s.cookies['bchydroparam'],
        'bchydroparam':s.cookies['bchydroparam']}
s.headers.update(headers)

r = s.post('https://app.bchydro.com/datadownload/web/validate-download-request.html',data=form)
print('Validate download request POST: '+r.reason)
time.sleep(0.2)

r = s.post('https://app.bchydro.com/datadownload/web/create-download-request.html',data=form)
print('Create download request POST: '+r.reason)
time.sleep(0.2)

r = s.get('https://app.bchydro.com/datadownload/web/download-file.html?requestId=recent')
print('Download file request GET: '+r.reason)

f=open('out.csv','wt')
f.write(r.text)
f.close()

s.close()
jsdrive.close()

#Got the file!!!
