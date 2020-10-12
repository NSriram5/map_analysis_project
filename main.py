from node import Node
from packet import Packet

nodelist = []

#Initialize

#simple node map for testing and debugging
maplist = [{"name": "apple","neighbors": [("pear",4),("mango",3),("banana",2)]},{"name": "banana","neighbors": [("apple",2),("mango",3),("kiwi",1)]},{"name": "mango","neighbors": [("banana",2),("apple",3),("pear",2)]},{"name": "pear","neighbors": [("apple",4),("mango",2),("kiwi",1)]},{"name": "kiwi","neighbors": [("banana",1),("pear",1)]}]

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

#/Handle Commands/NetworkIntroduction

#/Handle Commands/Reporting

#Simulation

#/Simulation/Loop
def sim_loop(nextfunc,endcondfunc):
    day = 0
    datalog = ""
    packet_orders = ""
    end_condition = False

    #/Simulation/Helper functs
    def create_packet(sourcestr,recipientstr,load = 1,):
        name = f'{sourcestr},{recipientstr},{day},{packet_iter}'
        nonlocal packet_iter
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
                file.write(node.notification)
                node.newday()
        #Increment day value
        nonlocal day
        day = day + 1
        return True

    while True:
        packet_iter = 0
        packet_orders = packet_orders.split(",")
        for order in packet_orders:
            order = order.split(":")
            packet_iter += create_packet(order[0],order[1],order[2])

        if endcondfunc == None or end_condition:
            break
        while not check_if_all_exhausted():
            if check_all_node_queues_empty():
                #something next happens
                if nextfunc == None:
                    break
                elif nextfunc == "end_sim":
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
        #do things
        pass
    elif inp == "run_random":
        #do things
        pass
    elif inp == "help":
        #do things
        pass
    else:
        print("Command not recognized. Please use \"help\" if you're confused about commands")
