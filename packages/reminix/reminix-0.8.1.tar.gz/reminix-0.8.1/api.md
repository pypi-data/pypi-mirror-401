# Project

Types:

```python
from reminix.types import ProjectRetrieveResponse
```

Methods:

- <code title="get /project">client.project.<a href="./src/reminix/resources/project.py">retrieve</a>() -> <a href="./src/reminix/types/project_retrieve_response.py">ProjectRetrieveResponse</a></code>

# Agents

Types:

```python
from reminix.types import Context, AgentChatResponse, AgentInvokeResponse
```

Methods:

- <code title="post /agents/{name}/chat">client.agents.<a href="./src/reminix/resources/agents.py">chat</a>(name, \*\*<a href="src/reminix/types/agent_chat_params.py">params</a>) -> <a href="./src/reminix/types/agent_chat_response.py">AgentChatResponse</a></code>
- <code title="post /agents/{name}/invoke">client.agents.<a href="./src/reminix/resources/agents.py">invoke</a>(name, \*\*<a href="src/reminix/types/agent_invoke_params.py">params</a>) -> <a href="./src/reminix/types/agent_invoke_response.py">AgentInvokeResponse</a></code>
