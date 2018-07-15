'''Bla bla

'''
from core.agent import Agent
from core.organ import Interpreter

class Bacteria(Agent):
    '''Bla bla

    '''
    def _request_surface_profile(self):
        '''Bla bla

        '''
        return self.scaffold['surface_profile']

    def _interpret_selfsimilarity_neighbourhood(self):
        '''Bla bla

        '''
        self.belief['selfsimilarity_neighbourhood'] = None

        if not surface_profile[0] is None:
            my_profile = self.scaffold['surface_profile']
            for char_me, char_other in zip(my_profile, surface_profile):
                if char_me == char_other:
                    n_same += 1

            frac_same = float(n_same) / float(len(my_profile))
            self.belief['my_neighbour'] = frac_same

        return ('my_neighbour')

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
        buzz_1 = self.sense('neighbour_surface')
        self.interpret(buzz_1)
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

        interpreter = Interpreter('similar_hood', 
                                  ['surface_profile'],
                                  self._interpret_selfsimilarity_neighbourhood)
        self.set_organ(interpreter)

        self.set_organ('interpreter', 'selfsimilarity_neighbourhood', 
                       self._interpret_selfsimilarity_neighbourhood)
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
