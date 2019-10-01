================================
Fjarrsyn Library Design
================================

Fjarrsyn is a library to perform ABM. It is built as a very general and 
flexible tool, such that the nature of the agents or the system they are
part of is unconstrained by any particular domain, such as biology, markets,
spatial orientation and so on.

This section describes the design of Fjarrsyn, the conceptual framework
that informs the implementation and object definitions, as well as 
terminology. Implementation details are *not* part of this section, rather
handled when specific classes are documented. Concepts and terminology
defined here are used throughout the remainder of the documentation.

The terminology and model constraints that are defined below are 
particular to Fjarrsyn and may not apply to ABM in general. 

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

Essence and Resources have functionally different roles than the 
other types of Arrays. This will be clearly defined in subsequent 
sections. The semantic grouping is *Scaffold* and *Message*, 
and is illustrated in the table below.

+--------------------+---------------+------------------+
|                    | Imprint       | Flash            |
+====================+===============+==================+
| **Scaffold**       | Resource,     | ...              |
|                    | Essence       |                  |
+--------------------+---------------+------------------+
| **Message**        | Belief        | Buzz,            |
|                    |               | Direction,       |
|                    |               | Feature          |
+--------------------+---------------+------------------+

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
genetic code of an Agent or the continuous thermal degradation of a 
semiconductor with time.

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

Instructor Structure and Execution
----------------------------------

In this section the internal structure of an Instructor are described and
terminology is defined. The image below shows the most general structure of 
an Instructor.

.. image:: /_static/fjarrsyn_instructor_structure.png

The mandatory part of an Instructor is the *Engine*. This corresponds to 
an executable.

An Instructor that requires a Message as input, and yields a Message as
output is a *transformer* Instructor. The Interpreter belongs to this
category because it transform the content in a Buzz message into content
of a Belief message.

An Instructor that requires a Message as input, but has no Message as
output is a *consumer* Instructor. The Actuator belongs to this
category.

An Instructor that requires a Message as output, but has no Message as
input is a *producer* Instructor. The Sensor belongs to this
category.

Instructors can also produce a *Scaffold Map*. These are described in more
detail below. These are executables, which when applied to the appropriate
Scaffold alters the content as specified in the executable. An Instructor 
that generates a Scaffold Map is called a *tangible* Instructor, while an
Instructor without a Scaffold Map as output is called an *abstract* Instructor.
Scaffold Map outputs can appear with or without Message inputs or outputs.
Hence, an Instructor can for example be an abstract transformer, tangible
transformer, tangible producer etc. Different types of Instructors enforce
different input and output requirements.

The Engine of an Instructor can access a subset of the Agent Scaffold,
that is the Agent Resource and Essence. Note these are read-only relations.

The creation of a specific Instructor therefore defines the objects that
corresponds to each of the relevant inputs and outputs, as well as the Engine.
That is the structure of the Instructor.

An Instructor that is an Organ is executed by invoking the appropriate verb 
and object. The invokation of the verb and object furthermore executes
the scaffold map. 

This chain of events for an Organ, and within which object it takes place, is
illustrated in the swim-lane diagram below. 

.. image:: /_static/fjarrsyn_swim_organ.png

Each step is further exemplified 
as an invokation of an Interpreter Organ in which a transducer signal that
senses audio in the environment is interpreted and turned into a Belief
about an engine failure. The interpretation requires parameters about how
sensitive, or suspicious, the interpretation should be, wherein said parameters
are part of the Essence of the Agent. The interpretation in the example 
consumes battery resources, which is embodied as a Resource Map. 

Scaffold Map Definition
-----------------------
As described in an earlier section, the scaffold of an Agent is comprised
of the Essence and Resources of the Agent. The Agent Organs can only read
the content of the Resources and Essence, but not *directly* alter the
scaffold. This embodies that Organs perform *intentional* efforts. However,
in case an intentional effort has a necessary consequence, that is 
something not
within the purview of the agent's intentions and choice, that part of
the effort should be modelled distinctly from the output message of the Organ.

A Scaffold Map is an *executable instruction* for how to alter either
a Resource or an Essence. As illustrated in a figure in the previous 
section, an Organ can populate a Scaffold Map for subsequent execution. 
This is therefore the mechanism by which intentional efforts can imply
necessary consequences, while maintaining a clear distinction between what
is modelled as intentional and what is modelled as non-intentional in any
given Agent-Based Model.

Scaffold Maps are the only output from Principle Instructors, since these
models non-intentional efforts. How they fit within the ABM in Fjarrsyn is
further described in the section on the Agent System Manager (ASM).

Agent System Manager Definition
-------------------------------
Bla bla

Agent Network Definition
------------------------
Bla bla

Agent Environment Definition
----------------------------
Bla bla

Propagator and Simulator Definitions
------------------------------------
Bla bla




