'''Bla bla

'''
from core.agent_ms import AgentManagementSystem

from core.graph import Graph, Node

class AntColony(AgentManagementSystem):
    '''Bla bla

    '''
    def _obtain_neighbours_opinions(self, agent_index):
        '''Bla bla

        '''
        neighbour_agents = self.graph_neighbours_to(agent_index)

        ret = []
        for agent in neighbour_agents:
            opinion, responded = agent.request_service('what_is_opinion')

            if responded:
                ret.append(opinion)

        return ret

    def __init__(self, name, agents, graph_type='poisson', graph_p=0.5):

        ant_relations = Graph()
        nodes = [Node('ant_%s' %(str(k)), agent) for k, agent in enumerate(agents)]
        if graph_type == 'poisson':
            ant_relations.build_poisson_nondirectional(nodes, graph_p)
        else:
            raise RuntimeError('Unknown graph type for ant colony: %s' %(graph_type))

        super().__init__(name, agents, full_agents_graph=ant_relations)

        for ant in self.iteritems():
            ant.update_sensor('neighbours_opinions',
                              self._obtain_neighbours_opinions, 
                              {'agent_index': ant.agent_id_system})
