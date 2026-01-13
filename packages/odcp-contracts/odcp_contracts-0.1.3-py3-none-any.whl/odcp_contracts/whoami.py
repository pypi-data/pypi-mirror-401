"""
WhoAmI response contracts for CP↔DP interface.

This module defines the stable Pydantic models for the /api/v1/users/whoami
response that CP returns and DP consumes. These models must remain backward-compatible.
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class WhoAmIRole(BaseModel):
    """Role information in WhoAmI response."""

    model_config = ConfigDict(extra="allow")

    id: UUID
    code: str
    name: str
    description: Optional[str] = None
    is_system: bool


class WhoAmIWorkspaceMembership(BaseModel):
    """Workspace membership information in WhoAmI response."""

    model_config = ConfigDict(extra="allow")

    workspace_id: UUID
    workspace_name: str
    workspace_slug: str
    organization_id: UUID
    status: str
    role: WhoAmIRole


class WhoAmIUser(BaseModel):
    """User information in WhoAmI response."""

    model_config = ConfigDict(extra="allow")

    id: UUID
    email: EmailStr
    display_name: Optional[str] = None
    is_active: bool


class WhoAmIResponse(BaseModel):
    """
    Complete /api/v1/users/whoami response.

    This represents the full response returned by CP's whoami endpoint,
    containing user details and all workspace memberships with their roles.
    """

    model_config = ConfigDict(extra="allow")

    user: WhoAmIUser
    memberships: List[WhoAmIWorkspaceMembership]
