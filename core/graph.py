'''Bla bla

'''
ALWAYS_COMPLY = True
'''For possible extension to agents that responds to requests

'''

class Node:
    '''Bla bla
    
    '''
    def set_name(self, name):
        '''Set name of node
        
        Parameters
        ----------
        name
            The name to assign to node

        Returns
        -------
        bool
            Boolean if naming request was complied with

        '''
        self.name = name
    
        return ALWAYS_COMPLY
        
    def __init__(self):

        self.name = ''
        self.node_type = None
        self.engine = None

class EdgeProperty:
    '''Bla bla
    
    '''
    def __init__(self):

        self.weight = None
        self.direction = None

class Graph:
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

        self._manual_build(nodes, connections)

    def _manual_build(self, nodes, connections):
        '''Manually build a graph from ordered containers of nodes and
        correspondingly ordered edges.

        Parameters
        ----------
        nodes
            List of node objects part of graph

        '''
        self.nodes = nodes
        self.edges = connections

    def __init__(self):

        self.nodes = None
        self.edges = None


