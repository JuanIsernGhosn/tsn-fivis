from threading import Thread, Event
from handler import RequestHandler
import time

class Application(Thread):
    def __init__(self, measure_every=1, send_every=20):
        self.handlers = {}
        self._stop_event = Event()
        self.measure_every = measure_every
        self.send_every = send_every
        super(Application, self).__init__()

    def addHandler(self, handler: RequestHandler):
        self.handlers[handler.getId()] = handler

    def addHandlers(self, handlers):
        for handler in handlers:
            self.addHandler(handler)

    def stop(self):
        self._stop_event.set()

    def isStopped(self):
        return self._stop_event.is_set()

    def recordData(self):
        for key, handler in self.handlers.items():
            handler.readValues()

    def sendData(self):
        for key, handler in self.handlers.items():
            if handler.dataAvailable():
                handler.sendInformation()

    def run(self) -> None:
        n_times_recorded = 0
        while not self.isStopped():
            self.recordData()
            time.sleep(self.measure_every)
            n_times_recorded += 1
            if n_times_recorded == self.send_every:
                self.sendData()
                n_times_recorded = 0
        self.sendData()

