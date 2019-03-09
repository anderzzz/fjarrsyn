'''Agent unit

'''
from core.agent import Agent

from core.instructor import Cortex
from core.message import Essence, Resource, Belief, Feature, MessageOperator

from core.helper_funcs import sigmoid_10

import numpy as np

STRICT_ENGINE = True

class Unit(Agent):
    '''Bla bla

    '''
    def _cmp_frac_share(self, x_val):
        '''Bla bla

        '''
        return sigmoid_10(self.essence['max_share'],
                          self.essence['midpoint_share'],
                          False, x_val)

    def _cmp_cooperative_feature(self, midpoint_share, max_share, truthfulness):
        '''Compute a surface feature based on cooperative nature of agent

        '''
        ff = self._cmp_frac_share(1.0)
        rando = np.random.uniform()
        ff = truthfulness * ff + (1.0 - truthfulness) * rando

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
        slicer_of_essence = MessageOperator(unit_essence, 
                               slice_labels=['midpoint_share', 'max_share'])

        #
        # Resource
        unit_resource = Resource('Internal Resources',
                                 ('info_a', 'info_b', 'info_c',
                                  'toxic'))
        unit_resource.set_values([0.0, 0.0, 0.0, 0.0])
        self.set_scaffold(unit_resource)

        #
        # Belief
        unit_belief = Belief('Surrounding', ('cooperative_env',))
        unit_belief.set_values([1.0])
        self.set_message(unit_belief)

        #
        # Interpreters

        #
        # Moulders

        #
        # Cortex
        coop_expose = Feature('Cooperative Reveal',
                              ('coop_with_coop',))
        cortex = Cortex('Reveal Cooperation', self._cmp_cooperative_feature,
                        slicer_of_essence, coop_expose,
                        cortex_func_kwargs={'truthfulness' : 1.0})
        self.set_organ(cortex)
