import json
import time
from dataclasses import dataclass

import requests
from typing import Any, TypedDict, NotRequired, Callable


# Exception classes for Studio API operations
class StudioSdkException(Exception):
    """Base exception for all Studio API errors."""
    def __init__(self,
                 message: str,
                 status_code: int | None = None,
                 original_exception: Exception | None = None) -> None:
        self.message = message
        self.status_code = status_code
        self.original_exception = original_exception
        super().__init__(message)


class StudioConnectionException(StudioSdkException):
    """Exception for connection errors when accessing Studio APIs."""
    pass


class StudioTimeoutException(StudioSdkException):
    """Exception for timeout errors when accessing Studio APIs."""
    pass


class StudioRequestException(StudioSdkException):
    """Exception for general request errors when accessing Studio APIs."""
    pass


def _handle_request_exceptions(
    exception_class: type[StudioSdkException],
    context: str,
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    Execute a function and handle HTTP exceptions, converting them to Studio API exceptions.

    :param exception_class: The Studio API exception class to raise
    :param context: Descriptive context for error messages
    :param func: The function to execute
    :param args: Positional arguments for the function
    :param kwargs: Keyword arguments for the function
    :return: The result of the function call
    """
    try:
        return func(*args, **kwargs)
    except requests.exceptions.Timeout as e:
        raise StudioTimeoutException(
            f"Timeout while {context}",
            original_exception=e
        ) from e
    except requests.exceptions.ConnectionError as e:
        raise StudioConnectionException(
            f"Connection error while {context}: {str(e)}",
            original_exception=e
        ) from e
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else None
        raise exception_class(
            f"HTTP error while {context}: {str(e)}",
            status_code=status_code,
            original_exception=e
        ) from e
    except requests.exceptions.RequestException as e:
        raise exception_class(
            f"Request failed while {context}: {str(e)}",
            original_exception=e
        ) from e


def _make_http_request_without_raise(
    method: Callable[..., Any],
    url: str,
    exception_class: type[StudioSdkException],
    context: str,
    **kwargs: Any
) -> Any:
    """
    Make an HTTP request with automatic exception handling, but without calling raise_for_status().
    This is useful when you need to check status codes manually.

    :param method: The HTTP method to call (e.g., http_client.post, http_client.get)
    :param url: The URL to request
    :param exception_class: The exception class to raise on error
    :param context: Descriptive context for error messages
    :param kwargs: Additional arguments to pass to the HTTP method
    :return: The response object
    """
    def _request() -> Any:
        return method(url, **kwargs)

    return _handle_request_exceptions(exception_class, context, _request)


def _make_http_request(
    method: Callable[..., Any],
    url: str,
    exception_class: type[StudioSdkException],
    context: str,
    **kwargs: Any
) -> Any:
    """
    Make an HTTP request with automatic exception handling.

    :param method: The HTTP method to call (e.g., http_client.post, http_client.get)
    :param url: The URL to request
    :param exception_class: The exception class to raise on error
    :param context: Descriptive context for error messages
    :param kwargs: Additional arguments to pass to the HTTP method
    :return: The response object
    """
    def _request() -> Any:
        response = method(url, **kwargs)
        response.raise_for_status()
        return response

    return _handle_request_exceptions(exception_class, context, _request)


class Secret(TypedDict):
    name: str
    value: str


class StudioConfig(TypedDict):
    name: str
    api_key: str
    create_database: NotRequired[bool]
    database_uuid: NotRequired[str]
    database_type: NotRequired[str]
    resources: NotRequired[dict[str, Any]]
    ingress_rate_limits: NotRequired[dict[str, Any]]
    database_quota: NotRequired[dict[str, Any]]
    secrets: NotRequired[list[Secret]]


@dataclass
class StudioUrls:
    """URLs for accessing the studio."""
    api: str
    raw: dict[str, Any]


@dataclass
class DatabaseInfo:
    """Database information for the studio."""
    database_name: str | None
    database_uuid: str | None
    username: str | None
    raw: dict[str, Any]


@dataclass
class StudioCreateResponse:
    """Response from creating a studio."""
    urls: StudioUrls
    database: DatabaseInfo | None
    raw: dict[str, Any]


@dataclass
class StudioDeleted:
    """Represents a successful studio deletion."""
    studio_name: str
    database_deleted: bool


@dataclass
class StudioNotFound:
    """Represents a studio that was not found during deletion."""
    studio_name: str


def _get_manager_api_url() -> str:
    # todo: implement dynamic retrieval of the manager API URL
    return "http://api.local-studio-manager.svc.cluster.local:8080"


class StudioManager:
    """Manages studio lifecycle operations via the Studio Manager API."""

    def __init__(self, http_client: Any = None) -> None:
        """
        Initialize the StudioManagerAPI.

        :param http_client: Optional HTTP client. Only required for testing.
        :type http_client: Any
        """
        self.manager_api_url: str = _get_manager_api_url()
        self.http_client = http_client if http_client is not None else requests

    def delete_studio(
            self,
            studio_name: str,
            delete_database: bool = False
    ) -> StudioDeleted | StudioNotFound:
        """
        Delete an existing studio.

        :param studio_name: Name of the studio to delete
        :type studio_name: str
        :param delete_database: Whether to also delete the associated database
        :type delete_database: bool
        :returns: StudioDeleted if successful, StudioNotFound if studio doesn't exist
        :rtype: StudioDeleted | StudioNotFound
        :raises StudioSdkException: If the request fails (except for 404)
        """
        delete_url = f"{self.manager_api_url}/studios/{studio_name}"
        if delete_database:
            delete_url += "?delete_database=true"

        response = _make_http_request_without_raise(
            self.http_client.delete,
            delete_url,
            StudioSdkException,
            f"deleting studio '{studio_name}'"
        )

        if response.status_code == 404:
            return StudioNotFound(studio_name=studio_name)
        elif response.status_code < 300:
            return StudioDeleted(studio_name=studio_name, database_deleted=delete_database)
        else:
            raise StudioSdkException(
                f"Failed to delete studio '{studio_name}': "
                f"{response.text if hasattr(response, 'text') else 'Unknown error'}",
                status_code=response.status_code
            )


    def create_studio(self, studio_config: StudioConfig) -> StudioCreateResponse:
        """
        Create a new studio.

        :param studio_config: Configuration dictionary for the studio
        :type studio_config: StudioConfig
        :returns: Studio creation response containing URLs and database info
        :rtype: StudioCreateResponse
        :raises StudioSdkException: If the request fails
        """
        response = _make_http_request(
            self.http_client.post,
            f"{self.manager_api_url}/studios",
            StudioSdkException,
            f"creating studio '{studio_config['name']}'",
            json=studio_config
        )

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise StudioSdkException(
                f"Invalid JSON response while creating studio '{studio_config['name']}'",
                status_code=response.status_code,
                original_exception=e
            ) from e

        # Parse URLs
        urls = StudioUrls(
            api=data["urls"]["api"],
            raw=data["urls"]
        )

        # Parse database info if present
        database = None
        if "database" in data and data["database"]:
            db_data = data["database"]
            database = DatabaseInfo(
                database_name=db_data.get("database_name"),
                database_uuid=db_data.get("database_uuid"),
                username=db_data.get("username"),
                raw=db_data
            )

        return StudioCreateResponse(
            urls=urls,
            database=database,
            raw=data
        )


class StudioAdmin:
    """Manages studio configuration via the Studio Admin API."""

    def __init__(self, api_url: str, api_key: str, http_client: Any = None) -> None:
        """
        Initialize the StudioAdminAPI.

        :param api_url: Base URL for the studio API
        :type api_url: str
        :param api_key: API key for authentication
        :type api_key: str
        :param http_client: Optional HTTP client (defaults to requests module)
        :type http_client: Any
        """
        self.api_url = api_url
        self.api_key = api_key
        self.http_client = http_client if http_client is not None else requests

    def wait_until_ready(self, max_retries: int = 15, retry_delay_seconds: float = 2) -> None:
        """
        Wait until the studio API is ready.

        :param max_retries: Maximum number of retry attempts
        :type max_retries: int
        :param retry_delay_seconds: Delay in seconds between retries
        :type retry_delay_seconds: float
        :raises StudioTimeoutError: If the studio API does not become ready in time
        """
        for i in range(max_retries):
            try:
                response = self.http_client.get(
                    f"{self.api_url}/api-docs.json",
                    headers={"x-api-key": self.api_key},
                    verify=False,
                    timeout=2
                )
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException as e:
                print(f"Attempt {i + 1}/{max_retries} failed: {e}")

            time.sleep(retry_delay_seconds)

        raise StudioTimeoutException(f"Studio API did not become ready "
                                 f"within {max_retries * retry_delay_seconds} seconds")

    def create_admin_user(self, username: str, password: str) -> None:
        """
        Create an admin user with retry logic.

        :param username: Admin username
        :type username: str
        :param password: Admin password
        :type password: str
        :raises StudioSdkException: If the request fails
        """
        admin_config = {
            "username": username,
            "password": password
        }

        _make_http_request(
            self.http_client.post,
            f"{self.api_url}/api/admin/users",
            StudioSdkException,
            f"creating admin user '{username}'",
            json=admin_config,
            headers={"x-api-key": self.api_key},
            verify=False,
            timeout=2
        )

    def configure_catalogue(self, catalogue_url: str) -> None:
        """
        Configure a catalogue for the studio.

        :param catalogue_url: URL of the catalogue to configure
        :type catalogue_url: str
        :raises StudioSdkException: If the request fails
        """
        _make_http_request(
            self.http_client.post,
            f"{self.api_url}/api/admin/catalogues",
            StudioSdkException,
            f"configuring catalogue '{catalogue_url}'",
            json={"url": catalogue_url},
            headers={"x-api-key": self.api_key},
            verify=False
        )

    def import_flows(self, flows_json: str) -> None:
        """
        Import flows into the studio.

        :param flows_json: JSON string containing flows data
        :type flows_json: str
        :raises StudioSdkException: If the request fails or JSON is invalid
        """
        try:
            flows_data = json.loads(flows_json)
        except json.JSONDecodeError as e:
            raise StudioSdkException(
                f"Invalid JSON in flows_json: {str(e)}",
                original_exception=e
            ) from e

        _make_http_request(
            self.http_client.post,
            f"{self.api_url}/api/admin/flows",
            StudioSdkException,
            "importing flows",
            json=flows_data,
            headers={"x-api-key": self.api_key},
            verify=False
        )

    def import_credentials(self, credentials_json: str) -> None:
        """
        Import credentials into the studio.

        :param credentials_json: JSON string containing credentials data
        :type credentials_json: str
        :raises StudioSdkException: If the request fails or JSON is invalid
        """
        try:
            credentials_data = json.loads(credentials_json)
        except json.JSONDecodeError as e:
            raise StudioSdkException(
                f"Invalid JSON in credentials_json: {str(e)}",
                original_exception=e
            ) from e

        _make_http_request(
            self.http_client.post,
            f"{self.api_url}/api/admin/credentials",
            StudioSdkException,
            "importing credentials",
            json=credentials_data,
            headers={"x-api-key": self.api_key},
            verify=False
        )

    def restart_node_red(self) -> None:
        """
        Restart Node-RED to apply changes.

        :raises StudioSdkException: If the request fails
        """
        _make_http_request(
            self.http_client.post,
            f"{self.api_url}/api/admin/restart",
            StudioSdkException,
            "restarting Node-RED",
            headers={"x-api-key": self.api_key},
            verify=False
        )
