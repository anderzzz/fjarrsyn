'''Message classes

'''
from fjarrsyn.core.array import _Imprint, _Flash, _ArrayOperator

class Buzz(_Flash):
    '''The Buzz class that is used to define the output of sensors and input to
    interpreters. The class is a child class of a more general _Array class,
    however in applications the Buzz class should be used

    Parameters
    ----------
    buzz_name : str
        The name of the Buzz
    buss_element_names : iterable
        An iterable of names for each element of the Buzz, each name describing
        some relevant semantics

    '''
    pass

class Direction(_Flash):
    '''The Direction class that is used to define the output of moulders
    and input to actuators. The class is a child class of a more general _Array
    class, however in applications the Direction class should be used

    Parameters
    ----------
    direction_name : str
        The name of the Direction
    direction_element_names : iterable
        An iterable of names for each element of the Direction, each name describing
        some relevant semantics

    '''
    pass

class Feature(_Flash):
    '''The Feature class that is used to define the output of cortex. The class
    is a child class of a more general _Array class, however in applications
    the Feature class should be used

    Parameters
    ----------
    feature_name : str
        The name of the Feature
    feature_element_names : iterable
        An iterable of names for each element of the Feature, each name describing
        some relevant semantics

    '''
    pass

class Belief(_Imprint):
    '''The Belief class that is used to define the persistent output of
    interpreter and input to moulder. The class is a child class of a more
    general _Array class, however in applications the Belief class should be
    used

    Parameters
    ----------
    belief_name : str
        The name of the Belief
    belief_element_names : iterable
        An iterable of names for each element of the Belief, each name describing
        some relevant semantics

    '''
    pass

class Resource(_Imprint):
    '''The Resource class that is used to define the items organs can
    intentionally control as part of their execution. In applications 
    the Resource class should only be edited using the ResourceMap class 
    and related classes

    Parameters
    ----------
    resource_name : str
        The name of the Resource
    resource_element_names : iterable
        An iterable of names for each element of the Resource, each name describing
        some relevant semantics

    '''
    pass

class Essence(_Imprint):
    '''The Essence class that is used to define the items of the agent that are
    beyond intentional control. In applications where external forces alters
    the essence the Essence class should only be edited using the EssenceMap
    class and related classes

    Parameters
    ----------
    essence_name : str
        The name of the Essence
    essence_element_names : iterable
        An iterable of names for each element of the Essence, each name describing
        some relevant semantics

    '''
    pass

class MessageOperator(_ArrayOperator):
    '''Operator to retrieve some selection or combination of message values. 

    Parameters
    ----------
    base_messages
        One or an iterable of messages on which to operate. Note that only
        messages of identical type can be operated on simultaneously.
    slice_labels : iterable, optional
        In case the base message should be sliced to yield a subset of value 
        elements, this iterable should contain the corresponding element labels
    extend : bool, optional
        In case the base messages should be extended to a larger set of values,
        this flag should be set to True
    mix_indeces : dict, optional
        If the values from two or more messages should be combined into an
        output that mixes values from the plurality of base messages, this
        dictionary should as keys have the semantic labels and the value should
        be the index in the `base_messages` iterable
    new_name : str, optional
        The name to give the final message after operation. 

    Notes
    -----
    The message operator is used to access some combination or subset of
    message values. Observe that the message operator is not used to create new
    message instances, it is only meant to be a means to retrieve values for
    reading and further processing by an instructor.

    '''
    def __init__(self, base_messages, 
                 slice_labels=None, extend=False, mix_indeces=None,
                 new_namer=None):

        super().__init__(base_messages, slice_labels, extend, mix_indeces,
                         new_namer, True)


