# Scenario with a refactoring advisor (LLM agent), a validator agent (human), and a manager agent (AgentSpeak).

This example shows a manager agent that talks with a LLM agent and 
with a validator agent (human or LLM based)
to improve the quality of a source code.

## Refactoring advisor agent
The refactoring advisor agent is provided as a ACL/A2A agent that handles a LLM.

```bash
    python3 PATH/TO/a2a-acl/sample_agents/ll_refactoring_advice/run_advisor_agent.py
```
_The validator agent should run on port 9999._

## Validator agent

Several validator agents are shipped in the `a2a-acl` source repository. 
They are programmed in python, not in AgentSpeak. 
Run one the one with user in the loop.

* To run the user-in-the-loop validator agent :

    ```bash
    python3 PATH/TO/sample_agents/human_validation/run_validator_agent.py
    ```

_The validator agent should run on port 9999._


## Manager agent

The manager agents sends requests to the refactoring advisor agent, then submits the result to the validator agent.
After reply from the validator agent, according to the answer, the manager will either keep the original source code,
or keep the refactored one.

Run the manager agent:

```bash
    python3 run_manager.py 
```

_The manager agent should run on port 9981._

## Client to init the test

The client send messages to the manager with a specification and the code to refactor.

```bash
    python3 run_test_client.py 
```
### Parameters

* The specification is defined in `context.py` .
* The initial source code is also defined in `context.py` .

## The upload illocution

Because source code must not be parsed by the AgentSpeak tools, we use a particular illocution, **upload**, that is handled as a **tell**/**upload** message (here **tell** is the illocution and **upload** is the entry-point, or the functor of an AgentSpeak literal **upload(code)**).

The interface of the manager agent declares the **upload** skill (the ability to receive an upload), see `manager.asi` . 

The manager also sends **upload** messages with the `.send_str` action (that does not parse its content parameter, unlike `.send` action). 


### Collaboration

Collaboration diagram:

![Collaboration diagram](collaboration.svg)

Note that the refactoring advisor agent replies with an _asynchronous_ message while the validator agent replies with a _synchronous_ message. 
The AgentSpeak manager agent handles those two kinds of answers in this example.