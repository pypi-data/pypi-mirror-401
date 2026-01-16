# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import namespace_list_params, namespace_create_params, namespace_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.namespace import Namespace
from ..types.delete_response import DeleteResponse
from ..types.namespace_list_response import NamespaceListResponse

__all__ = ["NamespacesResource", "AsyncNamespacesResource"]


class NamespacesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NamespacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return NamespacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NamespacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return NamespacesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        owner_org_id: str,
        slug: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Create a new namespace for multi-tenant isolation.

        Args:
          name: Human-readable name.

          owner_org_id: Stytch organization ID that owns this namespace.

          slug: URL-friendly unique identifier (lowercase alphanumeric and hyphens).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/namespaces",
            body=maybe_transform(
                {
                    "name": name,
                    "owner_org_id": owner_org_id,
                    "slug": slug,
                },
                namespace_create_params.NamespaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )

    def retrieve(
        self,
        namespace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Get a namespace by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_id:
            raise ValueError(f"Expected a non-empty value for `namespace_id` but received {namespace_id!r}")
        return self._get(
            f"/namespaces/{namespace_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )

    def update(
        self,
        namespace_id: str,
        *,
        gcp_sa_email: Optional[str] | Omit = omit,
        gcs_bucket: Optional[str] | Omit = omit,
        k8s_namespace: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Update a namespace's properties.

        Args:
          gcp_sa_email: GCP service account email (set by infra).

          gcs_bucket: GCS bucket name (set by infra).

          k8s_namespace: K8s namespace name (set by infra).

          name: Human-readable name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_id:
            raise ValueError(f"Expected a non-empty value for `namespace_id` but received {namespace_id!r}")
        return self._patch(
            f"/namespaces/{namespace_id}",
            body=maybe_transform(
                {
                    "gcp_sa_email": gcp_sa_email,
                    "gcs_bucket": gcs_bucket,
                    "k8s_namespace": k8s_namespace,
                    "name": name,
                },
                namespace_update_params.NamespaceUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page_number: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceListResponse:
        """
        List all namespaces the user has access to.

        Args:
          limit: Maximum number of results

          page_number: Page number

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/namespaces",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page_number": page_number,
                    },
                    namespace_list_params.NamespaceListParams,
                ),
            ),
            cast_to=NamespaceListResponse,
        )

    def delete(
        self,
        namespace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete a namespace (must be empty).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_id:
            raise ValueError(f"Expected a non-empty value for `namespace_id` but received {namespace_id!r}")
        return self._delete(
            f"/namespaces/{namespace_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def retrieve_by_slug(
        self,
        slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Get a namespace by its slug.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not slug:
            raise ValueError(f"Expected a non-empty value for `slug` but received {slug!r}")
        return self._get(
            f"/namespaces/slug/{slug}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )


class AsyncNamespacesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNamespacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncNamespacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNamespacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncNamespacesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        owner_org_id: str,
        slug: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Create a new namespace for multi-tenant isolation.

        Args:
          name: Human-readable name.

          owner_org_id: Stytch organization ID that owns this namespace.

          slug: URL-friendly unique identifier (lowercase alphanumeric and hyphens).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/namespaces",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "owner_org_id": owner_org_id,
                    "slug": slug,
                },
                namespace_create_params.NamespaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )

    async def retrieve(
        self,
        namespace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Get a namespace by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_id:
            raise ValueError(f"Expected a non-empty value for `namespace_id` but received {namespace_id!r}")
        return await self._get(
            f"/namespaces/{namespace_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )

    async def update(
        self,
        namespace_id: str,
        *,
        gcp_sa_email: Optional[str] | Omit = omit,
        gcs_bucket: Optional[str] | Omit = omit,
        k8s_namespace: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Update a namespace's properties.

        Args:
          gcp_sa_email: GCP service account email (set by infra).

          gcs_bucket: GCS bucket name (set by infra).

          k8s_namespace: K8s namespace name (set by infra).

          name: Human-readable name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_id:
            raise ValueError(f"Expected a non-empty value for `namespace_id` but received {namespace_id!r}")
        return await self._patch(
            f"/namespaces/{namespace_id}",
            body=await async_maybe_transform(
                {
                    "gcp_sa_email": gcp_sa_email,
                    "gcs_bucket": gcs_bucket,
                    "k8s_namespace": k8s_namespace,
                    "name": name,
                },
                namespace_update_params.NamespaceUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        page_number: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceListResponse:
        """
        List all namespaces the user has access to.

        Args:
          limit: Maximum number of results

          page_number: Page number

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/namespaces",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "page_number": page_number,
                    },
                    namespace_list_params.NamespaceListParams,
                ),
            ),
            cast_to=NamespaceListResponse,
        )

    async def delete(
        self,
        namespace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete a namespace (must be empty).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_id:
            raise ValueError(f"Expected a non-empty value for `namespace_id` but received {namespace_id!r}")
        return await self._delete(
            f"/namespaces/{namespace_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def retrieve_by_slug(
        self,
        slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Namespace:
        """
        Get a namespace by its slug.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not slug:
            raise ValueError(f"Expected a non-empty value for `slug` but received {slug!r}")
        return await self._get(
            f"/namespaces/slug/{slug}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Namespace,
        )


class NamespacesResourceWithRawResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.create = to_raw_response_wrapper(
            namespaces.create,
        )
        self.retrieve = to_raw_response_wrapper(
            namespaces.retrieve,
        )
        self.update = to_raw_response_wrapper(
            namespaces.update,
        )
        self.list = to_raw_response_wrapper(
            namespaces.list,
        )
        self.delete = to_raw_response_wrapper(
            namespaces.delete,
        )
        self.retrieve_by_slug = to_raw_response_wrapper(
            namespaces.retrieve_by_slug,
        )


class AsyncNamespacesResourceWithRawResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.create = async_to_raw_response_wrapper(
            namespaces.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            namespaces.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            namespaces.update,
        )
        self.list = async_to_raw_response_wrapper(
            namespaces.list,
        )
        self.delete = async_to_raw_response_wrapper(
            namespaces.delete,
        )
        self.retrieve_by_slug = async_to_raw_response_wrapper(
            namespaces.retrieve_by_slug,
        )


class NamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.create = to_streamed_response_wrapper(
            namespaces.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            namespaces.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            namespaces.update,
        )
        self.list = to_streamed_response_wrapper(
            namespaces.list,
        )
        self.delete = to_streamed_response_wrapper(
            namespaces.delete,
        )
        self.retrieve_by_slug = to_streamed_response_wrapper(
            namespaces.retrieve_by_slug,
        )


class AsyncNamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.create = async_to_streamed_response_wrapper(
            namespaces.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            namespaces.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            namespaces.update,
        )
        self.list = async_to_streamed_response_wrapper(
            namespaces.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            namespaces.delete,
        )
        self.retrieve_by_slug = async_to_streamed_response_wrapper(
            namespaces.retrieve_by_slug,
        )
