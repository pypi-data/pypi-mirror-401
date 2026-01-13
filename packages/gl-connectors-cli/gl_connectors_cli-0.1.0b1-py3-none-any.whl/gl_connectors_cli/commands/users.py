"""User management commands for GL Connectors CLI.

Author:
    I Gusti Ngurah Gana Untaran (i.gusti.n.g.untaran@gdplabs.id)
"""

from argparse import RawDescriptionHelpFormatter
from typing import Optional

from gl_connectors_cli.api import UsersAPIClient
from gl_connectors_cli.commands.base import BaseCommands
from gl_connectors_cli.config import CLIConfig
from gl_connectors_cli.constants import (
    EXIT_AUTH_ERROR,
    EXIT_INVALID_SUBCOMMAND,
    EXIT_REQUEST_ERROR,
    USERS_CREATE_EPILOG,
    USERS_MAIN_EPILOG,
)
from gl_connectors_cli.utils import (
    CLIError,
    fail,
    print_header,
    print_info,
    print_success,
    print_warning,
    prompt_for_input,
    succeed,
)


class UsersCommands(BaseCommands):
    """User management command handlers."""

    def __init__(self, config: Optional[CLIConfig] = None):
        """Initialize user commands.

        Args:
            config: CLI configuration (optional for parser setup)

        """
        super().__init__(config)
        if config:
            self.api_client = UsersAPIClient(config.get_api_url())

    @classmethod
    def add_subparser(cls, subparsers):
        """Add command-specific subparser and arguments (class method).

        Args:
            subparsers: Parent subparsers object

        Returns:
            The users parser for help display

        """
        users_parser = subparsers.add_parser(
            "users", help="User management", epilog=USERS_MAIN_EPILOG, formatter_class=RawDescriptionHelpFormatter
        )
        users_subparsers = users_parser.add_subparsers(dest="users_command", required=False)
        users_parser.error = cls.users_error_handler

        # Create command
        create_parser = users_subparsers.add_parser(
            "create", help="Create a new user", epilog=USERS_CREATE_EPILOG, formatter_class=RawDescriptionHelpFormatter
        )
        create_parser.add_argument(
            "username",
            metavar="<user_identifier> (example: john_doe, john.doe@example.com)",
            help="Identifier for the new user",
        )
        create_parser.add_argument(
            "--client-api-key",
            help="Client API key (sk-client-...). If not provided, will prompt for input.",
        )
        cls.parser = users_parser

        return users_parser

    @classmethod
    def users_error_handler(cls, message: str) -> None:
        """Handle user command errors.

        Args:
            message: Error message

        """
        cls.parser.print_help()
        return fail(message, EXIT_INVALID_SUBCOMMAND)

    def handle(self, args):
        """Handle user commands.

        Args:
            args: Parsed command line arguments

        Returns:
            Exit code (0 for success, 1 for error)

        """
        match args.users_command:
            case "create":
                # Create user doesn't require authentication (it's for registration)
                client_api_key = getattr(args, "client_api_key", None)
                return self.create_user(args.username, client_api_key)
            case _:
                # Other user commands require authentication
                if not self._is_authenticated():
                    return fail("Not authenticated", EXIT_AUTH_ERROR)

    def create_user(self, username: str, client_api_key: Optional[str] = None) -> int:
        """Create a new user.

        Args:
            username: Username for the new user
            client_api_key: Client API key (optional, will prompt if not provided)

        Returns:
            Exit code (0 for success, 1 for error)

        """
        try:
            # Get client API key from parameter or prompt
            if not client_api_key:
                client_api_key = prompt_for_input("Client API Key", hide=True)

            print_info(f"Creating user '{username}'...")
            user_data = self.api_client.create_user(client_api_key, username)

            print_success("User created successfully!")
            print()
            print_header("User Details")
            print_info(f"Username: {user_data.identifier or 'N/A'}")

            print()
            print_warning("The full user secret is only shown once and cannot be recovered.")
            print_info(f"Full secret: {user_data.secret or 'Not provided'}")

            return succeed()

        except CLIError as e:
            return fail(str(e), EXIT_REQUEST_ERROR)
        except Exception as e:
            return fail(f"Failed to create user: {str(e)}")
