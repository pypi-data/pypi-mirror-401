### Concepts

In this example, an agent asks two other agents to generate some requirements
for a given specification, then it asks another agent to arbitrate between the
two received answers.

This example illustrates how an AgentSpeak agent can instantiate other 
AgentSpeak agents and delegate some tasks to them.


### Agents

Four agents are run in this example:
 * An orchestrator (defined in `orchestrator.asl`, run by `run_agent.py`).
 * Two requirement generators (launched by the orchestrator).
 * An arbitrator (launched by the orchestrator).


### Collaboration

When the orchestrator starts, it spawns two worker agents based on their 
AgentSpeak code found in
`../../sample_agents/requirement_generators/stub_requirement_manager` 
and `../../sample_agents/requirement_generators/naive_requirement_manager` .

Then the orchestrator sends to those workers the specification at hand 
and the request to build some lists of requirements.

Each worker replies to the orchestrator.

When all the replies are received, the orchestrator spawns an arbitrator agent 
based on `arbitrator.asl` AgentSpeak code (and its interface in `arbitrator.asi`).
Then the orchestrator sends to the arbitrator the specification and the two 
proposals.
Then the arbitrator replies with a selected list of requirements, 
and the orchestrator prints that list to the user.


![diagram](collaboration.svg)


### To go further

* Make the requirement manager use a LLM.
* Make the arbitrator use a LLM.
* Make the orchestrator handle failures from the generators.
 