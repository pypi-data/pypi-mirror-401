from typing import Any

import requests
import json


class AppCreationException(Exception):
    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class MissingTokenException(Exception):
    pass


def sanizatize_auth_token(token: str) -> str:
    """
    Sanitize the auth token to ensure it starts with Bearer
    :param token: The token to sanitize
    :return: The sanitized token
    """
    return f"Bearer {token}" if "Bearer" not in token else token

def headers_with_token(token: str) -> dict:
    """
    Create headers with the given token
    :param token: The token to use
    :return: Headers dictionary
    """
    return {
        "Authorization": sanizatize_auth_token(token)
    }

def create_app(remote_server: str, name: str, id: str | None = None, token: str | None = None) -> str:
    """
    Create a new APP on the SCP APP store
    :param remote_server: SCP APP store server url
    :param name: name of the APP
    :param id: optional APP ID
    :param token: authentication token
    :return: APP ID
    """
    headers = None
    if not token:
        # why does the function allow a None token if it's required???
        raise MissingTokenException("Token is required to create an APP on the SCP APP store")

    headers = headers_with_token(token)
    data = dict(
        name=name
    )
    if id:
        data['id'] = id
    try:
        response = requests.post(
            url=f'{remote_server}/api/v1/apps',
            headers=headers,
            verify=False,
            json=data
        )
    except requests.exceptions.RequestException as e:
        status = response.status_code if 'response' in locals() and response else 599
    
        raise AppCreationException(
            f"SCP APP store error {status}",
            status_code=status,
            response_body=response.text if status != 599 else json.dumps({"error": str(e)})
        )

    if response.status_code not in (200, 201):
        raise AppCreationException(
            f"SCP APP store error {response.status_code}",
            status_code=response.status_code,
            response_body=response.text
        )

    return response.json().get('id')


def delete_app(remote_server: str, name: str, id: str | None = None, token: str | None = None) -> None: # used only to rollback creation of app
    """
    Delete an APP on the SCP APP store
    :param remote_server: SCP APP store server url
    :param name: name of the APP
    """
    headers = None
    if not token:
        raise MissingTokenException("Token is required to delete an APP on the SCP APP store")

    headers = headers_with_token(token)

    if not id:
        raise AppCreationException("APP ID is required to delete an APP on the SCP APP store")

    try:
        response = requests.delete(
            url=f'{remote_server}/api/v1/apps/{id}',
            headers=headers,
            verify=False
        )
    except requests.exceptions.RequestException as e:
        status = response.status_code if 'response' in locals() and response else 599

        raise AppCreationException(
            f"SCP APP store error {status}",
            status_code=status,
            response_body=response.text if status != 599 else json.dumps({"error": str(e)})
        )

    if response.status_code not in (200, 204):
        raise AppCreationException(
            f"SCP APP store error {response.status_code}",
            status_code=response.status_code,
            response_body=response.text
        )