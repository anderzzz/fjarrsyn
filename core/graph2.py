'''Bla bla

'''
import random
import pandas as pd

import networkx as nx

class Node(object):
    '''Bla bla
    
    '''
    def __str__(self):
        
        return self.name

    def __contains__(self, item):

        if self.agent_content is None:
            return False

        else:
            return item == self.agent_content.agent_id_system

    def __init__(self, name, agent_content, aux_content=None):

        self.name = name 
        self.agent_content = agent_content
        self.aux_content = aux_content

class Graph(object):
    '''Bla bla

    '''
    def build_complete_nondirectional(self, nodes):
        '''Build a complete non-directional graph from nodes

        Parameters
        ----------
        nodes
            List of node objects

        '''
        connections = []
        for k_node1, node1 in enumerate(nodes):
            for node2 in nodes[k_node1:]:
                connections.append((node1, node2, EdgeProperty()))

        self.populate(nodes, connections)

    def build_poisson_nondirectional(self, nodes, p):
        '''Bla bla

        '''
        connections = []
        for k_node1, node1 in enumerate(nodes):
            for node2 in nodes[k_node1:]:
                yes_no = random.random()
                if yes_no < p:
                    connections.append((node1, node2, EdgeProperty()))

        self.populate(nodes, connections)

    def get_adjacency_list(self):
        '''Return the adjacency list

        '''
        return self.agent_network.adjacency()

    def get_neighbours(self, node):
        '''Bla bla

        '''
        return self.agent_network.neighbors(node)

    def populate(self, connections):
        '''Manually build a graph from container of node pairs that constitute
        the edges of the graph

        Parameters
        ----------
        connections
            Container of node object pairs that define the edges of the graph

        '''
        self.agent_network.add_edges_from(connections)

    def __getitem__(self, key):

        ret = None
        for node in self.nodes:
            if key in node:
                ret = node
                break

        if ret is None:
            raise KeyError('Agent with ID %s not found in graph' %(key))

        return ret

    def __iter__(self):

        for node in self.nodes:

            yield node

    def __len__(self):

        return len(self.nodes)

    def __init__(self, name):

        self.name = name
        self.agent_network = nx.Graph()

class CubicGrid(Graph):
    '''Bla bla

    '''
    def __init__(self, n_slots=10):

        super().__init__()

        cells = []
        coords = []
        connections = []
        for x_slot in range(0, n_slots):
            for y_slot in range(0, n_slots):
                for z_slot in range(0, n_slots):
                    cell = Node('grid_cell_%s_%s_%s' %(str(x_slot),
                                                       str(y_slot), 
                                                       str(z_slot)), None, None) 
                    cells.append(cell)
                    coord = (x_slot, y_slot, z_slot)
                    coords.append(coord)

                    for k_cell, coord_past in zip(cells, coords):
                        x_diff = abs(coord[0] - coord_past[0])
                        y_diff = abs(coord[1] - coord_past[1])
                        z_diff = abs(coord[2] - coord_past[2])

                        if (x_diff + y_diff + z_diff) == 1:
                            connections.append((k_cell, cell, EdgeProperty()))

        self.populate(cells, connections)

