'''Bla bla

'''
import csv

class AgentSystemIO(object):
    '''Bla bla

    '''
    def flatten_imprint(self, imprint):
        '''Rename imprint data by merging scaffold and beliefs with their
        respective labels. Typical label can be `scaffold_money`.

        Parameters
        ----------
        imprint : dict
            The imprint of an agent

        Returns
        -------
        flat_imprint : dict
            The dictionary where keys have been flattened

        '''
        flat_imprint = {}
        for imprint_type, imprint_data in imprint.items():
            for unit_name, unit_value in imprint_data.items():
                key_union = imprint_type + '_' + unit_name
                flat_imprint[key_union] = unit_value

        return flat_imprint

    def write_state_of_(self, system, write_count):
        '''Write the agent states of the system

        Parameters
        ----------
        system
            The agent management system

        '''
        for agent_id, agent in system.agents_in_scope.items(): 
            data_dict = self.flatten_imprint(agent.imprint)
            data_dict['agent_id'] = agent_id
            data_dict['generation_count'] = str(write_count)
            
            self.writer.writerow(data_dict)

    def flush(self):
        '''Bla bla

        '''
        self.file_handle.flush()

    def __init__(self, file_name, file_format, imprints_sample):

        fieldnames = ['agent_id'] + ['generation_count'] + imprints_sample

        self.file_handle = open(file_name, 'w')

        if file_format == 'csv':
            self.writer = csv.DictWriter(self.file_handle,
                                         fieldnames=fieldnames,
                                         extrasaction='ignore')
            self.writer.writeheader()

        else:
            raise ValueError('Unknown agent system file format: %s' %(file_format))
