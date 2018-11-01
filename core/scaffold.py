'''Scaffold Class

'''
class _Scaffold(object):
    '''Bla bla

    '''
    def set_elements(self, value_container):
        '''Bla bla

        '''
        if self.n_items > 1:
            if not isinstance(value_container, Iterable):
                raise TypeError('Scaffold with multiple elements given ' + \
                                'non-iterable value')

            if len(value_container) != self.n_items:
                raise ValueError('Scaffold container of incorrect length given')

            values = value_container

        else:
            values = [value_container]

        for value_index, value in enumerate(values):
            self._items[self.item_names[value_index]] = value

    def set_empty_scaffold(self):
        '''Bla bla

        '''
        return {key : None for key in self.item_names}

    def __init__(self, item_names):

        self.item_names = item_names
        self.n_items = len(item_names)
        self._items = self.set_empty_scaffold()

class Resource(_Scaffold):
    '''Bla bla

    '''
    def __init__(self, resource_names):

        super().__init__(resource_names)

class Essence(_Scaffold):
    '''Bla bla

    '''
    def __init__(self, essence_names):

        super().__init__(essence_names)
