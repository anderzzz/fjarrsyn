'''Bla bla

'''
from simulator.runner import Runner

class BeakerSimulator(Runner):
    '''Bla bla

    '''
    def __call__(self, system):
        '''Bla bla

        '''
        for k_iter in range(self.n_iter):

            for agent, aux_object in system:

                if agent is None:
                    continue

                else:
                    agent_survived = agent()

                if agent_survived:
                    self.agent_mutator(agent)

            for agent, aux_object in system:

                self.aux_objectforce(aux_object) 

            if self.time_to_sample(k_iter):
                self.write_state_of_(system)

    def __init__(self, n_iter, n_sample_steps, sample_file_name, agent_mutator, aux_objectforce):

        super.__init__(n_iter, n_sample_steps, sample_file_name)



