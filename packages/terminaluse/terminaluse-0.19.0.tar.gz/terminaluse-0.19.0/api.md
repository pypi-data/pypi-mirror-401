# Agents

Types:

```python
from sb0.types import (
    Agent,
    AgentInputType,
    AgentRpcMethod,
    AgentRpcRequest,
    AgentRpcResponse,
    AgentRpcResult,
    AgentStatus,
    CancelTaskRequest,
    CreateTaskRequest,
    DeleteResponse,
    DeployRequest,
    DeployResponse,
    HTTPValidationError,
    JsonRpcErrorObject,
    SendEventRequest,
    SendMessageRequest,
    ValidationError,
    AgentListResponse,
)
```

Methods:

- <code title="get /agents/{agent_id}">client.agents.<a href="./src/sb0/resources/agents/agents.py">retrieve</a>(agent_id) -> <a href="./src/sb0/types/agent.py">Agent</a></code>
- <code title="get /agents">client.agents.<a href="./src/sb0/resources/agents/agents.py">list</a>(\*\*<a href="src/sb0/types/agent_list_params.py">params</a>) -> <a href="./src/sb0/types/agent_list_response.py">AgentListResponse</a></code>
- <code title="delete /agents/{agent_id}">client.agents.<a href="./src/sb0/resources/agents/agents.py">delete</a>(agent_id) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="delete /agents/name/{namespace_slug}/{agent_name}">client.agents.<a href="./src/sb0/resources/agents/agents.py">delete_by_name</a>(agent_name, \*, namespace_slug) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="post /agents/deploy">client.agents.<a href="./src/sb0/resources/agents/agents.py">deploy</a>(\*\*<a href="src/sb0/types/agent_deploy_params.py">params</a>) -> <a href="./src/sb0/types/deploy_response.py">DeployResponse</a></code>
- <code title="post /agents/{agent_id}/rpc">client.agents.<a href="./src/sb0/resources/agents/agents.py">handle_rpc</a>(agent_id, \*\*<a href="src/sb0/types/agent_handle_rpc_params.py">params</a>) -> <a href="./src/sb0/types/agent_rpc_response.py">AgentRpcResponse</a></code>
- <code title="get /agents/name/{namespace_slug}/{agent_name}">client.agents.<a href="./src/sb0/resources/agents/agents.py">retrieve_by_name</a>(agent_name, \*, namespace_slug) -> <a href="./src/sb0/types/agent.py">Agent</a></code>
- <code title="post /agents/{agent_id}/rpc">client.agents.<a href="./src/sb0/resources/agents/agents.py">rpc</a>(agent_id, \*\*<a href="src/sb0/types/agent_rpc_params.py">params</a>) -> <a href="./src/sb0/types/agent_rpc_response.py">AgentRpcResponse</a></code>
- <code title="post /agents/name/{namespace_slug}/{agent_name}/rpc">client.agents.<a href="./src/sb0/resources/agents/agents.py">rpc_by_name</a>(agent_name, \*, namespace_slug, \*\*<a href="src/sb0/types/agent_rpc_by_name_params.py">params</a>) -> <a href="./src/sb0/types/agent_rpc_response.py">AgentRpcResponse</a></code>

## Name

Methods:

- <code title="get /agents/name/{namespace_slug}/{agent_name}">client.agents.name.<a href="./src/sb0/resources/agents/name.py">retrieve</a>(agent_name, \*, namespace_slug) -> <a href="./src/sb0/types/agent.py">Agent</a></code>
- <code title="delete /agents/name/{namespace_slug}/{agent_name}">client.agents.name.<a href="./src/sb0/resources/agents/name.py">delete</a>(agent_name, \*, namespace_slug) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="post /agents/name/{namespace_slug}/{agent_name}/rpc">client.agents.name.<a href="./src/sb0/resources/agents/name.py">handle_rpc</a>(agent_name, \*, namespace_slug, \*\*<a href="src/sb0/types/agents/name_handle_rpc_params.py">params</a>) -> <a href="./src/sb0/types/agent_rpc_response.py">AgentRpcResponse</a></code>

## Forward

### Name

Methods:

- <code title="get /agents/forward/name/{namespace_slug}/{agent_name}/{path}">client.agents.forward.name.<a href="./src/sb0/resources/agents/forward/name.py">get</a>(path, \*, namespace_slug, agent_name) -> object</code>
- <code title="post /agents/forward/name/{namespace_slug}/{agent_name}/{path}">client.agents.forward.name.<a href="./src/sb0/resources/agents/forward/name.py">post</a>(path, \*, namespace_slug, agent_name) -> object</code>

## Schedules

Types:

```python
from sb0.types.agents import (
    ScheduleActionInfo,
    ScheduleListItem,
    ScheduleListResponse,
    ScheduleResponse,
    ScheduleSpecInfo,
    ScheduleState,
)
```

Methods:

- <code title="post /agents/{agent_id}/schedules">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">create</a>(agent_id, \*\*<a href="src/sb0/types/agents/schedule_create_params.py">params</a>) -> <a href="./src/sb0/types/agents/schedule_response.py">ScheduleResponse</a></code>
- <code title="get /agents/{agent_id}/schedules/{schedule_name}">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">retrieve</a>(schedule_name, \*, agent_id) -> <a href="./src/sb0/types/agents/schedule_response.py">ScheduleResponse</a></code>
- <code title="get /agents/{agent_id}/schedules">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">list</a>(agent_id, \*\*<a href="src/sb0/types/agents/schedule_list_params.py">params</a>) -> <a href="./src/sb0/types/agents/schedule_list_response.py">ScheduleListResponse</a></code>
- <code title="delete /agents/{agent_id}/schedules/{schedule_name}">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">delete</a>(schedule_name, \*, agent_id) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="post /agents/{agent_id}/schedules/{schedule_name}/pause">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">pause</a>(schedule_name, \*, agent_id, \*\*<a href="src/sb0/types/agents/schedule_pause_params.py">params</a>) -> <a href="./src/sb0/types/agents/schedule_response.py">ScheduleResponse</a></code>
- <code title="post /agents/{agent_id}/schedules/{schedule_name}/trigger">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">trigger</a>(schedule_name, \*, agent_id) -> <a href="./src/sb0/types/agents/schedule_response.py">ScheduleResponse</a></code>
- <code title="post /agents/{agent_id}/schedules/{schedule_name}/unpause">client.agents.schedules.<a href="./src/sb0/resources/agents/schedules.py">unpause</a>(schedule_name, \*, agent_id, \*\*<a href="src/sb0/types/agents/schedule_unpause_params.py">params</a>) -> <a href="./src/sb0/types/agents/schedule_response.py">ScheduleResponse</a></code>

## Deployments

Methods:

- <code title="get /agents/{namespace_slug}/{agent_name}/deployments/{branch}">client.agents.deployments.<a href="./src/sb0/resources/agents/deployments/deployments.py">retrieve</a>(branch, \*, namespace_slug, agent_name) -> <a href="./src/sb0/types/deployment_response.py">DeploymentResponse</a></code>
- <code title="get /agents/{namespace_slug}/{agent_name}/deployments">client.agents.deployments.<a href="./src/sb0/resources/agents/deployments/deployments.py">list</a>(agent_name, \*, namespace_slug, \*\*<a href="src/sb0/types/agents/deployment_list_params.py">params</a>) -> <a href="./src/sb0/types/deployment_list_response.py">DeploymentListResponse</a></code>

### Versions

Methods:

- <code title="get /agents/{namespace_slug}/{agent_name}/deployments/{branch}/versions">client.agents.deployments.versions.<a href="./src/sb0/resources/agents/deployments/versions.py">list</a>(branch, \*, namespace_slug, agent_name, \*\*<a href="src/sb0/types/agents/deployments/version_list_params.py">params</a>) -> <a href="./src/sb0/types/version_list_response.py">VersionListResponse</a></code>

## Environments

Types:

```python
from sb0.types.agents import (
    CreateEnvRequest,
    DeleteEnvResponse,
    EnvListResponse,
    EnvResponse,
    ResolveEnvResponse,
    UpdateEnvRequest,
)
```

Methods:

- <code title="post /agents/{namespace_slug}/{agent_name}/environments">client.agents.environments.<a href="./src/sb0/resources/agents/environments/environments.py">create</a>(agent_name, \*, namespace_slug, \*\*<a href="src/sb0/types/agents/environment_create_params.py">params</a>) -> <a href="./src/sb0/types/agents/env_response.py">EnvResponse</a></code>
- <code title="get /agents/{namespace_slug}/{agent_name}/environments/{env_name}">client.agents.environments.<a href="./src/sb0/resources/agents/environments/environments.py">retrieve</a>(env_name, \*, namespace_slug, agent_name) -> <a href="./src/sb0/types/agents/env_response.py">EnvResponse</a></code>
- <code title="put /agents/{namespace_slug}/{agent_name}/environments/{env_name}">client.agents.environments.<a href="./src/sb0/resources/agents/environments/environments.py">update</a>(env_name, \*, namespace_slug, agent_name, \*\*<a href="src/sb0/types/agents/environment_update_params.py">params</a>) -> <a href="./src/sb0/types/agents/env_response.py">EnvResponse</a></code>
- <code title="get /agents/{namespace_slug}/{agent_name}/environments">client.agents.environments.<a href="./src/sb0/resources/agents/environments/environments.py">list</a>(agent_name, \*, namespace_slug) -> <a href="./src/sb0/types/agents/env_list_response.py">EnvListResponse</a></code>
- <code title="delete /agents/{namespace_slug}/{agent_name}/environments/{env_name}">client.agents.environments.<a href="./src/sb0/resources/agents/environments/environments.py">delete</a>(env_name, \*, namespace_slug, agent_name) -> <a href="./src/sb0/types/agents/delete_env_response.py">DeleteEnvResponse</a></code>
- <code title="get /agents/{namespace_slug}/{agent_name}/resolve-env">client.agents.environments.<a href="./src/sb0/resources/agents/environments/environments.py">resolve_env</a>(agent_name, \*, namespace_slug, \*\*<a href="src/sb0/types/agents/environment_resolve_env_params.py">params</a>) -> <a href="./src/sb0/types/agents/resolve_env_response.py">ResolveEnvResponse</a></code>

### Deployments

Methods:

- <code title="get /agents/{namespace_slug}/{agent_name}/environments/{env_name}/deployments">client.agents.environments.deployments.<a href="./src/sb0/resources/agents/environments/deployments.py">list</a>(env_name, \*, namespace_slug, agent_name) -> <a href="./src/sb0/types/deployment_list_response.py">DeploymentListResponse</a></code>

### Secrets

Types:

```python
from sb0.types.agents.environments import (
    DeleteEnvVarResponse,
    DeployedSecretKey,
    DeployedSecretsResponse,
    EnvVarListResponse,
    EnvVarResponse,
    SetEnvVarRequest,
    SetEnvVarResponse,
)
```

Methods:

- <code title="get /agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets">client.agents.environments.secrets.<a href="./src/sb0/resources/agents/environments/secrets.py">list</a>(env_name, \*, namespace_slug, agent_name, \*\*<a href="src/sb0/types/agents/environments/secret_list_params.py">params</a>) -> <a href="./src/sb0/types/agents/environments/env_var_list_response.py">EnvVarListResponse</a></code>
- <code title="delete /agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets/{key}">client.agents.environments.secrets.<a href="./src/sb0/resources/agents/environments/secrets.py">delete</a>(key, \*, namespace_slug, agent_name, env_name, \*\*<a href="src/sb0/types/agents/environments/secret_delete_params.py">params</a>) -> <a href="./src/sb0/types/agents/environments/delete_env_var_response.py">DeleteEnvVarResponse</a></code>
- <code title="get /agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets/deployed">client.agents.environments.secrets.<a href="./src/sb0/resources/agents/environments/secrets.py">list_deployed</a>(env_name, \*, namespace_slug, agent_name) -> <a href="./src/sb0/types/agents/environments/deployed_secrets_response.py">DeployedSecretsResponse</a></code>
- <code title="put /agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets">client.agents.environments.secrets.<a href="./src/sb0/resources/agents/environments/secrets.py">set</a>(env_name, \*, namespace_slug, agent_name, \*\*<a href="src/sb0/types/agents/environments/secret_set_params.py">params</a>) -> <a href="./src/sb0/types/agents/environments/set_env_var_response.py">SetEnvVarResponse</a></code>

### Rollback

Types:

```python
from sb0.types.agents.environments import RollbackRequest, RollbackResponse
```

Methods:

- <code title="post /agents/{namespace_slug}/{agent_name}/environments/{env_name}/rollback">client.agents.environments.rollback.<a href="./src/sb0/resources/agents/environments/rollback.py">create</a>(env_name, \*, namespace_slug, agent_name, \*\*<a href="src/sb0/types/agents/environments/rollback_create_params.py">params</a>) -> <a href="./src/sb0/types/agents/environments/rollback_response.py">RollbackResponse</a></code>

## Secrets

Types:

```python
from sb0.types.agents import CrossEnvSecretResponse, CrossEnvSecretsListResponse, EnvSecretInfo
```

Methods:

- <code title="get /agents/{namespace_slug}/{agent_name}/secrets">client.agents.secrets.<a href="./src/sb0/resources/agents/secrets.py">list</a>(agent_name, \*, namespace_slug, \*\*<a href="src/sb0/types/agents/secret_list_params.py">params</a>) -> <a href="./src/sb0/types/agents/cross_env_secrets_list_response.py">CrossEnvSecretsListResponse</a></code>

# Deployments

Types:

```python
from sb0.types import (
    DeploymentAcpType,
    DeploymentListResponse,
    DeploymentResponse,
    DeploymentStatus,
    RedeployResponse,
    RegisterContainerRequest,
    RegisterContainerResponse,
    VersionListResponse,
    VersionResponse,
    VersionStatus,
    VersionSummary,
)
```

Methods:

- <code title="get /deployments/{deployment_id}">client.deployments.<a href="./src/sb0/resources/deployments/deployments.py">retrieve</a>(deployment_id) -> <a href="./src/sb0/types/deployment_response.py">DeploymentResponse</a></code>
- <code title="post /deployments/{deployment_id}/redeploy">client.deployments.<a href="./src/sb0/resources/deployments/deployments.py">redeploy</a>(deployment_id) -> <a href="./src/sb0/types/redeploy_response.py">RedeployResponse</a></code>
- <code title="post /deployments/register">client.deployments.<a href="./src/sb0/resources/deployments/deployments.py">register</a>(\*\*<a href="src/sb0/types/deployment_register_params.py">params</a>) -> <a href="./src/sb0/types/register_container_response.py">RegisterContainerResponse</a></code>
- <code title="post /deployments/{deployment_id}/rollback">client.deployments.<a href="./src/sb0/resources/deployments/deployments.py">rollback</a>(deployment_id, \*\*<a href="src/sb0/types/deployment_rollback_params.py">params</a>) -> <a href="./src/sb0/types/agents/environments/rollback_response.py">RollbackResponse</a></code>

## Versions

Methods:

- <code title="get /deployments/{deployment_id}/versions">client.deployments.versions.<a href="./src/sb0/resources/deployments/versions.py">list</a>(deployment_id, \*\*<a href="src/sb0/types/deployments/version_list_params.py">params</a>) -> <a href="./src/sb0/types/version_list_response.py">VersionListResponse</a></code>

## Events

Methods:

- <code title="get /deployments/{deployment_id}/events">client.deployments.events.<a href="./src/sb0/resources/deployments/events.py">list</a>(deployment_id, \*\*<a href="src/sb0/types/deployments/event_list_params.py">params</a>) -> <a href="./src/sb0/types/versions/version_event_list_response.py">VersionEventListResponse</a></code>

# Versions

Methods:

- <code title="get /versions/{version_id}">client.versions.<a href="./src/sb0/resources/versions/versions.py">retrieve</a>(version_id) -> <a href="./src/sb0/types/version_response.py">VersionResponse</a></code>

## Events

Types:

```python
from sb0.types.versions import (
    VersionEventContent,
    VersionEventListResponse,
    VersionEventResponse,
    VersionEventTrigger,
    VersionEventType,
)
```

Methods:

- <code title="get /versions/{version_id}/events">client.versions.events.<a href="./src/sb0/resources/versions/events.py">list</a>(version_id, \*\*<a href="src/sb0/types/versions/event_list_params.py">params</a>) -> <a href="./src/sb0/types/versions/version_event_list_response.py">VersionEventListResponse</a></code>

# Registry

Types:

```python
from sb0.types import RegistryAuthResponse
```

Methods:

- <code title="get /registry/auth">client.registry.<a href="./src/sb0/resources/registry.py">auth</a>(\*\*<a href="src/sb0/types/registry_auth_params.py">params</a>) -> <a href="./src/sb0/types/registry_auth_response.py">RegistryAuthResponse</a></code>

# Tasks

Types:

```python
from sb0.types import (
    ReasoningContentDelta,
    ReasoningSummaryDelta,
    Task,
    TaskMessage,
    TaskMessageContent,
    TaskMessageDelta,
    TaskMessageUpdate,
    TaskRelationships,
    TaskResponse,
    TaskStatus,
    TextDelta,
    ToolRequestDelta,
    ToolResponseDelta,
    UpdateTask,
    TaskListResponse,
)
```

Methods:

- <code title="get /tasks/{task_id}">client.tasks.<a href="./src/sb0/resources/tasks.py">retrieve</a>(task_id, \*\*<a href="src/sb0/types/task_retrieve_params.py">params</a>) -> <a href="./src/sb0/types/task_response.py">TaskResponse</a></code>
- <code title="put /tasks/{task_id}">client.tasks.<a href="./src/sb0/resources/tasks.py">update</a>(task_id, \*\*<a href="src/sb0/types/task_update_params.py">params</a>) -> <a href="./src/sb0/types/task.py">Task</a></code>
- <code title="get /tasks">client.tasks.<a href="./src/sb0/resources/tasks.py">list</a>(\*\*<a href="src/sb0/types/task_list_params.py">params</a>) -> <a href="./src/sb0/types/task_list_response.py">TaskListResponse</a></code>
- <code title="delete /tasks/{task_id}">client.tasks.<a href="./src/sb0/resources/tasks.py">delete</a>(task_id) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="delete /tasks/name/{task_name}">client.tasks.<a href="./src/sb0/resources/tasks.py">delete_by_name</a>(task_name) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="get /tasks/name/{task_name}">client.tasks.<a href="./src/sb0/resources/tasks.py">retrieve_by_name</a>(task_name, \*\*<a href="src/sb0/types/task_retrieve_by_name_params.py">params</a>) -> <a href="./src/sb0/types/task_response.py">TaskResponse</a></code>
- <code title="get /tasks/{task_id}/stream">client.tasks.<a href="./src/sb0/resources/tasks.py">stream_events</a>(task_id) -> object</code>
- <code title="get /tasks/name/{task_name}/stream">client.tasks.<a href="./src/sb0/resources/tasks.py">stream_events_by_name</a>(task_name) -> object</code>
- <code title="put /tasks/name/{task_name}">client.tasks.<a href="./src/sb0/resources/tasks.py">update_by_name</a>(task_name, \*\*<a href="src/sb0/types/task_update_by_name_params.py">params</a>) -> <a href="./src/sb0/types/task.py">Task</a></code>

# Messages

Types:

```python
from sb0.types import (
    ClaudeMessageContent,
    DataContent,
    DataDelta,
    FileAttachment,
    MessageAuthor,
    MessageStyle,
    PaginatedMessagesResponse,
    ReasoningContent,
    TextContent,
    TextFormat,
    ToolRequestContent,
    ToolResponseContent,
    MessageListResponse,
)
```

Methods:

- <code title="post /messages">client.messages.<a href="./src/sb0/resources/messages/messages.py">create</a>(\*\*<a href="src/sb0/types/message_create_params.py">params</a>) -> <a href="./src/sb0/types/task_message.py">TaskMessage</a></code>
- <code title="get /messages/{message_id}">client.messages.<a href="./src/sb0/resources/messages/messages.py">retrieve</a>(message_id) -> <a href="./src/sb0/types/task_message.py">TaskMessage</a></code>
- <code title="put /messages/{message_id}">client.messages.<a href="./src/sb0/resources/messages/messages.py">update</a>(message_id, \*\*<a href="src/sb0/types/message_update_params.py">params</a>) -> <a href="./src/sb0/types/task_message.py">TaskMessage</a></code>
- <code title="get /messages">client.messages.<a href="./src/sb0/resources/messages/messages.py">list</a>(\*\*<a href="src/sb0/types/message_list_params.py">params</a>) -> <a href="./src/sb0/types/message_list_response.py">MessageListResponse</a></code>
- <code title="get /messages/paginated">client.messages.<a href="./src/sb0/resources/messages/messages.py">list_paginated</a>(\*\*<a href="src/sb0/types/message_list_paginated_params.py">params</a>) -> <a href="./src/sb0/types/paginated_messages_response.py">PaginatedMessagesResponse</a></code>

## Batch

Types:

```python
from sb0.types.messages import BatchCreateResponse, BatchUpdateResponse
```

Methods:

- <code title="post /messages/batch">client.messages.batch.<a href="./src/sb0/resources/messages/batch.py">create</a>(\*\*<a href="src/sb0/types/messages/batch_create_params.py">params</a>) -> <a href="./src/sb0/types/messages/batch_create_response.py">BatchCreateResponse</a></code>
- <code title="put /messages/batch">client.messages.batch.<a href="./src/sb0/resources/messages/batch.py">update</a>(\*\*<a href="src/sb0/types/messages/batch_update_params.py">params</a>) -> <a href="./src/sb0/types/messages/batch_update_response.py">BatchUpdateResponse</a></code>

# Spans

Types:

```python
from sb0.types import Span, SpanListResponse
```

Methods:

- <code title="post /spans">client.spans.<a href="./src/sb0/resources/spans.py">create</a>(\*\*<a href="src/sb0/types/span_create_params.py">params</a>) -> <a href="./src/sb0/types/span.py">Span</a></code>
- <code title="get /spans/{span_id}">client.spans.<a href="./src/sb0/resources/spans.py">retrieve</a>(span_id) -> <a href="./src/sb0/types/span.py">Span</a></code>
- <code title="patch /spans/{span_id}">client.spans.<a href="./src/sb0/resources/spans.py">update</a>(span_id, \*\*<a href="src/sb0/types/span_update_params.py">params</a>) -> <a href="./src/sb0/types/span.py">Span</a></code>
- <code title="get /spans">client.spans.<a href="./src/sb0/resources/spans.py">list</a>(\*\*<a href="src/sb0/types/span_list_params.py">params</a>) -> <a href="./src/sb0/types/span_list_response.py">SpanListResponse</a></code>

# States

Types:

```python
from sb0.types import State, StateListResponse
```

Methods:

- <code title="post /states">client.states.<a href="./src/sb0/resources/states.py">create</a>(\*\*<a href="src/sb0/types/state_create_params.py">params</a>) -> <a href="./src/sb0/types/state.py">State</a></code>
- <code title="get /states/{state_id}">client.states.<a href="./src/sb0/resources/states.py">retrieve</a>(state_id) -> <a href="./src/sb0/types/state.py">State</a></code>
- <code title="put /states/{state_id}">client.states.<a href="./src/sb0/resources/states.py">update</a>(state_id, \*\*<a href="src/sb0/types/state_update_params.py">params</a>) -> <a href="./src/sb0/types/state.py">State</a></code>
- <code title="get /states">client.states.<a href="./src/sb0/resources/states.py">list</a>(\*\*<a href="src/sb0/types/state_list_params.py">params</a>) -> <a href="./src/sb0/types/state_list_response.py">StateListResponse</a></code>
- <code title="delete /states/{state_id}">client.states.<a href="./src/sb0/resources/states.py">delete</a>(state_id) -> <a href="./src/sb0/types/state.py">State</a></code>

# Events

Types:

```python
from sb0.types import Event, EventListResponse
```

Methods:

- <code title="get /events/{event_id}">client.events.<a href="./src/sb0/resources/events.py">retrieve</a>(event_id) -> <a href="./src/sb0/types/event.py">Event</a></code>
- <code title="get /events">client.events.<a href="./src/sb0/resources/events.py">list</a>(\*\*<a href="src/sb0/types/event_list_params.py">params</a>) -> <a href="./src/sb0/types/event_list_response.py">EventListResponse</a></code>

# Logs

Types:

```python
from sb0.types import (
    LogAuthResponse,
    LogEntry,
    LogIngestionRequest,
    LogIngestionResponse,
    LogSource,
)
```

Methods:

- <code title="get /logs/auth">client.logs.<a href="./src/sb0/resources/logs.py">auth</a>(\*\*<a href="src/sb0/types/log_auth_params.py">params</a>) -> <a href="./src/sb0/types/log_auth_response.py">LogAuthResponse</a></code>
- <code title="post /logs">client.logs.<a href="./src/sb0/resources/logs.py">ingest</a>(\*\*<a href="src/sb0/types/log_ingest_params.py">params</a>) -> <a href="./src/sb0/types/log_ingestion_response.py">LogIngestionResponse</a></code>

# Tracker

Types:

```python
from sb0.types import AgentTaskTracker, TrackerListResponse
```

Methods:

- <code title="get /tracker/{tracker_id}">client.tracker.<a href="./src/sb0/resources/tracker.py">retrieve</a>(tracker_id) -> <a href="./src/sb0/types/agent_task_tracker.py">AgentTaskTracker</a></code>
- <code title="put /tracker/{tracker_id}">client.tracker.<a href="./src/sb0/resources/tracker.py">update</a>(tracker_id, \*\*<a href="src/sb0/types/tracker_update_params.py">params</a>) -> <a href="./src/sb0/types/agent_task_tracker.py">AgentTaskTracker</a></code>
- <code title="get /tracker">client.tracker.<a href="./src/sb0/resources/tracker.py">list</a>(\*\*<a href="src/sb0/types/tracker_list_params.py">params</a>) -> <a href="./src/sb0/types/tracker_list_response.py">TrackerListResponse</a></code>

# AgentAPIKeys

Types:

```python
from sb0.types import (
    AgentAPIKey,
    AgentAPIKeyType,
    CreateAPIKeyResponse,
    AgentAPIKeyListResponse,
    AgentAPIKeyDeleteResponse,
)
```

Methods:

- <code title="post /agent_api_keys">client.agent_api_keys.<a href="./src/sb0/resources/agent_api_keys/agent_api_keys.py">create</a>(\*\*<a href="src/sb0/types/agent_api_key_create_params.py">params</a>) -> <a href="./src/sb0/types/create_api_key_response.py">CreateAPIKeyResponse</a></code>
- <code title="get /agent_api_keys/{id}">client.agent_api_keys.<a href="./src/sb0/resources/agent_api_keys/agent_api_keys.py">retrieve</a>(id) -> <a href="./src/sb0/types/agent_api_key.py">AgentAPIKey</a></code>
- <code title="get /agent_api_keys">client.agent_api_keys.<a href="./src/sb0/resources/agent_api_keys/agent_api_keys.py">list</a>(\*\*<a href="src/sb0/types/agent_api_key_list_params.py">params</a>) -> <a href="./src/sb0/types/agent_api_key_list_response.py">AgentAPIKeyListResponse</a></code>
- <code title="delete /agent_api_keys/{id}">client.agent_api_keys.<a href="./src/sb0/resources/agent_api_keys/agent_api_keys.py">delete</a>(id) -> str</code>

## Name

Types:

```python
from sb0.types.agent_api_keys import NameDeleteResponse
```

Methods:

- <code title="get /agent_api_keys/name/{name}">client.agent_api_keys.name.<a href="./src/sb0/resources/agent_api_keys/name.py">retrieve</a>(name, \*\*<a href="src/sb0/types/agent_api_keys/name_retrieve_params.py">params</a>) -> <a href="./src/sb0/types/agent_api_key.py">AgentAPIKey</a></code>
- <code title="delete /agent_api_keys/name/{api_key_name}">client.agent_api_keys.name.<a href="./src/sb0/resources/agent_api_keys/name.py">delete</a>(api_key_name, \*\*<a href="src/sb0/types/agent_api_keys/name_delete_params.py">params</a>) -> str</code>

# Namespaces

Types:

```python
from sb0.types import (
    CreateNamespaceRequest,
    Namespace,
    UpdateNamespaceRequest,
    NamespaceListResponse,
)
```

Methods:

- <code title="post /namespaces">client.namespaces.<a href="./src/sb0/resources/namespaces.py">create</a>(\*\*<a href="src/sb0/types/namespace_create_params.py">params</a>) -> <a href="./src/sb0/types/namespace.py">Namespace</a></code>
- <code title="get /namespaces/{namespace_id}">client.namespaces.<a href="./src/sb0/resources/namespaces.py">retrieve</a>(namespace_id) -> <a href="./src/sb0/types/namespace.py">Namespace</a></code>
- <code title="patch /namespaces/{namespace_id}">client.namespaces.<a href="./src/sb0/resources/namespaces.py">update</a>(namespace_id, \*\*<a href="src/sb0/types/namespace_update_params.py">params</a>) -> <a href="./src/sb0/types/namespace.py">Namespace</a></code>
- <code title="get /namespaces">client.namespaces.<a href="./src/sb0/resources/namespaces.py">list</a>(\*\*<a href="src/sb0/types/namespace_list_params.py">params</a>) -> <a href="./src/sb0/types/namespace_list_response.py">NamespaceListResponse</a></code>
- <code title="delete /namespaces/{namespace_id}">client.namespaces.<a href="./src/sb0/resources/namespaces.py">delete</a>(namespace_id) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>
- <code title="get /namespaces/slug/{slug}">client.namespaces.<a href="./src/sb0/resources/namespaces.py">retrieve_by_slug</a>(slug) -> <a href="./src/sb0/types/namespace.py">Namespace</a></code>

# Projects

Types:

```python
from sb0.types import CreateProjectRequest, Project, UpdateProjectRequest, ProjectListResponse
```

Methods:

- <code title="post /projects">client.projects.<a href="./src/sb0/resources/projects.py">create</a>(\*\*<a href="src/sb0/types/project_create_params.py">params</a>) -> <a href="./src/sb0/types/project.py">Project</a></code>
- <code title="get /projects/{project_id}">client.projects.<a href="./src/sb0/resources/projects.py">retrieve</a>(project_id) -> <a href="./src/sb0/types/project.py">Project</a></code>
- <code title="patch /projects/{project_id}">client.projects.<a href="./src/sb0/resources/projects.py">update</a>(project_id, \*\*<a href="src/sb0/types/project_update_params.py">params</a>) -> <a href="./src/sb0/types/project.py">Project</a></code>
- <code title="get /projects">client.projects.<a href="./src/sb0/resources/projects.py">list</a>(\*\*<a href="src/sb0/types/project_list_params.py">params</a>) -> <a href="./src/sb0/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /projects/{project_id}">client.projects.<a href="./src/sb0/resources/projects.py">delete</a>(project_id) -> <a href="./src/sb0/types/delete_response.py">DeleteResponse</a></code>

# Workspaces

Types:

```python
from sb0.types import (
    PresignedURLRequest,
    PresignedURLResponse,
    SyncCompleteRequest,
    SyncCompleteResponse,
    WorkspaceCreate,
    WorkspaceDirectory,
    WorkspaceFile,
    WorkspaceFileResponse,
    WorkspaceResponse,
    WorkspaceStatus,
    WorkspaceListResponse,
    WorkspaceListFilesResponse,
)
```

Methods:

- <code title="post /workspaces">client.workspaces.<a href="./src/sb0/resources/workspaces.py">create</a>(\*\*<a href="src/sb0/types/workspace_create_params.py">params</a>) -> <a href="./src/sb0/types/workspace_response.py">WorkspaceResponse</a></code>
- <code title="get /workspaces/{workspace_id}">client.workspaces.<a href="./src/sb0/resources/workspaces.py">retrieve</a>(workspace_id) -> <a href="./src/sb0/types/workspace_response.py">WorkspaceResponse</a></code>
- <code title="get /workspaces">client.workspaces.<a href="./src/sb0/resources/workspaces.py">list</a>() -> <a href="./src/sb0/types/workspace_list_response.py">WorkspaceListResponse</a></code>
- <code title="post /workspaces/{workspace_id}/download-url">client.workspaces.<a href="./src/sb0/resources/workspaces.py">get_download_url</a>(workspace_id, \*\*<a href="src/sb0/types/workspace_get_download_url_params.py">params</a>) -> <a href="./src/sb0/types/presigned_url_response.py">PresignedURLResponse</a></code>
- <code title="get /workspaces/{workspace_id}/files/{file_path}">client.workspaces.<a href="./src/sb0/resources/workspaces.py">get_file</a>(file_path, \*, workspace_id, \*\*<a href="src/sb0/types/workspace_get_file_params.py">params</a>) -> <a href="./src/sb0/types/workspace_file_response.py">WorkspaceFileResponse</a></code>
- <code title="post /workspaces/{workspace_id}/upload-url">client.workspaces.<a href="./src/sb0/resources/workspaces.py">get_upload_url</a>(workspace_id, \*\*<a href="src/sb0/types/workspace_get_upload_url_params.py">params</a>) -> <a href="./src/sb0/types/presigned_url_response.py">PresignedURLResponse</a></code>
- <code title="get /workspaces/{workspace_id}/files">client.workspaces.<a href="./src/sb0/resources/workspaces.py">list_files</a>(workspace_id, \*\*<a href="src/sb0/types/workspace_list_files_params.py">params</a>) -> <a href="./src/sb0/types/workspace_list_files_response.py">WorkspaceListFilesResponse</a></code>
- <code title="post /workspaces/{workspace_id}/sync-complete">client.workspaces.<a href="./src/sb0/resources/workspaces.py">sync_complete</a>(workspace_id, \*\*<a href="src/sb0/types/workspace_sync_complete_params.py">params</a>) -> <a href="./src/sb0/types/sync_complete_response.py">SyncCompleteResponse</a></code>
