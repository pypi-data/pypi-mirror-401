"""Shared data models for GL Connectors CLI API clients.

Author:
    I Gusti Ngurah Gana Untaran (i.gusti.n.g.untaran@gdplabs.id)
"""

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class User(BaseModel):
    """GL Connectors user information."""

    id: str
    identifier: str = ""
    secret_preview: str = ""
    is_active: bool = True
    client_id: str = ""
    integrations: List[Dict[str, Any]] = Field(default_factory=list)


class CreatedUser(User):
    """GL Connectors user information with secret."""

    secret: str = ""


class Token(BaseModel):
    """GL Connectors authentication token."""

    token: str
    token_type: str = "Bearer"
    expires_at: datetime = Field(default_factory=datetime.now)
    is_revoked: bool = False
    user_id: str = ""


class IntegrationDetail(BaseModel):
    """Integration detail."""

    connector: str
    user_identifier: str
    auth_string: str
    auth_scopes: List[str]
    selected: bool = False
