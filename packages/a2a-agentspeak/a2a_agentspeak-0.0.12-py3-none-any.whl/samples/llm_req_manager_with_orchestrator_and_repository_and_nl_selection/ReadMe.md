## Summary
This example shows a selector/orchestrator agent that talks with a repository of running agents
to find an agent capable of building a list of requirements from a short specification.
If the selected solution agent fails, then the selector agents consults again the repository to get another solution agent.

## Run the example

### Run the repository
The repository is an A2A/ACL agent. It stores information about running A2A/ACL agents.

Run the repository server :

   ```bash
   python3 ../../hot_repository/run_hot_repository_server.py
   ```

### Run the selector agent
The selector/orchestrator agent is an A2A/ACL agent programmed in AgentSpeak (files `agent_selector.asl` and `agent_selector.asi`).

To run the selector agent:

```bash
python3 run_agent_selector_agent.py
```

### Run the solution agents

Several solution agents will be running and will be registered on the repository. 
All those agents are A2A/ACL agents and programmed in AgentSpeak.

Then you can run any number of agents among those:

```bash
python3 run_bad_requirement_manager_agent.py
```

```bash
python3 run_naive_requirement_manager_agent.py
```

```bash
python3 run_requirement_manager_agent_on_mistral.py
```

```bash
python3 run_requirement_manager_agent_on_openai.py
```

```bash
python3 run_robot_agent.py
```

```bash
python3 run_stub_requirement_manager_agent.py
```

### Run the client
The client first registers the solution agents in the repository, then it initiates the request to the orchestrator agent.

Run the client :

```bash
python3 run_test_client.py
```

### Parameters

* The specification is defined in `context.py` .
* A sleep time is defined in `agent_selector.asl` . It is used by agents dealing with a LLM. Change that duration to relax or stress the rate limit of the LLM provider. 

## Diagram

![collaboration diagram](collaboration.drawio.svg)