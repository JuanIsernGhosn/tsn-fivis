import json
from requester import FivisRequester
from handler import RequestHandler
from requestformatter import *
import os


class ApplicationConfigurer(object):

    def __init__(self, api_config, log_folder):

        with open(api_config, 'r') as f:
            self.api_config = json.load(f)

        self.log_folder = log_folder

    def geNodeHandlers(self):

        try:
            files = os.listdir(self.log_folder)
        except KeyError:
            raise Exception("Must specify a valid directory where the logs are")

        nodes_handlers = []

        for log_file in files:
            log_file_full = os.path.join(self.log_folder, log_file)
            if os.path.isfile(log_file_full) and log_file.endswith('.log'):

                node_reader = NodeReader(log_file_full)
                node_formatter = NodeFormatter(node_reader)

                signal_set = log_file[:-4]

                fivis_requester = self._getFivisRequester(signal_set, node_formatter.getSchema())
                nodes_handlers.append(RequestHandler(node_formatter, fivis_requester))

        return nodes_handlers

    def _getFivisRequester(self, signal_set, schema):
        fivis_requester = FivisRequester(self.api_config["api_endpoint"],
                                         self.api_config["token"],
                                         self.api_config["partner"],
                                         signal_set,
                                         schema)
        return fivis_requester



