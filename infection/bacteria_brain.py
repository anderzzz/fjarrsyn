'''Bla bla

'''
from core.helper_funcs import sigmoid_10

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
        print (ret_env)

        ret = {'dx_molecules_poison' : ret_env}

        return ret

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
