'''Bla bla

'''
import csv

class Runner(object):
    '''Bla bla

    '''
    def write_state_of_(self, system):
        '''Bla bla

        '''
        for agent_id, agent in system.agents_in_scope.items(): 
            pass

    def time_to_sample(self, k_iter):
        '''Bla bla

        '''
        return (k_iter % self.n_sample_steps) == 0

    def __init__(self, n_iter, n_sample_steps, sample_file_name,
                 imprints_sample):

        self.n_iter = n_iter
        self.n_sample_steps = n_sample_steps

        self.sample_file_name = sample_file_name
        self.file_handle = open(self.sample_file_name, 'w')
        self.writer = csv.DictWrite(self.file_handle, 
                                    fieldnames=XX,
                                    extrasaction='ignore')
