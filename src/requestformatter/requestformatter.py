from abc import ABC, abstractmethod
from datetime import datetime
from inforeader import NodeReader

class RequestFormatter(ABC):
    def __init__(self, info_reader):
        self.info_reader = info_reader


    @staticmethod
    @abstractmethod
    def getSchema():...

    def getInformation(self):...


class NodeFormatter(RequestFormatter):
    def __init__(self, tsn_reader: NodeReader):
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
        now = datetime.utcnow()
        data_temp = self.info_reader.data()
        data_temp['ts'] = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data_temp['id'] = now.timestamp()
        return data_temp
