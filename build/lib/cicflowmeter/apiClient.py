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
                pkts,
                bytes,
                dur,
                mean,
                stddev,
                sum,
                min,
                max,
                spkts,
                dpkts,
                sbytes,
                dbytes,
                rate,
                srate,
                drate,
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
        #print("API CALL")
        order = {
            'pkts': 0,
            'bytes': 1,
            'dur': 2,
            'mean': 3,
            'stddev': 4,
            'sum': 5,
            'min': 6,
            'max': 7,
            'spkts': 8,
            'dpkts': 9,
            'sbytes': 10,
            'dbytes': 11,
            'rate': 12,
            'srate': 13,
            'drate': 14,
        }

        payload = self.__dict__
        model_name = ''
        data = [None] * len(order)
        for key, value in payload.items():
            if key == 'model_name':
                model_name = value
            else:
                data[order[key]] = value
        
        if model_name == '':
            model_name = 'Decision Tree'

        headers = {'Content-type': 'application/json'}
        print(json.dumps(payload))
        response = requests.post(MODEL_URL,data=json.dumps(self.__dict__),headers=headers) 
        return response.json()  