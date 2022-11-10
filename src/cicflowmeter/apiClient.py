import json

import requests

# features description
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

#MODEL_URL = "https://thesis-ddos.herokuapp.com/api/identify/occ"
MODEL_URL = "http://54.172.102.91/classify"
#MODEL_URL = "https://thesis-ddos.herokuapp.com/api/identify"
#MODEL_URL = "http://127.0.0.1:3000/"


class Request:

    def __init__(self,
                 Dur,
                 SrcBytes,
                 DstBytes,
                 TotBytes,
                 SrcPkts,
                 DstPkts,
                 TotPkts,
                 SrcRate,
                 DstRate,
                 Rate,
                 Min,
                 Max,
                 Sum,
                 Mean,
                 StdDev,
                 model):
        self.Dur = Dur
        self.SrcBytes = SrcBytes
        self.DstBytes = DstBytes
        self.TotBytes = TotBytes
        self.SrcPkts = SrcPkts
        self.DstPkts = DstPkts
        self.TotPkts = TotPkts
        self.SrcRate = SrcRate
        self.DstRate = DstRate
        self.Rate = Rate
        self.Min = Min
        self.Max = Max
        self.Sum = Sum
        self.Mean = Mean
        self.StdDev = StdDev
        self.model = model

    def apiCall(self):
        #print("API CALL")
        headers = {'Content-type': 'application/json'}
        response = requests.post(MODEL_URL, data=json.dumps(self.__dict__), headers=headers, verify=False)
        return response.json()
