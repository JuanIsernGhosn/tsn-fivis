import subprocess
import json
from datetime import datetime
import os
import shutil


class InfoReader(object):

    FAIL_MSG = {
        "id": "??",
        "ts": "??",
        "sync_min": "0",
        "sync_max": "0",
        "sync_mean": "0",
        "link_delay_0": "0",
        "link_delay_1": "0",
        "link_delay_2": "0",
        "link_delay_3": "0",
        "port_role_0": "0",
        "port_role_1": "0",
        "port_role_2": "0",
        "port_role_3": "0",
        "node_status": "0",
        "GM": "",
        "path_trace1": "",
        "path_trace2": "",
        "last_failover": "0"
    }

    def __init__(self):
        pass

    @staticmethod
    def _readChunk(sys_file):
        if sys_file is None:
            return None

        out = subprocess.Popen(['cat', sys_file], universal_newlines=True,
                               stdout=subprocess.PIPE, stderr=None)
        stdout, stderr = out.communicate()

        return stdout

    @staticmethod
    def _readValue(sys_file):
        if sys_file is None:
            return None

        out = subprocess.Popen(['cat', sys_file],
                               stdout=subprocess.PIPE, stderr=None)
        stdout, stderr = out.communicate()

        return float(stdout) / 1000


    @staticmethod
    def _readFile(command, args):
        out = subprocess.Popen(['sudo', command, args],
                               stdout=subprocess.PIPE, stderr=None)
        stdout, stderr = out.communicate()
        stdout = stdout.decode("utf-8")
        stdout_splitted = stdout.splitlines()

        return stdout_splitted


class NodeReader(InfoReader):
    def __init__(self, log_path, board, simulate):
        self.log_path = log_path
        self.simulate = simulate
        self.board = board
        self.read_failures_count = 0
        self.last_failover = 0
        super(NodeReader, self).__init__()

    def data(self):

        if self.simulate:

            try:
                folders = os.listdir(self.log_path)
                print(folders)
            except KeyError:
                raise Exception("Must specify a valid directory where the logs are")

            date = [datetime.strptime(folder.replace('_', ' '), "%d%m%y %H%M") for folder in folders]

            newest = folders[date.index(min(date))]

            try:
                logs = [each for each in os.listdir(os.path.join(self.log_path, newest, self.board)) if each.endswith('.log')]
            except Exception as e:
                print("Must specify a valid directory where the logs are")
                return None

            logs.sort()

            try:
                log = logs[0]
            except Exception as e:
                return None

            log_path = os.path.join(self.log_path, newest, self.board, log)
            data = '{' + self._readChunk(log_path) + '}'
            os.remove(log_path)

            count = 0

            for root, dirs, files in os.walk(os.path.join(self.log_path, newest, self.board)):
                for file in files:
                    if file.endswith(".log"):
                        count += 1
            if count == 0:

                if os.path.exists(os.path.join(self.log_path, newest, self.board)):
                    shutil.rmtree(os.path.join(self.log_path, newest, self.board))
                    if len(os.listdir(os.path.join(self.log_path, newest))) == 0:
                        print('{} vacía, borrado'.format(newest))
                        shutil.rmtree(os.path.join(self.log_path, newest))
                        folders.remove(newest)
                        date.remove(min(date))
                return None

            try:
                data = json.loads(data)
                data = data['data'][0]
            except Exception as e:
                data = self.FAIL_MSG
                print(e)
                return data

        else:
            data = self._readChunk(self.log_path)

            try:
                data = json.loads(data)['data'][0]
            except Exception as e:
                data = self.FAIL_MSG
                print(e)
                return data

        last_fail_real = data['last_failover']

        if data['last_failover'] == self.last_failover:
            self.read_failures_count += 1
            if self.read_failures_count >= 2:
                data = self.FAIL_MSG
        else:
            self.read_failures_count = 0

        self.last_failover = last_fail_real
        return data
