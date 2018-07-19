'''Bla bla

'''
import random
import pandas as pd

class Node(object):
    '''Bla bla
    
    '''
    def __str__(self):
        
        return self.name

    def __contains__(self, item):

        return item == self.agent_content.agent_id_system

    def __init__(self, name, agent_content, aux_content=None):

        self.name = name 
        self.agent_content = agent_content
        self.aux_content = aux_content

class EdgeProperty(object):
    '''Bla bla
    
    '''
    def __init__(self):

        self.weight = None
        self.direction = None

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

    def get_adjacency_matrix(self):
        '''Create and return the adjacency matrix

        '''
        matrix = {} 
        for node1 in self.nodes:
            row = []
            for node2 in self.nodes:
                if ((node1, node2) in self.adjacency_list) or \
                   ((node2, node1) in self.adjacency_list):
                    row.append(True)
                else:
                    row.append(False)
            matrix[node1] = row

        return pd.DataFrame.from_dict(matrix, orient='index', columns=self.nodes)

    def get_adjacency_list(self):
        '''Return the adjacency list

        '''
        return pd.Series(self.adjacency_list)

    def _compute_adjacency_list(self, connections):
        '''Compute the adjacency list from connections

        '''
        return [(n1, n2) for (n1, n2, edge_property) in connections]

    def populate(self, nodes, connections):
        '''Manually build a graph from ordered containers of nodes and
        correspondingly ordered edges.

        Parameters
        ----------
        nodes
            List of node objects part of graph

        '''
        self.nodes = nodes
        self.edges = connections
        self.adjacency_list = self._compute_adjacency_list(connections)

    def __getitem__(self, key):

        ret = None
        for node in self.nodes:
            if key in node:
                ret = node
                break

        if ret is None:
            raise KeyError('Agent with ID %s not found in graph' %(key))

        return ret

    def __len__(self):

        return len(self.nodes)

    def __init__(self):

        self.nodes = [] 
        self.edges = []

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

