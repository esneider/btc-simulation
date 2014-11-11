#!/usr/bin/env python
import random
import math
import heapq
import argparse
import os

# Network connection properties

MEAN_DOWNLOAD_KBPS = 100
STD_DOWNLOAD_KBPS = 30

MEAN_UPLOAD_KBPS = 100
STD_UPLOAD_KBPS = 30

MEAN_DELAY_SECS = 0.500
STD_DELAY_SECS = 0.100

class Node(object):
    id = 0
    def __init__(self, download, upload):
        Node.id += 1
        self.id = Node.id
        self.download = download
        self.upload = upload
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
    def __init__(self, timestamp, miner, size):
        Block.id += 1
        self.id = Block.id
        self.timestamp = timestamp
        self.miner = miner
        self.parent = miner.head
        self.size = size
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
    def __init__(self, timestamp, miner, size, velocity):
        super(BlockMined, self).__init__(timestamp)
        self.miner = miner
        self.size = size
        self.velocity = velocity
        self.status = 'mined'

    def apply(self, network, ledger):
        events = []
        self.block = Block(self.timestamp, self.miner, self.size)
        self.miner.head = self.block
        ledger.blocks.append(self.block)
        time = self.timestamp + randomTimeBetweenBlocks(self.velocity);
        events.append(BlockMined(time, network.randomNode(), self.size, self.velocity))
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

    def apply(self, network, ledger):
        if self.receiver.head and self.receiver.head.height >= self.block.height:
            # TODO: Make this look at same height
            self.status = 'ignored' if self.receiver.head.id == self.block.id else 'rejected'
            return []
        self.status = 'accepted'
        self.receiver.head = self.block
        return createPropagationEvents(self.receiver, self.block, self.timestamp)

    def log(self):
        return '[%s] node %d received block %d and %s it' % (
            makeTimestamp(self.timestamp),
            self.receiver.id, self.block.id, self.status
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

def randomDownloadSpeed():
    norm = random.normalvariate(MEAN_DOWNLOAD_KBPS, STD_DOWNLOAD_KBPS)
    return norm if norm > 1 else 1

def randomUploadSpeed():
    norm = random.normalvariate(MEAN_UPLOAD_KBPS, STD_UPLOAD_KBPS)
    return norm if norm > 1 else 1

def randomDelay():
    norm = random.normalvariate(MEAN_DELAY_SECS, STD_DELAY_SECS)
    return norm if norm > 0.010 else 0.010

def randomTimeBetweenBlocks(velocity):
    norm = random.expovariate(velocity)
    return norm if norm > 0.1 else 0.1

def createRandomNetwork(numNodes, numConnections):
    network = Network()

    for _ in xrange(numNodes):
        network.nodes.append(Node(randomDownloadSpeed(), randomUploadSpeed()))

    for node in network.nodes:
        for _ in xrange(numConnections/2):
            peer = network.randomNode()
            delay = randomDelay()
            node.connections.append(Connection(peer, delay))
            peer.connections.append(Connection(node, delay))

    return network

def createPropagationEvents(sender, block, timestamp):
    events = []
    # random.shuffle(sender.connections)
    for connection in sender.connections:
        receiver = connection.peer
        bandwidth = min(receiver.download, sender.upload)
        time = timestamp + connection.delay + block.size / bandwidth
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

def parseArguments():
    parser = argparse.ArgumentParser(
        description='Run a simultion of the Bitcoin Network.',
        add_help=False
    )

    param = parser.add_argument_group('Block parameters')
    param.add_argument(
        '-s', default=1024, type=int, dest='size',
        help='maximum block size in KB', metavar='SIZE'
    )
    param.add_argument(
        '-t', default=45, type=int, dest='time',
        help='mean time between blocks in seconds', metavar='TIME'
    )

    topo = parser.add_argument_group('Network topology')
    topo.add_argument(
        '-n', default=20, type=int, dest='nodes',
        help='number of nodes in the network', metavar='NODES'
    )
    topo.add_argument(
        '-c', default=4, type=int, dest='connections',
        help='average number of connections per node', metavar='CONN'
    )

    out = parser.add_argument_group('Output')
    out.add_argument(
        '-v', action='store_true', dest='verbose', help='be verbose'
    )
    out.add_argument(
        '-g', action='store_true', dest='gui', help='show dot "gui"'
    )
    out.add_argument(
        '-h', action='help', help='show this help message and exit'
    )

    return parser.parse_args()

if __name__ == "__main__":

    args = parseArguments()
    events = Events()
    ledger = Ledger()
    network = createRandomNetwork(args.nodes, args.connections)

    if args.gui:
        drawLedger(ledger)
        drawNetwork(network)
        os.system('make dot open')

    events.push(BlockMined(0, network.randomNode(), args.size, 1.0 / args.time))

    while not events.empty():
        event = events.pop()
        for e in event.apply(network, ledger):
            events.push(e)

        if args.verbose and event.status != 'ignored':
            print event.log()

        if args.gui and event.status in ('accepted', 'mined'):
            drawLedger(ledger)
            drawNetwork(network)
            os.system('make dot refresh')
            raw_input()
