# coding: utf-8
import json
import requests, base64
import time, datetime
import glob
import getpass
import httplib
import oauth.oauth as oauth
import pytumblr 

### Get Inputs from User

print("This program will help you send a Paper Doc to Tumblr as a Draft")

print("First we need a Dropbox API token from you: ")
papertoken = getpass.getpass()

print('Input the Paper Doc here: ')
paperDoc = raw_input()

### Split for specific Paper doc ID
paperDocId = paperDoc.split('-')[-1]

###  Define the API Arguments, and choose if you need a folder or not
paperApiArgs = json.dumps({'doc_id': paperDocId, 'export_format': 'markdown'})

###  Define the API headers and URL
paperApiHeaders = {'Authorization': 'Bearer %s' % paperToken, 
		'Dropbox-API-Arg': '%s' % paperApiArgs}
paperApiUrl = "https://api.dropboxapi.com/2/paper/docs/download"


###  Call the API to create the Paper Doc
paperApiResult = requests.post(paperApiUrl, headers=paperApiHeaders)


###  API responses, first if an error occurs for reporting and second grab the doc markdown into a variable
if( paperApiResult.status_code != 200 ):
	print ('* Failed to get a response to call for /paper/docs/download. \nWe got an error [%s] with text "%s"' % (paperApiResult.status_code, paperApiResult.text))
elif ( paperApiResult.status_code == 200 ):
    paperTitle = paperApiResult.text.split('\n', 1)[0]
    paperTitle = paperTitle.replace("# ","")
    paperBody = paperApiResult.text.split('\n', 1)[-1]

### Credentials from the application page - COPIED from OAUTH and Tumblr Libraries
key = 'TUMBLRkey'
secret = 'TUMBLRsecret'

# OAuth URLs given on the application page
request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorization_base_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'

# Fetch a request token
from requests_oauthlib import OAuth1Session
tumblr = OAuth1Session(key, client_secret=secret, callback_uri='http://www.tumblr.com/dashboard')
tumblr.fetch_request_token(request_token_url)

# Link user to authorization page
authorization_url = tumblr.authorization_url(authorization_base_url)
print 'Please go here and authorize,', authorization_url

# Get the verifier code from the URL
redirect_response = raw_input('Paste the full redirect URL here: ')
tumblr.parse_authorization_response(redirect_response)

# Fetch the access token
returnTokens = tumblr.fetch_access_token(access_token_url)
t_oAuthToken = returnTokens['oauth_token']
t_oAuthTokenSecret = returnTokens['oauth_token_secret']

### END OAUTH LIBRARY COPY

client = pytumblr.TumblrRestClient(
    key,
    secret,
    t_oAuthToken,
    t_oAuthTokenSecret,
)

#Creating a text post
client.create_text('shakesonaplane', state="draft", slug="testing-text-posts", title=paperTitle, format = "markdown", body=paperBody)















