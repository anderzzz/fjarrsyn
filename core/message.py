'''All flash classes of the basic Agent are contained in this file.

'''
from collections import Iterable

class _Message(object):

    def set_elements(self, value_container):
        '''Bla bla

        '''
        if self.n_elements > 1:
            if not isinstance(value_container, Iterable):
                raise ValueError('Message with multiple elements given ' + \
                                 'non-iterable value')

            if len(value_container) != self.n_elements:
                raise ValueError('Message container of incorrect length given')

            values = value_container

        else:
            values = [value_container]

        for value_index, value in enumerate(values):
            self.message_return[self.message_element_names[value_index]] = value

    def set_empty_message(self):
        '''Bla bla

        '''
        return {key : None for key in self.message_element_names}

    def __init__(self, message_name, message_element_names):

        self.message_name = message_name
        self.message_element_names = tuple(message_element_names)
        self.n_elements = len(self.message_element_names)

        self.message_return = self.set_empty_message()

class _Flash(_Message):
    '''Bla bla

    '''
    def read_value(self):
        '''Bla bla

        '''
        data = tuple(self.message_return.values())
        self.message_return = self.set_empty_message()

        return data

    def __init__(self, flash_name, flash_element_names):

        super().__init__(flash_name, flash_element_names)

class Buzz(_Flash):
    '''Bla bla

    '''
    def __init__(self, buzz_name, buzz_element_names):

        super().__init__(buzz_name, buzz_element_names)

class Direction(_Flash):
    '''Bla bla

    '''
    def __init__(self, direction_name, direction_element_names):

        super().__init__(direction_name, direction_element_names)

class Feature(_Flash):
    '''Bla bla

    '''
    def __init__(self, feature_name, feature_element_names):

        super().__init__(feature_name, feature_element_names)

class _Imprint(_Message):
    '''Bla bla

    '''
    def read_value(self):
        '''Bla bla

        '''
        data = tuple(self.message_return.values())

        return data

    def __init__(self, imprint_name, imprint_element_names):

        super().__init__(imprint_name, imprint_element_names)
        
class Scaffold(_Imprint):
    '''Bla bla

    '''
    def __init__(self, scaffold_name, scaffold_element_names):

        super().__init__(scaffold_name, scaffold_element_names)

class Belief(_Imprint):
    '''Bla bla

    '''
    def __init__(self, belief_name, belief_element_names):

        super().__init__(belief_name, belief_element_names)
