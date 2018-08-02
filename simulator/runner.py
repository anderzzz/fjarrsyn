'''Bla bla

'''
import csv

class Runner(object):
    '''Bla bla

    '''
    def flatten_imprint(self, imprint):
        '''Bla bla

        '''
        ret = {}
        for imprint_type, imprint_data in imprint.items():
            for unit_name, unit_value in imprint_data.items():
                key_union = imprint_type + '_' + unit_name
                ret[key_union] = unit_value

        return ret

    def write_state_of_(self, system):
        '''Bla bla

        '''
        for agent_id, agent in system.agents_in_scope.items(): 
            data_dict = self.flatten_imprint(agent.imprint)
            data_dict['agent_id'] = agent_id
            data_dict['write_count'] = str(self.write_count)
            
            self.writer.writerow(data_dict)

        self.write_count += 1

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
        fieldnames = ['agent_id'] + ['write_count'] + imprints_sample
        self.writer = csv.DictWriter(self.file_handle, 
                                     fieldnames=fieldnames,
                                     extrasaction='ignore')
        self.writer.writeheader()
        self.write_count = 0
