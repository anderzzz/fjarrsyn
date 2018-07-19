'''Bla bla

'''
from core.helper_funcs import sigmoid_10
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
        share_percentage = sigmoid_10(self.scaffold['generosity_mag'], 
                                      self.scaffold['generosity'], False, 
                                      my_neighbour)
        poison_percentage = sigmoid_10(self.scaffold['attack_mag'],
                                       self.scaffold['attacker'], True,
                                       my_neighbour)
        
        ret_env = {}
        key_molecule = [key for key in self.scaffold if 'molecule_' in key]
        for molecule in key_molecule:
            current_amount = self.scaffold[molecule]
            dx_amount = share_percentage * current_amount
            ret_env[molecule] = dx_amount
            left_over = current_amount - dx_amount
            self.scaffold[molecule] = left_over

        current_amount = self.scaffold['poison']
        dx_amount = poison_percentage * current_amount
        ret_env['poison'] = dx_amount
        left_over = current_amount - dx_amount
        self.scaffold['poison'] = left_over

        return ret_env

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
        '''The executive function of the bacteria agent wherein it executes a
        plan and returns actuators to the caller

        Returns
        -------
        actuators : list
            List of actuators to be executed in the World in order to become
            actions

        '''
        return_actuator = []

        buzz_1 = self.sense('neighbour_surface')
        self.interpret('similar_hood', buzz_1)

        if self.belief['my_neighbour'] is None:
            # ADD OBJECTFORCE
            pass
        
        else:
            print ('aaa1')
            actuator = self.mould('share_molecules')
            print ('aaa2')
            return_actuator.append(actuator)

        return return_actuator
        
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
