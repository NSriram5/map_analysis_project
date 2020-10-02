from node import Node
from packet import Packet

nodelist = []

#simple node map for testing and debugging
maplist = [{"name": "apple","neighbors": [("pear",4),("mango",3),("banana",2)]},{"name": "banana","neighbors": [("apple",2),("mango",3),("kiwi",1)]},{"name": "mango","neighbors": [("banana",2),("apple",3),("pear",2)]},{"name": "pear","neighbors": [("apple",4),("mango",2),("kiwi",1)]},{"name": "kiwi","neighbors": [("banana",1),("pear",1)]}]



#Setup node map
for item in maplist:
    n = Node(item["name"],100)
for node in nodeList:
    for item in maplist:
        if 
