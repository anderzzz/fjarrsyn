'''Bla bla

'''
from core.agent import EngagedAgent

class Bacteria(EngagedAgent):
    '''Bla bla

    '''
    def _request_surface_profile(self):
        '''Bla bla

        '''
        return self.scaffold['surface_profile']

    def _execute_probe_surrounding(self) 

    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_data('scaffold', 'surface_profile', surface_profile)
        self.set_organ('service', 'reveal_surface_profile', self._request_surface_profile)
        self.set_data('scaffold', 'molecule_A', molecules[0])
        self.set_data('scaffold', 'molecule_B', molecules[1])
        self.set_data('scaffold', 'molecule_C', molecules[2])
        self.set_data('scaffold', 'molecule_D', molecules[3])

#        self.set_organ('plan', 'react_to_neighbour', self._execute_react_neighbour)
        self.set_organ('plan', 'probe_surrounding', self._execute_probe_surrounding)
#        self.set_organ('plan', 'split_off_child', self._execute_split_child)

class ExtracellEnvironment(PassiveAgent):
    '''Bla bla

    '''
    def __init__(self, name, natures_init):

        super().__init__(name)

        for nature_key, nature_value in natures_init.items():
            self.set_data('scaffold', nature_key, nature_value)
