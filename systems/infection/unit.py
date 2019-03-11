'''Agent unit

'''
from core.agent import Agent

from core.instructor import Cortex, Interpreter, Moulder
from core.message import Essence, Resource, Belief, Feature, \
                         Buzz, Direction, MessageOperator
from core.scaffold_map import ResourceMap, MapCollection

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

    def _cmp_cooperative_feature(self, truthfulness):
        '''Compute a surface feature based on cooperative nature of agent

        '''
        ff = self._cmp_frac_share(1.0)
        rando = np.random.uniform()
        ff = truthfulness * ff + (1.0 - truthfulness) * rando

        return ff

    def _cmp_friendly_env(self, revealed_coop, current_belief):
        '''Update belief about environment friendliness

        '''
        if revealed_coop is None:
            return current_belief

        new_belief = 0.5 * current_belief + 0.5 * revealed_coop

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

    def __init__(self, name, 
                 midpoint_share, max_share,
                 midpoint_gulp, max_gulp,
                 midpoint_tox, max_tox):

        super().__init__(name, STRICT_ENGINE)

        #
        # Essence
        unit_essence = Essence('Exterior Disposition',
                               ('midpoint_share', 'max_share',
                                'midpoint_gulp', 'max_gulp',
                                'midpoint_tox', 'max_tox'))
        unit_essence.set_values([midpoint_share, max_share, 
                                 midpoint_gulp, max_gulp,
                                 midpoint_tox, max_tox])
        self.set_scaffold(unit_essence)
        slicer1_of_essence = MessageOperator(unit_essence, 
                               slice_labels=['midpoint_share', 'max_share'])

        #
        # Resource
        unit_resource = Resource('Internal Resources',
                                 ('info_a', 'info_b', 'info_c',
                                  'toxic'))
        unit_resource.set_values([0.0, 0.0, 0.0, 0.0])
        self.set_scaffold(unit_resource)
        unit_resource_info = MessageOperator(unit_resource, 
                                 slice_labels=['info_a', 'info_b', 'info_c'])

        #
        # Belief
        unit_belief = Belief('Surrounding', ('cooperative_env',))
        unit_belief.set_values([1.0])
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

        #
        # Cortex
        coop_expose = Feature('Cooperative Reveal',
                              ('coop_with_coop',))
        cortex = Cortex('Reveal Cooperation', self._cmp_cooperative_feature,
                        None, coop_expose,
                        cortex_func_kwargs={'truthfulness' : 1.0})
        self.set_organ(cortex)

class AgentAuxEnv(object):

    def __init__(self, info_a, info_b, info_c, toxin):

        self.container = {'info_a' : info_a, 'info_b' : info_b,
                          'info_c' : info_c, 'toxin' : toxin}

