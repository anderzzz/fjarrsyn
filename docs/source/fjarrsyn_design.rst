================================
Fjarrsyn Design
================================

Fjarrsyn is a library to perform ABM. It is built as a general and 
flexible tool, such that the nature of the agents or the system they are
part of is not narrowly fit to any particular domain, such as biology, markets,
spatial orientation and so on.

This section describes the design of Fjarrsyn, the conceptual framework
that informs the implementation and object definitions, as well as 
terminology. Implementation details are *not* part of this section, rather
handled when specific classes are documented. Concepts and terminology
defined here are used throughout the remainder of the documentation.

At a high-level of abstraction, the design splits the system across two
binary variables: who and what. The *who* is either intentional aspects
of the Agent, or it is non-intentional aspects of the system. This is a
fundamental distinction of an ABM. The *what* is either structure
or dynamics. The structure is how the state and objects of the system are
composed and logically related, and dynamics is how the structure is
executed in order to evolve the system over time. Therefore in the sections
that follow, almost all design elements fit unambiguously into one of the
four combined categories.

The terminology and model constraints that are defined below are 
particular to Fjarrsyn and may not apply to ABM in general. 

Intentional Structure
---------------------
The Agent is the key unit in ABM. The components, and logical connections
and constraints of the Agent design are described in the subsections below.

Agent Structure
^^^^^^^^^^^^^^^

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

Semantically a chain of actions can be coded as an ordered set of 
*verbs and objects*. The Sensor senses an external precept, 
the Interpreter interprets 
sensory data, the Moulder moulds direction on basis of current beliefs,
and the Actuator acts on the environment as directed. This enables
a compact and semantically meaningful encoding of what an Agent 
is doing, see more later. 

As described in detail below, a plurality of
verbs and objects can be combined into *named clauses*. Therefore the
verbs above are referred to as *atomic verbs* when it is salient to make
the distinction.

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

Array Structure
^^^^^^^^^^^^^^^^

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

Instructor Function
^^^^^^^^^^^^^^^^^^^^^

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

Instructor Structure
^^^^^^^^^^^^^^^^^^^^^^

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

An Instructor that is an Organ is executed by invoking the appropriate 
atomic verb 
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

Scaffold Map
^^^^^^^^^^^^

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

Non-Intentional Structure
--------------------------
All structure other than the Agents are described next. This is contained
in an Agent System Manager (ASM). Unlike the Agent, this unit of the design
does not necessarily correspond to a real-world unit. It can be a collection
of external geometrical and natural constraints on the actions of the Agents.

Agent System Manager Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
An Agent System Manager (ASM) is an object
that defines the system and methods for its management. 
These properties include how the
Agents relate to each other as well as anything that is not modelled as
part of the intentional aspects of the Agents.

The system properties are defined next, some of which
are given more detailed descriptions in separate sections to follow.

.. image:: /_static/fjarrsyn_system_structure.png

The *Agent Network* defines the relative positions of the
Agents of the system. In the figure above the network is illustrated with 
a line topology with three nodes.
Since agents can influence each other, but not
necessarily to the same degree due to different pairwise
association or abstract proximity, a network or graph enables quantification of 
this relation through its topology
and optional edge weights. In the particular case where there is no variable
degree of association or abstract proximity, the network is fully connected.
In the general case any weighted non-directional graph can be used. The 
network topology and node content can also change during the modelling,
as described in more detail later.

An *Environment* is an object that is external to any Agent, but which can
be, in part or entirely, be sensed and acted upon by Agents. The Environment
can be subdivided into objects associated to specific Agents, thus 
modelling a local environment. The Environment can also be a single common
object to all Agents. The Environment object is therefore contained in
the same node in the Agent Network as the relevant Agent. Note that a node
in the Agent Network can also contain only an Environment object without
an Agent.

As described in an earlier section, non-intentional qualities can also alter
the state of an Agent, referred to as Principles. Since these are not within
the control of the Agent, the Principles are rather attributes of the ASM.
Collectively the Principles are referred to as the ASM *Lawbook*, which 
matches which Principles should apply to which Agents.

Finally the ASM contains a number of read and write methods that can alter
the network, environment or lawbook, or iterate over or otherwise index
node content in useful ways.

Agent Environment Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Environment is not required to conform to any particular structure.
It can be something as simple as a single variable that is read or written
by the Sensor and Actuator engine. It can be a web-service that returns
a range of meterological data.

It is therefore in the implementation of the engine of the relevant 
Sensor or Actuator that the particular properties of the Environment are
fit into the internal structure of the Agent. The structure of the Agent
otherwise only has to know which environment object belongs to which
Agent. 

Intentional Dynamics
---------------------
The structure of the Agents is not sufficient to evolve the Agents. 
The intentional dynamics of an Agent is the
manner and order the components of the Agent are executed as processes
over time. 

.. image:: /_static/fjarrsyn_policy.png

The various intentional dynamics of an Agent are impleneted as
*Policy* attributes of the Agent. A Policy in turn is comprised of 
a *Plan* object. As described in further detail
below, a Plan is comprised of a directional graph of *Clause* and *Heartbeat*
objects. The Agent *enact* a Plan, which accordingly invokes verb-object
pairs corresponding the Organs of the Agent. The enactment of a Plan can
therefore create or update Beliefs and Resources of the Agent, and due to
the Actuator also update the Environment of the Agent.

For reasons of practical convenience, a Policy can also 
consist of a single Clause or Heartbeat. 
Formally this is the same as a Plan with a single node in the graph.

Clause and Auto Condition
^^^^^^^^^^^^^^^^^^^^^^^^^
A Clause is comprised of a sequence of verb-object pairs, the length of
the sequence can be one or greater. The pairs are labels that the Agent
has associated to a particular invokation of an Organ. This part of the
Clause is therefore only labels with no information of how the Agent
or its Organs transform them into intentional action or meaning.

A Clause can optionally conclude with an evaluation of a logical test with
respect to Belief or Resource. These are the two internal
Imprints that are transparent to the Agent as the Agent is engaged in
intentional action. The logical test is encoded in an *Auto Condition* 
object, further specialized in objects *Auto Resource Condition* and
*Auto Belief Condition*. 

By default when an Agent *pronounce* a Clause, it returns *True*, unless
an Auto Condition is present and it evaluates to *False*.

Typically the verb-object pairs of a Clause consist of atomic verbs. 
However, it can use other verbs too, including pronouncing other Clauses.
Hence a Clause can be nested, though it ultimately translates into the 
one and same sequence of atomic verb-object pairs when deconvoluted.

Heartbeat
^^^^^^^^^
A Policy can also contain a *Hearbeat* object, which encodes a special-case
type of dynamics. The Heartbeat 
defines a *death condition* (or sanity condition) for the Agent. 
It is possible with the tools defined so far to model an Agent
that *chooses* death, and it is possible to model an Agent that is terminated
by another external Agent. But an Agent that terminates due to a necessary
internal condition, like exhaustion of battery power, or a random release of
radioactive poison, has neither chosen that outcome nor had it imposed 
from an external source. Heartbeat is therefore not really part of the
Agent exercising intentions, however it is part of an internal logic that
can have an impact during the course of a sequence of verb-object pairs.
Heartbeat is therefore a feature of an Agent that does not fit perfectly
in the abstraction used in Fjarrsyn.

The death/sanity condition is in turn encoded by an Auto Condition, as
described in the previous section.

Heartbeat also contains an integer value *ticker*, which is incremented
by some arithmetic operation, typically addition by 1. This is a special
variable or resource, which models how often the Heartbeat has been 
invoked. The value of *ticker* can be used to define a death condition as well.

Agent Plan
^^^^^^^^^^^^
The executive function of an Agent, where intentional decisions are made,
is encoded as a *Plan*. As a Plan
is executed, a specific sequence of atomic verbs and objects are executed.

A *Plan* is an execution tree object. The tree is comprised of
*cargo* and *dependencies*. Each cargo is comprised of one or more
verb and object pairs, which implies a specific invokation of Agent Organs.
A unit of cargo returns a Boolean output, by default *True*. A collection
of cargo is joined into parent-child relationships by adding dependencies,
where the dependencies are based on the Boolean output.

The verb and object pair of the cargo can be atomic verbs. Since for many
Agent models many atomic verbs only make sense in unison with other 
specific verbs, a convenience object *Clause* is available. The Clause
is a named object comprised of several atomic verbs and objects. A Clause
is invoked with the verb *pronounce* and the associated object name.

The Boolean output of cargo is True unless an *Auto Condition* is defined
and evaluated to be False. An Auto Condition is a relation with respect to
either a Belief or a Resource of the Agent.  In other words the particular sequence of Organ
invokations a Plan imply can depend explicitly on current 
Beliefs and Resources.


.. image:: /_static/fjarrsyn_exampleplan.png

The image above illustrates one possible Plan. A particular verb-object
pair A, is followed by an Auto Condition. Another verb-object pair B is
also part of the Plan, but it is not associated with any condition. All
possible executions of the Plan concludes with a Hearbeat.

Finally, a plan is executed by an Agent through the verb *enact*. 

All verbs an Agent has are summarized
in the table below.

+--------------------+---------------+--------+-----------------------------------------------------------------------+
| Agent Verb         | Object Type   | Atomic | What Invokation Accomplishes                                          |
+====================+===============+========+=======================================================================+
| **sense**          | Sensor        | Yes    | External precept to internal Buzz                                     |
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **interpret**      | Interpreter   | Yes    | Process internal Buzz/Belief to internal Belief                       |
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **mould**          | Moulder       | Yes    | Process internal Belief to internal Direction                         |
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **act**            | Actuator      | Yes    | Process internal Direction to external interaction                    |
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **tickle**         | Cortex        | Yes    | Process internal state to external Feature. NB not for internal action|
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **pronouce**       | Clause        | No     | Execute sequence of other Agent verbs                                 |
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **pump**           | Heartbeat     | No     | Check internal termination condition                                  |
+--------------------+---------------+--------+-----------------------------------------------------------------------+
| **enact**          | Plan          | No     | Execute sequence of other Agent verbs and internal imprint conditions |
+--------------------+---------------+--------+-----------------------------------------------------------------------+

Non-Intentional Dynamics
-------------------------
STRUCTURE THIS SECTION BETTER

Any evolving aspect of the system, not part of the internal actions of 
the Agent, are modelled as propagation of the AMS. As defined above, the AMS
is comprised of three distinct objects: the Agent Network, the Environment,
and the Lawbook. Each of these can be propagated.

The Lawbook is comprised of a number of Principles that can be applied to one
or many of the Agents of the system. Therefore the propagation of the Lawbook
is similar to the Agent Plan in that a sequence of verb-object pairs are
invoked, for the Lawbook, however, the verbs are *compel* and *mutate*.

The Agent Network can be propagated in any way a network can be transformed.
The specific implementation of the network, as detailed in later sections,
enables custom functionality to be written. Particular Agent Network 
transformations included are switching an Agent from one node to another,
changing the edge properties of the network, including breaking an edge.

The Environment is as defined above very general and therefore the dynamics
can be defined generally as well. As described in relation to specific 
implementations, there are convenience functions that allows easy 
implementations of standard dynamics, like Wiener processes or exponential
decay of defined half-life.

The AMS propagation contain two additional features. The order in which the
Agents of the system are propagated can matter, since the actions of one
Agent can alter the Environment of a second Agent, and thus making the 
outcome dependent on the order in which the first and second Agent are
executed. In a single-threaded execution this is reduced to how to iterate
over the set of Agents. The AMS provides a variety of ways to do so. In a
multi-threaded execution this is reduced to how to model the synchronicity
of the real-world process, and how to ensure common system properties,
are handled properly. At this time, no standard methods have been implemented
for this.

Finally, if an Agent has died or terminated due to an internal condition,
as implemented in the Heartbeat object, the Agent is not immediately removed
from the system. The reason is that an Agent cannot delete itself. 
The termination of an Agent is marked with an attribute. As part of the
propagation of the AMS, terminated Agents can be deleted from the
system.