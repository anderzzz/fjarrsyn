'''Bla bla

'''
import networkx as nx
import json

class GraphIO(object):
    '''Bla bla

    '''
    def _make_agent_label_graph(self, network):
        '''Bla bla

        '''
        empty_counter = 0
        mapping = {}
        for node in network:
            agent_content = node.agent_content

            if not agent_content is None:
                mapping[node] = agent_content.agent_id_system

            else:
                mapping[node] = 'unoccupied_%s' %(str(empty_counter))
                empty_counter += 1

        network_agent_labels = nx.relabel_nodes(network, mapping)

        return network_agent_labels

    def write_graph_state(self, network, generation_counter=None):
        '''bla bla

        '''
        print ('aaa')
        network_agent_labels = self._make_agent_label_graph(network)
        
        if not self.preprocessor is None:
            write_data = self.preprocessor(network_agent_labels)

        else:
            write_data = network_agent_labels

        if not generation_counter is None:
            pos = [p for p, c in enumerate(self.file_name) if c == '.']
            pos_last_dot = pos[-1]
            file_name = self.file_name[0:pos_last_dot] + \
                        '_%s' %(str(generation_counter)) + \
                        self.file_name[pos_last_dot:]

        else:
            file_name = self.file_name

        with open(file_name, self.mode) as fout:
            self.writer(write_data, fout)

    def __init__(self, file_name_body, file_format, mode='w'):

        file_name_parts = file_name_body.split('.')
        if len(file_name_parts) == 1:
            self.file_name = file_name_body + '.' + file_format

        self.file_format = file_format
        if self.file_format == 'json':
            self.preprocessor = nx.readwrite.json_graph.node_link_data
            self.writer = json.dump

        elif self.file_format == 'gml':
            self.preprocessor = None
            self.writer = nx.readwrite.gml.write_gml
        else:
            raise ValueError('Unrecognized file format: %s' %(file_format))

        self.mode = mode
