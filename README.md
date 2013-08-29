xyhandler
=========

Yahoo Fantasy Football API
  Simply provides the access to Yahoo and pulls the data from Yahoo.
  What you do with that data is up to you.

Basic Instructions:
1. Register with Yahoo: http://developer.yahoo.com/fantasysports/guide/
2. Put the secret and key from Yahoo in the auth.csv file.
3. Figure out what data you want and what to do with the data...

Example use:
  1 #!/usr/bin/python
  2 
  3 from xyhandler import xYHandler
  4 
  5 handle = xYHandler("auth.csv")
  6 querystring = 'player/273.p.5479/stats'
  7 user_request = handle.api_req(querystring).json()
  8 print user_request
