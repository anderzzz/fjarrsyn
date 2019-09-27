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

An *Imprint* is a type of Array with persistent content. That means
that once the content is input to a process of an Instructor, the
Imprint remains in memory unchanged. Imprints can be updated as
output from an Instructor, see below.

A *Belief* is an Imprint that represents the manifest interpreted
understanding an Agent has of its environment and possibly of its own
internal state. Beliefs are formed and updated through intentional
actions by the Agent. Content of Belief is information.

A *Resource* is an Imprint that represents objects that can be
transacted as part of intentional as well as non-intentional actions 
by the Agent. Resource defines an object variable of
the Agent. An example of a real-world object that can be modelled
as a Resource is cash on hand.

An *Essence* is an Imprint that represents properties that can
configure intentional actions by the Agent, as well as
non-intentional actions. Essence defines a parameter of the
Agent, though it is beyond the *intentional* adjustment of
the Agent. An example of a real-world object that can be modelled
as an Essence is the DNA code.

A *Flash* is a type of Array whose content is transient. That means that
once the content is input to a process of an Instructor, the Flash
is lost from memory.

A *Buzz* is a Flash that represents the content immediately present
within an Agent upon sensing the external environment. In some literature
this content is called the *sense datum*. Buzz is *not* an interpreted
content. An example of a real-world object that can be modelled
as a Buzz is the electric waveform generated by a transducer.

A *Direction* is a Flash that represent the inferred intention to
take a specific action. The Direction is not the action itself, that
instead follows from an Actuator that receives the Direction as input. 

A *Feature* is a Flash that represent how an intrinsic property of the
Agent appear to an external observer. As described in relation to the
Cortex Instructor below, this models a property of the Agent beyond the
Agent's intentional control.

As noted in the Introduction the exact boundaries between what is contained
in the various Arrays are a matter of model conventions, like what is
intentional and what is non-intentional.

Instructor Definitions
----------------------

The types of Instructors are hierarchically defined in parent-child relations
as represented in the figure below. In practical usage of Fjarrsyn, 
only the Instructors at the lowest level are used.

.. image:: /_static/fjarrsyn_figs-3.png

An *Instructor* encodes function. Function can correspond to transformation
of content of the real-world that is modelled. Therefore Arrays in
Fjarrsyn only changes as output from Instructors.

An *Organ* is an Instructor internal to the Agent. All intentional aspects
of an Agent involve Organs. Organs can take as input the Essence and 
Resources of the Agent (these connections are omitted from the earlier figure).
Organs can have mandatory, or primary, input and output Arrays, as well as
secondary output Arrays, as described in detail in the next section.

An *Interfacial Organ* is an Organ that engages 
directly with the external environment. A *Cognitive Organ* is an Organ that is
not engaging directly with the external environment, rather interprets 
sense data and creates (or selects) intentions in relation to the 
*perceived* external environment. This division enables Agent models that
are not naively realist, rather where mistakes, lies and uncertainty can
be part of the model. As stated elsewhere, there are convenience methods
to model simpler Agents that do not require this differentiation.

A *Sensor* is an Interfacial Organ that upon execution interacts with a
property of the environment (in some literature called the precept) 
and creates Buzz as its primary output.

An *Actuator* is an Interfacial Organ that upon execution takes a Direction
as input and interacts with a property of the environment, typically to alter
it, though the environment can contain friction, which prevents the 
intention to be actualized. An Actuator has no primary output.

A *Cortex* is an Interfacial Organ that upon execution generates a Feature
for an external Agent to access. The Cortex therefore reveals to an external
observer an intrinsic property of the Agent. Typically the Feature is 
derived from the Essence and Resources of the Agent, though the relation
does not have to be an identity relation, such that obscured, imprecise or
adulterated relations between what is instrincically factual and what is
revealed to an observer can be modelled.

An *Interpreter* is a Cognitive Organ that upon execution takes Buzz and
optionally Beliefs as input and creates Belief, or updates to Beliefs, 
as output. The Interpreter models the cognitive layer between sensing
the external environment and forming an understanding or belief of the
environment, such that belief can be in an incomplete, imprecise or 
adulterated relation to the factual state of the environment.

A *Moulder* is a Cognitive Organ that upon execution takes Belief as
input and creates Direction as primary output. The Moulder models the
cognitive layer between a belief about the world and an intention to
engage with the world somehow, such that intrinsic conditions with respect
to the relevant Actuator can make an intention to act in a certain
way not be actualized that way.

A *Principle* is an Instructor external to the Agent. All necessary laws that
constrain or govern non-intentional transformations of content internal
to the Agent are modelled as a Principle. 

A *Mutation* is a Principle that alters the Essence of an Agent. The 
Mutation is a property of the Agent System Manager (ASM), see further below,
but it can be specifically applied to a given Agent. An example of a real-world
function that can be modelled as a Mutation is a random mutation to the
genetic code of an Agent or the physical degradation of a semiconductor with
time.

A *Compulsion* is a Principle that alters the Resource of an Agent. The
Compulsion is a property of the Agent System Manager (ASM), see further below,
but it can be specifically applied to a given Agent. An example of a real-world
gunction that can be modelled as a Compulsion is the necessary energy expended
upon mechanical motion or a rate of inflation that reduces the real value
of cash on hand with time.

The Mutation and Compulsion are only semantically distinct given that
both Essence and Resource are Imprints, and that they are both Principles. 
Essence and Resource relate to the function of Organs differently, however, 
and therefore the semantic distinction is justified. 

For simpler Agents Principles do not model any property of the system
under study. Therefore Principles are optional features.

Instructor Method Types
-----------------------

In this section the internal structure of an Instructor are described and
terminology is defined.

Agent System Manager (ASM)
--------------------------




