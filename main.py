from node import Node
from packet import Packet
import json
import random


nodelist = []

# Initialize
def load_map_from_file(fname):
    '''\
    Given a txt filename, this function parses the text into a nodelist map'''
    with open(fname, "r") as file:
        material = file.read()

    # remove carriage returns
    material = material.replace("\n", "")
    try:
        maplist = json.loads(material)
    except:
        print("The text file could not be loaded. Ensure it is in json "+
        "format.")
    try:
        define_nodelist(maplist)
    except:
        print("There was an issue with reading the map into a nodelist. "+
        "Please check formatting.")


def define_nodelist(maplist):
    '''\
    Uses the items in a maplist to develop a list of nodes that's stored
    in a global variable'''
    for item in maplist:
        n = Node(address_name=item["name"], bandwidth=item["bandwidth"])
        nodelist.append(n)
    for node in nodelist:
        for item in maplist:
            if item["name"] == node.address:
                for tup in item["neighbors"]:
                    for tar_node in nodelist:
                        if tar_node.address == tup[0]:
                            node.assign_neighbor(tar_node, tup[1])


# Handle Commands

# /Handle Commands/Help
def print_help():
    '''\
    Prints a brief introduction to the Node network map functions'''
    print('Here\'s a list of the current commands that function:')

    print('load [filename].txt')
    print('--'+load_map_from_file.__doc__)
    print('run_introduction')
    print('--'+network_introduction.__doc__)
    print('run_random')
    print('--'+rnd_sim_loop.__doc__)
    print('exit')
    print('--   Exits the utility')

# /Handle Commands/NetworkIntroduction
def every_connect_generator():
    '''A generator function that retuns a tuple of two different nodes'''
    for node1 in nodelist:
        for node2 in nodelist:
            if node1.address != node2.address:
                yield node1, node2


introduction_generator = every_connect_generator()

def network_introduction():
    '''\
    This function introduces all of the nodes to one another so that they
    know how to send packets in the future'''
    while True:
        try:
            start, end = next(introduction_generator)
        except StopIteration:
            break
        name = f'{start.address},{end.address},intro,introduction'
        packet = Packet(name, end.address, start.address, 0, 0)
        start.recieve_packet(packet)

        while not all([not bool(node.queue_emptyq()) for node in nodelist]):
            for node in nodelist:
                node.process_one_item()


SEED = 0
random.seed(a=SEED)
def random_packet_maker():
    '''Yield's a random packet using the global collection nodelist
    The packet's day and name may need to be updated to make it unique
    '''
    step_from_seed = 0
    while True:
        choice1, choice2 = None, None
        choice1 = random.choice(nodelist)
        choice2 = random.choice(nodelist)
        while choice1.address == choice2.address:
            choice1 = random.choice(nodelist)
            choice2 = random.choice(nodelist)
        step_from_seed += 1
        name = f'{choice1.address},{choice2.address},seed:{step_from_seed}'
        load = 1
        packet = Packet(name, choice2.address, choice1.address, 0, load)
        yield packet

rnd_packet_maker = random_packet_maker()

def check_all_node_queues_empty():
    "Returns true when all queues in all the nodes of nodelist are empty"
    return all([bool(node.queue_emptyq()) == False for node in nodelist])


def check_if_all_exhausted():
    "Returns true when all nodes are exhausted"
    return all([n.is_exhausted() for n in nodelist])


def check_all_exhausted_or_empty():
    "Returns if a node either has no packets to process or is exhausted"
    return all([(n.queue_emptyq() == False) or 
    (not n.is_exhausted()) for n in nodelist])

# /Simulation/Loop
def rnd_sim_loop():
    '''\
    Runs a simulation of numerous days while generating a random set of 
    packets each day'''
    day = 0
    max_packets_per_day = len(nodelist)
    simulation_length = 100
    datalog = ""

    def new_day():
        # collect_notification flags form the map and write to file
        nonlocal day
        with open("output.txt", 'a') as file:
            for node in nodelist:
                if node.notification != "":
                    file.write(f'Day: {day} ' + node.notification)
                node.new_day()
        # Increment day value
        day = day + 1
        return True

    for node in nodelist:
        node.new_day()

    while simulation_length > day:
        # make packets
        todays_packets = [next(rnd_packet_maker)
                        for b in range(random.randrange(max_packets_per_day))]
        # finalize packet details and deliver them to the starting node
        packet_iter = 0
        for packet in todays_packets:
            packet.time_created = day
            packet.name += f',{packet_iter}'
            packet_iter += 1
            start_node = list(filter(lambda n: n.address ==
                                     packet.source, nodelist))[0]
            start_node.recieve_packet(packet)

        # nodes do work in sequence until they are all exhausted or have 
        # finished all their tasks
        while check_all_exhausted_or_empty():
            for node in nodelist:
                node.process_one_item()
        new_day()
    return datalog


# Main Loop
current_command = ""
while current_command.lower() != "exit":
    inp = input("Command Prompt (exit to quit; help to see list of commands): ")
    if inp == "exit":
        break
    elif inp.lower() == "run_introduction":
        print("Running network introduction")
        network_introduction()
    elif inp.lower() == "run_random":
        print("Running random packet simulation. Results will be output to file")
        rnd_sim_loop()
    elif inp.lower() == "help":
        print_help()
    elif inp[0:5].lower() == "load ":
        try_filename = inp[5:]
        if try_filename[::-1][0:4] != "txt.":
            print("That doesn't look like a txt file please enter a text file")
        else:
            load_map_from_file(try_filename)
    else:
        print(
        "Command not recognized. Please use \"help\" if you're confused" +
        "about commands")
