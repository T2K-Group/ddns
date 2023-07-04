###############################
# Author: Jack Fitton
# Project: Dynamic DNS Updater
# File: utils/cf.py
# Company: T2K Group 
# Created: 03/07/2023
# Modified: 03/07/2023
# License: MIT
###############################
# https://t2k.group
# https://github.com/T2K-Group
###############################

import aiohttp, json, asyncio, logging

#Required Inputs:
# API_KEY: CloudFlare API Key
# DNS_DOMAIN: Domain to update w/ subdomain (e.g. subdomain.domain.com) if applicable
# IP: IP Address to update DNS record to
# RECORD_TYPE: DNS Record Type (e.g. A, AAAA, CNAME, etc.)

#TODO: Create record if it doesn't exist already

async def updateCloudFlareDns(API_KEY: str, DNS_DOMAIN: str, IP: str, RECORD_TYPE: str = "A") -> bool:


    # if domain has a subdomain then split and get subdomain and domain
    # if domain is just domain.com then subdomain is @ and domain is domain.com
    def split_domain(domain):
        # Strip "www." if present
        domain = domain.replace("www.", "")

        # Strip "http://" or "https://" if present
        if domain.startswith("http://"):
            domain = domain[len("http://"):]
        elif domain.startswith("https://"):
            domain = domain[len("https://"):]
        
        parts = domain.split('.')
        subdomain = parts[0] if len(parts) > 2 else '@'
        domain = '.'.join(parts[-2:])
        return subdomain, domain
    
    subdomain, ZONE_NAME = split_domain(DNS_DOMAIN)



    


    async def testAPI(API_KEY: str) -> bool:
        url = "https://api.cloudflare.com/client/v4/user/tokens/verify"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:

            async with session.get(url=url, headers=headers) as response:

                if response.status == 200:
                    if (await response.json())["success"]:
                        return True
                    else:
                        return False
                else:
                    return False

    async def getZoneId(API_KEY: str, ZONE_NAME: str) -> str:

        url = f"https://api.cloudflare.com/client/v4/zones?name={ZONE_NAME}"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        print(headers)

        async with aiohttp.ClientSession() as session:
                
                async with session.get(url=url, headers=headers) as response:
    
                    if response.status == 200:

                        jsonOutput = await response.json()
                        id = jsonOutput["result"][0]["id"]
                        return id
                    
                    else:
                        return False

    async def getZoneRecords(API_KEY: str, ZONE_ID: str) -> str:

        url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"

        headers = {
            "Authorization":f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
                
                async with session.get(url=url, headers=headers) as response:
    
                    if response.status == 200:
                        return (await response.json())
                    else:
                        return await response.text()

    def parseRecords(records: str, recordType: str) -> dict:

        recordData = {}

        for record in records["result"]:

            if record["type"] == recordType.upper():
                recordData[record["name"]] = [record["content"], record["id"]]

        return recordData

    async def updateRecord(API_KEY: str, ZONE_ID: str, recordID: str, payload: list) -> bool:

        url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{recordID}"

        headers = {
            "Authorization":f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        name = payload[0]
        ip_addr = payload[1]
        recordType = payload[2]


        data = {
            "type": recordType.upper(),
            "name": name,
            "content": ip_addr,
        }

        async with aiohttp.ClientSession() as session:
                    
                    async with session.put(url=url, headers=headers, data=json.dumps(data)) as response:
        
                        if response.status == 200:
                            return True
                        else:
                            return False






    API_STATUS = await testAPI(API_KEY)

    if API_STATUS:
        # get zone id from domain name (ZONE_NAME)
        ZONE_ID = await getZoneId(API_KEY, ZONE_NAME)
        if ZONE_ID:
            # get all records from zone
            records = await getZoneRecords(API_KEY, ZONE_ID)
            if records:
                # parse records into dict
                recordData = parseRecords(records, RECORD_TYPE)

                if subdomain == "@":
                    recordName = ZONE_NAME
                else:
                    recordName = f"{subdomain}.{ZONE_NAME}"

                if recordName in recordData:

                    if recordData[recordName][0] == IP:
                        return True
                    
                    else:
                        payload = [recordName, IP, RECORD_TYPE]

                        if await updateRecord(API_KEY, ZONE_ID, recordData[recordName][1], payload):
                            return True



        else:
            logging.error("CloudFlare Zone Name / ID is invalid")
            return False
            

    else:
        logging.error("CloudFlare API Key is invalid")
        return False








