'''
import requests
import json

ONOS_URL= 'http://1270.0.1:8181/onos/v1/flows/of%3A0000000000000001?appId=0'
ONOS_BASE_URL = 'http://1270.0.1:8181/onos/v1/'


class OnosClient:

    def __init__(self) -> None:
        pass
    
    headers = {'Content-type': 'application/json'}

    @staticmethod
    def auth():
        print("auth")
        response = requests.post(ONOS_URL,,headers=headers) 
        return response.json()  



    @staticmethod
    def getDevices():
        print("Devices")
        response = requests.post(ONOS_BASE_URL,,headers=headers) 
        return response.json()  

    @staticmethod
    def block():
        print("block")
        
        data = {
            "priority": 6,      
            "timeout": 0,      
            "isPermanent": "true",      
            "deviceId": "of:0000000000000001",     
            "treatment": {      
                "instructions": [      
                        
                ]      
            },      
            "selector": {      
                "criteria": [      
                    {      
                    "type": "ETH_TYPE",      
                    "ethType": "0x0800"   
                    },   
                    {   
                    "type": "ETH_SRC",   
                    "mac": "00:00:00:00:00:03"   
                    },   
                    {   
                    "type": "ETH_DST",   
                    "mac": "00:00:00:00:00:01"   
                    },   
                    {    
                    "type": "IN_PORT",   
                    "port": 3   
                    },   
                    { "type": "IPV4_SRC",   
                    "ip": "10.0.0.3/32"   
                    },   
                    { "type": "IPV4_DST",   
                    "ip": "10.0.0.1/32"   
                    }   
                ]      
            }      
        }
        response = requests.post(ONOS_URL,data=json.dumps(data),headers=headers) 
        return response.json()  
'''