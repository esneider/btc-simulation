#!/usr/bin/env python
import random
import math
import heapq
import os

# Simulation parameters

NUM_NODES = 20
MAX_BLOCK_SIZE_KB = 1000
CONNECTIONS_PER_NODE = 4
MEAN_TIME_BETWEEN_BLOCKS_SECS = 45

# Network connection properties

MEAN_BANDWIDTH_KBPS = 100
STD_BANDWIDTH_KBPS = 30

MEAN_DELAY_SECS = 0.500
STD_DELAY_SECS = 0.100

class Node(object):
    id = 0
    def __init__(self, bandwidth):
        # self.latency = latency
        Node.id += 1
        self.id = Node.id
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

class Ledger(object):
    def __init__(self):
        self.blocks = []

class Block(object):
    id = 0
    def  __init__(self, timestamp, miner):
        Block.id += 1
        self.id = Block.id
        self.timestamp = timestamp
        self.miner = miner
        self.parent = miner.head
        self.height = self.parent.height + 1 if self.parent else 0
        if self.parent:
            assert self.timestamp > self.parent.timestamp

class Event(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __cmp__(self, other):
        if self.timestamp == other.timestamp:
            return 0
        return 1 if self.timestamp > other.timestamp else -1

    def __str__(self):
        return '(%s created at %.3f)' % (type(self).__name__, self.timestamp)

class BlockMined(Event):
    def __init__(self, timestamp, miner):
        super(BlockMined, self).__init__(timestamp)
        self.miner = miner
        self.ignored = False
        self.accepted = True

    def apply(self, network, ledger):
        events = []
        self.block = Block(self.timestamp, self.miner)
        self.miner.head = self.block
        ledger.blocks.append(self.block)
        events.append(createBlockEvent(network, self.timestamp))
        events += createPropagationEvents(self.miner, self.block, self.block.timestamp)
        return events

    def log(self):
        return '[%s] node %d mined block %d at height %d' % (
            makeTimestamp(self.timestamp), self.miner.id, self.block.id, self.block.height
        )

class BlockReceived(Event):
    def __init__(self, timestamp, receiver, block):
        super(BlockReceived, self).__init__(timestamp)
        self.receiver = receiver
        self.block = block
        self.accepted = False
        self.ignored = False

    def apply(self, network, ledger):
        if self.receiver.head and self.receiver.head.height >= self.block.height:
            # TODO: Make this look at same height
            self.ignored = self.receiver.head.id == self.block.id
            return []
        self.accepted = True
        self.receiver.head = self.block
        return createPropagationEvents(self.receiver, self.block, self.timestamp)

    def log(self):
        return '[%s] node %d received block %d and %s it' % (
            makeTimestamp(self.timestamp),
            self.receiver.id, self.block.id,
            'accepted' if self.accepted else 'ignored' if self.ignored else 'rejected'
        )

class Events(object):
    def __init__(self):
        self.events = []
        self.lastPop = None

    def push(self, event):
        assert not self.lastPop or event.timestamp >= self.lastPop.timestamp
        heapq.heappush(self.events, event)

    def pop(self):
        event = heapq.heappop(self.events)
        assert not self.lastPop or event.timestamp >= self.lastPop.timestamp
        self.lastPop = event
        return event

    def empty(self):
        return len(self.events) == 0

def makeTimestamp(timestamp):
    ts = int(timestamp * 1000)
    return '%02d:%02d:%02d.%03d' % (ts / 3600000, (ts / 60000) % 60, (ts / 1000) % 60, ts % 1000)

def randomBandwidth():
    norm = random.normalvariate(MEAN_BANDWIDTH_KBPS, STD_BANDWIDTH_KBPS)
    return norm if norm > 0 else 1

def randomDelay():
    norm = random.normalvariate(MEAN_DELAY_SECS, STD_DELAY_SECS)
    return norm if norm > 0 else 0.010

def randomTimeBetweenBlocks():
    norm = random.expovariate(1./MEAN_TIME_BETWEEN_BLOCKS_SECS)
    return norm if norm > 0 else 0.1

def createRandomNetwork(numNodes, numConnections):
    network = Network()

    for _ in xrange(numNodes):
        network.nodes.append(Node(randomBandwidth()))

    for node in network.nodes:
        for _ in xrange(numConnections/2):
            peer = network.randomNode()
            delay = randomDelay()
            node.connections.append(Connection(peer, delay))
            peer.connections.append(Connection(node, delay))

    return network

def createBlockEvent(network, currentTime):
    time = currentTime + randomTimeBetweenBlocks();
    return BlockMined(time, network.randomNode())

def createPropagationEvents(sender, block, timestamp):
    events = []
    for connection in sender.connections:
        receiver = connection.peer
        bandwidth = min(receiver.bandwidth, sender.bandwidth)
        time = timestamp + connection.delay + MAX_BLOCK_SIZE_KB / bandwidth
        # TODO: take into consideration node's total bandwith
        events.append(BlockReceived(time, receiver, block))
    return events

def blockColor(block):
    colors = ['aquamarine', 'coral', 'green', 'darkorchid1', 'gold', 'snow3', 'deeppink']
    return colors[block.id % 7 if block else 0]

def drawNetwork(network):
    with open('network.dot', 'w') as f:
        f.write('graph network {\n')
        for node in network.nodes:
            f.write('\tnode%d [label="%d (%s)" fillcolor="%s" style="filled"];\n' % (
                node.id,
                node.id,
                str(node.head.height) if node.head else '-',
                blockColor(node.head)
            ))
        for node in network.nodes:
            for connection in node.connections:
                if node.id < connection.peer.id:
                    f.write('\tnode%d -- node%d;\n' % (node.id, connection.peer.id))
        f.write('}')

def drawLedger(ledger):
    with open('ledger.dot', 'w') as f:
        f.write('digraph ledger {\n')
        for block in ledger.blocks:
            f.write('\tblock%d [label="%d (%d)" fillcolor="%s" style="filled" shape="box"];\n' % (
                block.id,
                block.id,
                block.height,
                blockColor(block)
            ))
        for block in ledger.blocks:
            if block.parent:
                f.write('\tblock%d -> block%d;\n' % (block.id, block.parent.id))
        f.write('}')

if __name__ == "__main__":

    events = Events()
    ledger = Ledger()
    network = createRandomNetwork(NUM_NODES, CONNECTIONS_PER_NODE)

    drawLedger(ledger)
    drawNetwork(network)
    os.system('make dot open')

    events.push(createBlockEvent(network, 0))
    while not events.empty():
        event = events.pop()
        # print event.timestamp
        results = event.apply(network, ledger)
        if not event.ignored:
            print event.log()
            if event.accepted:
                drawLedger(ledger)
                drawNetwork(network)
                os.system('make dot refresh')
                raw_input()
        # if type(event) == BlockMined:
        #     raw_input()
        for event in results:
            events.push(event)

    print network

