'''Unit and World propagation code

'''
from core.policy import Plan, Clause, AutoResourceCondition, Heartbeat

class UnitPolicy(object):
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
        return bad_info > self.thrs_bad_info_death 
        
    def __init__(self, name, thrs_info_to_split, thrs_bad_info_death):

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

        clausul_3b = Clause('Breed',
                            [('mould', 'Create Agent Offspring'),
                             ('act', 'Push Offspring Onto World')])

        clausul_4 = Clause('Eject To Env',
                           [('mould', 'Resources to Share'),
                            ('act', 'Share Resources to Neighbours'),
                            ('mould', 'Eject Lies'),
                            ('act', 'Spread Lies to Neighbours')])

        heartbeat = Heartbeat('Death by Bad Info', death_by_bad_info)

        the_plan = Plan(name)
        k_0 = the_plan.add_cargo('pronounce', 'Figure Out Env')
        k_1 = the_plan.add_cargo('pronounce', 'Collect From Env')
        k_2 = the_plan.add_cargo('pump', 'Death by Bad Info')
        k_3 = the_plan.add_cargo('pump', 'Death by Bad Info')
        k_4 = the_plan.add_cargo('pronounce', 'Breed')
        k_5 = the_plan.add_cargo('pronounce', 'Eject To Env')
        k_6 = the_plan.add_cargo('pronounce', 'Eject To Env')

        the_plan.add_dependency(k_0, k_1)
        the_plan.add_dependency(k_1, k_4, k_2)
        the_plan.add_dependency(k_4, k_3)
        the_plan.add_dependency(k_3, k_5)
        the_plan.add_dependency(k_2, k_6)

        the_plan.stamp_and_approve()

        self.all = (the_plan, clausul_1, clausul_2, clausul_3b,
                    clausul_4, heartbeat)

def system_propagator(system, plan_name):
    
    system.cleanse_inert()

    n_nodes = system.get_n_nodes()
    for node in system.shuffle_nodes(False, n_nodes, False):
        if not node.agent_content is None:
            node.agent_content.enact(plan_name)
            system.engage_all_verbs(node.agent_content)

        node.aux_content.decay()
