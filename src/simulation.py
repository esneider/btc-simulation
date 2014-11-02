#!/usr/bin/env python
import random
import math
import heapq

class Node(object):
    def __init__(self, bandwidth):
        # self.latency = latency
        self.bandwidth = bandwidth
        self.connections = []
        self.tipHead = 0

class Connection(object):
    def __init__(self, destination, delay):
        self.destination = destination
        self.delay = delay

class Network(object):
    def __init__(self):
        self.nodes = []
    def randomNode(self):
        return random.choice(self.nodes)

class Block(object):
    id = 0
    def  __init__(self, timestamp, miner, parent):
        id = id + 1
        self.id = id
        self.timestamp = timestamp
        self.miner = miner
        self.parent = parent
        self.height = parent.height + 1 if parent else 0

class Event(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp
    def __lt__(self, other):
        return self.timestamp - other.timestamp

class BlockMined(Event):
    def __init__(self, timestamp, miner):
        super(BlockMined, self).__init__(timestamp)
        self.miner = miner

    def apply(self, network):
        pass

class BlockReceived(Event):
    def __init__(self, timestamp, receiver, block):
        super(BlockReceived, self).__init__(timestamp)
        self.receiver = receiver
        self.block = block

    def apply(self):
        pass



MAX_BANDWIDTH_KBPS = 10000
MAX_DELAY_MS = 15
MS_PER_SECONDS = 1000


def randomBandwidth():
    return random.random() * MAX_BANDWIDTH_KBPS

def randomDelay():
    return random.random() * MAX_DELAY_MS

def randomTimeBetweenBlocks(time):
    return random.random() * time


def createRandomNetwork(numNodes, numConnections):
    network = Network()

    for _ in xrange(numNodes):
        network.nodes.append(Node(randomBandwidth()))

    for node in network.nodes:
        for _ in xrange(numConnections):
            node.connections.append(Connection(network.randomNode(), randomDelay()))

    return network

def createBlockEvent(network, currentTime):
    time = currentTime + randomTimeBetweenBlocks(EXPECTED_MS_BETWEEN_BLOCKS);
    return BlockMined(time, network.randomNode())


EXPECTED_MS_BETWEEN_BLOCKS = 600 * MS_PER_SECONDS
NUM_NODES = 10
CONNECTIONS_PER_NODE = 3

if __name__ == "__main__":

    events = []
    network = createRandomNetwork(NUM_NODES, CONNECTIONS_PER_NODE)

    heapq.heappush(createBlockEvent(network, 0))
    while len(events):
        results = heapq.heappop(events).apply(network)
        for event in results:
            heapq.heappush(events, event)

    print network

