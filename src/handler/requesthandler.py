from requestformatter import RequestFormatter
from requester import FivisRequester

class RequestHandler(object):
    def __init__(self, request_formatter: RequestFormatter,
                 request_sender: FivisRequester):
        self.r_formatter = request_formatter
        self.request_sender = request_sender
        self.data = []

    def getId(self):
        return id(self)

    def dataAvailable(self):
        return len(self.data) > 0

    def readValues(self):
        self.data.append(self.r_formatter.getInformation())

    def sendInformation(self):
        self.request_sender.postData(self.data)
        self.data = []