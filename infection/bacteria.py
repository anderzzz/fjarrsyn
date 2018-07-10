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

    def _execute_supply_molecules_to_env(self):
        '''Bla bla

        '''
        pass

    def _execute_gulp_molecules_from_env(self):
        '''Bla bla

        '''
        pass

    def _execute_cell_division(self):
        '''Bla bla

        '''
        pass

    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_data('scaffold', 'surface_profile', surface_profile)
        self.set_organ('service', 'reveal_surface_profile', self._request_surface_profile)
        self.set_data('scaffold', 'molecule_A', molecules[0])
        self.set_data('scaffold', 'molecule_B', molecules[1])
        self.set_data('scaffold', 'molecule_C', molecules[2])
        self.set_data('scaffold', 'molecule_D', molecules[3])

        self.set_organ('plan', 'supply_molecules_to_env',
                               self._execute_supply_molecules_to_env)
        self.set_organ('plan', 'gulp_molecules_from_env',
                               self._execute_gulp_molecules_from_env)
        self.set_organ('plan', 'cell_division',
                               self._execute_cell_division)

class ExtracellEnvironment(PassiveAgent):
    '''Bla bla

    '''
    def _request_molecules_scaffold(self):
        '''Bla bla

        '''
        return dict([(x, y) for x, y in self.scaffold.items() if 'molecule_' in x]
               

    def __init__(self, name, natures_init):

        super().__init__(name)

        for nature_key, nature_value in natures_init.items():
            self.set_data('scaffold', nature_key, nature_value)

        self.set_organ('service', 'how_many_molecules',
                       self._request_molecules_scaffold)
