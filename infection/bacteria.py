'''Specific objects, agents included, for the infection scenario

'''
import logging

from core.agent import Agent
from core.organs import Interpreter, Moulder, Cortex
from infection.bacteria_brain import BacteriaBrain

#def pretty_print(dd):
#    l = ['(%s : %s)' %(key, str(dd[key])) for key in sorted(dd.keys())]
#    j = ' ; '.join(l)
#    return j

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
#        logging.debug('----> AGENT ID: %s' %(self.agent_id_system))
#        logging.debug('Scaffold upon entry')
#        logging.debug(pretty_print(self.scaffold))
        # Ascertain if there is a neighbour and how similar it is
        self.perceive('neighbour_surface', 'similar_hood')
        if not self.belief['my_neighbour'] is None:
#            logging.debug('Belief after sensing neighbourhood')
#            logging.debug(pretty_print(self.belief))

#            self.engage('share_molecules')
            self.engage('share_molecules_one')

#        logging.debug('Scaffold after sharing')
#        logging.debug(pretty_print(self.scaffold))

        # Gulp molecules from the nearby environment
        self.engage('gulp_environment')
#        logging.debug('Scaffold after gulping')
#        logging.debug(pretty_print(self.scaffold))

        # Contemplate suicide
        self.engage('contemplate_suicide')
        if not self.hooked_up():
#            logging.debug('Agent death')
            return False

        # Make poison. Internal action only, hence no actuator employed
        self.mould('make_poison')
#        logging.debug('Scaffold after making poison')
#        logging.debug(pretty_print(self.scaffold))

        # Determine if to split in two
        self.engage('split_in_two')
#        logging.debug('Scaffold after attempted splitting')
#        logging.debug(pretty_print(self.scaffold))

        return True

    def __init__(self, name, scaffold_init):

        super().__init__(name)

        self.set_imprint_bulk('scaffold', scaffold_init)

        cortex = Cortex('surface_signal', 
                        'surface_profile',
                        self._tickle_surface_profile)
        self.set_organ(cortex)
                        
        brain = BacteriaBrain(self.scaffold, self.belief)
        interpreter = Interpreter('similar_hood', 
                                  ['surface_profile', 'neighbour_id'],
                                  brain._interpret_selfsimilarity_neighbourhood)
        self.set_organ(interpreter)

        moulder = Moulder('share_molecules',
                          ['my_neighbour', 'my_neighbour_id'],
                          brain._mould_supply_molecules_to_env)
        self.set_organ(moulder)

        moulder = Moulder('share_molecules_one',
                          ['my_neighbour', 'my_neighbour_id'],
                          brain._mould_supply_molecules_to_one)
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
    def __init__(self, name, scaffold_init):

        self.name = name 
        self.scaffold = scaffold_init
