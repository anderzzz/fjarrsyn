'''Agent unit

'''
from core.agent import Agent

from core.instructor import Cortex
from core.message import Essence, Resource, Belief

STRICT_ENGINE = True

class Unit(Agent):
    '''Bla bla

    '''

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

        #
        # Resource
        unit_resource = Resource('Internal Resources',
                                 ('info_a', 'info_b', 'info_c',
                                  'toxic'))
        unit_resource.set_values([0.0, 0.0, 0.0, 0.0])
        self.set_scaffold(unit_resource)

        #
        # Belief
        unit_belief = Belief('Surrounding', ('friendliness',))
        unit_belief.set_values([1.0])
        self.set_message(unit_belief)

        #
        # Sensor
