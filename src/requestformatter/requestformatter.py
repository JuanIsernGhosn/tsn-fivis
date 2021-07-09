from abc import ABC, abstractmethod
from datetime import datetime
from inforeader import NodeReader
import time


class RequestFormatter(ABC):
    def __init__(self, info_reader):
        self.info_reader = info_reader


    @staticmethod
    @abstractmethod
    def getSchema():...

    def getInformation(self):...


class NodeFormatter(RequestFormatter):
    def __init__(self, tsn_reader: NodeReader):
        self.time_epoch = time.time()
        self.init_time_tsn = None
        super(NodeFormatter, self).__init__(tsn_reader)

    @staticmethod
    def getSchema():
        schema_temp = {
            "ts": "datetime",
            "sync_min": "double",
            "sync_max": "double",
            "sync_mean": "double",
            "link_delay_0": "integer",
            "link_delay_1": "integer",
            "link_delay_2": "integer",
            "link_delay_3": "integer",
            "port_role_0": "integer",
            "port_role_1": "integer",
            "port_role_2": "integer",
            "port_role_3": "integer",
            "node_status": "integer",
            "GM": "string",
            "path_trace1": "string",
            "path_trace2": "string",
            "last_failover": "integer"
        }
        return schema_temp

    def getInformation(self):

        data_temp = self.info_reader.data()

        if data_temp is None:
            return

        try:
            data_temp['ts'] = datetime.fromtimestamp((self.time_epoch-7200)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        except Exception as e:
            data_temp['ts'] = datetime.fromtimestamp((self.time_epoch-7200)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data_temp['id'] = self.time_epoch - 7200

        self.time_epoch = self.time_epoch + 5

        return data_temp
