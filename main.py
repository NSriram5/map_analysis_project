from node import Node
from packet import Packet
import json

nodelist = []

#Initialize

#simple node map for testing and debugging
maplist = [
    {"name": "apple",
    "neighbors": [("pear",4),("mango",3),("banana",2)]},
    {"name": "banana",
    "neighbors": [("apple",2),("mango",3),("kiwi",1)]},
    {"name": "mango",
    "neighbors": [("banana",2),("apple",3),("pear",2)]},
    {"name": "pear",
    "neighbors": [("apple",4),("mango",2),("kiwi",1)]},
    {"name": "kiwi",
    "neighbors": [("banana",1),("pear",1)]}]

def load_map_from_file(fname):
    pass

#/Initialize/Setup node map
for item in maplist:
    n = Node(addressname = item["name"],bandwidth = 100)
    nodelist.append(n)
for node in nodelist:
    for item in maplist:
        if item["name"]==node.address:
            for tup in item["neighbors"]:
                for tar_node in nodelist:
                    if tar_node.address == tup[0]:
                        node.assign_neighbor(tar_node,tup[1])




#Handle Commands

#/Handle Commands/Help
def print_help():
    print('Here\'s a list of the current commands that function:')
    print('run_introduction')
    print(network_introduction.__doc__)
    #print('Random Packet Simulation')
    #print()

#/Handle Commands/NetworkIntroduction
def every_connect_generator():
    for node1 in nodelist:
        for node2 in nodelist:
            if node1.address != node2.address:
                yield node1,node2
introduction_generator = every_connect_generator()

def network_introduction():
    'This function introduces all of the nodes to one another so that they know how to send packets in the future'
    while True:
        try:
            start,end = next(introduction_generator)
        except StopIteration:
            break
        name = f'{start.address},{end.address},intro,introduction'
        packet = Packet(name,end.address,start.address,0,0)
        start.recieve_packet(packet)

        while not all([not bool(node.queue_emptyq()) for node in nodelist]):
            for node in nodelist:
                node.process_one_item()
    
    #Report on how to get from any node to any other node with a node waypoint
    for node in nodelist:
        for place,nextplace in node.networkaware_map.items():
            print(f'To get from {node.address} to {place} you need to travel to {nextplace.address}')
        



#/Handle Commands/Reporting

#Simulation

#/Simulation/Loop
def sim_loop(type_of_sim):
    day = 0
    end_condition = False
    datalog = ""

    #/Simulation/Helper functs
    def create_packet(sourcestr,recipientstr,load = 1,):
        nonlocal packet_iter
        name = f'{sourcestr},{recipientstr},{day},{packet_iter}'
        packet_iter += 1
        source = list(filter(lambda node:node.address==sourcestr,nodelist))[0]
        recipient = list(filter(lambda node: node.address == recipientstr,nodelist))[0]
        packet = Packet(name,recipient,source,day,load)
        source.recieve_packet(packet)
        return True

    def check_all_node_queues_empty():
        return not any(node.queue_emptyq() for node in nodelist)

    def check_if_all_exhausted():
        return all([n.is_exhausted() for n in nodelist])

    def new_day():
        #collect_notification flags form the map and write to file
        with open("output.txt",'a') as file:
            for node in nodelist:
                if node.notification != "":
                    file.write(node.notification)
                node.newday()
        #Increment day value
        nonlocal day
        day = day + 1
        return True

    while True:
        packet_iter = 0

        if end_condition:
            break
        while not check_if_all_exhausted():
            if check_all_node_queues_empty():
                if type_of_sim == "introduction":
                    try:
                        source,destination = next(introduction_generator)
                        create_packet(source,destination)
                    except StopIteration:
                        end_condition = True
                elif type_of_sim == "random":
                    end_condition = True
                    break
            for node in nodelist:
                node.process_one_item
        new_day()

    return datalog

#Main Loop
current_command = ""

while current_command != "exit":
    inp = input("Command Prompt (exit to quit; help to see list of commands): ")
    if inp == "exit":
        break
    elif inp == "run_introduction":
        print("Running network introduction")
        network_introduction()
        pass
    elif inp == "run_random":
        #do things
        pass
    elif inp == "help":
        print_help()
    else:
        print("Command not recognized. Please use \"help\" if you're confused about commands")
