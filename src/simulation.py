#!/usr/bin/env python
import random
import math
import heapq

EXPECTED_MS_BETWEEN_BLOCKS = 600 * MS_PER_SECONDS
NUM_NODES = 10
CONNECTIONS_PER_NODE = 3
MAX_BLOCK_SIZE_KB = 1000
MAX_BANDWIDTH_KBPS = 10000
MAX_DELAY_MS = 15
MS_PER_SECONDS = 1000

class Node(object):
    def __init__(self, bandwidth):
        # self.latency = latency
        self.bandwidth = bandwidth
        self.connections = []
        self.head = None

class Connection(object):
    def __init__(self, peer, delay):
        self.peer = peer
        self.delay = delay

class Network(object):
    def __init__(self):
        self.nodes = []
    def randomNode(self):
        return random.choice(self.nodes)

class Block(object):
    id = 0
    def  __init__(self, timestamp, miner):
        id = id + 1
        self.id = id
        self.timestamp = timestamp
        self.miner = miner
        self.parent = miner.head
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
        events = []
        block = Block(self.timestamp, self.miner)
        events.append(createBlockEvent(network, self.timestamp))
        events += createPropagationEvents(self.miner, block)
        return events

class BlockReceived(Event):
    def __init__(self, timestamp, receiver, block):
        super(BlockReceived, self).__init__(timestamp)
        self.receiver = receiver
        self.block = block

    def apply(self):
        if self.receiver.head.height >= block.height:
            return []
        self.receiver.head = block
        return createPropagationEvents(self.receiver, block)

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

def createPropagationEvents(sender, block):
    events = []
    for connection in sender.connections:
        receiver = connection.peer
        bandwidth = min(receiver.bandwidth, sender.bandwidth)
        time = block.timestamp + connection.delay + bandwidth * MAX_BLOCK_SIZE_KB
        # TODO: take into consideration node's total bandwith
        events.append(BlockReceived(time, receiver, block))
    return events


if __name__ == "__main__":

    events = []
    network = createRandomNetwork(NUM_NODES, CONNECTIONS_PER_NODE)

    heapq.heappush(createBlockEvent(network, 0))
    while len(events):
        results = heapq.heappop(events).apply(network)
        for event in results:
            heapq.heappush(events, event)

    print network

