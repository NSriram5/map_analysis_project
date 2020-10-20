
class Packet:
    def __init__(self,idname,destination,source,time,load = 1):
        self.load = load
        self.name = idname
        self.destination = destination
        self.time_created = time
        self.latest_handler = None
        self.source = source
        self.distance = 0

    def copy(self):
        '''\
        Creates deep copy of the Packet'''
        c = Packet(self.name,self.destination,
                    self.source,self.time_created,self.load)
        c.distance = self.distance
        return c
    
    def __str__(self):
        '''\
        A string representation of the Packet'''
        return (f'Packet:{self.name},From:{self.source},To:{self.destination}'+
        f',Sent:{self.time_created},Distance:{self.distance},Load:{self.load}')

    def __repr__(self):
        return (f'{self.name},{self.time_created},{self.source},'+
        '{self.destination},{self.distance},{self.load}')

    def distance_increase(self,distance):
        '''\
        Increases the packet internal measurement of distance'''
        self.distance += distance