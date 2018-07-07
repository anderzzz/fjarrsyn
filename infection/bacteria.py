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

    def __init__(self, name, surface_profile):

        super().__init__(name)

        self.set_nature('surface_profile', surface_profile)
        self.set_service('reveal_surface_profile', self._request_surface_profile)

