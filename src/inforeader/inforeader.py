import subprocess
import json


class InfoReader(object):
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
    def __init__(self, log_path):
        self.log_path = log_path
        super(NodeReader, self).__init__()

    def data(self):
        data = '{' + self._readChunk(self.log_path) + '}'
        data = json.loads(data)
        return data['data'][0]
