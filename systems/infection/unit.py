'''Agent unit

'''
from core.agent import Agent

from core.instructor import Cortex, Interpreter, Moulder
from core.message import Essence, Resource, Belief, Feature, \
                         Buzz, Direction, MessageOperator
from core.scaffold_map import universal_map_maker, MapCollection 

from core.helper_funcs import sigmoid_10

import numpy as np

STRICT_ENGINE = True

class Unit(Agent):
    '''Bla bla

    '''
    def _cmp_frac_gulp(self, x_val):
        '''Bla bla

        '''
        return sigmoid_10(self.essence['max_gulp'],
                          self.essence['midpoint_gulp'],
                          False, x_val)

    def _cmp_frac_share(self, x_val):
        '''Bla bla

        '''
        return sigmoid_10(self.essence['max_share'],
                          self.essence['midpoint_share'],
                          False, x_val)

    def _cmp_frac_lies(self, x_val):
        '''Bla bla

        '''
        return sigmoid_10(self.essence['max_tox'],
                          self.essence['midpoint_tox'],
                          True, x_val)

    def _cmp_cooperative_feature(self):
        '''Compute a surface feature based on cooperative nature of agent

        '''
        ff = self._cmp_frac_share(1.0)
        rando = np.random.uniform()
        ff = self.essence['truthful_reveal'] * ff + \
             (1.0 - self.essence['truthful_reveal']) * rando

        return ff

    def _cmp_cooperative_feature2(self):
        '''Bla bla

        '''
        f1 = self._cmp_frac_share(1.0)
        f2 = min(1.0, max(0.0, 1.0 - self.essence['midpoint_share']))
        rando = np.random.uniform()

        pheno = self.essence['truthful_reveal'] * f1 * f2 + \
                (1.0 - self.essence['truthful_reveal']) * rando

        return pheno

    def _cmp_friendly_env(self, revealed_coop, current_belief):
        '''Update belief about environment friendliness

        '''
        if revealed_coop is None:
            return current_belief

        new_belief = self.essence['inv_forget_rate'] * current_belief + \
                     (1.0 - self.essence['inv_forget_rate']) * revealed_coop

        return new_belief

    def _cmp_share_resources(self, belief_coop, 
                             info_a, info_b, info_c):
        '''Compute amount of resources to share with neighbouring environment

        '''
        ff = self._cmp_frac_share(belief_coop)

        d_a = ff * info_a
        d_b = ff * info_b
        d_c = ff * info_c

        return d_a, d_b, d_c

    def _cmp_gulp_fraction(self, belief_coop):
        '''Compute fraction of environment to gulp up

        '''
        ff = self._cmp_frac_gulp(belief_coop)

        return ff

    def _cmp_lies_ejection(self, belief_coop,
                           info_a, info_b, info_c):
        '''Make info into lies

        '''
        ff = self._cmp_frac_lies(belief_coop)

        info_limit = min(info_a, min(info_b, info_c))
        lies = 3.0 * ff * info_limit 

        return lies

    def _cmp_offspring(self):
        '''Generate offspring through division

        '''
        offspring_agent = self.deepcopy()
        offspring_agent.name = 'offspring'

        self.essence_map_reset.set_values(self.essence.values())
        self.essence_map_reset.apply_to(offspring_agent)

        self.resource_reset.set_values(self.resource.values()) 
        self.resource_reset.apply_to(offspring_agent)
        self.resource_scale.set_values([0.5, 0.5, 0.5, 0.5])
        self.resource_scale.apply_to(offspring_agent)

        return offspring_agent, 0.5, 0.5, 0.5, 0.5

    def __init__(self, name,
                 midpoint_share=0.0, max_share=0.0,
                 midpoint_gulp=0.0, max_gulp=0.0,
                 midpoint_tox=0.0, max_tox=0.0,
                 truthful_reveal=1.0, inverse_forget_rate=0.5,
                 agent_id=None):

        super().__init__(name, agent_id_system=agent_id, strict_engine=STRICT_ENGINE)

        #
        # Essence
        unit_essence = Essence('Exterior Disposition',
                               ('midpoint_share', 'max_share',
                                'midpoint_gulp', 'max_gulp',
                                'midpoint_tox', 'max_tox',
                                'truthful_reveal', 'inv_forget_rate'))
        unit_essence.set_values([midpoint_share, max_share, 
                                 midpoint_gulp, max_gulp,
                                 midpoint_tox, max_tox,
                                 truthful_reveal, inverse_forget_rate])
        self.set_scaffold(unit_essence)

        # Essence reset map, convenience function for offspring creation
        self.essence_map_reset = universal_map_maker(unit_essence, 'reset', ('value',))

        #
        # Resource
        unit_resource = Resource('Internal Resources',
                                 ('info_a', 'info_b', 'info_c',
                                  'bad_info'))
        unit_resource.set_values([0.0, 0.0, 0.0, 0.0])
        self.set_scaffold(unit_resource)

        # Resource reset and scale map, convenience function for offspring creation
        self.resource_reset = universal_map_maker(unit_resource, 'reset', ('value',))
        self.resource_scale = universal_map_maker(unit_resource, 'scale', ('value',))

        # Resource operator only relating to info resource, not toxin
        unit_resource_info = MessageOperator(unit_resource, 
                                 slice_labels=['info_a', 'info_b', 'info_c'])

        #
        # Belief
        unit_belief = Belief('Surrounding', ('cooperative_env',))
        unit_belief.set_values([0.0])
        self.set_message(unit_belief)

        #
        # Interpreters
        buzz = Buzz('Neighbour Cooperator', ('revealed_coop',))
        self.set_message(buzz)
        interpreter = Interpreter('Friendly Environment', 
                                  self._cmp_friendly_env,
                                  buzz,
                                  unit_belief,
                                  belief_updater=True)
        self.set_organ(interpreter)

        #
        # Moulders
        direction = Direction('Resources to Share', 
                              ('d_info_a', 'd_info_b', 'd_info_c'))
        moulder = Moulder('Share Resources', self._cmp_share_resources,
                          unit_belief, 
                          direction,
                          resource_op_input=unit_resource_info)
        self.set_organ(moulder)

        direction = Direction('Fraction to Gulp', ('f_gulp',))
        moulder = Moulder('Gulp from Env', self._cmp_gulp_fraction,
                          unit_belief,
                          direction)
        self.set_organ(moulder)

        split_resource = universal_map_maker(self.resource, 'scale', ('factor',))
        direction = Direction('Offspring', ('agent_split',))
        moulder = Moulder('Create Agent Offspring', self._cmp_offspring,
                          None, 
                          direction,
                          resource_map_output=split_resource)
        self.set_organ(moulder)

        direction = Direction('Lies to Eject', ('amount',))
        moulder = Moulder('Eject Lies', self._cmp_lies_ejection,
                          unit_belief,
                          direction,
                          resource_op_input=unit_resource_info)
        self.set_organ(moulder)

        #
        # Cortex
        coop_expose = Feature('Cooperative Reveal',
                              ('coop_with_coop',))
        cortex = Cortex('Reveal Cooperation', self._cmp_cooperative_feature2,
                        None, coop_expose)
        self.set_organ(cortex)

class AgentAuxEnv(object):

    def decay(self):
        '''Bla bla

        '''
        ret = {}
        for resource_type, resource_amount in self.container.items():
            resource_amount_new = self.inverse_rate * resource_amount
            ret[resource_type] = resource_amount_new

        self.container = ret

    def __init__(self, info_a, info_b, info_c, bad_info, inverse_rate):

        self.container = {'info_a' : info_a, 'info_b' : info_b,
                          'info_c' : info_c, 'bad_info' : bad_info}
        self.inverse_rate = inverse_rate
