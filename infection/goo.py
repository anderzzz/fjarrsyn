'''Bla bla

'''
import copy
import random

from core.agent_ms import AgentManagementSystem
from core.graph import CubicGrid

from core.organs import Sensor, Actuator
from core.naturallaw import ObjectForce

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
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
        neighbour_agents = self.neighbours_to(agent_index)

        bacteria = random.choice(list(neighbour_agents))
        if bacteria is None:
            ret = {'surface_profile' : None, 'neighbour' : None} 

        else:
            ret = {'surface_profile' : bacteria.tickle('surface_profile'), 
                   'neighbour' : bacteria.agent_id_system}

        return ret

    def _act_gulp_my_environment(self, agent_index, how_much):
        '''Actuator method to collect a fraction of the content of the
        environment and push that content back as a reaction to the agent

        Parameters
        ----------
        agent_index : str
            The index of the agent that is gulping environment content
        how_much : float
            Fraction of environment content to gulp, should be between zero and
            one

        Returns
        -------
        reaction : ObjectForce instance
            The reaction the environment provides as a fraction of it is gulped
            by the agent. The reaction must subsequently be executed in order
            to update the internal state of the agent

        '''
        reaction = ObjectForce('scaffold_reaction')

        node_with_agent = self.agents_graph[agent_index]
        environment = node_with_agent.aux_content
        molecules = environment.molecule_content 

        for molecule_name, molecule_amount in molecules.items():
            gulped_amount = how_much * float(molecule_amount)
            remaining_amount = float(molecule_amount) - gulped_amount
            environment.molecule_content[molecule_name] = remaining_amount

            reaction.set_force_func(molecule_name, 'delta', 
                                    {'increment' : gulped_amount})

        return reaction 

    def _act_add_molecules_to_env(self, agent_index, dx_molecules_poison):
        '''Actuator method to add molecules from one agent to all neighbouring
        agent environments

        Parameters
        ----------
        agent_index : str
            Agent index to agent to which's environment molecules are to be
            added
        dx_molecules_poison : dict
            Amount of molecules and poison to add based on its key

        '''
        neighbour_nodes = self.neighbours_to(agent_index, agents_only=False)
        n_neighbours = len(neighbour_nodes)

        for neighbour_node in neighbour_nodes:
            environment = neighbour_node.aux_content
            for molecule, dx in dx_molecules_poison.items():
                x = environment.molecule_content[molecule] 
                x_new = x + dx / float(n_neighbours)
                environment.molecule_content[molecule] = x_new 

    def _act_new_cell_into_matrix(self, agent_index, do_it):
        '''Bla bla

        '''
        if do_it:
            node = self.agents_graph[agent_index]


    def _act_suicide(self, agent_index, do_it):
        '''Actuator to remove agent from the agent management system

        Parameters
        ----------
        agent_index : str
            Agent index to agent to remove from system
        do_it : bool
            Boolean flag to instruct actuator if agent suicide should be done

        '''
        if do_it:
            del self[agent_index]

        else:
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

            actuator = Actuator('agent_suicide',
                                'contemplate_suicide',
                                self._act_suicide,
                                ['do_it'], 
                                bacteria.agent_id_system)
            bacteria.set_organ(actuator)

            actuator = Actuator('environment_gulper',
                                'gulp_environment',
                                self._act_gulp_my_environment,
                                ['how_much'],
                                bacteria.agent_id_system)
            bacteria.set_organ(actuator)

            sensor = Sensor('random_neighbour_surface', 
                            'neighbour_surface',
                            self._sense_random_neighbour_surface,
                            ['surface_profile', 'neighbour'],
                            {'agent_index' : bacteria.agent_id_system})
            bacteria.set_organ(sensor)
                                       

