'''Bla bla

'''
import copy
import random

from core.agent_ms import AgentManagementSystem
from core.graph import CubicGrid

from core.sensor import _Sensor

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
    def _gulp_my_environment(self, agent_index, how_much):
        '''Bla bla

        '''
        node_with_agent = self.matrix[agent_index]
        environment = node_with_agent.aux_content
        molecules = environment.molecules_content 

        ret = {}
        for molecule_name, molecule_amount in molecules.items():
            gulped_amount = how_much * float(molecule_amount)
            remaining_amount = float(molecule_amount) - gulped_amount

            ret[molecule_name] = gulped_amount

            environment.molecules_content[molecule_name] = remaining_amount

        return ret 

    def _obtain_random_neighbour_surface(self, agent_index):
        '''Bla bla

        '''
        neighbour_agents = self.graph_neighbours_to(agent_index)

        bacteria = random.choice(neighbour_agents)
        if bacteria is None:
            ret = (None, None)
        else:
            ret = (bacteria.request_service('surface_profile'), bacteria.agent_id_system)

        return ret

    def _add_molecules_to_env(self, agent_index, dx_molecules):
        '''Bla bla

        '''
        node_with_agent = self.matrix[agent_index]
        environment = node_with_agent.aux_content
        for molecule, dx in dx_molecules.items():
            x = environment.molecule_content[molecule] 
            x_new = x + dx
            environment.molecule_content[molecule] = x_new 

    def _new_cell_into_matrix(self):
        '''Bla bla

        '''
        pass

    def __init__(self, name, beaker_length, bacterial_agents, env_object):

        self.relation = {}

        matrix = CubicGrid(n_slots=beaker_length) 
        matrix_size = len(matrix)

        env_objects = [copy.deepcopy(env_object) for k in range(matrix_size)]
        random_index = random.sample(range(matrix_size), 
                                     len(bacterial_agents))

        for ind, env_object in enumerate(env_object):
            matrix.nodes[ind].aux_content = env_object
            if ind in random_index:
                bact_agent = bacterial_agents.pop(0)
                matrix.nodes[ind].agent_content = bact_agent
            else:
                matrix.nodes[ind].agent_content = None 

        for bacteria in bacterial_agents:
            actuator = Actuator('add_molecules_to_environment',
                                'share_molecules',
                                self._add_molecules_to_env,
                                ['dx_molecules'],
                                bacteria.agent_id_system)
            bacteria.set_organ(actuator)

            sensor = Sensor('random_neighbour_surface', 
                            'neighbour_surface',
                            self._obtain_random_neighbour_surface,
                            {'agent_index' : bacteria.agent_id_system})
            bacteria.set_organ(sensor)
                                       
        super().__init__(name, bacterial_agents, matrix)

