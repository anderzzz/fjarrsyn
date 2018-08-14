'''Specific objects, agents included, for the infection scenario

'''
import logging

from core.helper_funcs import sigmoid_10
from core.agent import Agent
from core.organs import Interpreter, Moulder, Cortex
from core.naturallaw import ObjectMapCollection, ObjectMapManyMany
from infection.bacteria_brain import BacteriaBrain

#def pretty_print(dd):
#    l = ['(%s : %s)' %(key, str(dd[key])) for key in sorted(dd.keys())]
#    j = ' ; '.join(l)
#    return j

class Bacteria(Agent):
    '''Bla bla

    '''
    def _derive_surface_profile(self, generosity, generosity_mag, profile_length):
        '''Bla bla

        '''
        share_fraction_identical = sigmoid_10(generosity_mag, 1.0 - generosity, False, 1.0)
        n_chars = int(round(profile_length * share_fraction_identical))
        profile = ['w'] * (profile_length - n_chars) + ['a'] * (n_chars)

        return [''.join(profile)]

    def _tickle_surface_profile(self):
        '''Bla bla

        '''
        return self.scaffold['surface_profile']

    def __call__(self):
        '''The executive function of the bacteria agent wherein it executes a
        plan and experiences an object force

        '''
        self.derived_scaffold(self)
#        logging.debug('----> AGENT ID: %s' %(self.agent_id_system))
#        logging.debug('Scaffold upon entry')
#        logging.debug(pretty_print(self.scaffold))
        # Ascertain if there is a neighbour and how similar it is
        self.perceive('neighbour_surface', 'generous_hood')
        if not self.belief['neighbour_id'] is None:
#            logging.debug('Belief after sensing neighbourhood')
#            logging.debug(pretty_print(self.belief))

            if self.scaffold['share_generally']:
                self.engage('share_molecules')
            else:
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

        #
        # Initialize the scaffold scalar values
        #
        self.set_imprint_bulk('scaffold', scaffold_init)

        #
        # Add constraing force for derived scaffold scalars
        #
        self.derived_scaffold = ObjectMapManyMany(['generosity', 'generosity_mag'],
                                             ['surface_profile'])
        self.derived_scaffold.set_func(self._derive_surface_profile,
                        {'profile_length' : self.scaffold['profile_length']})
        self.derived_scaffold(self)

        #
        # Add cortex organs
        #
        cortex = Cortex('surface_signal', 
                        'surface_profile',
                        self._tickle_surface_profile)
        self.set_organ(cortex)
        
        #
        # Add organs part of the executive function
        #
        brain = BacteriaBrain(self.scaffold, self.belief)

        #
        # Interpret the buzz from sensing a neighbour's surface profile
        #
        interpreter = Interpreter('similar_hood', 
                                  ['surface_profile', 'neighbour_id'],
                                  brain._interpret_selfsimilarity_neighbourhood)
        self.set_organ(interpreter)

        interpreter = Interpreter('generous_hood', 
                                  ['surface_profile', 'neighbour_id'],
                                  brain._interpret_generosity_neighbourhood)
        self.set_organ(interpreter)

        #
        # Mould the action to share molecules with all neighbour environments.
        # This induces a scaffold force
        #
        scaffold_force = ObjectMapCollection(['molecule_A', 'molecule_B', 
                                              'molecule_C', 'poison_vacuole'], 
                                              standard_funcs=True)
        moulder = Moulder('share_molecules',
                          ['neighbour_generous', 'neighbour_id'],
                          brain._mould_supply_molecules_to_env,
                          {'induction' : scaffold_force})
        self.set_organ(moulder)

        #
        # Mould the action to share molecules with a specified environment.
        # This induces a scaffold force
        #
        scaffold_force = ObjectMapCollection(['molecule_A', 'molecule_B', 
                                              'molecule_C', 'poison_vacuole'], 
                                              standard_funcs=True)
        moulder = Moulder('share_molecules_one',
                          ['neighbour_generous', 'neighbour_id'],
                          brain._mould_supply_molecules_to_one,
                          {'induction' : scaffold_force})
        self.set_organ(moulder)

        #
        # Mould the action of agent killing itself
        #
        moulder = Moulder('contemplate_suicide', 
                          [],
                          brain._mould_contemplate_suicide)
        self.set_organ(moulder)

        #
        # Mould the action to gulp a fraction of the environment. This induces
        # no scaffold force, rather changes to scaffold follows as a reaction
        # from the corresponding actuator
        #
        moulder = Moulder('gulp_environment', 
                          ['neighbour_generous'],
                          brain._mould_gulp_molecules_from_env)
        self.set_organ(moulder)

        #
        # Mould the internal change of creating poison. This populates no
        # actuator, rather it only induces a scaffold force
        #
        scaffold_force = ObjectMapCollection(['molecule_A', 'molecule_B', 
                                              'molecule_C', 'poison_vacuole'], 
                                              standard_funcs=True)
        moulder = Moulder('make_poison',
                          [],
                          brain._mould_make_poison,
                          {'induction' : scaffold_force})
        self.set_organ(moulder)

        #
        # Mould the splitting of the agent in two identical agents. This
        # induces a scaffold force
        #
        scaffold_force = ObjectMapCollection(['molecule_A', 'molecule_B', 
                                              'molecule_C', 'poison_vacuole',
                                              'poison'], 
                                              standard_funcs=True)
        moulder = Moulder('split_in_two',
                          [],
                          brain._mould_cell_division,
                          {'induction' : scaffold_force})
        self.set_organ(moulder)
        
class ExtracellEnvironment(object):
    '''Bla bla

    '''
    def __init__(self, name, scaffold_init):

        self.name = name 
        self.scaffold = scaffold_init
