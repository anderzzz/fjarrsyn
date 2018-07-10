'''Bla bla

'''
import copy
import random

from core.agent_ms import AgentManagementSystem
from core.graph import CubicGrid

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
    def _gulp_my_environment(self, agent_index, how_much):
        '''Bla bla

        '''
        env_agent = self.agents_in_scope[self.relation[agent_index]]
        molecules = env_agent.request_service('how_many_molecules')

        ret = {}
        for molecule_name, molecule_amount in molecules.items():
            gulped_amount = how_much * float(molecule_amount)
            remaining_amount = float(molecule_amount) - gulped_amount

            ret[molecule_name] = gulped_amount

            env_agent.scaffold[molecule_name] = remaining_amount

        return ret 

    def _obtain_random_neighbour_surface(self, agent_index):
        '''Bla bla

        '''
        neighbour_agents = self.graph_neighbours_to(agent_index)

        bacteria = random.choice(neighbour_agents)['bacteria']
        if bacteria is None:
            ret = (None, None)
        else:
            ret = (bacteria.request_service('surface_profile'), bacteria.agent_id_system)

        return ret

    def _add_molecules_to_env(self, agent_index, dx_molecules):
        '''Bla bla

        '''
        env_agent = self.agents_in_scope[self.relation[agent_index]]
        for molecule, dx in dx_molecules.items():
            x = env_agent.scaffold[molecule]
            x_new =+ dx
            env_agent.set_data('scaffold', molecule, x_new)

    def _new_cell_into_matrix(self):
        '''Bla bla

        '''
        pass

    def update_bact_env_map(self, bacteria_id, env_id):
        '''Bla bla

        '''
        self.relation[bacteria_id] = env_id
        self.relation[env_id] = bacteria_id

    def __init__(self, name, beaker_length, bacterial_agents, env_agent):

        self.relation = {}

        matrix = CubicGrid(n_slots=beaker_length) 
        matrix_size = len(matrix)

        env_agents = [copy.deepcopy(env_agent) for k in range(matrix_size)]
        random_index = random.sample(range(matrix_size), 
                                     len(bacterial_agents))

        for ind, env_agent in enumerate(env_agents):
            if ind in random_index:
                bact_agent = bacterial_agents.pop(0)
                matrix.nodes[ind].content = {'bacteria':bact_agent,
                                             'env':env_agent}
                self.update_bact_env_map(bact_agent.agent_id_system,
                                         env_agent.agent_id_system)
            else:
                matrix.nodes[ind].content = {'bacteria':None,
                                             'env':env_agent}

        for bacteria in bacterial_agents:
            bacteria.set_organ('actuator', 'add_molecules_to_env',
                                           self._add_molecules_to_env)
            bacteria.set_organ('actuator', 'gulp_environment',
                                           self._gulp_my_environment)
            bacteria.set_organ('actuator', 'bring_new_cell_into_matrix',
                                           self._new_cell_into_matrix)
            bacteria.set_organ('sensor', 'sense_random_neighbour_surface',
                                         self._obtain_random_neighbour_surface)
                                       

        agents = bacterial_agents + env_agents
        super().__init__(name, agents, matrix)

