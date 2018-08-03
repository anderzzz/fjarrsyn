'''Bla bla

'''
import csv

class FiniteSystemRunner(object):
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

    def write_graph_state(self, system):
        '''Bla bla

        '''
        pass

    def time_to_sample(self, k_iter):
        '''Bla bla

        '''
        if self.n_sample_steps < 0:
            return False
        else:
            return (k_iter % self.n_sample_steps) == 0

    def __call__(self, system):
        '''Bla bla

        '''
        for k_iter in range(self.n_iter):

            self.propagate_(system, **self.propagate_kwargs)

            if self.time_to_sample(k_iter):
                self.write_state_of_(system)

    def __init__(self, n_iter, 
                 n_sample_steps=-1, sample_file_name='sample.csv',
                 imprints_sample=[], 
                 graph_file_name='graph.csv', 
                 system_propagator=None, system_propagator_kwargs={}):

        self.n_iter = n_iter
        self.n_sample_steps = n_sample_steps

        self.sample_file_name = sample_file_name
        self.graph_file_name = graph_file_name
        self.write_count = 0
        if not self.n_sample_steps < 0:
            self.file_handle = open(self.sample_file_name, 'w')
            fieldnames = ['agent_id'] + ['write_count'] + imprints_sample
            self.writer = csv.DictWriter(self.file_handle, 
                                         fieldnames=fieldnames,
                                         extrasaction='ignore')
            self.writer.writeheader()

            self.graph_handle = open(self.graph_file_name, 'w')
            # ADD GRAPH CSV PRINTER

        self.propagate_ = system_propagator
        self.propagate_kwargs = system_propagator_kwargs
