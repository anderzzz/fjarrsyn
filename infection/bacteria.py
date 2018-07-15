'''Bla bla

'''
from core.agent import Agent
from core.organs import Interpreter, Moulder, Cortex

class BacteriaBrain(object):
    '''Bla bla

    '''
    def _interpret_selfsimilarity_neighbourhood(self, surface_profile):
        '''Bla bla

        '''
        self.belief['my_neighbour'] = None

        if not surface_profile is None:
            my_profile = self.scaffold['surface_profile']
            n_same = 0
            for char_me, char_other in zip(my_profile, surface_profile):
                if char_me == char_other:
                    n_same += 1

            frac_same = float(n_same) / float(len(my_profile))
            self.belief['my_neighbour'] = frac_same

        return ('my_neighbour',)

    def _mould_supply_molecules_to_env(self, my_neighbour):
        '''Bla bla

        '''
        # HOW TO DO THIS NOW?
        raise RuntimeError('dummy')

    def _mould_gulp_molecules_from_env(self):
        '''Bla bla

        '''
        pass

    def _mould_cell_division(self):
        '''Bla bla

        '''
        pass

    def _mould_spontaneous_growth(self):
        '''Bla bla

        '''
        pass

    def __init__(self, scaffold, belief):
        
        self.scaffold = scaffold
        self.belief = belief

class Bacteria(Agent):
    '''Bla bla

    '''
    def _tickle_surface_profile(self):
        '''Bla bla

        '''
        return self.scaffold['surface_profile']

    def __call__(self):
        '''Bla bla

        '''
        return_actuator = []

        buzz_1 = self.sense('neighbour_surface')
        self.interpret('similar_hood', buzz_1)

        if self.belief['my_neighbour'] is None:
            # ADD OBJECTFORCE
            pass
        
        else:
            actuator = self.mould('share_molecules',
                                  self.belief['my_neighbour'], 
                                  self.actuator['share_molecules'])
            return_actuator.append(actuator)

        return return_actuator
        
    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_data('scaffold', 'surface_profile', surface_profile)
        self.set_data('scaffold', 'molecule_A', molecules[0])
        self.set_data('scaffold', 'molecule_B', molecules[1])
        self.set_data('scaffold', 'molecule_C', molecules[2])
        self.set_data('scaffold', 'molecule_D', molecules[3])

        cortex = Cortex('surface_signal', 
                        'surface_profile',
                        self._tickle_surface_profile)
        self.set_organ(cortex)
                        
        brain = BacteriaBrain(self.scaffold, self.belief)
        interpreter = Interpreter('similar_hood', 
                                  ['surface_profile'],
                                  brain._interpret_selfsimilarity_neighbourhood)
        self.set_organ(interpreter)

        moulder = Moulder('share_molecules',
                          ['my_neighbour'],
                          brain._mould_supply_molecules_to_env)
        self.set_organ(moulder)

#        self.set_organ('handler', 'supply_molecules_to_env',
#                       self._handle_supply_molecules_to_env)
#        self.set_organ('handler', 'gulp_molecules_from_env',
#                       self._handle_gulp_molecules_from_env)
#        self.set_organ('handler', 'cell_division',
#                       self._handle_cell_division) 
#        self.set_organ('handler', 'spontaneous_growth',
#                       self._spontaneous_growth) 

class ExtracellEnvironment(object):
    '''Bla bla

    '''
    def __init__(self, name, molecules):

        self.name = name 
        self.molecule_content = molecules
