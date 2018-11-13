'''Bla bla

'''
import copy
import numpy as np
import numpy.random
import networkx as nx

from core.agent_ms import AgentManagementSystem
from core.graph import Node

from core.organs import Sensor, Actuator
from core.naturallaw import ObjectMapCollection

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

        bacteria = np.random.choice(list(neighbour_agents))
        if bacteria is None:
            ret = {'surface_profile' : None, 'neighbour_id' : None} 

        else:
            ret = {'surface_profile' : bacteria.tickle('surface_profile'), 
                   'neighbour_id' : bacteria.agent_id_system}

        return ret

    def _act_gulp_my_environment(self, agent_index, how_much, reaction):
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
        reaction : ObjectMapCollection instance
            The reaction the environment provides as a fraction of it is gulped
            by the agent. The reaction must subsequently be executed in order
            to update the internal state of the agent

        '''
        node_with_agent = self.node_from_agent_id_[agent_index]
        environment = node_with_agent.aux_content
        molecules = environment.scaffold

        for molecule_name, molecule_amount in molecules.items():
            gulped_amount = how_much * float(molecule_amount)
            remaining_amount = float(molecule_amount) - gulped_amount
            environment.scaffold[molecule_name] = remaining_amount

            reaction.set_map_func(molecule_name, 'force_func_delta', 
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
                x = environment.scaffold[molecule] 
                x_new = x + dx / float(n_neighbours)
                environment.scaffold[molecule] = x_new 

    def _act_add_molecules_to_one(self, agent_index, dx_molecules_poison,
                                  give_to_id):
        '''Actuator method to add molecules from one agent to all neighbouring
        agent environments

        Parameters
        ----------
        agent_index : str
            Agent index to agent to which's environment molecules are to be
            added
        dx_molecules_poison : dict
            Amount of molecules and poison to add based on its key
        give_to_id : str
            Agent ID for the neighbour to which to add the molecules

        '''
        one_node = self.node_from_agent_id_[give_to_id]

        environment = one_node.aux_content
        for molecule, dx in dx_molecules_poison.items():
            x = environment.scaffold[molecule] 
            x_new = x + dx 
            environment.scaffold[molecule] = x_new 

    def _act_new_cell_into_matrix(self, agent_index, do_it):
        '''Actuator method to duplicate an agent and add its child to the agent
        system

        Parameters
        ----------
        agent_index : str
            Agent index to agent that is to be duplicated
        do_it : bool
            Boolean flag that signals if a duplication actually should happen
            or not. If `True` the duplication is done.

        '''
        if do_it:

            split_failed = False

            #
            # Obtain an empty neighbouring node, if available. If not available
            # take any neighbouring node.
            #
            neighbours = self.neighbours_to(agent_index, agents_only=False)
            empty_nodes = [x for x in neighbours if x.agent_content is None]
            if len(empty_nodes) > 0:
                node_to_populate = np.random.choice(empty_nodes)

            else:
                if np.random.random() < self.newborn_compete:
                    node_to_populate = np.random.choice(list(neighbours))
                    del self[node_to_populate.agent_content.agent_id_system]

                else:
                    split_failed = True

            #
            # Create agent child and add to system and node selected above
            #
            if not split_failed:
                parent_agent = self.node_from_agent_id_[agent_index].agent_content
                agent_child = parent_agent.__class__('bacteria_child', parent_agent.scaffold)
                agent_child.set_organ_bulk(self.make_affordances())
                self.situate(agent_child, node_to_populate)

        else:
            pass

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

    def make_affordances(self):
        '''Bla bla

        '''
        organs = []

        #
        # Actuator to push an amount of molecules to all neighbouring
        # environments
        #
        organs.append(Actuator('molecules_to_environment',
                               'share_molecules',
                               self._act_add_molecules_to_env,
                               ['dx_molecules_poison']))

        #
        # Actuator to push an amount of molecules to a specific neighbouring
        # environment
        #
        organs.append(Actuator('molecules_to_one_environment',
                               'share_molecules_one',
                               self._act_add_molecules_to_one,
                               ['dx_molecules_poison', 'give_to_id']))

        #
        # Actuator to terminate the present agent, which requires its removal
        # from the management system
        #
        organs.append(Actuator('agent_suicide',
                               'contemplate_suicide',
                               self._act_suicide,
                               ['do_it']))

        #
        # Actuator to gulp some fraction of the environment. This leads to a
        # reaction of a scaffold force
        #
        scaffold_force = ObjectMapCollection(['molecule_A', 'molecule_B',
                                              'molecule_C', 'poison'],
                                              standard_funcs=True)
        organs.append(Actuator('environment_gulper',
                               'gulp_environment',
                               self._act_gulp_my_environment,
                               ['how_much'],
                               {'reaction' : scaffold_force}))

        #
        # Actuator to split current agent in two, which requires one to be
        # added to the management system
        #
        organs.append(Actuator('agent_splitter',
                               'split_in_two',
                               self._act_new_cell_into_matrix,
                               ['do_it']))

        #
        # Sensor to probe a neighbours surface profile and generate a buzz
        #
        organs.append(Sensor('random_neighbour_surface', 
                             'neighbour_surface',
                             self._sense_random_neighbour_surface,
                             ['surface_profile', 'neighbour_id']))

        return organs

    def __init__(self, name, bacterial_agents, env_object, beaker_length,
                 periodic, newborn_compete, coord_agents):

        #
        # Create agent graph as cubic grid 
        #
        matrix = nx.grid_graph([beaker_length, beaker_length, beaker_length],
                               periodic=periodic)
        matrix_size = matrix.number_of_nodes() 

        #
        # Make assignment of where to place bacterial nodes
        #
        if len(bacterial_agents) != len(coord_agents):
            raise ValueError('Agent coordinates not identical in number ' + \
                             'to number of agents')

        index_match = []
        for kount, node_coord in enumerate(matrix.nodes()):
            if node_coord in coord_agents:
                index_match.append(kount)

        if len(index_match) != len(bacterial_agents):
            raise ValueError('Grid coordinates unmatched to matrix')

        #
        # Create the nodes to insert into the cubic grid
        #
        env_objects = [copy.deepcopy(env_object) for k in range(matrix_size)]

        k_bacteria = 0 
        nodes = []
        for grid_index, env_object in enumerate(env_objects):

            if grid_index in index_match:
                bact_agent = bacterial_agents[k_bacteria]
                k_bacteria += 1

                node = Node('node_%s' %(str(grid_index)), bact_agent, env_object)

            else:
                node = Node('node_%s' %(str(grid_index)), None, env_object)

            nodes.append(node)
        
        #
        # Insert the nodes into the grid
        #
        mapping = {}
        for grid_coordinate in matrix.nodes():
            mapping[grid_coordinate] = nodes.pop(0)
        matrix = nx.relabel_nodes(matrix, mapping)

        #
        # Initialize parent
        #
        super().__init__(name, bacterial_agents, matrix)

        #
        # Equip agents with organs to interact with the World
        #
        for bacteria in bacterial_agents:
            bacteria.set_organ_bulk(self.make_affordances()) 

        #
        # Special constants of the bacterial goo
        #
        self.newborn_compete = newborn_compete

