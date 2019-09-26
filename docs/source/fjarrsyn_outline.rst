================================
Fjarrsyn ABM Library Definitions
================================

Fjarrsyn is a library to perform ABM. It is built as a very general and 
flexible tool, such that the nature of the agents or the system they are
part of is unconstrained by any particular domain, such as biology, markets,
spatial orientation and so on.

The terminology and model constraints that are defined below are 
particular to Fjarrsyn and may not apply to ABM in general. 
The specific documentation of the classes, methods, attributes, and 
other software components and how to work with these, is available
in a section to follow. Later sections will use terminology and
definitions introduced in this section.

Agent Definition
----------------

The agent is constrained with respect to its internal structure,
such that the logic connections between inputs and outputs fit in
a useful semantics. The functional constraints are few however, and
therefore agents in Fjarrsyn can model a diverse type of domain
specific agents.

A visual representation of key structural features and nomenclature of an
agent is shown below. The details of this image will be
described in later sections. 

.. image:: /_static/fjarrsyn_figs.png

The dotted line defines the boundary of an agent. Entities represented
as rectangles are different types of instructors. Entities represented
as rhomboids are different types of arrays. A rhomboid with solid line
boundary is a persistent array, while a rhomboid with a 
dashed line boundary is a transient array. Arrows represent logical
connections, though some connection are omitted for clarity.
The details of each entity are given below.

A typical chain of *intentional action* for an agent can be as follows:

#. A Sensor *senses* some precept of the environment to the agent and
   outputs the raw datum, named Buzz.
#. An Interpreter *interprets* the Buzz and outputs encoded information
   about the environment, named Belief. Note that the prior Belief can
   influence the process of interpretation.
#. A Moulder *moulds* an output that is intended to interact with the
   environment, said output is named Direction, and Beliefs guide 
   the process of moulding.
#. An Actuator *acts on* a given Direction and engages accordingly with
   the environment to the agent. Note that the Actuator can return
   something to the Agent.

Semantically a chain of actions can be coded as an ordered set of verbs 
and objects. The Sensor senses object, the Interpreter interprets 
sensory data, the Moulder moulds direction on basis of current beliefs,
and the Actuator acts on the environment as directed. This enables
a compact and semantically meaningful encoding of what an Agent 
is doing, see more later. 

The Agent can also have non-intentional qualities. These are 
encoded in the other entities in the above figure. Further details
are given in the sections below.

For very simple Agents it may not be useful to separate the sensing
of an external precept and the belief it informs. In these cases the
Interpreter would be an identity function that turns the Buzz into
a Belief. 

For more complex Agents the sensing of a precept may lead to 
different beliefs, given other qualities of the Agent. With 
complex environments that can not necessarily be truthfully and
comprehensively sensed, interpretation on basis of other
information and pre-dispositions are required.

Analogous arguments apply to the connection between Belief, Moulder,
and Actuator.

Array Definitions
-----------------

The types of Arrays are hierarchically defined in parent-child relations
as represented in the figure below. In practical usage of Fjarrsyn, 
only the Arrays at the lowest level are used.

.. image:: /_static/fjarrsyn_figs-2.png

An *Array* encodes content. Content can correspond to information in the
real-world that is modelled. Content can correspond to substance in
the real-world that is modelled. 

An *Imprint* is a type of Array whose content is persistent. That means
that once the content is input to a process of an Instructor, the
Imprint remains in memory unchanged.

A *Belief* is an Imprint that represents the conscious and interpreted
understanding an Agent has of its environment and possibly of its own
internal state. Beliefs can be formed and updated through intentional
actions by the Agent. Content of Belief is information.

A *Resource* is an Imprint that represents objects that can be
transacted as part of intentional actions by the Agent, as well as
non-intentional actions. Resource defines an object variable of
the Agent. An example of a real-world object that can be modelled
as a Resource is cash on hand.

An *Essence* is an Imprint that represents properties that can
configure intentional actions by the Agent, as well as
non-intentional actions. Essence defines a parameter of the
Agent. An example of a real-world object that can be modelled
as an Essence is the DNA code.

A *Flash* is a type of Array whose content is transient. That means that
once the content is input to a process of an Instructor, the Flash
is lost from memory.

<CONTINUE HERE>

Instructor Definitions
----------------------

Bla bla

.. image:: /_static/fjarrsyn_figs-3.png

Instructor Method Types
-----------------------

Bla bla

Agent System Definition
-----------------------

Bla bla


