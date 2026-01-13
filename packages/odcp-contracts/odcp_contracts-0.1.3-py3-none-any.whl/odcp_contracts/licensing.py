"""
License JWT claims contracts for CP↔DP interface.

This module defines the stable Pydantic models for deployment license JWTs
that CP signs and DP verifies. These models must remain backward-compatible.
"""

from datetime import datetime
from typing import Any, Dict, Optional, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrganizationClaims(BaseModel):
    """Organization details embedded in license claims."""

    model_config = ConfigDict(extra="allow")

    id: UUID
    name: str
    slug: str
    external_id: Optional[str] = None
    status: str


class DeploymentClaims(BaseModel):
    """Deployment details embedded in license claims."""

    model_config = ConfigDict(extra="allow")

    id: UUID
    name: str
    type: Literal["cloud", "demo", "onprem"]

    region: Optional[str] = None
    api_base_url: Optional[str] = None
    status: str


class SubscriptionClaims(BaseModel):
    """Subscription details embedded in license claims."""

    model_config = ConfigDict(extra="allow")

    id: UUID
    status: str
    seat_cap: int
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    trial_ends_at: Optional[datetime] = None
    external_id: Optional[str] = None


class PlanClaims(BaseModel):
    """Plan details embedded in license claims."""

    model_config = ConfigDict(extra="allow")

    code: str
    name: str
    description: Optional[str] = None
    default_features: Dict[str, Any]


class LicenseBodyClaims(BaseModel):
    """Nested license body within JWT claims."""

    model_config = ConfigDict(extra="allow")

    license_id: UUID
    seat_cap: int
    features: Dict[str, Any]
    organization: OrganizationClaims
    deployment: DeploymentClaims
    subscription: SubscriptionClaims
    plan: PlanClaims


class DeploymentLicenseClaims(BaseModel):
    """
    Top-level JWT claims for deployment licenses.

    This represents the complete payload that CP signs into a JWT
    and DP verifies. It includes standard JWT claims plus the
    license body with organization, deployment, subscription, and plan details.
    """

    model_config = ConfigDict(extra="allow")

    # Standard JWT claims
    iss: str
    aud: str
    sub: UUID
    jti: UUID
    iat: int
    nbf: int
    exp: Optional[int] = None

    # License payload
    license: LicenseBodyClaims
