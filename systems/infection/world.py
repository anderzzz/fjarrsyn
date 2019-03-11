'''The World in which units reside, the AMS

'''
from core.agent_ms import AgentManagementSystem

from core.instructor import Sensor, Actuator, MultiMutation
from core.message import MessageOperator
from core.scaffold_map import EssenceMap, ResourceMap, MapCollection, universal_map_maker

import numpy as np

STRICT_ENGINE = True

class World(AgentManagementSystem):

    def _cmp_neighbour_coop(self, calling_agent_id):
        '''Bla bla

        '''
        neighbour_nodes = self.neighbours_to(calling_agent_id, agents_only=False)
        node = np.random.choice(list(neighbour_nodes))
        if node is None:
            return None

        else:
            return node.agent_content.tickle('Reveal Cooperation').values()

    def _cmp_alter_env_resources(self, da, db, dc, calling_agent_id):
        '''Bla bla

        '''
        neighbour_nodes = self.neighbours_to(calling_agent_id, agents_only=False)
        n_neighbours = len(neighbour_nodes)

        for node in neighbour_nodes:
            node.aux_content.container['info_a'] += da / n_neighbours
            node.aux_content.container['info_b'] += db / n_neighbours
            node.aux_content.container['info_c'] += dc / n_neighbours

        return -da, -db, -dc

    def _cmp_gulp_env(self, f_gulp, calling_agent_id):
        '''Bla bla

        '''
        env = self.get(calling_agent_id, get_aux=True)
        
        da = env.container['info_a'] * f_gulp
        db = env.container['info_b'] * f_gulp
        dc = env.container['info_c'] * f_gulp
        d_tox = env.container['toxin'] * f_gulp

        env.container['info_a'] -= da
        env.container['info_b'] -= db
        env.container['info_c'] -= dc
        env.container['toxin'] -= d_tox
        
        return da, db, dc, d_tox

    def _midpoint_move(self):

        return self.midpoint_max_move

    def _max_move(self):

        return self.max_max_move, 0.0, 1.0

    def __init__(self, name, agents, local_ambient, 
                 midpoint_max_move, max_max_move, mutate_prob):

        super().__init__(name, agents, agent_env=local_ambient,
                         strict_engine=STRICT_ENGINE)

        self.midpoint_max_move = midpoint_max_move
        self.max_max_move = max_max_move

        for agent in agents:
            
            #
            # Sensor
            sensor = Sensor('Feel Neighbour Surface', 
                            self._cmp_neighbour_coop,
                            agent.buzz['Neighbour Cooperator'],
                            agent_id_to_engine=True)
            agent.set_organ(sensor)

            #
            # Actuator
            a_resources = MessageOperator(agent.resource,
                              slice_labels=['info_a', 'info_b', 'info_c'])
            a_a_subtract = ResourceMap('Consume A', 'delta', 'info_a', ('removal',))
            a_b_subtract = ResourceMap('Consume B', 'delta', 'info_b', ('removal',))
            a_c_subtract = ResourceMap('Consume C', 'delta', 'info_c', ('removal',))
            consume_resources = MapCollection([a_a_subtract, a_b_subtract, a_c_subtract])
            actuator = Actuator('Share Resources to Neighbours',
                                self._cmp_alter_env_resources,
                                agent.direction['Resources to Share'],
                                agent_id_to_engine=True,
                                resource_map_output=consume_resources)
            agent.set_organ(actuator)

            add_from_env = universal_map_maker(agent.resource, 'delta', ('add',))
            actuator = Actuator('Gulp Environment',
                                self._cmp_gulp_env,
                                agent.direction['Fraction to Gulp'],
                                agent_id_to_engine=True,
                                resource_map_output=add_from_env)
            agent.set_organ(actuator)

        #
        # Mutation
        map_midpoint_share = EssenceMap('mutate_1', 'wiener',
                                        'midpoint_share', ('range_step',))
        map_midpoint_gulp = EssenceMap('mutate_2', 'wiener',
                                       'midpoint_gulp', ('range_step',))
        map_midpoint_tox = EssenceMap('mutate_3', 'wiener',
                                      'midpoint_tox', ('range_step',))
        map_max_share = EssenceMap('mutate_1b', 'wiener_bounded',
                                   'max_share', ('range_step', 'lower', 'upper'))
        map_max_gulp = EssenceMap('mutate_2b', 'wiener_bounded',
                                  'max_gulp', ('range_step', 'lower', 'upper'))
        map_max_tox = EssenceMap('mutate_3b', 'wiener_bounded',
                                 'max_tox', ('range_step', 'lower', 'upper'))
        mapper_midpoint = MapCollection([map_midpoint_share, 
                                         map_midpoint_gulp, 
                                         map_midpoint_tox])
        mapper_max = MapCollection([map_max_share, map_max_gulp, map_max_tox])
        mutate_midpoint = MultiMutation('Perturb Essence 1', self._midpoint_move, 
                                        mapper_midpoint,
                                        mutation_prob=mutate_prob)
        mutate_max = MultiMutation('Perturb Essence 2', self._max_move, 
                                   mapper_max, 
                                   mutation_prob=mutate_prob)

        self.set_laws(mutate_midpoint, mutate_max)
