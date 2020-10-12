
class Packet:
    def __init__(self,idname,destination,source,time,load = 1):
        self.load = load
        self.name = idname
        self.destination = destination
        self.timecreated = time
        self.latesthandler = None
        self.source = source
        self.distance = 0

    def copy(self):
        c = Packet(self.name,self.destination,self.source,self.timecreated,self.load)
        c.distance = self.distance
        return c
    
    def __str__(self):
        return f'Packet:{self.name},From:{self.source},To:{self.destination},Sent:{self.timecreated},Distance:{self.distance},Load:{self.load}'

    def __repr__(self):
        return f'{self.name},{self.timecreated},{self.source},{self.destination},{self.distance},{self.load}'

    def distanceincrease(self,distance):
        self.distance += distance