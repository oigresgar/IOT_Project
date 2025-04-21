import requests


class AmiLabHttp:
    """
    A class to encapsulate the HTTP requests to the AmiLab API.

    Args:
        url (str): The URL of the AmiLab API.
        token (str): The token for authentication.
    """

    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token

    @property
    def token(self):
        """
        Get the token.

        Returns:
            str: The token.
        """
        return self._token

    @token.setter
    def token(self, token: str):
        """
        Set the token.

        Args:
            token (str): The token.
        """
        self._token = token

    @token.getter
    def token(self):
        """
        Get the token.

        Returns:
            str: The token.
        """
        if self._token is None:
            raise ValueError("AmiLab token not set, check your environment variables.")
        return self._token

    @property
    def url(self):
        """
        Get the URL.

        Returns:
            str: The URL.
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """
        Set the URL.

        Args:
            url (str): The URL.
        """
        self._url = url

    @url.getter
    def url(self):
        """
        Get the URL.

        Returns:
            str: The URL.
        """
        if self._url is None:
            raise ValueError("AmiLab URL not set, check your environment variables.")
        return self._url

    def get_state(self, entity_id: str):
        """
        Get the state of an entity.

        Args:
            entity_id (str): The ID of the entity.

        Returns:
            dict: The state of the entity as a json.
        """
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }
        return requests.get(self.url + "/states/" + entity_id, headers=headers).json()

    def post_service(
        self, entity_id: str, service: str, command: str, extra_data: dict = {}
    ):
        """
        Post a service command to an entity.

        Args:
            entity_id (str): The ID of the entity.
            service (str): The service to call.
            command (str): The command to call.
            extra_data (dict): Extra data to send with the command.

        Returns:
            dict: The response from the API as a json.
        """
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }
        data = {
            "entity_id": entity_id,
        }
        data.update(extra_data)
        return requests.post(
            self.url + "/services/" + service + "/" + command,
            headers=headers,
            json=data,
        ).json()

    def get_snapshot(self, mock=False) -> bytes:
        """
        Get a snapshot from the AmiLab camera.

        Args:
            mock (bool): Whether to use a mock image instead of the actual camera.
                Defaults to False.
        Returns:
            bytes: The snapshot image as bytes.
        """
        if mock:
            with open("utils/mock.jpg", "rb") as f:
                return f.read()
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "image/jpeg",
        }
        return requests.get(
            self.url + "/camera_proxy/camera.amicam", headers=headers
        ).content
