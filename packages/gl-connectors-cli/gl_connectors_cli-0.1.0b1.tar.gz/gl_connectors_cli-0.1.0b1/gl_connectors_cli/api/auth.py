"""Authentication API client for GL Connectors CLI.

Author:
    I Gusti Ngurah Gana Untaran (i.gusti.n.g.untaran@gdplabs.id)
"""

from gl_connectors_cli.api.base import BaseAPIClient
from gl_connectors_cli.api.models import Token
from gl_connectors_cli.constants import API_KEY_HEADER, HTTP_POST
from gl_connectors_cli.utils import CLIError


class AuthAPIClient(BaseAPIClient):
    """Authentication API client."""

    def authenticate_user(self, client_key: str, identifier: str, secret: str) -> Token:
        """Authenticate user and get JWT token.

        Args:
            client_key: Client API key
            identifier: User identifier
            secret: User secret

        Returns:
            Authentication token information

        Raises:
            CLIError: If authentication fails

        """
        headers = {
            API_KEY_HEADER: client_key,
        }

        data = {"identifier": identifier, "secret": secret}

        try:
            response = self._make_request(HTTP_POST, "/clients/oauth-token", headers=headers, data=data)
            token_data = response.get("data", None)

            if not token_data:
                raise CLIError("Authentication error. Please check your credentials and try again.")

            return Token(**token_data)

        except Exception as e:
            raise CLIError(str(e)) from e
