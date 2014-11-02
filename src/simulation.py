#!/usr/bin/env python
import random
import math

class Node(object):
    def __init__(self, bandwidth):
        # self.latency = latency
        self.bandwidth = bandwidth
        self.connections = []

class Connection(object):
    def __init__(self, destination, delay):
        self.destination = destination
        self.delay = delay

class Network(object):
    def __init__(self):
        self.nodes = []


MAX_BANDWIDTH_KBPS = 10000
MAX_DELAY_MS = 15


def randomBandwidth():
    return random.random() * MAX_BANDWIDTH_KBPS

def randomDelay():
    return random.random() * MAX_DELAY_MS

def randomNode(network):
    return random.choice(network.nodes)

def createRandomNetwork(numNodes, numConnections):
    network = Network()

    for _ in xrange(numNodes):
        network.nodes.append(Node(randomBandwidth()))

    for node in network.nodes:
        for _ in xrange(numConnections):
            node.connections.append(Connection(randomNode(), randomDelay())

    return network

if __name__ == "__main__":
    network = createRandomNetwork(10, 3)



