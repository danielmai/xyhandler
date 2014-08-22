#!/usr/bin/python

#import requests
from rauth import OAuth1Service
from urlparse import parse_qs
import webbrowser
import csv
import time
import logging
log = logging.getLogger(__name__)
logfmt = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=logfmt,level=logging.INFO)

BaseAccessUrl     = 'https://api.login.yahoo.com/oauth/v2/'
GetTokenUrl       = BaseAccessUrl + 'get_token'
AuthorizationUrl  = BaseAccessUrl + 'request_auth'
RequestTokenUrl   = BaseAccessUrl + 'get_request_token'
CallbackUrl       = 'oob'
BaseApiUrl        = 'http://fantasysports.yahooapis.com/fantasy/v2/'

class xYHandler(object):

  def __init__(self, authf):
    self.authf = authf
    self.authd = self.get_authvals_csv(self.authf)
    self.yahoo = OAuth1Service(consumer_key=self.authd['consumer_key'],
                               consumer_secret=self.authd['consumer_secret'],
                               name='yahoo',
                               access_token_url=GetTokenUrl,
                               authorize_url=AuthorizationUrl,
                               request_token_url=RequestTokenUrl,
                               base_url=BaseAccessUrl)

  def get_authvals_csv(self, authf):
    vals = {}	#dict of vals to be returned
    with open(authf, 'rb') as f:
      f_iter = csv.DictReader(f)
      vals = f_iter.next()
      return vals

  def write_authvals_csv(self, authd, authf):
    f = open(authf, 'wb')
    fieldnames = tuple(authd.iterkeys())
    headers = dict((n,n) for n in fieldnames)
    f_iter = csv.DictWriter(f, fieldnames=fieldnames)
    f_iter.writerow(headers)
    f_iter.writerow(authd)
    f.close

  def reg_user(self):
    log.info("Calling reg_user")
    request_token, request_token_secret = self.yahoo.get_request_token(data = {'oauth_callback': CallbackUrl})
    self.authd['oauth_token'] = request_token
    self.authd['oauth_token_secret'] = request_token_secret
    # Now send user to approve app.
    print "You will now be directed to a website for authorization.\n\
    Please authorize the app, and then copy and paste the provide PIN below."
    webbrowser.open("%s?oauth_token=%s" % (AuthorizationUrl, self.authd['oauth_token']))
    time.sleep(1)
    self.authd['oauth_verifier'] = raw_input('Please enter your PIN:')
    # Get final auth token
    session = self.yahoo.get_auth_session(request_token, request_token_secret, method='POST', data={'oauth_verifier': self.authd['oauth_verifier']})
    self.authd['access_token'] = session.access_token
    self.authd['access_token_secret'] = session.access_token_secret
    self.write_authvals_csv(self.authd, self.authf)
    # Return new session
    return session

  def refresh_session(self):
    session = self.yahoo.get_session((self.authd['access_token'], self.authd['access_token_secret']))
    time.sleep(.5)
    return session

  def api_req(self, querystring, req_meth='GET', data=None, headers=None):
    log.info("Calling api_req")
    url = BaseApiUrl + querystring
    params={'format': 'json'}
    if ('oauth_token' not in self.authd) or ('oauth_token_secret' not in self.authd) or (not (self.authd['oauth_token'] and self.authd['oauth_token_secret'])):
      log.info("Inside first if statement in api_req.")
      session = self.reg_user()
    else:
      log.info("Inside else clause in api_req.")
      session = self.refresh_session()
    query = session.get(url, params=params)

    log.info("query = %s", query.text)
    log.info("header = %s", query.headers)

    # We may need to add sleep statement here
    
    if query.status_code != 200: #We have both authtokens but are being rejected. Assume token expired. This could be a LOT more robust
      log.warn("Status code is %d", query.status_code)
      log.warn("query = %s", query.text)
      session = self.reg_user()
      query = session.get(url, params=params)
    return query
