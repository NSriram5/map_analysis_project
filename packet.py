
class Packet:
    def __init__(self,idname,destination,source,time,load = 1):
        self.load = load
        self.name = idname
        self.destination = destination
        self.timecreated = time
        self.latesthandler = None
        self.source = source
        self.distance = 0

    def __copy__(self):
        c = Packet(self.name,self.destination,self.source,self.timecreated,self.load)
        c.distance = self.distance
        return c
    
    def __str__(self):
        return "Packet:{},From:{},To:{},Sent:{},Distance:{},Load:{}".format(self.name,self.source,self.destination,self.timecreated,self.distance,self.load)

    def distanceincrease(self,distance):
        self.distance += distance