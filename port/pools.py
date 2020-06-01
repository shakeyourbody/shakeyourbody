from utils.types import Event


class DataPool():

    def __init__(self):
        self.clear()

    def clear(self):
        self.pool = []
        return self

    def append(self, data):
        self.pool.append(data)
        return self

    def remove(self, data):
        self.pool.remove(data)

    def each(self, cbk):
        for data in self.pool:
            cbk(data)

    def filter(self, condition):
        survivors = DataPool()
        for data in self.pool:
            if condition(data):
                survivors.append(data)
        return survivors


class EventsPool():

    def __init__(self):
        self.events = DataPool()
        self.clear()

    def clear(self):
        self.events.clear()
        self.clock = 0
        return self

    def at(self, timestamp, cbk, *args):
        self.events.append(Event(timestamp, cbk, args))
        return self

    def update(self, elapsed):
        self.clock += elapsed
        self.events = self.events.filter(self.__update_event)

    def __update_event(self, event):
        if event.timestamp <= self.clock:

            return event()
        return True
