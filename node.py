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
        self.exhausted = False
        self.operating = True
        self.notification = ""

        #TODO define a private variable
        #self.__private = something

    #Setup functionality
    def assign_neighbor(self,neighbor,distance):
        self.neighbors[neighbor.address] = (neighbor,distance)

    #Change functionality
    def remove_neighbor(self,neighbor):
       self.neighbors.pop(neighbor)    

    #Operations functionality
    def recieve_packet(self, packet):
        #check to verify that I haven't already seen this packet before
        if (not packet.name in [packet.name for packet in self.completedpackets]) and (not packet.name in [packet.name for packet in self.packetqueue]):
            self.packetqueue.append(packet) #add packet to queue

            #If the packet source isn't on the network aware map then add it with the value being the vector it arrived on
            if not self.networkaware_map.get(packet.source,False):
                self.networkaware_map[packet.source] = packet.latesthandler #update my information about the network map

#Done
    def send_packet(self,destnode,packet,distance):
        copypacket = packet.copy() #create deep copy of packet
        copypacket.distanceincrease(distance)#update packet distance marker
        copypacket.latesthandler=self
        destnode.recieve_packet(copypacket)

#Done
    def process_queue(self):
        #work through queue until bandwidth is met
        while self.bandwidth > self.bandwidthtoday:
            self.exhausted = not self.process_one_item()

#Done
    def process_one_item(self):
        for i in range(0,len(self.packetqueue)):
            packet = self.packetqueue[i]
            if self.bandwidthtoday - packet.load >= 0:
                #is the packet addressed to a neighbor?
                if packet.destination in self.neighbors.keys():
                    self.send_packet(self.neighbors[packet.destination][0],packet,self.neighbors[packet.destination][1])
                #does the node know which vector to send the packet on?
                elif packet.destination in self.networkaware_map.keys():
                    next_node = self.networkaware_map[packet.destination]
                    distance = self.neighbors.get(next_node)[1]
                    self.send_packet(next_node,packet,distance)
                #am I the recipient of this packet?
                elif packet.destination == self.address:
                    self.notification += "Packet recieved! --" + str(packet) + "\n"
                else:
                    #blindly send packet to all neighbors
                    for nodetuple in self.neighbors.values():
                        next_node = nodetuple[0]
                        distance = nodetuple[1]
                        self.send_packet(next_node,packet,distance)
                self.bandwidthtoday -= packet.load
                self.packetqueue = self.packetqueue[0:i]+self.packetqueue[i+1:]
                self.completedpackets.append(packet)
                return True
        if len(self.packetqueue)>0 and self.bandwidthtoday == self.bandwidth:
            self.notification += "There might be a logjam with packets with me \n"
        return False

#Done
    def newday(self):
        #the dawn of a new day capacity is reset
        self.bandwidthtoday = self.bandwidth
        self.notification = ""

    #Simulation functionality
#Done
    def set_disable(self):
        self.operating = False

#Done
    def set_enable(self):
        self.operating = True
    
    def queue_emptyq(self):
        return len(self.packetqueue)

    def is_exhausted(self):
        return self.exhausted

if __name__ == "__main__":
    kiwi = ("Kiwi",10)
    kiwi = Node("Kiwi",10)
    pear = Node("Pear",4)
    mango = Node("Mango",10)
    kiwi.assign_neighbor(pear,1)
    apple = Node("Apple",10)
    pear.assign_neighbor(apple,4)
    pear.assign_neighbor(kiwi,1)
    pear.assign_neighbor(mango,2)
    apple.assign_neighbor(pear,4)
    mango.assign_neighbor(pear,2)
    banana = Node("Banana",2)
    banana.assign_neighbor(apple,2)
    apple.assign_neighbor(banana,2)
    best_gift = Packet("Best Gift",banana.address,kiwi.address,5,load = 5)
    lesser_gift = Packet("Lesser Gift",banana.address,kiwi.address,6)
    kiwi.recieve_packet(best_gift)
    kiwi.recieve_packet(lesser_gift)
    print("Kiwi's queue before transmission")
    print(kiwi.packetqueue)
    kiwi.process_one_item()
    print("Kiwi's queue after transmission")
    print(kiwi.packetqueue)
    print("Pear's queue after transmission")
    print(pear.packetqueue)
    print("Next transmission")
    pear.process_one_item()
    print("Pear's queue after 2nd transmission")
    print(pear.packetqueue)
    print("Apple's queue after 2nd transmission")
    print(apple.packetqueue)
    print("Next transmission")
    apple.process_one_item()
    print("Pear's queue after 3nd transmission")
    print(pear.packetqueue)
    print("Apple's queue after 3nd transmission")
    print(apple.packetqueue)
    print("Banana's queue after 3nd transmission")
    print(banana.packetqueue)
    print("Banana processes the item in it's queue")
    banana.process_one_item()
    print("Banana should now have a notification")
    print(banana.notification)
    print("Apple should now know something about where to find Kiwi")
    print(apple.networkaware_map['Kiwi'].address)
    print("Mango got a copy of the packet because pear didn't know where to send it")
    print(mango.packetqueue)
    print("Mango can send the packet again back upstream but Pear discards it because it already has seen the packet")
    print("What does Mango remember processing?")
    print(pear.completedpackets)
    mango.process_one_item()
    print("Mango packet queue")
    print(mango.packetqueue)
    print("Pear packet queue")
    print(pear.packetqueue)
    print("Sending the best gift to Banana was hard work how much bandwidth do the nodes have left?")
    print(f'Mango: {mango.bandwidthtoday}')
    print(f'Pear: {pear.bandwidthtoday}')
    print(f'Apple: {apple.bandwidthtoday}')
    print(f'Kiwi: {kiwi.bandwidthtoday}')