###############################
# Author: Jack Fitton
# Project: Dynamic DNS Updater
# File: main.py
# Company: T2K Group 
# Created: 03/07/2023
# Modified: 03/07/2023
# License: MIT
###############################
# https://t2k.group
# https://github.com/T2K-Group
###############################

#!/usr/bin/python3 

import asyncio, aiohttp, json, requests, logging, re, os, sys
from utils import cf


#load config.json if it exists
if os.path.isfile("config.json"):
    with open("config.json", "r") as f:
        config = json.load(f)

else:
    logging.error("config.json not found. Exiting...")
    sys.exit(1)


for dns in config:

    try:
        provider = dns["provider"]
        domain = dns["domain"]
        api_key = dns["api_key"]
        record_type = dns["record_type"]

    except KeyError as e:
        logging.warning(f"Missing required key: {e}")
        sys.exit(1)

    if provider == "cloudflare":
        asyncio.run(cf.updateCloudFlareDns(api_key, domain, record_type))

    else:
        logging.warning(f"Provider {provider} not supported. Skipping...")
        continue

    








