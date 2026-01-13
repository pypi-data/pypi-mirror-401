"""Constants for GL Connectors CLI.

Author:
    I Gusti Ngurah Gana Untaran (i.gusti.n.g.untaran@gdplabs.id)
"""

COMMAND_NAME = "glcon"
DEFAULT_API_URL = "https://connector.gdplabs.id"

# Table Fields
INTEGRATION_FIELD = "Integration"
INTEGRATIONS_COUNT_FIELD = "Integrations Count"
USER_IDENTIFIER_FIELD = "User Identifier"

# Messages
AUTH_NOT_AUTHENTICATED = "Not authenticated. Please run 'glcon auth login' first."
AUTH_LOGIN_HELP = "Run 'glcon auth login <client-api-key> <user-identifier> <user-secret>' to login"

# Main
MAIN_EPILOG = """Examples:
  # Authentication (sets up config)
  glcon auth login                                    # Interactive login (production)
  glcon auth login --api-url http://localhost:8000    # Interactive login (local dev)
  glcon auth login <client-key> <username> <secret>   # Direct login (production)
  glcon auth login --api-url http://localhost:8000 <client-key> <username> <secret>  # Direct login (local dev)
  glcon auth logout                                   # Logout
  glcon auth status                                   # Show auth status

  # Integration Management (uses stored config)
  glcon integrations                                  # List all integrations
  glcon integrations add github                       # Add GitHub integration
  glcon integrations remove github user@example.com  # Remove specific integration
  glcon integrations show github user@example.com    # Show integration details
  glcon integrations select github user@example.com  # Set integration as selected

  # User Registration (no authentication required)
  glcon users create <username>                       # Create new user (will prompt for client API key)
  glcon users create <username> --client-api-key <key> # Create new user with API key

  # Verbose output
  glcon -v auth login                                 # Show detailed progress
"""

# Auth
AUTH_LOGIN_EPILOG = """Examples:
  glcon auth login                                      # Interactive login (prompts for credentials)
  glcon auth login --api-url http://localhost:8000      # Use custom API URL
  glcon auth login <client-api-key> <user> <secret>     # Direct mode (no prompts)
"""

AUTH_MAIN_EPILOG = """Examples:
  glcon auth login                                      # Interactive login
  glcon auth login --api-url http://localhost:8000      # Local development
  glcon auth login <key> <user> <secret>                # Direct login
  glcon auth status                                     # Show current status
  glcon auth logout                                     # Clear session
"""

# Integrations
INTEGRATIONS_MAIN_EPILOG = """Examples:
  glcon integrations                                   # List all integrations
  glcon integrations add github                        # Add GitHub integration
  glcon integrations remove github john@example.com    # Remove specific integration
  glcon integrations show github                       # Show all GitHub integrations account
  glcon integrations show github john@example.com      # Show specific integration details
"""

INTEGRATIONS_ADD_EPILOG = """Examples:
  glcon integrations add github
  glcon integrations add google
"""

INTEGRATIONS_REMOVE_EPILOG = """Examples:
  glcon integrations remove github john@example.com
  glcon integrations remove google john@example.com
"""

INTEGRATIONS_SHOW_EPILOG = """Examples:
  glcon integrations show github                              # Show all GitHub integrations accounts
  glcon integrations show google                              # Show all Google integrations accounts
  glcon integrations show google user@gmail.com              # Show specific integration details
"""

METAVAR_CONNECTOR = "<connector> (example: github, google)"
METAVAR_ACCOUNT = "<user_identifier> (example: john@example.com)"

HELP_IDENTIFIER = "User identifier (optional, e.g., email for Google, username for GitHub)"
HELP_CONNECTOR = "Connector name (e.g., github, google)"

# Users
USERS_MAIN_EPILOG = """Examples:
  glcon users create john_doe                           # Create new user (will prompt for client API key)
  glcon users create john_doe --client-api-key <key>    # Create new user with API key
"""

USERS_CREATE_EPILOG = """Examples:
  glcon users create john_doe                           # Interactive (prompts for client API key)
  glcon users create jane_smith --client-api-key <key>  # With client API key
  """

# HTTP Methods
HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"
HTTP_PATCH = "PATCH"

# HTTP Headers
API_KEY_HEADER = "x-api-key"
AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer"

# Exit codes for better CLI automation
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_AUTH_ERROR = 2
EXIT_INVALID_SUBCOMMAND = 3
EXIT_INVALID_PARAMETERS = 4
EXIT_REQUEST_ERROR = 5
