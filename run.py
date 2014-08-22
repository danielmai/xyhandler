#!/usr/bin/python
from xyhandler import xYHandler
import time
import random
import logging

def init_logging():
    """Initialize logging."""
    global log
    log = logging.getLogger(__name__)
    logfmt = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(format=logfmt,level=logging.DEBUG)

    

init_logging()

handle = xYHandler("auth.csv")
querystring = 'player/273.p.5479/stats'

query_count = 1
while True:
    user_request = handle.api_req(querystring).json()

    log.debug(str(user_request))
    log.info("Number of API calls done: %d", query_count)
    
    query_count += 1

    # Sleep, because maybe we're getting rejected for being a robot
    sleep_time = 8
    log.info("Sleep for %d seconds", sleep_time)
    time.sleep(sleep_time)
