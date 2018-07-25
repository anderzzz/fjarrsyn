'''Helper functions used by various actors

'''
import numpy as np

RAPID_SHIFT_STEEPNESS = 10.0
HORIZONTAL_SHIFT = 0.25

def sigmoid(max_height, steepness, midpoint, up_down, x_value):
    '''Basic sigmoidal function

    Parameters
    ----------
    max_height : float
        The maximum value the sigmoidal function can assume
    steepness : float
        The factor to the exponent, which determines how steep the change
        between low and high values is
    midpoint : float
        The inflection point position
    up_down : bool
        The flag to determine if the sigmoid has its high values at low input
        values, or if the high values are at high input values, or simply if
        the sigmoid should go up or go down as we move on the horizontal axis
    x_value : float
        The value on the horizontal axis for which to evaluate the sigmoid

    Returns
    -------
    outcome : float
        The value of the sigmoid function

    '''
    if up_down:
        alpha = -1.0 * steepness
    else:
        alpha = 1.0 * steepness

    exp_value = np.exp(alpha * (midpoint - x_value))

    return max_height / (1.0 + exp_value)

def sigmoid_10(max_height, midpoint, up_down, x_value):
    '''Sigmoidal function bounded vertically between 0.0 and 1.0 and calibrated
    steepness suitable for horizontal bounded between 0.0 and 1.0.

    Parameters
    ----------
    max_height : float
        The maximum value the sigmoidal function can assume
    midpoint : float
        The inflection point position
    up_down : bool
        The flag to determine if the sigmoid has its high values at low input
        values, or if the high values are at high input values, or simply if
        the sigmoid should go up or go down as we move on the horizontal axis
    x_value : float
        The value on the horizontal axis for which to evaluate the sigmoid

    Returns
    -------
    outcome : float
        The value of the sigmoid function

    '''
    if max_height > 1.0 or max_height < 0.0:
        raise ValueError('Sigmoid vertical value range should be between ' + \
                         '0.0 and 1.0, not %s' %(str(max_height)))

    if x_value > 1.0 or x_value < 0.0:
        raise ValueError('Sigmoid horizontal value range should be between ' + \
                         '0.0 and 1.0, not %s' %(str(x_value)))

    return sigmoid(max_height, RAPID_SHIFT_STEEPNESS, midpoint, up_down, x_value)

def linear_step(low_bend, high_bend, max_val, min_val, up_down, x_value):
    '''Bla bla

    '''
    if low_bend >= high_bend:
        raise ValueError('Lower bound must be strictly smaller than higher bound')

    if x_value < low_bend:
        val = min_val

    elif x_value > high_bend:
        val = max_val

    else:
        val = min_val + (max_val - min_val) * (x_value - low_bend) / (high_bend - low_bend)

    if up_down:
        val = (max_val + min_val) - val

    return val

def linear_step_10(max_val, min_val, mid_point, up_down, x_value):
    '''Bla bla

    '''
    if max_val > 1.0 or max_val < 0.0:
        raise ValueError('Linear step value should be between ' + \
                         '0.0 and 1.0, not %s' %(str(max_val)))

    if x_value > 1.0 or x_value < 0.0:
        raise ValueError('Linear step horizontal value range should be between ' + \
                         '0.0 and 1.0, not %s' %(str(x_value)))

    return linear_step(mid_point - HORIZONTAL_SHIFT, mid_point + HORIZONTAL_SHIFT,
                       max_val, min_val, up_down, x_value)
