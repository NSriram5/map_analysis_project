from packet import Packet

class Node:
    def __init__(self,address_name,bandwidth):
        '''Create a Node Object'''

        #a unique identifier that a packet uses to send to me
        self.address = address_name
        #the node's packet backlog
        self.__packet_queue = []
        #a log of the packets this node has serviced
        self.__completed_packets = []
        #how much packet units can I work through before I need to stop?
        self.bandwidth = bandwidth
        #the bandwidth at the beginning of a day
        self.bandwidth_today = bandwidth
        #a dict of immediate neighbors addresses and node, distance tuples 
        #that will be built before the simulation runs
        self.neighbors = {}
        #a map that the node slowly builds as it gains information about its 
        # surroundings
        self.network_aware_map = {}
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
        '''\
        Object method to recieve a packet and correctly add it to the queue'''
        #check to verify that I haven't already seen this packet before
        if ((not packet.name in 
        [packet.name for packet in self.__completed_packets]) and 
        (not packet.name in [packet.name for packet in self.__packet_queue])):
            self.__packet_queue.append(packet) #add packet to queue

            #If the packet source isn't on the network aware map then add it 
            # with the value being the vector it arrived on
            if packet.source != self.address:
                if not self.network_aware_map.get(packet.source,False):
                    #update my information about the network map
                    last = packet.latest_handler
                    self.network_aware_map[packet.source] = last

    def send_packet(self,destnode,packet,distance):
        '''\
        Object method to update a packet copy with a new distance increment\
        and to then utilize the recieve_packet() function of a target node'''
        copy_packet = packet.copy() #create deep copy of packet
        copy_packet.distance_increase(distance)#update packet distance marker
        copy_packet.latest_handler=self
        destnode.recieve_packet(copy_packet)

    def process_queue(self):
        '''\
        Function that iterates through a Node's queue and works until the node\
        is fully exhausted.'''
        #work through queue until bandwidth is met
        while ((self.bandwidth > self.bandwidth_today) and 
                len(self.__packet_queue)>0):
            self.exhausted = not self.process_one_item()

#Done
    def process_one_item(self):
        for i in range(0,len(self.__packet_queue)):
            packet = self.__packet_queue[i]
            if self.bandwidth_today - packet.load >= 0:
                #is the packet addressed to a neighbor?
                if packet.destination in self.neighbors.keys():
                    dest = self.neighbors[packet.destination][0]
                    distance = self.neighbors[packet.destination][1]
                    self.send_packet(dest,packet,distance)
                #does the node know which vector to send the packet on?
                elif packet.destination in self.network_aware_map.keys():

                    next_node = self.network_aware_map[packet.destination]
                    distance = self.neighbors.get(next_node.address)[1]
                    self.send_packet(next_node,packet,distance)
                #am I the recipient of this packet?
                elif packet.destination == self.address:
                    self.notification += "Packet recieved! --"+str(packet)+"\n"
                else:
                    #blindly send packet to all neighbors
                    for nodetuple in self.neighbors.values():
                        next_node = nodetuple[0]
                        distance = nodetuple[1]
                        self.send_packet(next_node,packet,distance)
                self.bandwidth_today -= packet.load
                self.__packet_queue = (self.__packet_queue[0:i]+
                                self.__packet_queue[i+1:])
                self.__completed_packets.append(packet)
                return True
            elif ((self.bandwidth_today - packet.load<0)and
                                (len(self.__packet_queue)-1==i)):
                self.exhausted = True
        if (len(self.__packet_queue)>0 and self.bandwidth_today == 
                                                                self.bandwidth):
            self.notification += "There might be a logjam with packets with me \n"
        return False

#Done
    def newday(self):
        #the dawn of a new day capacity is reset
        self.bandwidth_today = self.bandwidth
        self.notification = ""
        self.exhausted = False

    #Simulation functionality
#Done
    def set_disable(self):
        self.operating = False

#Done
    def set_enable(self):
        self.operating = True
    
    def queue_emptyq(self):
        return len(self.__packet_queue)

    def is_exhausted(self):
        return self.exhausted

if __name__ == "__main__":
    
    #Building the test node map
    kiwi = Node("Kiwi",10)
    pear = Node("Pear",4)
    mango = Node("Mango",10)
    apple = Node("Apple",10)
    banana = Node("Banana",2)
    kiwi.assign_neighbor(pear,1)
    pear.assign_neighbor(apple,4)
    pear.assign_neighbor(kiwi,1)
    pear.assign_neighbor(mango,2)
    apple.assign_neighbor(pear,4)
    apple.assign_neighbor(banana,2)
    mango.assign_neighbor(pear,2)
    banana.assign_neighbor(apple,2)
    #Building test packets
    best_gift = Packet("Best Gift",banana.address,kiwi.address,5,load = 4)
    lesser_gift = Packet("Lesser Gift",banana.address,kiwi.address,6)
    
    
    #Check to verify that packet was correctly recieved
    kiwi.recieve_packet(best_gift)
    kiwi.recieve_packet(lesser_gift)
    assert len(kiwi._Node__packet_queue) == 2, "Trouble with adding packet to queue"

    #Check to see if packet was removed after process step
    kiwi.process_one_item()
    assert len(kiwi._Node__packet_queue) == 1, "Packet was not removed from queue"
    
    #Check queue length after process step
    assert len(pear._Node__packet_queue) == 1, "Packet is not transmitting properly"

    pear.process_one_item()
    apple.process_one_item()

    #A node processes a packet, but the only packet in it's queue is too big
    #for it to practice ever. The node produces a notification that there's
    #a logjam
    banana.process_one_item()
    assert banana.notification == ("There might be a logjam with packets " +
    "with me \n"),"Logjam not displaying when it potentially should"

    #Help with easing the logjam now allows the final recipient of the packet
    #to produce the right notification flag
    banana.notification = ''
    banana.bandwidth_today = 4
    banana.process_one_item()

    validation_noti = ('Packet recieved! --Packet:Best Gift,From:Kiwi,' +
    'To:Banana,Sent:5,Distance:7,Load:4\n')
    assert banana.notification == validation_noti,('Packet destination is '+
    'not publishing the correct notification')
    
    #In the future, apple now knows to send things the right way to get to
    #node kiwi
    assert apple.network_aware_map['Kiwi'].address == 'Pear', ('Network ' +
    'awareness map didn\'t update as expected')

    #When Pear doesn't know where to send a packet. It defaults to sending it
    #to all it's neighbors. Mango should have a copy of the packet as a result
    assert mango._Node__packet_queue[0].name == 'Best Gift', ('A side branch of the '+
    'node network didn\'t recieve a packet when the node needed to transmit '+
    'blind')

    #When a packet is recieved it is discarded if it's seen before. When Mango
    #sends the packet back to Pear it is terminated
    queue_length_before = len(pear._Node__packet_queue)
    mango.process_one_item()
    assert len(pear._Node__packet_queue) <= queue_length_before , ('Packet got ' +
    'echoed back to a node that it came from')


    #Sending the best gift to Banana was hard work how much bandwidth do the 
    # nodes have left?
    assert mango.bandwidth_today == mango.bandwidth - best_gift.load, ('Load ' +
    'didn\'t update as expected.')
    assert pear.bandwidth_today == pear.bandwidth - best_gift.load, ('Load ' +
    'didn\'t update as expected.')
    assert apple.bandwidth_today == apple.bandwidth - best_gift.load, ('Load ' +
    'didn\'t update as expected.')
    assert kiwi.bandwidth_today == kiwi.bandwidth - best_gift.load, ('Load ' +
    'didn\'t update as expected.')
