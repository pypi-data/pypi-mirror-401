# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Literal, Mapping, cast
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import (
        logs,
        spans,
        tasks,
        agents,
        events,
        states,
        tracker,
        messages,
        projects,
        registry,
        versions,
        namespaces,
        workspaces,
        deployments,
        agent_api_keys,
    )
    from .resources.logs import LogsResource, AsyncLogsResource
    from .resources.spans import SpansResource, AsyncSpansResource
    from .resources.tasks import TasksResource, AsyncTasksResource
    from .resources.events import EventsResource, AsyncEventsResource
    from .resources.states import StatesResource, AsyncStatesResource
    from .resources.tracker import TrackerResource, AsyncTrackerResource
    from .resources.projects import ProjectsResource, AsyncProjectsResource
    from .resources.registry import RegistryResource, AsyncRegistryResource
    from .resources.namespaces import NamespacesResource, AsyncNamespacesResource
    from .resources.workspaces import WorkspacesResource, AsyncWorkspacesResource
    from .resources.agents.agents import AgentsResource, AsyncAgentsResource
    from .resources.messages.messages import MessagesResource, AsyncMessagesResource
    from .resources.versions.versions import VersionsResource, AsyncVersionsResource
    from .resources.deployments.deployments import DeploymentsResource, AsyncDeploymentsResource
    from .resources.agent_api_keys.agent_api_keys import AgentAPIKeysResource, AsyncAgentAPIKeysResource

__all__ = ["ENVIRONMENTS", "Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Sb0", "AsyncSb0", "Client", "AsyncClient"]

ENVIRONMENTS: Dict[str, str] = {
    "production": "http://localhost:5003",
    "development": "http://localhost:5003",
}


class Sb0(SyncAPIClient):
    # client options
    api_key: str | None
    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        environment: Literal["production", "development"] | NotGiven = not_given,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Sb0 client instance.

        This automatically infers the `api_key` argument from the `SB0_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("SB0_API_KEY")
        self.api_key = api_key

        self._environment = environment

        base_url_env = os.environ.get("SB0_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `SB0_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def agents(self) -> AgentsResource:
        from .resources.agents import AgentsResource

        return AgentsResource(self)

    @cached_property
    def deployments(self) -> DeploymentsResource:
        from .resources.deployments import DeploymentsResource

        return DeploymentsResource(self)

    @cached_property
    def versions(self) -> VersionsResource:
        from .resources.versions import VersionsResource

        return VersionsResource(self)

    @cached_property
    def registry(self) -> RegistryResource:
        from .resources.registry import RegistryResource

        return RegistryResource(self)

    @cached_property
    def tasks(self) -> TasksResource:
        from .resources.tasks import TasksResource

        return TasksResource(self)

    @cached_property
    def messages(self) -> MessagesResource:
        from .resources.messages import MessagesResource

        return MessagesResource(self)

    @cached_property
    def spans(self) -> SpansResource:
        from .resources.spans import SpansResource

        return SpansResource(self)

    @cached_property
    def states(self) -> StatesResource:
        from .resources.states import StatesResource

        return StatesResource(self)

    @cached_property
    def events(self) -> EventsResource:
        from .resources.events import EventsResource

        return EventsResource(self)

    @cached_property
    def logs(self) -> LogsResource:
        from .resources.logs import LogsResource

        return LogsResource(self)

    @cached_property
    def tracker(self) -> TrackerResource:
        from .resources.tracker import TrackerResource

        return TrackerResource(self)

    @cached_property
    def agent_api_keys(self) -> AgentAPIKeysResource:
        from .resources.agent_api_keys import AgentAPIKeysResource

        return AgentAPIKeysResource(self)

    @cached_property
    def namespaces(self) -> NamespacesResource:
        from .resources.namespaces import NamespacesResource

        return NamespacesResource(self)

    @cached_property
    def projects(self) -> ProjectsResource:
        from .resources.projects import ProjectsResource

        return ProjectsResource(self)

    @cached_property
    def workspaces(self) -> WorkspacesResource:
        from .resources.workspaces import WorkspacesResource

        return WorkspacesResource(self)

    @cached_property
    def with_raw_response(self) -> Sb0WithRawResponse:
        return Sb0WithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Sb0WithStreamedResponse:
        return Sb0WithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }


    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSb0(AsyncAPIClient):
    # client options
    api_key: str | None
    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        environment: Literal["production", "development"] | NotGiven = not_given,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncSb0 client instance.

        This automatically infers the `api_key` argument from the `SB0_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("SB0_API_KEY")
        self.api_key = api_key

        self._environment = environment

        base_url_env = os.environ.get("SB0_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `SB0_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def agents(self) -> AsyncAgentsResource:
        from .resources.agents import AsyncAgentsResource

        return AsyncAgentsResource(self)

    @cached_property
    def deployments(self) -> AsyncDeploymentsResource:
        from .resources.deployments import AsyncDeploymentsResource

        return AsyncDeploymentsResource(self)

    @cached_property
    def versions(self) -> AsyncVersionsResource:
        from .resources.versions import AsyncVersionsResource

        return AsyncVersionsResource(self)

    @cached_property
    def registry(self) -> AsyncRegistryResource:
        from .resources.registry import AsyncRegistryResource

        return AsyncRegistryResource(self)

    @cached_property
    def tasks(self) -> AsyncTasksResource:
        from .resources.tasks import AsyncTasksResource

        return AsyncTasksResource(self)

    @cached_property
    def messages(self) -> AsyncMessagesResource:
        from .resources.messages import AsyncMessagesResource

        return AsyncMessagesResource(self)

    @cached_property
    def spans(self) -> AsyncSpansResource:
        from .resources.spans import AsyncSpansResource

        return AsyncSpansResource(self)

    @cached_property
    def states(self) -> AsyncStatesResource:
        from .resources.states import AsyncStatesResource

        return AsyncStatesResource(self)

    @cached_property
    def events(self) -> AsyncEventsResource:
        from .resources.events import AsyncEventsResource

        return AsyncEventsResource(self)

    @cached_property
    def logs(self) -> AsyncLogsResource:
        from .resources.logs import AsyncLogsResource

        return AsyncLogsResource(self)

    @cached_property
    def tracker(self) -> AsyncTrackerResource:
        from .resources.tracker import AsyncTrackerResource

        return AsyncTrackerResource(self)

    @cached_property
    def agent_api_keys(self) -> AsyncAgentAPIKeysResource:
        from .resources.agent_api_keys import AsyncAgentAPIKeysResource

        return AsyncAgentAPIKeysResource(self)

    @cached_property
    def namespaces(self) -> AsyncNamespacesResource:
        from .resources.namespaces import AsyncNamespacesResource

        return AsyncNamespacesResource(self)

    @cached_property
    def projects(self) -> AsyncProjectsResource:
        from .resources.projects import AsyncProjectsResource

        return AsyncProjectsResource(self)

    @cached_property
    def workspaces(self) -> AsyncWorkspacesResource:
        from .resources.workspaces import AsyncWorkspacesResource

        return AsyncWorkspacesResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncSb0WithRawResponse:
        return AsyncSb0WithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSb0WithStreamedResponse:
        return AsyncSb0WithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }


    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class Sb0WithRawResponse:
    _client: Sb0

    def __init__(self, client: Sb0) -> None:
        self._client = client

    @cached_property
    def agents(self) -> agents.AgentsResourceWithRawResponse:
        from .resources.agents import AgentsResourceWithRawResponse

        return AgentsResourceWithRawResponse(self._client.agents)

    @cached_property
    def deployments(self) -> deployments.DeploymentsResourceWithRawResponse:
        from .resources.deployments import DeploymentsResourceWithRawResponse

        return DeploymentsResourceWithRawResponse(self._client.deployments)

    @cached_property
    def versions(self) -> versions.VersionsResourceWithRawResponse:
        from .resources.versions import VersionsResourceWithRawResponse

        return VersionsResourceWithRawResponse(self._client.versions)

    @cached_property
    def registry(self) -> registry.RegistryResourceWithRawResponse:
        from .resources.registry import RegistryResourceWithRawResponse

        return RegistryResourceWithRawResponse(self._client.registry)

    @cached_property
    def tasks(self) -> tasks.TasksResourceWithRawResponse:
        from .resources.tasks import TasksResourceWithRawResponse

        return TasksResourceWithRawResponse(self._client.tasks)

    @cached_property
    def messages(self) -> messages.MessagesResourceWithRawResponse:
        from .resources.messages import MessagesResourceWithRawResponse

        return MessagesResourceWithRawResponse(self._client.messages)

    @cached_property
    def spans(self) -> spans.SpansResourceWithRawResponse:
        from .resources.spans import SpansResourceWithRawResponse

        return SpansResourceWithRawResponse(self._client.spans)

    @cached_property
    def states(self) -> states.StatesResourceWithRawResponse:
        from .resources.states import StatesResourceWithRawResponse

        return StatesResourceWithRawResponse(self._client.states)

    @cached_property
    def events(self) -> events.EventsResourceWithRawResponse:
        from .resources.events import EventsResourceWithRawResponse

        return EventsResourceWithRawResponse(self._client.events)

    @cached_property
    def logs(self) -> logs.LogsResourceWithRawResponse:
        from .resources.logs import LogsResourceWithRawResponse

        return LogsResourceWithRawResponse(self._client.logs)

    @cached_property
    def tracker(self) -> tracker.TrackerResourceWithRawResponse:
        from .resources.tracker import TrackerResourceWithRawResponse

        return TrackerResourceWithRawResponse(self._client.tracker)

    @cached_property
    def agent_api_keys(self) -> agent_api_keys.AgentAPIKeysResourceWithRawResponse:
        from .resources.agent_api_keys import AgentAPIKeysResourceWithRawResponse

        return AgentAPIKeysResourceWithRawResponse(self._client.agent_api_keys)

    @cached_property
    def namespaces(self) -> namespaces.NamespacesResourceWithRawResponse:
        from .resources.namespaces import NamespacesResourceWithRawResponse

        return NamespacesResourceWithRawResponse(self._client.namespaces)

    @cached_property
    def projects(self) -> projects.ProjectsResourceWithRawResponse:
        from .resources.projects import ProjectsResourceWithRawResponse

        return ProjectsResourceWithRawResponse(self._client.projects)

    @cached_property
    def workspaces(self) -> workspaces.WorkspacesResourceWithRawResponse:
        from .resources.workspaces import WorkspacesResourceWithRawResponse

        return WorkspacesResourceWithRawResponse(self._client.workspaces)


class AsyncSb0WithRawResponse:
    _client: AsyncSb0

    def __init__(self, client: AsyncSb0) -> None:
        self._client = client

    @cached_property
    def agents(self) -> agents.AsyncAgentsResourceWithRawResponse:
        from .resources.agents import AsyncAgentsResourceWithRawResponse

        return AsyncAgentsResourceWithRawResponse(self._client.agents)

    @cached_property
    def deployments(self) -> deployments.AsyncDeploymentsResourceWithRawResponse:
        from .resources.deployments import AsyncDeploymentsResourceWithRawResponse

        return AsyncDeploymentsResourceWithRawResponse(self._client.deployments)

    @cached_property
    def versions(self) -> versions.AsyncVersionsResourceWithRawResponse:
        from .resources.versions import AsyncVersionsResourceWithRawResponse

        return AsyncVersionsResourceWithRawResponse(self._client.versions)

    @cached_property
    def registry(self) -> registry.AsyncRegistryResourceWithRawResponse:
        from .resources.registry import AsyncRegistryResourceWithRawResponse

        return AsyncRegistryResourceWithRawResponse(self._client.registry)

    @cached_property
    def tasks(self) -> tasks.AsyncTasksResourceWithRawResponse:
        from .resources.tasks import AsyncTasksResourceWithRawResponse

        return AsyncTasksResourceWithRawResponse(self._client.tasks)

    @cached_property
    def messages(self) -> messages.AsyncMessagesResourceWithRawResponse:
        from .resources.messages import AsyncMessagesResourceWithRawResponse

        return AsyncMessagesResourceWithRawResponse(self._client.messages)

    @cached_property
    def spans(self) -> spans.AsyncSpansResourceWithRawResponse:
        from .resources.spans import AsyncSpansResourceWithRawResponse

        return AsyncSpansResourceWithRawResponse(self._client.spans)

    @cached_property
    def states(self) -> states.AsyncStatesResourceWithRawResponse:
        from .resources.states import AsyncStatesResourceWithRawResponse

        return AsyncStatesResourceWithRawResponse(self._client.states)

    @cached_property
    def events(self) -> events.AsyncEventsResourceWithRawResponse:
        from .resources.events import AsyncEventsResourceWithRawResponse

        return AsyncEventsResourceWithRawResponse(self._client.events)

    @cached_property
    def logs(self) -> logs.AsyncLogsResourceWithRawResponse:
        from .resources.logs import AsyncLogsResourceWithRawResponse

        return AsyncLogsResourceWithRawResponse(self._client.logs)

    @cached_property
    def tracker(self) -> tracker.AsyncTrackerResourceWithRawResponse:
        from .resources.tracker import AsyncTrackerResourceWithRawResponse

        return AsyncTrackerResourceWithRawResponse(self._client.tracker)

    @cached_property
    def agent_api_keys(self) -> agent_api_keys.AsyncAgentAPIKeysResourceWithRawResponse:
        from .resources.agent_api_keys import AsyncAgentAPIKeysResourceWithRawResponse

        return AsyncAgentAPIKeysResourceWithRawResponse(self._client.agent_api_keys)

    @cached_property
    def namespaces(self) -> namespaces.AsyncNamespacesResourceWithRawResponse:
        from .resources.namespaces import AsyncNamespacesResourceWithRawResponse

        return AsyncNamespacesResourceWithRawResponse(self._client.namespaces)

    @cached_property
    def projects(self) -> projects.AsyncProjectsResourceWithRawResponse:
        from .resources.projects import AsyncProjectsResourceWithRawResponse

        return AsyncProjectsResourceWithRawResponse(self._client.projects)

    @cached_property
    def workspaces(self) -> workspaces.AsyncWorkspacesResourceWithRawResponse:
        from .resources.workspaces import AsyncWorkspacesResourceWithRawResponse

        return AsyncWorkspacesResourceWithRawResponse(self._client.workspaces)


class Sb0WithStreamedResponse:
    _client: Sb0

    def __init__(self, client: Sb0) -> None:
        self._client = client

    @cached_property
    def agents(self) -> agents.AgentsResourceWithStreamingResponse:
        from .resources.agents import AgentsResourceWithStreamingResponse

        return AgentsResourceWithStreamingResponse(self._client.agents)

    @cached_property
    def deployments(self) -> deployments.DeploymentsResourceWithStreamingResponse:
        from .resources.deployments import DeploymentsResourceWithStreamingResponse

        return DeploymentsResourceWithStreamingResponse(self._client.deployments)

    @cached_property
    def versions(self) -> versions.VersionsResourceWithStreamingResponse:
        from .resources.versions import VersionsResourceWithStreamingResponse

        return VersionsResourceWithStreamingResponse(self._client.versions)

    @cached_property
    def registry(self) -> registry.RegistryResourceWithStreamingResponse:
        from .resources.registry import RegistryResourceWithStreamingResponse

        return RegistryResourceWithStreamingResponse(self._client.registry)

    @cached_property
    def tasks(self) -> tasks.TasksResourceWithStreamingResponse:
        from .resources.tasks import TasksResourceWithStreamingResponse

        return TasksResourceWithStreamingResponse(self._client.tasks)

    @cached_property
    def messages(self) -> messages.MessagesResourceWithStreamingResponse:
        from .resources.messages import MessagesResourceWithStreamingResponse

        return MessagesResourceWithStreamingResponse(self._client.messages)

    @cached_property
    def spans(self) -> spans.SpansResourceWithStreamingResponse:
        from .resources.spans import SpansResourceWithStreamingResponse

        return SpansResourceWithStreamingResponse(self._client.spans)

    @cached_property
    def states(self) -> states.StatesResourceWithStreamingResponse:
        from .resources.states import StatesResourceWithStreamingResponse

        return StatesResourceWithStreamingResponse(self._client.states)

    @cached_property
    def events(self) -> events.EventsResourceWithStreamingResponse:
        from .resources.events import EventsResourceWithStreamingResponse

        return EventsResourceWithStreamingResponse(self._client.events)

    @cached_property
    def logs(self) -> logs.LogsResourceWithStreamingResponse:
        from .resources.logs import LogsResourceWithStreamingResponse

        return LogsResourceWithStreamingResponse(self._client.logs)

    @cached_property
    def tracker(self) -> tracker.TrackerResourceWithStreamingResponse:
        from .resources.tracker import TrackerResourceWithStreamingResponse

        return TrackerResourceWithStreamingResponse(self._client.tracker)

    @cached_property
    def agent_api_keys(self) -> agent_api_keys.AgentAPIKeysResourceWithStreamingResponse:
        from .resources.agent_api_keys import AgentAPIKeysResourceWithStreamingResponse

        return AgentAPIKeysResourceWithStreamingResponse(self._client.agent_api_keys)

    @cached_property
    def namespaces(self) -> namespaces.NamespacesResourceWithStreamingResponse:
        from .resources.namespaces import NamespacesResourceWithStreamingResponse

        return NamespacesResourceWithStreamingResponse(self._client.namespaces)

    @cached_property
    def projects(self) -> projects.ProjectsResourceWithStreamingResponse:
        from .resources.projects import ProjectsResourceWithStreamingResponse

        return ProjectsResourceWithStreamingResponse(self._client.projects)

    @cached_property
    def workspaces(self) -> workspaces.WorkspacesResourceWithStreamingResponse:
        from .resources.workspaces import WorkspacesResourceWithStreamingResponse

        return WorkspacesResourceWithStreamingResponse(self._client.workspaces)


class AsyncSb0WithStreamedResponse:
    _client: AsyncSb0

    def __init__(self, client: AsyncSb0) -> None:
        self._client = client

    @cached_property
    def agents(self) -> agents.AsyncAgentsResourceWithStreamingResponse:
        from .resources.agents import AsyncAgentsResourceWithStreamingResponse

        return AsyncAgentsResourceWithStreamingResponse(self._client.agents)

    @cached_property
    def deployments(self) -> deployments.AsyncDeploymentsResourceWithStreamingResponse:
        from .resources.deployments import AsyncDeploymentsResourceWithStreamingResponse

        return AsyncDeploymentsResourceWithStreamingResponse(self._client.deployments)

    @cached_property
    def versions(self) -> versions.AsyncVersionsResourceWithStreamingResponse:
        from .resources.versions import AsyncVersionsResourceWithStreamingResponse

        return AsyncVersionsResourceWithStreamingResponse(self._client.versions)

    @cached_property
    def registry(self) -> registry.AsyncRegistryResourceWithStreamingResponse:
        from .resources.registry import AsyncRegistryResourceWithStreamingResponse

        return AsyncRegistryResourceWithStreamingResponse(self._client.registry)

    @cached_property
    def tasks(self) -> tasks.AsyncTasksResourceWithStreamingResponse:
        from .resources.tasks import AsyncTasksResourceWithStreamingResponse

        return AsyncTasksResourceWithStreamingResponse(self._client.tasks)

    @cached_property
    def messages(self) -> messages.AsyncMessagesResourceWithStreamingResponse:
        from .resources.messages import AsyncMessagesResourceWithStreamingResponse

        return AsyncMessagesResourceWithStreamingResponse(self._client.messages)

    @cached_property
    def spans(self) -> spans.AsyncSpansResourceWithStreamingResponse:
        from .resources.spans import AsyncSpansResourceWithStreamingResponse

        return AsyncSpansResourceWithStreamingResponse(self._client.spans)

    @cached_property
    def states(self) -> states.AsyncStatesResourceWithStreamingResponse:
        from .resources.states import AsyncStatesResourceWithStreamingResponse

        return AsyncStatesResourceWithStreamingResponse(self._client.states)

    @cached_property
    def events(self) -> events.AsyncEventsResourceWithStreamingResponse:
        from .resources.events import AsyncEventsResourceWithStreamingResponse

        return AsyncEventsResourceWithStreamingResponse(self._client.events)

    @cached_property
    def logs(self) -> logs.AsyncLogsResourceWithStreamingResponse:
        from .resources.logs import AsyncLogsResourceWithStreamingResponse

        return AsyncLogsResourceWithStreamingResponse(self._client.logs)

    @cached_property
    def tracker(self) -> tracker.AsyncTrackerResourceWithStreamingResponse:
        from .resources.tracker import AsyncTrackerResourceWithStreamingResponse

        return AsyncTrackerResourceWithStreamingResponse(self._client.tracker)

    @cached_property
    def agent_api_keys(self) -> agent_api_keys.AsyncAgentAPIKeysResourceWithStreamingResponse:
        from .resources.agent_api_keys import AsyncAgentAPIKeysResourceWithStreamingResponse

        return AsyncAgentAPIKeysResourceWithStreamingResponse(self._client.agent_api_keys)

    @cached_property
    def namespaces(self) -> namespaces.AsyncNamespacesResourceWithStreamingResponse:
        from .resources.namespaces import AsyncNamespacesResourceWithStreamingResponse

        return AsyncNamespacesResourceWithStreamingResponse(self._client.namespaces)

    @cached_property
    def projects(self) -> projects.AsyncProjectsResourceWithStreamingResponse:
        from .resources.projects import AsyncProjectsResourceWithStreamingResponse

        return AsyncProjectsResourceWithStreamingResponse(self._client.projects)

    @cached_property
    def workspaces(self) -> workspaces.AsyncWorkspacesResourceWithStreamingResponse:
        from .resources.workspaces import AsyncWorkspacesResourceWithStreamingResponse

        return AsyncWorkspacesResourceWithStreamingResponse(self._client.workspaces)


Client = Sb0

AsyncClient = AsyncSb0
