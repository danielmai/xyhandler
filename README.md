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

```python
#!/usr/bin/python
 
from xyhandler import xYHandler
  
handle = xYHandler("auth.csv")
querystring = 'player/273.p.5479/stats'
user_request = handle.api_req(querystring).json()
print user_request
```
