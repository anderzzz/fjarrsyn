'''Bla bla

'''
from core.agent import Agent

class Bacteria(Agent):
    '''Bla bla

    '''
    def _request_surface_profile(self):
        '''Bla bla

        '''
        return self.nature['surface_profile']

    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_nature('surface_profile', surface_profile)
        self.set_service('reveal_surface_profile', self._request_surface_profile)
        self.set_nature('molecule_A', molecules[0])
        self.set_nature('molecule_B', molecules[1])
        self.set_nature('molecule_C', molecules[2])
        self.set_nature('molecule_D', molecules[3])

class ExtracellEnvironment(Agent):
    '''Bla bla

    '''
    def __init__(self, name, natures_init):

        super().__init__(name)

        for nature_key, nature_value in natures_init.items():
            self.set_nature(nature_key, nature_value)
