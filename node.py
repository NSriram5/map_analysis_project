from packet import Packet

class Node:
    def __init__(self,addressname,bandwidth):
        #Initialize a node
        self.address = addressname #a unique identifier that a packet uses to send to me
        self.packetqueue = [] #the node's packet backlog
        self.completedpackets = [] #a log of the packets this node has serviced
        self.bandwidth = bandwidth #how much packet units can I work through before I need to stop?
        self.bandwidthtoday = bandwidth #the bandwidth at the beginning of a day
        self.neighbors = {} #a dict of immediate neighbors addresses and node, distance tuples that will be built before the simulation runs
        self.networkaware_map = {} #a map that the node slowly builds as it gains information about its surroundings
        self.operating = True
        self.notification = ""

    #Setup functionality
    def assign_neighbor(self,address,neighbor,distance):
        self.neighbors.update(address,(neighbor,distance))

    #Change functionality
    def remove_neighbor(self,neighbor):
       self.neighbors.pop(neighbor)    

    #Operations functionality
    def recieve_packet(self, packet):
        #check to verify that I haven't already seen this packet before
        if (not packet.name in [packet.name for packet in self.completedpackets]) and (not packet.name in [packet.name for packet in self.packetqueue]):
            self.packetqueue.append(packet) #add packet to queue
            if self.networkaware_map[packet.source]>packet.distance:
                self.networkaware_map[packet.source] = packet.distanceincrease #update my information about the network map

#Done
    def send_packet(self,destnode,packet,distance):
        #create deep copy of packet
        copypacket = packet.copy()
        #increase packet distance
        #use neighbor's recieve_packet function
        copypacket.distanceincrease(distance)#update packet distance marker
        destnode.recieve_packet(copypacket)

#Done
    def process_queue(self):
        #work through queue until bandwidth is met
        while self.bandwidth > self.bandwidthtoday:
            self.process_one_item()

#Done??
    def process_one_item(self):
        for i in range(0,len(self.packetqueue)):
            packet = self.packetqueue[i]
            if packet.load + self.bandwidthtoday <= self.bandwidth:
                #is the packet addressed to a neighbor?
                if packet.destination in self.neighbors.keys():
                    self.send_packet(self.neighbors[packet.destination][0],packet,self.neighbors[packet.destination][1])
                else:
                    #blindly send packet to all neighbors
                    for nodetuple in self.neighbors:
                        self.send_packet(nodetuple[0],packet,nodetuple[1])

#Done
    def newday(self):
        #the dawn of a new day capacity is reset
        self.bandwidthtoday = self.bandwidth

    #Simulation functionality
#Done
    def set_disable(self):
        self.operating = False

#Done
    def set_enable(self):
        self.operating = True
    
