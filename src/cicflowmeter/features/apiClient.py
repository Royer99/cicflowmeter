
import requests
import json

#features description
# dur Record total duration. - flow_duration
# sbytes Source-to-destination bytes count.
# spkts Source-to-destination packet count.
# max Maximum duration at records aggregate level.
# min Minimum duration at records aggregate level.
# dbytes Destination-to-source bytes count.
# sum Total duration at records aggregate level.
# dpkts Destination-to-source packet count
# pkts Total number of packets in transaction.
# drate  Destination-to-source packets per second.
# model_name Random Forest
# rate Total packets per second in transaction.
# bytes Total number of bytes in transaction.
# mean Average duration at records aggregate level.
# srate Source-to-destination packets per second.
# stddev Standard deviation of the duration at records aggregate level.

MODEL_URL = "https://thesis-ddos.herokuapp.com/api/identify/"
#MODEL_URL = "http://127.0.0.1:3000/"
class Request:

    def __init__(self,
                dur,
                sbytes,
                dbytes,
                bytes,
                spkts,
                dpkts,
                pkts,
                srate,
                drate,
                rate,
                min,
                max,
                sum,
                mean,
                stddev,
                model_name):
        self.dur = dur
        self.sbytes = sbytes
        self.spkts = spkts
        self.max = max
        self.dbytes = dbytes
        self.sum = sum
        self.dpkts = dpkts
        self.pkts = pkts
        self.drate = drate
        self.min = min
        self.model_name = model_name
        self.rate = rate
        self.bytes = bytes
        self.mean = mean
        self.srate = srate
        self.stddev = stddev

    def apiCall(self):
        print("API CALL")
        headers = {'Content-type': 'application/json'}
        response = requests.post(MODEL_URL,data=json.dumps(self.__dict__),headers=headers) 
        return response.content
       
    
        