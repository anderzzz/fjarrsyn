'''Bla bla

'''
from core.agent import Agent

class Bacteria(Agent):
    '''Bla bla

    '''
    def _request_surface_profile(self):
        '''Bla bla

        '''
        return self.scaffold['surface_profile']

    def _interpret_random_neighbour(self):
        '''Bla bla

        '''
        # USE SENSOR THEN MAP BELIEF OF FRIEND OR FOE
        pass

    def _handle_supply_molecules_to_env(self):
        '''Bla bla

        '''
        pass

    def _handle_gulp_molecules_from_env(self):
        '''Bla bla

        '''
        pass

    def _handle_cell_division(self):
        '''Bla bla

        '''
        pass

    def _handle_spontaneous_growth(self):
        '''Bla bla

        '''
        pass

    def __call__(self):
        '''Bla bla

        '''
        # HERE PLAN IS EXECUTED. HIERARCHY OF PLANS?
        pass

    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_data('scaffold', 'surface_profile', surface_profile)
        self.set_organ('service', 'reveal_surface_profile', self._request_surface_profile)
        self.set_data('scaffold', 'molecule_A', molecules[0])
        self.set_data('scaffold', 'molecule_B', molecules[1])
        self.set_data('scaffold', 'molecule_C', molecules[2])
        self.set_data('scaffold', 'molecule_D', molecules[3])

        self.set_organ('interpreter', 'random_neighbour', 
                       self._interpret_random_neighbour)
        self.set_organ('handler', 'supply_molecules_to_env',
                       self._handle_supply_molecules_to_env)
        self.set_organ('handler', 'gulp_molecules_from_env',
                       self._handle_gulp_molecules_from_env)
        self.set_organ('handler', 'cell_division',
                       self._handle_cell_division) 
        self.set_organ('handler', 'spontaneous_growth',
                       self._spontaneous_growth) 

class ExtracellEnvironment(object):
    '''Bla bla

    '''
    def __init__(self, name, molecules):

        self.name = name 
        self.molecule_content = molecules
