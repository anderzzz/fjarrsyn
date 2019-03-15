'''Unit and World propagation code

'''
from core.policy import Plan, Clause, AutoResourceCondition

class UnitPlan(Plan):
    '''Bla bla

    '''
    def _resource_to_split(self, info_a, info_b, info_c):
        '''Bla bla

        '''
        if info_a > self.thrs_info_to_split and \
           info_b > self.thrs_info_to_split and \
           info_c > self.thrs_info_to_split:
            
            return True

        else:
            return False

    def _death_test(self, bad_info):
        '''Bla bla

        '''
        pass
        
    def __init__(self, name, thrs_info_to_split, thrs_bad_info_death):

        super().__init__(name)

        self.thrs_info_to_split = thrs_info_to_split
        self.thrs_bad_info_death = thrs_bad_info_death

        split_offspring = AutoResourceCondition('Can Split Offspring?',
                              self._resource_to_split,
                              resource_keys=['info_a', 'info_b', 'info_c'])
        death_by_bad_info = AutoResourceCondition('Too Much Bad Info?',
                                self._death_test,
                                resource_keys=['bad_info'])

        clausul_1 = Clause('Figure Out Env',
                           [('sense', 'Feel Neighbour Surface'),
                            ('interpret', 'Friendly Environment')])

        clausul_2 = Clause('Collect From Env',
                           [('mould', 'Gulp from Env'),
                            ('act', 'Gulp Environment')],
                           condition=split_offspring)

        clausul_3a = Clause('Death',
                            condition=death_by_bad_info)

        clausul_3b = Clause('Breed',
                            [('mould', 'Create Agent Offspring'),
                             ('act', 'Push Offspring Onto World')])

        clausul_4 = Clause('Eject To Env',
                           [('mould', 'Resources to Share'),
                            ('act', 'Share Resources to Neighbours'),
                            ('mould', 'Eject Lies'),
                            ('act', 'Spread Lies to Neighbours')])


