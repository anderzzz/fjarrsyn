'''Bla bla

'''
import pandas as pd

class Node(object):
    '''Bla bla
    
    '''
    def __init__(self, name, object_content):

        self.name = name 
        self.content = object_content

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

        self._populate(nodes, connections)

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

    def _populate(self, nodes, connections):
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

    def __init__(self):

        self.nodes = None
        self.edges = None


