
class Propagator(object):
    '''Bla bla

    '''
    def __call__(self, system):
        '''Bla bla

        '''
        n_agents = len(system)
        for agent, aux_content in system.shuffle_iter(n_agents):
            
            agent()

            if agent.inert:
                del system[agent.agent_id_system]

            system.engage_all_verbs(agent)

    def __init__(self):

        pass

