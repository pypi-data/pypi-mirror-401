"""
Stable contracts for CP↔DP interface.

This package exposes Pydantic models that define the public interface
between Control Plane and Data Plane. These models should remain stable
and backward-compatible.

All models use extra="allow" to support forward compatibility - new fields
can be added without breaking existing DP deployments.

IMPORTANT:
- DP and other consumers should only import from `odcp_contracts`, not from
  submodules (e.g. `odcp_contracts.licensing`). Anything not exported in
  __all__ is considered internal and may change without notice.
"""

from .licensing import (DeploymentClaims, DeploymentLicenseClaims,
                        LicenseBodyClaims, OrganizationClaims, PlanClaims,
                        SubscriptionClaims)
from .whoami import (WhoAmIResponse, WhoAmIRole, WhoAmIUser,
                     WhoAmIWorkspaceMembership)

__all__ = [
    # License claims
    "DeploymentLicenseClaims",
    "LicenseBodyClaims",
    "OrganizationClaims",
    "DeploymentClaims",
    "SubscriptionClaims",
    "PlanClaims",
    # WhoAmI
    "WhoAmIResponse",
    "WhoAmIUser",
    "WhoAmIWorkspaceMembership",
    "WhoAmIRole",
]
