'''Bla bla

'''
import copy
import random

from core.agent_ms import AgentManagementSystem
from core.graph import CubicGrid

from core.organs import Sensor, Actuator

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
    def _act_gulp_my_environment(self, agent_index, how_much):
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

    def _sense_random_neighbour_surface(self, agent_index):
        '''Sensor method that selects random neighbour node and if agent is
        present tickles it for its surface profile

        Parameters
        ----------
        agent_index : str
            The index of the agent for which to sense its environment

        Returns
        -------
        buzz : dict
            A dictionary of the buzz the sensor elicits in the agent. The
            dictionary has two keys `surface_profile` and `neighbour`, the
            former being a string representing the surface profile obtained
            from the tickle, and the agent index of the neighbouring agent.

        '''
        neighbour_agents = self.graph_neighbours_to(agent_index)

        bacteria = random.choice(list(neighbour_agents))
        if bacteria is None:
            ret = {'surface_profile' : None, 'neighbour' : None} 

        else:
            ret = {'surface_profile' : bacteria.tickle('surface_profile'), 
                   'neighbour' : bacteria.agent_id_system}

        return ret

    def _act_add_molecules_to_env(self, agent_index, dx_molecules_poison):
        '''Actuator method to add molecules from one agent to another

        Parameters
        ----------
        agent_index : str
            Agent index to agent to which's environment molecules are to be
            added
        dx_molecules : dict
            Amount of molecules to add based on its key

        '''
        node_with_agent = self.agents_graph[agent_index]
        environment = node_with_agent.aux_content
        print (dx_molecules_poison)
        print ('aaa555')
        for molecule, dx in dx_molecules_poison.items():
            x = environment.molecule_content[molecule] 
            x_new = x + dx
            environment.molecule_content[molecule] = x_new 
        print (environment.molecule_content)

    def _act_new_cell_into_matrix(self):
        '''Bla bla

        '''
        pass

    def __init__(self, name, beaker_length, bacterial_agents, env_object):

        #
        # Create agent graph as cubic grid and initialize base agent management
        # system
        #
        matrix = CubicGrid(n_slots=beaker_length) 
        matrix_size = len(matrix)

        super().__init__(name, bacterial_agents, matrix)

        #
        # Assign content to the nodes of the grid
        #
        env_objects = [copy.deepcopy(env_object) for k in range(matrix_size)]
        random_index = random.sample(range(matrix_size), 
                                     len(bacterial_agents))

        k_bacteria = 0 
        for grid_index, env_object in enumerate(env_objects):
            matrix.nodes[grid_index].aux_content = env_object

            if grid_index in random_index:
                bact_agent = bacterial_agents[k_bacteria]
                k_bacteria += 1
                matrix.nodes[grid_index].agent_content = bact_agent

            else:
                matrix.nodes[grid_index].agent_content = None 

        #
        # Equip agents with organs to interact with the World
        #
        for bacteria in bacterial_agents:
            actuator = Actuator('molecules_to_environment',
                                'share_molecules',
                                self._act_add_molecules_to_env,
                                ['dx_molecules_poison'],
                                bacteria.agent_id_system)
            bacteria.set_organ(actuator)

            sensor = Sensor('random_neighbour_surface', 
                            'neighbour_surface',
                            self._sense_random_neighbour_surface,
                            ['surface_profile', 'neighbour'],
                            {'agent_index' : bacteria.agent_id_system})
            bacteria.set_organ(sensor)
                                       

