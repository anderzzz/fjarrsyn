'''Bla bla

'''
from core.helper_funcs import sigmoid_10
from core.agent import Agent
from core.organs import Interpreter, Moulder, Cortex
from infection.bacteria_brain import BacteriaBrain

class Bacteria(Agent):
    '''Bla bla

    '''
    def _tickle_surface_profile(self):
        '''Bla bla

        '''
        return self.scaffold['surface_profile']

    def __call__(self):
        '''The executive function of the bacteria agent wherein it executes a
        plan and returns actuators to the caller

        Returns
        -------
        actuators : list
            List of actuators to be executed in the World in order to become
            actions

        '''
        return_actuator_names = []

        buzz_1 = self.sense('neighbour_surface')
        self.interpret('similar_hood', buzz_1)

        if self.belief['my_neighbour'] is None:
            # ADD OBJECTFORCE
            pass
        
        else:
            self.mould('share_molecules')
            print ('abc1')
            self.act('share_molecules')
            print ('abc2')

        return return_actuator_names
        
    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_data('scaffold', 'surface_profile', surface_profile)
        self.set_data('scaffold', 'molecule_A', molecules[0])
        self.set_data('scaffold', 'molecule_B', molecules[1])
        self.set_data('scaffold', 'molecule_C', molecules[2])
        self.set_data('scaffold', 'poison', molecules[3])
        self.set_data('scaffold', 'generosity', 0.5)
        self.set_data('scaffold', 'attacker', 0.5)
        self.set_data('scaffold', 'generosity_mag', 0.5)
        self.set_data('scaffold', 'attack_mag', 0.5)

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

class ExtracellEnvironment(object):
    '''Bla bla

    '''
    def __init__(self, name, molecules):

        self.name = name 
        self.molecule_content = molecules
