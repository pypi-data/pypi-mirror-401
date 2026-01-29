# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
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
from ._exceptions import APIStatusError, SearchPilotError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import rules, steps, values, accounts, sections, customers, experiments, seo_experiment_results
    from .resources.rules import RulesResource, AsyncRulesResource
    from .resources.steps import StepsResource, AsyncStepsResource
    from .resources.values import ValuesResource, AsyncValuesResource
    from .resources.accounts import AccountsResource, AsyncAccountsResource
    from .resources.sections import SectionsResource, AsyncSectionsResource
    from .resources.customers import CustomersResource, AsyncCustomersResource
    from .resources.experiments import ExperimentsResource, AsyncExperimentsResource
    from .resources.seo_experiment_results import SeoExperimentResultsResource, AsyncSeoExperimentResultsResource

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "SearchPilot",
    "AsyncSearchPilot",
    "Client",
    "AsyncClient",
]


class SearchPilot(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
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
        """Construct a new synchronous SearchPilot client instance.

        This automatically infers the `api_key` argument from the `SEARCHPILOT_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("SEARCHPILOT_API_KEY")
        if api_key is None:
            raise SearchPilotError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SEARCHPILOT_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("SEARCHPILOT_BASE_URL")
        if base_url is None:
            base_url = f"https://app.searchpilot.com"

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
    def customers(self) -> CustomersResource:
        from .resources.customers import CustomersResource

        return CustomersResource(self)

    @cached_property
    def accounts(self) -> AccountsResource:
        from .resources.accounts import AccountsResource

        return AccountsResource(self)

    @cached_property
    def sections(self) -> SectionsResource:
        from .resources.sections import SectionsResource

        return SectionsResource(self)

    @cached_property
    def rules(self) -> RulesResource:
        from .resources.rules import RulesResource

        return RulesResource(self)

    @cached_property
    def steps(self) -> StepsResource:
        from .resources.steps import StepsResource

        return StepsResource(self)

    @cached_property
    def values(self) -> ValuesResource:
        from .resources.values import ValuesResource

        return ValuesResource(self)

    @cached_property
    def experiments(self) -> ExperimentsResource:
        from .resources.experiments import ExperimentsResource

        return ExperimentsResource(self)

    @cached_property
    def seo_experiment_results(self) -> SeoExperimentResultsResource:
        from .resources.seo_experiment_results import SeoExperimentResultsResource

        return SeoExperimentResultsResource(self)

    @cached_property
    def with_raw_response(self) -> SearchPilotWithRawResponse:
        return SearchPilotWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchPilotWithStreamedResponse:
        return SearchPilotWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
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


class AsyncSearchPilot(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
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
        """Construct a new async AsyncSearchPilot client instance.

        This automatically infers the `api_key` argument from the `SEARCHPILOT_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("SEARCHPILOT_API_KEY")
        if api_key is None:
            raise SearchPilotError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SEARCHPILOT_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("SEARCHPILOT_BASE_URL")
        if base_url is None:
            base_url = f"https://app.searchpilot.com"

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
    def customers(self) -> AsyncCustomersResource:
        from .resources.customers import AsyncCustomersResource

        return AsyncCustomersResource(self)

    @cached_property
    def accounts(self) -> AsyncAccountsResource:
        from .resources.accounts import AsyncAccountsResource

        return AsyncAccountsResource(self)

    @cached_property
    def sections(self) -> AsyncSectionsResource:
        from .resources.sections import AsyncSectionsResource

        return AsyncSectionsResource(self)

    @cached_property
    def rules(self) -> AsyncRulesResource:
        from .resources.rules import AsyncRulesResource

        return AsyncRulesResource(self)

    @cached_property
    def steps(self) -> AsyncStepsResource:
        from .resources.steps import AsyncStepsResource

        return AsyncStepsResource(self)

    @cached_property
    def values(self) -> AsyncValuesResource:
        from .resources.values import AsyncValuesResource

        return AsyncValuesResource(self)

    @cached_property
    def experiments(self) -> AsyncExperimentsResource:
        from .resources.experiments import AsyncExperimentsResource

        return AsyncExperimentsResource(self)

    @cached_property
    def seo_experiment_results(self) -> AsyncSeoExperimentResultsResource:
        from .resources.seo_experiment_results import AsyncSeoExperimentResultsResource

        return AsyncSeoExperimentResultsResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncSearchPilotWithRawResponse:
        return AsyncSearchPilotWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchPilotWithStreamedResponse:
        return AsyncSearchPilotWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
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


class SearchPilotWithRawResponse:
    _client: SearchPilot

    def __init__(self, client: SearchPilot) -> None:
        self._client = client

    @cached_property
    def customers(self) -> customers.CustomersResourceWithRawResponse:
        from .resources.customers import CustomersResourceWithRawResponse

        return CustomersResourceWithRawResponse(self._client.customers)

    @cached_property
    def accounts(self) -> accounts.AccountsResourceWithRawResponse:
        from .resources.accounts import AccountsResourceWithRawResponse

        return AccountsResourceWithRawResponse(self._client.accounts)

    @cached_property
    def sections(self) -> sections.SectionsResourceWithRawResponse:
        from .resources.sections import SectionsResourceWithRawResponse

        return SectionsResourceWithRawResponse(self._client.sections)

    @cached_property
    def rules(self) -> rules.RulesResourceWithRawResponse:
        from .resources.rules import RulesResourceWithRawResponse

        return RulesResourceWithRawResponse(self._client.rules)

    @cached_property
    def steps(self) -> steps.StepsResourceWithRawResponse:
        from .resources.steps import StepsResourceWithRawResponse

        return StepsResourceWithRawResponse(self._client.steps)

    @cached_property
    def values(self) -> values.ValuesResourceWithRawResponse:
        from .resources.values import ValuesResourceWithRawResponse

        return ValuesResourceWithRawResponse(self._client.values)

    @cached_property
    def experiments(self) -> experiments.ExperimentsResourceWithRawResponse:
        from .resources.experiments import ExperimentsResourceWithRawResponse

        return ExperimentsResourceWithRawResponse(self._client.experiments)

    @cached_property
    def seo_experiment_results(self) -> seo_experiment_results.SeoExperimentResultsResourceWithRawResponse:
        from .resources.seo_experiment_results import SeoExperimentResultsResourceWithRawResponse

        return SeoExperimentResultsResourceWithRawResponse(self._client.seo_experiment_results)


class AsyncSearchPilotWithRawResponse:
    _client: AsyncSearchPilot

    def __init__(self, client: AsyncSearchPilot) -> None:
        self._client = client

    @cached_property
    def customers(self) -> customers.AsyncCustomersResourceWithRawResponse:
        from .resources.customers import AsyncCustomersResourceWithRawResponse

        return AsyncCustomersResourceWithRawResponse(self._client.customers)

    @cached_property
    def accounts(self) -> accounts.AsyncAccountsResourceWithRawResponse:
        from .resources.accounts import AsyncAccountsResourceWithRawResponse

        return AsyncAccountsResourceWithRawResponse(self._client.accounts)

    @cached_property
    def sections(self) -> sections.AsyncSectionsResourceWithRawResponse:
        from .resources.sections import AsyncSectionsResourceWithRawResponse

        return AsyncSectionsResourceWithRawResponse(self._client.sections)

    @cached_property
    def rules(self) -> rules.AsyncRulesResourceWithRawResponse:
        from .resources.rules import AsyncRulesResourceWithRawResponse

        return AsyncRulesResourceWithRawResponse(self._client.rules)

    @cached_property
    def steps(self) -> steps.AsyncStepsResourceWithRawResponse:
        from .resources.steps import AsyncStepsResourceWithRawResponse

        return AsyncStepsResourceWithRawResponse(self._client.steps)

    @cached_property
    def values(self) -> values.AsyncValuesResourceWithRawResponse:
        from .resources.values import AsyncValuesResourceWithRawResponse

        return AsyncValuesResourceWithRawResponse(self._client.values)

    @cached_property
    def experiments(self) -> experiments.AsyncExperimentsResourceWithRawResponse:
        from .resources.experiments import AsyncExperimentsResourceWithRawResponse

        return AsyncExperimentsResourceWithRawResponse(self._client.experiments)

    @cached_property
    def seo_experiment_results(self) -> seo_experiment_results.AsyncSeoExperimentResultsResourceWithRawResponse:
        from .resources.seo_experiment_results import AsyncSeoExperimentResultsResourceWithRawResponse

        return AsyncSeoExperimentResultsResourceWithRawResponse(self._client.seo_experiment_results)


class SearchPilotWithStreamedResponse:
    _client: SearchPilot

    def __init__(self, client: SearchPilot) -> None:
        self._client = client

    @cached_property
    def customers(self) -> customers.CustomersResourceWithStreamingResponse:
        from .resources.customers import CustomersResourceWithStreamingResponse

        return CustomersResourceWithStreamingResponse(self._client.customers)

    @cached_property
    def accounts(self) -> accounts.AccountsResourceWithStreamingResponse:
        from .resources.accounts import AccountsResourceWithStreamingResponse

        return AccountsResourceWithStreamingResponse(self._client.accounts)

    @cached_property
    def sections(self) -> sections.SectionsResourceWithStreamingResponse:
        from .resources.sections import SectionsResourceWithStreamingResponse

        return SectionsResourceWithStreamingResponse(self._client.sections)

    @cached_property
    def rules(self) -> rules.RulesResourceWithStreamingResponse:
        from .resources.rules import RulesResourceWithStreamingResponse

        return RulesResourceWithStreamingResponse(self._client.rules)

    @cached_property
    def steps(self) -> steps.StepsResourceWithStreamingResponse:
        from .resources.steps import StepsResourceWithStreamingResponse

        return StepsResourceWithStreamingResponse(self._client.steps)

    @cached_property
    def values(self) -> values.ValuesResourceWithStreamingResponse:
        from .resources.values import ValuesResourceWithStreamingResponse

        return ValuesResourceWithStreamingResponse(self._client.values)

    @cached_property
    def experiments(self) -> experiments.ExperimentsResourceWithStreamingResponse:
        from .resources.experiments import ExperimentsResourceWithStreamingResponse

        return ExperimentsResourceWithStreamingResponse(self._client.experiments)

    @cached_property
    def seo_experiment_results(self) -> seo_experiment_results.SeoExperimentResultsResourceWithStreamingResponse:
        from .resources.seo_experiment_results import SeoExperimentResultsResourceWithStreamingResponse

        return SeoExperimentResultsResourceWithStreamingResponse(self._client.seo_experiment_results)


class AsyncSearchPilotWithStreamedResponse:
    _client: AsyncSearchPilot

    def __init__(self, client: AsyncSearchPilot) -> None:
        self._client = client

    @cached_property
    def customers(self) -> customers.AsyncCustomersResourceWithStreamingResponse:
        from .resources.customers import AsyncCustomersResourceWithStreamingResponse

        return AsyncCustomersResourceWithStreamingResponse(self._client.customers)

    @cached_property
    def accounts(self) -> accounts.AsyncAccountsResourceWithStreamingResponse:
        from .resources.accounts import AsyncAccountsResourceWithStreamingResponse

        return AsyncAccountsResourceWithStreamingResponse(self._client.accounts)

    @cached_property
    def sections(self) -> sections.AsyncSectionsResourceWithStreamingResponse:
        from .resources.sections import AsyncSectionsResourceWithStreamingResponse

        return AsyncSectionsResourceWithStreamingResponse(self._client.sections)

    @cached_property
    def rules(self) -> rules.AsyncRulesResourceWithStreamingResponse:
        from .resources.rules import AsyncRulesResourceWithStreamingResponse

        return AsyncRulesResourceWithStreamingResponse(self._client.rules)

    @cached_property
    def steps(self) -> steps.AsyncStepsResourceWithStreamingResponse:
        from .resources.steps import AsyncStepsResourceWithStreamingResponse

        return AsyncStepsResourceWithStreamingResponse(self._client.steps)

    @cached_property
    def values(self) -> values.AsyncValuesResourceWithStreamingResponse:
        from .resources.values import AsyncValuesResourceWithStreamingResponse

        return AsyncValuesResourceWithStreamingResponse(self._client.values)

    @cached_property
    def experiments(self) -> experiments.AsyncExperimentsResourceWithStreamingResponse:
        from .resources.experiments import AsyncExperimentsResourceWithStreamingResponse

        return AsyncExperimentsResourceWithStreamingResponse(self._client.experiments)

    @cached_property
    def seo_experiment_results(self) -> seo_experiment_results.AsyncSeoExperimentResultsResourceWithStreamingResponse:
        from .resources.seo_experiment_results import AsyncSeoExperimentResultsResourceWithStreamingResponse

        return AsyncSeoExperimentResultsResourceWithStreamingResponse(self._client.seo_experiment_results)


Client = SearchPilot

AsyncClient = AsyncSearchPilot
