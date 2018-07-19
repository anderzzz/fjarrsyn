'''Helper functions used by various actors

'''
import numpy as np

RAPID_SHIFT_STEEPNESS = 10.0

def sigmoid(max_height, steepness, midpoint, up_down, x_value):
    '''Bla bla

    '''
    if up_down:
        alpha = -1.0 * steepness
    else:
        alpha = 1.0 * steepness

    exp_value = np.exp(alpha * (midpoint - x_value))

    return max_height / (1.0 + exp_value)

def sigmoid_10(max_height, midpoint, up_down, x_value):
    '''Bla bla

    '''
    if max_height > 1.0 or max_height < 0.0:
        raise ValueError('Sigmoild value range should be between ' + \
                         '0.0 and 1.0, not %s' %(str(max_height)))

    return sigmoid(max_height, RAPID_SHIFT_STEEPNESS, midpoint, up_down, x_value)
