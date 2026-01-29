"""
VoiceBot
"""
import os
import requests

from requests import Response

from scp.app.sdk.service import voicebot_url

class VoiceBotClient():
    """
    VoiceBot class
    """
    def __init__(self, base_url:str | None = None, request_timeout: int|float|None = 5) -> None:
        """
        Initialize VoiceBotClient

        Args:
            base_url (str|None): The base URL for the VoiceBot service.
            request_timeout (int|float|None): The timeout for HTTP requests.
        """
        self.base_url=voicebot_url()
        self.timeout: int|float|None = request_timeout

    def list_voicebots(self) -> Response:
        """
        List VoiceBots

        Returns:
            Response: The HTTP response object containing the list of VoiceBots.
        """
        url = f"{self.base_url}/v1/voicebots"
        response = requests.get(url, timeout=self.timeout)
        return self._handle_response(response)

    def create_voicebot(self, user_id: str, callflow: dict|None = None) -> Response:
        """
        Create VoiceBot

        Args:
            user_id (str): The user ID for the VoiceBot.
            callflow (dict|None): The callflow configuration for the VoiceBot.

        Returns:
            Response: The HTTP response object containing the created VoiceBot details.
        """
        url = f"{self.base_url}/v1/voicebots/private"

        body = {
            "userId": user_id,
            "callflow": callflow
        }

        response = requests.post(url, json=body, timeout=self.timeout)
        print("response", response)
        return self._handle_response(response)

    def delete_voicebot_callback(self, user_id: str) -> Response:
        """
        Delete VoiceBot Callback

        Args:
            user_id (str): The user ID for the VoiceBot.

        Returns:
            Response: The HTTP response object.
        """
        url = f"{self.base_url}/v1/voicebots/callback/{user_id}"
        response = requests.post(url, timeout=self.timeout)
        return self._handle_response(response)

    def create_health_check(self, user_id: str) -> Response:
        """
        Create Health Check

        Args:
            user_id (str): The user ID for the VoiceBot.
        """
        url = f"{self.base_url}/v1/voicebots/{user_id}/health-check"
        response = requests.post(url, timeout=self.timeout)
        return self._handle_response(response)

    def delete_voicebot(self, user_id: str|None = None) -> Response:
        """
        Delete VoiceBot

        Args:
            user_id (str|None): The user ID for the VoiceBot.

        Returns:
            Response: The HTTP response object.
        """
        url = f"{self.base_url}/v1/voicebots/private/{user_id}"

        response = requests.delete(url, timeout=self.timeout)
        return self._handle_response(response)

    def update_callflow(self, user_id: str, body: str) -> Response:
        """
        Update Callflow

        Args:
            user_id (str): The user ID for the VoiceBot.
            body (str): The callflow configuration to update.

        Returns:
            Response: The HTTP response object.
        """
        url = f"{self.base_url}/v1/voicebots/{user_id}/callflow"
        response = requests.put(url, json=body, timeout=self.timeout)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: Response) -> Response:
        """
        Handle Response from HTTP request
        Raise an exception for HTTP errors or return the response.

        Args:
            response (Response): The HTTP response object.

        Returns:
            Response: The HTTP response object if no error occurred.
        """
        response.raise_for_status()
        return response
