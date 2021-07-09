import requests
import json


class FivisRequester(object):

    def __init__(self, api_endpoint, token, partner, signal_set, schema):
        self.api_endpoint = api_endpoint
        self.token = token
        self.partner = partner
        self.signal_set = signal_set
        self.schema = schema

        self.sending_queue = []

        self.headers = {'Content-Type': 'application/json',
                        'access-token': self.token}

    def postData(self, data_container):

        data = {'partnerId': self.partner,
                'signalSetId': self.signal_set,
                'schema': self.schema,
                'data': data_container}
        self.sending_queue.append(data)
        len_queue = len(self.sending_queue)
        for i in range(0, len_queue):
            data_to_send = self.sending_queue.pop(0)
            print(data_to_send)
            r = requests.post(self.api_endpoint, data=json.dumps(data_to_send), headers=self.headers)
            if r.text != "":
                self.sending_queue.append(data_to_send)

