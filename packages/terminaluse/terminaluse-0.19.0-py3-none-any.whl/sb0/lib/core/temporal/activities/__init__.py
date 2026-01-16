import httpx

from sb0 import AsyncSb0  # noqa: F401
from sb0.lib.core.tracing import AsyncTracer
from sb0.lib.core.services.adk.state import StateService
from sb0.lib.core.services.adk.tasks import TasksService
from sb0.lib.core.services.adk.events import EventsService
from sb0.lib.adk.utils._modules.client import create_async_sb0_client
from sb0.lib.core.services.adk.acp.acp import ACPService
from sb0.lib.core.services.adk.tracing import TracingService
from sb0.lib.core.services.adk.messages import MessagesService
from sb0.lib.core.services.adk.streaming import StreamingService
from sb0.lib.core.adapters.llm.adapter_litellm import LiteLLMGateway
from sb0.lib.core.services.adk.providers.openai import OpenAIService
from sb0.lib.core.services.adk.utils.templating import TemplatingService
from sb0.lib.core.adapters.streams.adapter_redis import RedisStreamRepository
from sb0.lib.core.services.adk.providers.litellm import LiteLLMService
from sb0.lib.core.services.adk.agent_task_tracker import AgentTaskTrackerService
from sb0.lib.core.temporal.activities.adk.state_activities import StateActivities
from sb0.lib.core.temporal.activities.adk.tasks_activities import TasksActivities
from sb0.lib.core.temporal.activities.adk.events_activities import EventsActivities
from sb0.lib.core.temporal.activities.adk.acp.acp_activities import ACPActivities
from sb0.lib.core.temporal.activities.adk.tracing_activities import TracingActivities
from sb0.lib.core.temporal.activities.adk.messages_activities import MessagesActivities
from sb0.lib.core.temporal.activities.adk.streaming_activities import (
    StreamingActivities,
)
from sb0.lib.core.temporal.activities.adk.providers.openai_activities import (
    OpenAIActivities,
)
from sb0.lib.core.temporal.activities.adk.utils.templating_activities import (
    TemplatingActivities,
)
from sb0.lib.core.temporal.activities.adk.providers.litellm_activities import (
    LiteLLMActivities,
)
from sb0.lib.core.temporal.activities.adk.agent_task_tracker_activities import (
    AgentTaskTrackerActivities,
)


def get_all_activities():
    """
    Returns a list of all standard activity functions that can be directly passed to worker.run().

    Returns:
        list: A list of activity functions ready to be passed to worker.run()
    """
    # Initialize common dependencies
    llm_gateway = LiteLLMGateway()
    stream_repository = RedisStreamRepository()
    sb0_client = create_async_sb0_client(
        timeout=httpx.Timeout(timeout=1000),
    )
    tracer = AsyncTracer(sb0_client)

    # Services

    ## ADK
    streaming_service = StreamingService(
        sb0_client=sb0_client,
        stream_repository=stream_repository,
    )
    messages_service = MessagesService(
        sb0_client=sb0_client,
        streaming_service=streaming_service,
        tracer=tracer,
    )
    events_service = EventsService(
        sb0_client=sb0_client,
        tracer=tracer,
    )
    agent_task_tracker_service = AgentTaskTrackerService(
        sb0_client=sb0_client,
        tracer=tracer,
    )
    state_service = StateService(
        sb0_client=sb0_client,
        tracer=tracer,
    )
    tasks_service = TasksService(
        sb0_client=sb0_client,
        tracer=tracer,
    )
    tracing_service = TracingService(
        tracer=tracer,
    )

    ## ACP
    acp_service = ACPService(
        sb0_client=sb0_client,
        tracer=tracer,
    )

    ## Providers
    litellm_service = LiteLLMService(
        sb0_client=sb0_client,
        llm_gateway=llm_gateway,
        streaming_service=streaming_service,
        tracer=tracer,
    )
    openai_service = OpenAIService(
        sb0_client=sb0_client,
        streaming_service=streaming_service,
        tracer=tracer,
    )

    ## Utils
    templating_service = TemplatingService(
        tracer=tracer,
    )

    # ADK

    ## Core activities
    messages_activities = MessagesActivities(messages_service=messages_service)
    events_activities = EventsActivities(events_service=events_service)
    agent_task_tracker_activities = AgentTaskTrackerActivities(agent_task_tracker_service=agent_task_tracker_service)
    state_activities = StateActivities(state_service=state_service)
    streaming_activities = StreamingActivities(streaming_service=streaming_service)
    tasks_activities = TasksActivities(tasks_service=tasks_service)
    tracing_activities = TracingActivities(tracing_service=tracing_service)

    ## ACP
    acp_activities = ACPActivities(acp_service=acp_service)

    ## Providers
    litellm_activities = LiteLLMActivities(litellm_service=litellm_service)
    openai_activities = OpenAIActivities(openai_service=openai_service)

    ## Utils
    templating_activities = TemplatingActivities(templating_service=templating_service)

    # Build list of standard activities
    activities = [
        # Core activities
        ## Messages activities
        messages_activities.create_message,
        messages_activities.update_message,
        messages_activities.create_messages_batch,
        messages_activities.update_messages_batch,
        messages_activities.list_messages,
        ## Events activities
        events_activities.get_event,
        events_activities.list_events,
        ## Agent Task Tracker activities
        agent_task_tracker_activities.get_agent_task_tracker,
        agent_task_tracker_activities.get_agent_task_tracker_by_task_and_agent,
        agent_task_tracker_activities.update_agent_task_tracker,
        ## State activities
        state_activities.create_state,
        state_activities.get_state,
        state_activities.update_state,
        state_activities.delete_state,
        ## Streaming activities
        streaming_activities.stream_update,
        ## Tasks activities
        tasks_activities.get_task,
        tasks_activities.delete_task,
        ## Tracing activities
        tracing_activities.start_span,
        tracing_activities.end_span,
        # ACP activities
        acp_activities.task_create,
        acp_activities.message_send,
        acp_activities.event_send,
        acp_activities.task_cancel,
        # Providers
        ## LiteLLM activities
        litellm_activities.chat_completion,
        litellm_activities.chat_completion_auto_send,
        litellm_activities.chat_completion_stream_auto_send,
        ## OpenAI activities
        openai_activities.run_agent,
        openai_activities.run_agent_auto_send,
        openai_activities.run_agent_streamed_auto_send,
        # Utils
        templating_activities.render_jinja,
    ]

    return activities
