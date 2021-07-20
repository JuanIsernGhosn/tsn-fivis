import json
from requester import FivisRequester
from handler import RequestHandler
from requestformatter import *
from inforeader import *
import os
from datetime import datetime
from distutils.dir_util import copy_tree



class ApplicationConfigurer(object):

    def __init__(self, api_config, log_folder, simulate):

        with open(api_config, 'r') as f:
            self.api_config = json.load(f)

        self.log_folder = log_folder
        self.simulate = simulate

    def getNodeHandlers(self):

        try:
            files_folders = os.listdir(self.log_folder)
        except KeyError:
            raise Exception("Must specify a valid directory where the logs are")

        nodes_handlers = []

        if self.simulate:
            date = [datetime.strptime(folder.replace('_', ' '), "%d%m%y %H%M") for folder in folders]
            newest = files_folders[date.index(min(date))]
            copy_tree(self.log_folder, '../res/logs_sim')
            self.log_folder = '../res/logs_sim'

            try:
                boards = os.listdir(os.path.join(self.log_folder, newest))
            except KeyError:
                raise Exception("Must specify a valid directory where the logs are")

            for board in boards:
                node_reader = NodeReader(self.log_folder, board, self.simulate)
                node_formatter = NodeFormatter(node_reader)
                signal_set = '7sols_' + board
                fivis_requester = self._getFivisRequester(signal_set, node_formatter.getSchema())
                nodes_handlers.append(RequestHandler(node_formatter, fivis_requester))
        else:

            logs = files_folders

            for log in logs:
                board = log.replace('.log','').split('_')[1]
                node_reader = NodeReader(self.log_folder+log, board, self.simulate)
                node_formatter = NodeFormatter(node_reader)
                signal_set = '7sols_' + board
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
