'''Environments

'''
class Lake(object):
    '''The lake and the fish in it

    The fish is uniformly randomly distributed over the lake grid. Extraction
    is done on a single lake grid where at most some fraction of the fish is
    extracted.

    Growth is stochastic logistic where crowding reduces the maximum growth

    '''
    def regrowth(self):

        n_spawn = 0
        for fish in range(0, self.n_fish):
            n_attempt = int(np.random.ranf() + self.spawn_prob)
            n_crowding = int(np.random.ranf() + self.n_fish / self.capacity)
            if n_attempt == 1 and n_crowding == 0:
                n_spawn += 1

        self.n_fish = min(self.capacity, self.n_fish + n_spawn)

    def extract(self, maximum, extract_prob):

        which_unit_is_fish = np.random.randint(0, self.size_units, self.n_fish)
        select_unit = np.random.randint(0, self.size_units)
        max_available = sum([1 for x in which_unit_is_fish if x == select_unit])
        extract_attempt = [np.random.ranf() < extract_prob for k in range(max_available)]
        n_extracted = min(maximum, sum(extract_attempt))

        self.n_fish -= n_extracted
        
        return n_extracted

    def __init__(self, n_fish, size, spawn_prob, max_capacity):

        self.n_fish = n_fish
        self.spawn_prob = spawn_prob
        self.size_units = size
        self.capacity = max_capacity

class Field(object):

    def sow(self, effort, seed_index):

        pass

    def growth(self):

        pass

    def harvest(self):

        pass

    def __init__(self, size):

        self.size = size
