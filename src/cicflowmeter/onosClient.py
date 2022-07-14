import requests
from requests.auth import HTTPBasicAuth
import json

ONOS_URL= 'http://1270.0.1:8181/onos/v1/flows/of%3A0000000000000001?appId=0'
ONOS_BASE_URL = 'https://c3ba-200-24-16-214.ngrok.io/onos/v1/'


class OnosClient:

    def __init__(self) -> None:
        pass
    
    headers = {'Accept': 'application/json'}
    devices =  []
    
    @staticmethod
    def getDevices():
        print("Devices")
        print(ONOS_BASE_URL + 'devices')
        url = ONOS_BASE_URL + 'devices'
        response = requests.get(ONOS_BASE_URL + 'devices', auth=HTTPBasicAuth('onos','rocks'),headers=OnosClient.headers)
        #print(response.json())
        for device in response.json()['devices']:
            OnosClient.devices.append(device['id'])
        print(OnosClient.devices)
    
    @staticmethod
    def block(src_ip):
        OnosClient.getDevices()
        for i in OnosClient.devices:
            #print("Sending flow for: " + src_ip,"ip in device: ", i)
            data = {
                "priority": 15,      
                "timeout": 0,      
                "isPermanent": "true",      
                "deviceId": i,     
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
                            "type": "IPV4_SRC",   
                            "ip": src_ip   
                        }     
                    ]      
                }      
            }
            #print(i[3::1])
            print(ONOS_BASE_URL + 'flows/of:'+i[3::1]+'?appId=0')
            url = ONOS_BASE_URL + 'flows/of%3A'+i[3::1]+'?appId=0'
            response = requests.post(url,data=json.dumps(data),headers={'Content-Type': 'application/json','Accept': 'application/json'},auth=HTTPBasicAuth('onos','rocks'))
            print(response.status_code)
            #print(response.json())
    
OnosClient.block('10.10.10.201/32')