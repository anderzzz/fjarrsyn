'''Bla bla

'''
from core.agent import Agent
from core.agent_ms import AgentManagementSystem

from core.graph import Graph, Node

class Ant(Agent):
    '''Bla bla

    '''
    def _request_what_is_opinion(self):
        '''Bla bla

        '''
        return self.belief['my_opinion']

    def _request_form_new_opinion(self):
        '''Bla bla

        '''
        pass

    def __init__(self, name, rebel_index, opinion_init):

        super().__init__(name)

        self.update_belief('rebel', rebel_index)
        self.update_belief('my_opinion', opinion_init)

        self.set_service('what_is_opinion', self._request_what_is_opinion)
        self.set_service('form_new_opinion', self._request_form_new_opinion)

class AntColony(AgentManagementSystem):
    '''Bla bla

    '''
    def _obtain_neighbours_opinions(self, agent_index):
        '''Bla bla

        '''
        self.get_neighbours(agent_index)
        # CALL NEIGHBOUR FUNC IN PARENT
        pass

    def __init__(self, name, agents, graph_type='poisson', graph_p=0.5):

        ant_relations = Graph()
        nodes = [Node('ant_%s' %(str(k)), agent) for k, agent in enumerate(agents)]
        if graph_type == 'poisson':
            ant_relations.build_poisson_nondirectional(nodes, graph_p)
        else:
            raise RuntimeError('Unknown graph type for ant colony: %s' %(graph_type))

        super().__init__(name, agents, full_agents_graph=ant_relations)

        for ant in self.agents_iter():
            # HOW TO SET SENSOR TO JUST PART OF GRAPH?
            ant.update_sensor('neighbours_opinions',
                              self._obtain_neighbours_opinions, ant.agent_id_system)
