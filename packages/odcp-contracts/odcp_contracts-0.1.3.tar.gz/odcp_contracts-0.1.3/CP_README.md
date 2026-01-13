# Owndivision Control Plane – How To & Concepts

This document explains **what the Control Plane (CP)** currently does, what the main
**domain objects** are (organization, workspace, user, subscription, license, etc.),
and **how it interacts with the Data Plane (DP)**.

It is written for:
- Future you
- Any developer onboarding to the project
- Anyone trying to understand how CP ↔ DP ↔ Auth0 fit together

---

## 1. Big Picture

### Control Plane (CP)

The CP is the **“brain” of the platform**:

- Knows your **customers** (organizations)
- Knows **workspaces** inside those organizations
- Manages **users, identities & roles**
- Manages **plans, subscriptions & deployments**
- Issues **license tokens** (signed JWTs) that the DP uses to:
  - Validate entitlement
  - Know which **deployment_id** it belongs to
  - Load license features/seat caps via a `LicenseContext`

### Data Plane (DP)

The DP is the **analytics app instance**:

- Exposes `/api/v1/...` for chats, charts, dashboards, alerts
- Talks to:
  - **MFI DB** for customer data
  - **Internal DB** for app metadata
- Validates every request via:
  - A **license token** (X-License-Token or `LICENSE_TOKEN` in `.env`)
  - An **Auth0 access token** (end-user identity)
- Uses CP’s `/users/whoami` to resolve:
  - Which **CP user** this Auth0 identity belongs to
  - Which **workspaces** and roles they have

---

## 2. Core Domain Objects

Below is what we currently have in the CP models & schemas.

### 2.1 Organization

Represents a **customer organization** (tenant at business level).

Key fields (simplified):

- `id: UUID`
- `name: str`
- `slug: str` (URL-friendly identifier)
- `status: OrganizationStatus` (e.g. `active`, `suspended`)
- `external_id: Optional[str]` – e.g. CRM/customer id

Relationships:

- Has many **Workspaces**
- Has many **Subscriptions**
- Has many **Deployments** (DP instances)
- Indirectly linked to **Licenses** via deployments and subscriptions

Typical lifecycle:

1. CP admin creates an organization.
2. Assigns a subscription + plan.
3. Creates one or more deployments (DP instances) and workspaces.

---

### 2.2 Workspace

Represents a **logical environment inside an organization**.

Example:  
`Acme Corp` (org) can have workspaces:

- `acme-prod`
- `acme-demo`
- `acme-sandbox`

Fields (from `WorkspaceCreateRequest` / `WorkspaceReadResponse`):

- `id: UUID`
- `organization_id: UUID`
- `name: str`
- `slug: str`
- `type: WorkspaceType` (e.g. `PROD`, `DEMO`, `TRIAL`, `SANDBOX`)
- `is_default: bool`

Usage:

- CP uses workspaces to group users & roles.
- DP currently **does not yet** segment data by workspace; it scopes by `deployment_id` + `owner_sub`. Workspaces are already exposed in `/users/whoami` and FE, so they’re ready for future per-workspace scoping.

---

### 2.3 User

Logical **CP user**, independent of the actual IdP.

Fields (simplified):

- `id: UUID`
- `email: str`
- `display_name: Optional[str]`
- `is_active: bool`

Relationships:

- Has many **AuthAccounts** (concrete identities at Auth0/authentik/etc.)
- Has many **WorkspaceMemberships** (with roles per workspace)

---

### 2.4 AuthAccount

Connects a `User` to a **concrete identity provider account**.

Fields:

- `id: UUID`
- `user_id: UUID` → `cp_users.id`
- `provider: AuthProvider` enum (e.g. `AUTH0`, `AUTHENTIK`, `LOCAL`)
- `subject: str` – stable external ID (`sub` claim / NameID)
- `idp_tenant: Optional[str]` – external IdP tenant/org id

Constraint:

- `(provider, subject)` is globally unique  
  → ensures we can look up **one** CP user for a given IdP identity.

This is what `/api/v1/users/whoami` uses when you pass `provider=auth0&subject=<sub>`.

---

### 2.5 Roles

A `Role` describes a **set of permissions** in a workspace (current implementation is mostly structural; enforcement is still light).

Fields:

- `id: UUID`
- `code: str` – machine-readable (e.g. `WORKSPACE_OWNER`, `WORKSPACE_ADMIN`, `WORKSPACE_MEMBER`)
- `name: str` – human-friendly
- `description: Optional[str]`
- `is_system: bool` – built-in vs custom

Roles are attached to memberships (below).

---

### 2.6 WorkspaceMembership

Connects a **User** with a **Workspace** and a **Role**.

Fields (from `WorkspaceMembershipReadResponse`):

- `id: UUID`
- `workspace_id: UUID`
- `user_id: UUID`
- `role_id: UUID`
- `status: MembershipStatus` – e.g. `ACTIVE`, `INVITED`, `SUSPENDED`
- `created_at`, `updated_at`
- Embedded:
  - `user: UserReadResponse`
  - `role: RoleReadResponse`

Semantics:

- This is where **“who can access which workspace and with what level”** lives.
- A user can have multiple memberships across orgs & workspaces.

---

### 2.7 Plans & Subscriptions

#### Plan

Represents a **billing / feature tier**.

From `PlanReadResponse`:

- `code: PlanCode` – stable machine code (`free`, `pro`, `enterprise`, …)
- `name: str`
- `description: Optional[str]`
- `is_public: bool`
- `default_features: Dict[str, Any]` – raw JSON config for limits/features

Examples of features (already supported in schema):

- `alerts_enabled: true/false`
- `max_workspaces: int`
- `max_dashboards_per_workspace: int`
- `max_users_per_organization: int`
- `exports_enabled: bool`, etc.

#### Subscription

Represents **an org’s subscription to a plan**.

From `SubscriptionReadResponse`:

- `id: UUID`
- `organization_id: UUID`
- `plan_code: PlanCode`
- `status: SubscriptionStatus` (e.g. `active`, `trialing`, `canceled`)
- `seat_cap: int`
- `starts_at`, `ends_at`, `trial_ends_at`
- `external_id: Optional[str]` – ID in Stripe/Paddle/etc.

Lifecycle:

1. Org is created.
2. Subscription with `plan_code` is attached.
3. Licenses for deployments draw their default `seat_cap` / features from the subscription + plan.

---

### 2.8 Deployment

A **logical DP instance** (cluster/on-prem install/demo).

From `DeploymentReadResponse`:

- `id: UUID`
- `organization_id: UUID`
- `name: str`
- `type: DeploymentType` (`CLOUD`, `ONPREM`, `DEMO`, etc.)
- `region: Optional[str]`
- `api_base_url: Optional[str]`
- `status: DeploymentStatus`

A single organization can have multiple deployments, e.g.:

- `Acme Cloud EU-West`
- `Acme On-Prem`
- `Acme Demo`

DPs know which deployment they are via the **license token**.

---

### 2.9 License

Represents an **entitlement for a specific deployment**.

From `LicenseReadResponse`:

- `id: UUID`
- `subscription_id: UUID`
- `deployment_id: UUID`
- `seat_cap: int`
- `features: Dict[str, Any]` – effective feature set
- `valid_from`, `valid_until`
- `key_id: Optional[str]` – which key was used to sign exports
- `bundle_hash: Optional[str]` – hash of last exported bundle
- `created_at`, `updated_at`

The key thing: **this is what gets turned into a License Token (JWT)** and installed in the DP.

---

### 2.10 License Bundle (License Token)

From `LicenseBundleResponse`:

- `license_id: UUID`
- `token: str` – signed JWT (compact JWS)
- `key_id: str` – `kid` of signing key (must match public key in JWKS)
- `algorithm: str` – e.g. `RS256`
- `issued_at`, `expires_at`
- `payload: Dict[str, Any]` – decoded claims (for debugging in dev)

This token is:

- Signed by the CP’s **private key** (`CP_SIGNING_PRIVATE_KEY_PATH`)
- Verifiable via the CP’s **JWKS endpoint**  
  (`/api/v1/.well-known/jwks.json` → used by DP)
- Installed into the DP:
  - Either via `LICENSE_TOKEN` env var (local/dev)
  - Or via `X-License-Token` header at the gateway in production

Inside the token:

- High-level standard claims (`iss`, `aud`, `sub`, `exp`, etc.)
- A `license` object with:
  - Organization (id, name, slug, status)
  - Deployment (id, name, type, region, status)
  - Subscription (id, status, seat_cap, dates)
  - Plan (code, name, default_features)
  - Features / limits for this license

The DP reads this and builds a `LicenseContext`.

---

## 3. “Who Am I” Flows

### 3.1 On the Control Plane (`/api/v1/users/whoami`)

Endpoint:  
`GET /api/v1/users/whoami?provider=<provider>&subject=<subject>`

Inputs:

- `provider` – e.g. `"auth0"` (`AuthProvider.AUTH0`)
- `subject` – IdP’s stable id (e.g. Auth0 `sub` claim)

Behavior:

1. Find `AuthAccount` via `(provider, subject)`.
2. Load the `User`.
3. Load all `WorkspaceMembership`s for that user (with embedded role).
4. Return a `WhoAmIResponse`:

   ```jsonc
   {
     "user": {
       "id": "...",
       "email": "...",
       "display_name": "...",
       "is_active": true
     },
     "memberships": [
       {
         "workspace_id": "...",
         "workspace_name": "...",
         "workspace_slug": "...",
         "organization_id": "...",
         "status": "ACTIVE",
         "role": {
           "id": "...",
           "code": "WORKSPACE_OWNER",
           "name": "Workspace Owner",
           "description": "...",
           "is_system": true
         }
       }
     ]
   }
   ```

## odcp-contracts: Versioning & Compatibility

The `odcp-contracts` package defines the **public contract** between the
Control Plane (CP) and Data Plane (DP).

### Public API

The only supported import path is:

```python
from odcp_contracts import DeploymentLicenseClaims, LicenseBodyClaims, WhoAmIResponse
```

### 2️⃣ Versioning & release ritual (how you’ll use it)

Whenever you change **public contracts**:

1. Bump version in `pyproject.toml`:

   ```toml
   [project]
   version = "0.2.0"
   ```

2. Optionally update docs:
   - `CP_README.md`
   - `CHANGELOG.md`

3. Commit and tag the release:

   ```bash
   git add .
   git commit -m "Bump odcp-contracts to v0.2.0"

   git tag -a contracts-v0.2.0 -m "odcp-contracts v0.2.0"
   git push origin main
   git push origin contracts-v0.2.0
   ```

4. The publish workflow runs:
   - `pytest`
   - `python -m build`
   - `twine upload dist/*`

5. In the DP repo, depend on the published package:

   ```toml
   # pyproject.toml of DP
   [project]
   dependencies = [
     "odcp-contracts~=0.2.0",
     # ...
   ]
   ```

Notes

- `odcp-contracts~=0.2.0` allows patch upgrades within `0.2.*` (recommended). Use `==0.2.0` if you want fully pinned builds.
- Stick to semantic versioning:
  - **MAJOR** for breaking contract changes
  - **MINOR** for backward-compatible additions
  - **PATCH** for backward-compatible fixes
