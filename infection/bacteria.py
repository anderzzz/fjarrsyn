'''Specific objects, agents included, for the infection scenario

'''
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
        plan and experiences an object force

        '''
        # Ascertain if there is a neighbour and how similar it is
        self.perceive('neighbour_surface', 'similar_hood')
        if not self.belief['my_neighbour'] is None:
            self.engage('share_molecules')

        # Gulp molecules from the nearby environment
        self.engage('gulp_environment')

        # Contemplate suicide
        self.engage('contemplate_suicide')
        if not self.hooked_up():
            return None

        # Make poison. Internal action only, hence no actuator employed
        self.mould('make_poison')

        # Determine if to split in two
        self.engage('split_in_two')

    def __init__(self, name, surface_profile, molecules):

        super().__init__(name)

        self.set_imprint('scaffold', 'surface_profile', surface_profile)
        self.set_imprint('scaffold', 'molecule_A', molecules[0])
        self.set_imprint('scaffold', 'molecule_B', molecules[1])
        self.set_imprint('scaffold', 'molecule_C', molecules[2])
        self.set_imprint('scaffold', 'poison', molecules[3])
        self.set_imprint('scaffold', 'poison_vacuole', molecules[4])
        self.set_imprint('scaffold', 'poison_vacuole_max', 0.2)
        self.set_imprint('scaffold', 'generosity', 0.5)
        self.set_imprint('scaffold', 'attacker', 0.5)
        self.set_imprint('scaffold', 'generosity_mag', 0.5)
        self.set_imprint('scaffold', 'attack_mag', 0.5)
        self.set_imprint('scaffold', 'vulnerability_to_poison', 2.0)
        self.set_imprint('scaffold', 'trusting', 0.5)
        self.set_imprint('scaffold', 'trusting_mag', 0.5)
        self.set_imprint('scaffold', 'split_thrs', 0.9)

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

        moulder = Moulder('contemplate_suicide', 
                          [],
                          brain._mould_contemplate_suicide)
        self.set_organ(moulder)

        moulder = Moulder('gulp_environment', 
                          ['my_neighbour'],
                          brain._mould_gulp_molecules_from_env)
        self.set_organ(moulder)

        moulder = Moulder('make_poison',
                          [],
                          brain._mould_make_poison)
        self.set_organ(moulder)

        moulder = Moulder('split_in_two',
                          [],
                          brain._mould_cell_division)
        self.set_organ(moulder)

class ExtracellEnvironment(object):
    '''Bla bla

    '''
    def __init__(self, name, molecules):

        self.name = name 
        self.molecule_content = molecules
