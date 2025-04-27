# OAuth 2.0 & Azure Identity Guide

A comprehensive reference covering OAuth 2.0 fundamentals, directory services, Azure Identity components, service identities, API management, and authentication for Azure data platforms. Includes detailed PlantUML mind-maps and full Python code examples using the Azure Identity library.

---

## Mind‑Map Explanations

### Protocol Components
```puml
@startmindmap
* OAuth 2.0
** Protocol Components
*** Roles
**** Resource Owner: End user who grants access to resources
**** Client: Application requesting access on behalf of user
**** Authorization Server: Issues tokens after authenticating Resource Owner
**** Resource Server: Hosts protected resources and validates tokens
*** Endpoints
**** Authorization Endpoint: User authorizes client and receives code
**** Token Endpoint: Client exchanges grant for tokens
**** Redirection Endpoint: Client receives authorization responses
**** Revocation Endpoint: Revoke access or refresh tokens
*** Grant Types
**** Authorization Code: Secure server-side exchange of code for tokens
**** Implicit: Direct token issuance in browser (legacy)
**** Client Credentials: Service-to-service without user context
**** Device Code: Device-based flow for input-constrained clients
**** Resource Owner Password Credentials (ROPC): Direct username/password exchange (not recommended)
**** Refresh Token: Obtain new access tokens silently
*** Token Types
**** Access Token: Grants access to resource APIs
**** Refresh Token: Used to renew access tokens
**** ID Token: Contains user identity claims (OIDC)
@endmindmap
```
This mind-map breaks down OAuth 2.0’s core elements—roles, endpoints, grant types, and token types—showing how each component fits into the overall protocol.

### OAuth Flows in Microsoft Identity Platform
```puml
@startmindmap
* OAuth 2.0
** OAuth Flows in Microsoft Identity Platform
*** Authorization Code Flow
**** Description: Secure server-side flow with code exchange
**** Features:
***** Supports PKCE (Proof Key for Code Exchange)
***** Redirect URI validation enforced
***** CSRF protection via state parameter
**** Use Cases:
***** Web applications (e.g., ASP.NET Core)
***** Single-page apps (SPA) using Auth Code + PKCE
**** Libraries:
***** MSAL.NET, MSAL.js
***** ADAL (legacy)
**** Example Sequence:
***** User → Auth endpoint → code → Token endpoint → Access/ID tokens

*** Implicit Flow (Legacy)
**** Description: Direct token issuance without code
**** Limitations:
***** No refresh tokens
***** Vulnerable to token leakage
**** Use Cases:
***** Very old SPAs (pre-PKCE)
**** Deprecation:
***** Replaced by Auth Code + PKCE

*** Client Credentials Flow
**** Description: Service-to-service without user context
**** Credentials:
***** client_id + client_secret or certificate
**** Use Cases:
***** Daemons, microservices, background jobs
***** Microsoft Graph app-only access
**** Token Type:
***** Access token only

*** On-Behalf-Of Flow (OBO)
**** Description: Delegation via user assertion
**** Flow:
***** API receives user token → exchanges for downstream token
**** Use Cases:
***** Middle-tier APIs calling other APIs
***** Requires Azure AD v2 tokens

*** Device Code Flow
**** Description: Interactive login for devices without browser
**** Steps:
***** App displays code and verification URL
***** User authenticates on separate device
***** App polls token endpoint
**** Use Cases:
***** CLI tools, TV apps, IoT devices

*** ROPC Flow (Resource Owner Password Credentials)
**** Description: Directly submits username/password
**** Risks:
***** High risk: credentials exposed
***** No MFA or Conditional Access
**** Use Cases:
***** Legacy migrations only (not recommended)

*** Refresh Token Flow
**** Description: Obtain new tokens silently
**** Features:
***** Rotating refresh tokens
***** Honors Conditional Access policies
**** Libraries:
***** Handled automatically by MSAL

*** Key Concepts
**** Scopes: Permissions requested by the app
**** State Parameter: CSRF mitigation
**** PKCE: Proof Key for Code Exchange
**** Consent: User grants or denies permissions
@endmindmap
```
An overview of every OAuth 2.0 flow supported by Azure AD, with details on when and why to use each—ranging from secure server-side authorization code exchanges to legacy implicit and ROPC flows.

### Windows Active Directory
```puml
@startmindmap
* Windows Active Directory
** Components
*** Forest, Domain, OU, DC, Global Catalog, Schema
** Services
*** LDAP, Kerberos, DNS, Replication, Group Policy
** Objects
*** Users, Groups, Computers, Service Accounts
** Trusts
*** Intra-Forest, External, Forest
@endmindmap
```
Shows on-prem AD’s structure: how forests, domains, and OUs organize objects; the services that enable directory functionality; and the trust relationships linking domains.

### LDAP Flows
```puml
@startmindmap
* LDAP Flows
** Bind (Simple/SASL)
** Search (Base/OneLevel/Subtree)
** Modify (Add/Replace/Delete)
** Add Entry
** Delete Entry
** Unbind
** Extended Operations (StartTLS, Password Modify)
@endmindmap
```
Depicts the lifecycle of an LDAP session: authenticating, querying, updating, and closing connections, as well as advanced operations like StartTLS.

### Azure Active Directory (Entra)
```puml
@startmindmap
* Azure Active Directory (Entra)
** Tenants & Subscriptions
** Identity Objects: Users, Groups, Service Principals, Managed Identities
** Protocols: OAuth 2.0, OpenID Connect, SAML
** Services: Conditional Access, Identity Protection, PIM, B2B/B2C
** Integrations: Microsoft 365, Azure RBAC, App Registrations, Hybrid Join
@endmindmap
```
Visualizes Entra ID’s tenant model, supported identity objects, protocols, security services, and integration points with other Microsoft platforms.

### Hybrid Identity
```puml
@startmindmap
* Hybrid Azure AD & Windows AD
** Azure AD Connect (Password Hash Sync, Pass-through Auth, Federation)
** Seamless SSO (Kerberos-based)
** Device Registration (Hybrid & Azure AD Join)
** App Proxy & SSO to On-Prem Apps
** Conditional Access policies
** Governance: GPO sync, audit, access reviews
** Topology: HA, DR
@endmindmap
```
Explains how on-prem AD and Entra ID synchronize identities and enable unified authentication, from password sync to seamless SSO and device join.

---

## 1. OAuth 2.0 Fundamentals 2.0 Fundamentals

### 1.1 Protocol Components

<details>
<summary>Details & Example</summary>

```puml
@startmindmap
* OAuth 2.0
** Protocol Components
*** Roles
**** Resource Owner: End user who grants access to resources
**** Client: Application requesting access on behalf of user
**** Authorization Server: Issues tokens after authenticating Resource Owner
**** Resource Server: Hosts protected resources and validates tokens
*** Endpoints
**** Authorization Endpoint: User authorizes client and receives code
**** Token Endpoint: Client exchanges grant for tokens
**** Redirection Endpoint: Client receives authorization responses
**** Revocation Endpoint: Revoke access or refresh tokens
*** Grant Types
**** Authorization Code: Secure server-side exchange of code for tokens
**** Implicit: Direct token issuance in browser (legacy)
**** Client Credentials: Service-to-service without user context
**** Device Code: Device-based flow for input-constrained clients
**** Resource Owner Password Credentials (ROPC): Direct username/password exchange (not recommended)
**** Refresh Token: Obtain new access tokens silently
*** Token Types
**** Access Token: Grants access to resource APIs
**** Refresh Token: Used to renew access tokens
**** ID Token: Contains user identity claims (OIDC)
@endmindmap
```

**What it is**: This mind-map visually represents the core components of the OAuth 2.0 protocol and their relationships.

**How it works**: Each branch delineates a component category (roles, endpoints, grants, tokens) and its sub-elements, enabling quick comprehension of the protocol's structure.

**Python Example**:
```python
from azure.identity import DefaultAzureCredential
cred = DefaultAzureCredential()
token = cred.get_token("https://graph.microsoft.com/.default")
print(token.token)
```
</details>

### 1.2 OAuth Flows in Microsoft Identity Platform OAuth Flows in Microsoft Identity Platform

```puml
@startmindmap
* OAuth 2.0
** OAuth Flows in Microsoft Identity Platform
*** Authorization Code Flow
**** Description: Secure server-side flow with code exchange
**** Features:
***** Supports PKCE (Proof Key for Code Exchange)
***** Redirect URI validation enforced
***** CSRF protection via state parameter
**** Use Cases:
***** Web applications (e.g., ASP.NET Core)
***** Single-page apps (SPA) using Auth Code + PKCE
**** Libraries:
***** MSAL.NET, MSAL.js
***** ADAL (legacy)
**** Example Sequence:
***** User → Auth endpoint → code → Token endpoint → Access/ID tokens

*** Implicit Flow (Legacy)
**** Description: Direct token issuance without code
**** Limitations:
***** No refresh tokens
***** Vulnerable to token leakage
**** Use Cases:
***** Very old SPAs (pre-PKCE)
**** Deprecation:
***** Replaced by Auth Code + PKCE

*** Client Credentials Flow
**** Description: Service-to-service without user context
**** Credentials:
***** client_id + client_secret or certificate
**** Use Cases:
***** Daemons, microservices, background jobs
***** Microsoft Graph app-only access
**** Token Type:
***** Access token only

*** On-Behalf-Of Flow (OBO)
**** Description: Delegation via user assertion
**** Flow:
***** API receives user token → exchanges for downstream token
**** Use Cases:
***** Middle-tier APIs calling other APIs
***** Requires Azure AD v2 tokens

*** Device Code Flow
**** Description: Interactive login for devices without browser
**** Steps:
***** App displays code and verification URL
***** User authenticates on separate device
***** App polls token endpoint
**** Use Cases:
***** CLI tools, TV apps, IoT devices

*** ROPC Flow (Resource Owner Password Credentials)
**** Description: Directly submits username/password
**** Risks:
***** High risk: credentials exposed
***** No MFA or Conditional Access
**** Use Cases:
***** Legacy migrations only (not recommended)

*** Refresh Token Flow
**** Description: Obtain new tokens silently
**** Features:
***** Rotating refresh tokens
***** Honors Conditional Access policies
**** Libraries:
***** Handled automatically by MSAL

*** Best Practices & Recommendations
**** Always use Authorization Code + PKCE for public clients
**** Avoid Implicit and ROPC flows
**** Secure client secrets and certificates
**** Implement proper token caching and revocation

*** Key OAuth Concepts
**** Scopes: Permissions requested by the application
**** State Parameter: CSRF mitigation
**** PKCE: Enhances security for public clients
**** Consent: User grants or denies permissions
@endmindmap
```puml
@startmindmap
* OAuth 2.0
** Flows (Azure AD)
*** Authorization Code (with PKCE)
*** Implicit (legacy)
*** Client Credentials
*** On-Behalf-Of
*** Device Code
*** ROPC
*** Refresh Token
@endmindmap
```

### 1.3 Flow Descriptions & Use Cases

- **Authorization Code Flow**: Server-side apps redirect users to auth endpoint, exchange code for tokens. Supports PKCE, `state`, redirect validation. Use for web apps and SPAs.
- **Implicit Flow**: Browser-based direct token issuance. No refresh tokens, vulnerable. Legacy only.
- **Client Credentials Flow**: App uses client ID & secret/certificate to get tokens without user context. For daemons, microservices.
- **On-Behalf-Of Flow**: Middle-tier API exchanges incoming user token for downstream API token. For multi-tier services.
- **Device Code Flow**: CLI/IoT apps show code & URL; user authenticates elsewhere; app polls for token.
- **ROPC Flow**: App directly submits username/password. High risk, no MFA. Legacy migrations only.
- **Refresh Token Flow**: Use refresh token to silently renew access tokens. Handled by MSAL/MSIdentity libraries.

### 1.4 Example Scenarios

1. Web application (Authorization Code)
2. SPA with PKCE (Auth Code + PKCE)
3. Daemon service (Client Credentials)
4. CLI tool (Device Code)
5. Middle-tier API (On-Behalf-Of)
6. Legacy migration (ROPC)
7. Long-lived session (Refresh Token)

### 1.5 Python Code Examples (Azure Identity)

#### 1. Authorization Code Flow

```python
from azure.identity import InteractiveBrowserCredential

cred = InteractiveBrowserCredential(
    tenant_id="<TENANT_ID>",
    client_id="<CLIENT_ID>"
)
token = cred.get_token("User.Read")
print(token.token)
```

#### 2. Implicit Flow (Manual URL Construction)

```python
import urllib.parse

params = {
    "client_id": "<CLIENT_ID>",
    "response_type": "token id_token",
    "redirect_uri": "http://localhost:5000/callback",
    "scope": "openid profile User.Read",
    "state": "12345",
    "nonce": "678910"
}
auth_url = (
    f"https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/authorize?" +
    urllib.parse.urlencode(params)
)
print("Open this URL in a browser:", auth_url)
```

#### 3. Client Credentials Flow

```python
from azure.identity import ClientSecretCredential

cred = ClientSecretCredential(
    tenant_id="<TENANT_ID>",
    client_id="<CLIENT_ID>",
    client_secret="<CLIENT_SECRET>"
)
token = cred.get_token("https://graph.microsoft.com/.default")
print(token.token)
```

#### 4. On-Behalf-Of Flow

```python
from azure.identity import OnBehalfOfCredential

cred = OnBehalfOfCredential(
    tenant_id="<TENANT_ID>",
    client_id="<CLIENT_ID>",
    client_secret="<CLIENT_SECRET>",
    user_assertion="<USER_ACCESS_TOKEN>"
)
token = cred.get_token("https://graph.microsoft.com/.default")
print(token.token)
```

#### 5. Device Code Flow

```python
from azure.identity import DeviceCodeCredential

cred = DeviceCodeCredential(
    client_id="<CLIENT_ID>",
    tenant_id="<TENANT_ID>"
)
token = cred.get_token("User.Read")
print(token.token)
```

#### 6. ROPC Flow

```python
from azure.identity import UsernamePasswordCredential

cred = UsernamePasswordCredential(
    client_id="<CLIENT_ID>",
    username="<USERNAME>",
    password="<PASSWORD>",
    tenant_id="<TENANT_ID>"
)
token = cred.get_token("User.Read")
print(token.token)
```

#### 7. Refresh Token Flow

```python
from azure.identity import DefaultAzureCredential

cred = DefaultAzureCredential()
# First request obtains initial token
tok1 = cred.get_token("https://graph.microsoft.com/.default")
print("Initial token:", tok1.token)
# Subsequent request triggers silent refresh
tok2 = cred.get_token("https://graph.microsoft.com/.default")
print("Refreshed token:", tok2.token)
```

---

## 2. Directory Services

### 2.1 Windows Active Directory

```puml
@startmindmap
* Windows Active Directory
** Components
*** Forest, Domain, OU, DC, Global Catalog, Schema
** Services
*** LDAP, Kerberos, DNS, Replication, Group Policy
** Objects
*** Users, Groups, Computers, Service Accounts
** Trusts
*** Intra-Forest, External, Forest
@endmindmap
```

### 2.2 LDAP Flows

```puml
@startmindmap
* LDAP Flows
** Bind (Simple/SASL)
** Search (Base/OneLevel/Subtree)
** Modify (Add/Replace/Delete)
** Add/Delete Entry
** Unbind
** Extended Operations (StartTLS, Password Modify)
@endmindmap
```

### 2.3 Querying LDAP (Python)

```python
from ldap3 import Server, Connection, ALL, SUBTREE

server = Server('ldap://ad.example.com', get_info=ALL)
conn = Connection(
    server,
    user='CN=svc_account,OU=Service Accounts,DC=example,DC=com',
    password='P@ssw0rd',
    auto_bind=True
)
conn.search(
    search_base='DC=example,DC=com',
    search_filter='(objectClass=user)',
    search_scope=SUBTREE,
    attributes=['cn', 'mail', 'memberOf']
)
for entry in conn.entries:
    print(entry)
conn.unbind()
```

---

## 3. Azure Identity Core

### 3.1 Azure Active Directory (Entra)

```puml
@startmindmap
* Azure Active Directory (Entra)
** Tenants & Subscriptions
** Identity Objects: Users, Groups, Service Principals, Managed Identities
** Protocols: OAuth 2.0, OpenID Connect, SAML
** Services: Conditional Access, Identity Protection, PIM, B2B/B2C
** Integrations: Microsoft 365, Azure RBAC, App Registrations, Hybrid Join
@endmindmap
```

### 3.2 Hybrid Identity

```puml
@startmindmap
* Hybrid Azure AD & Windows AD
** Azure AD Connect (Password Hash Sync, Pass-through Auth, Federation)
** Seamless SSO (Kerberos-based)
** Device Registration (Hybrid & Azure AD Join)
** App Proxy & SSO to On-Prem Apps
** Conditional Access across environments
** Governance: GPO sync, Audit logs, Access reviews
** Topology: HA, Disaster Recovery
@endmindmap
```

---

## 4. Azure Service Identities

### 4.1 Service Principals & Managed Identities

```puml
@startmindmap
* Azure Service Identities
** Service Principals: App identities in AAD
** Managed Identities
*** System-Assigned: tied to resource lifecycle
*** User-Assigned: standalone, assignable to many
** Auth Flow
*** Resource fetches token from IMDS
*** Uses token to call Azure APIs
** Use Cases: CI/CD, VMs, Functions, Multi-resource access
@endmindmap
```

#### 4.1.1 Azure Service Principal Functionalities

```puml
@startmindmap
* Azure Service Principal
** Definition
*** Represents an application in AAD
*** Acts as security identity for apps/services
** Authentication Methods
*** Client Secret
*** Client Certificate
*** Federated Identity Credential (OIDC)
** Authorization Models
*** App Roles
*** OAuth 2.0 Scopes
*** Azure RBAC assignments
** Lifecycle Management
*** Creation via Portal, CLI, ARM templates
*** Credential rotation and expiry
*** Deletion and cleanup
** Integration Points
*** App Registrations
*** Enterprise Applications
*** CI/CD pipelines (e.g. GitHub Actions, Azure Pipelines)
*** Managed Identity federation for workload identity
@endmindmap
```puml
@startmindmap
* Azure Service Identities
** Service Principals: App identities in AAD
** Managed Identities
*** System-Assigned: tied to resource lifecycle
*** User-Assigned: standalone, assignable to many
** Auth Flow
*** Resource fetches token from IMDS
*** Uses token to call Azure APIs
** Use Cases: CI/CD, VMs, Functions, Multi-resource access
@endmindmap
```

### 4.2 Workload Identity (AKS)

```puml
@startmindmap
* AKS Workload Identity
** OIDC Issuer enabled on cluster
** Kubernetes Service Account with annotations
** Federated Identity Credential in AAD App
** Pod requests JWT via TokenRequest API
** API server exchanges JWT for Azure AD token
** Use Cases: Key Vault, Storage, Azure Resource access
@endmindmap
```

### 4.3 AKS Cluster Authentication

```puml
@startmindmap
* AKS Cluster Authentication
** Cluster Admin Authentication
*** Azure AD Admins & Admin Groups
*** OIDC Issuer Profile configured
*** API Server enforces AAD tokens
** User Access
*** `az aks get-credentials` retrieves kubeconfig with AAD auth
*** kubectl uses AAD-issued access tokens
*** Kubernetes RBAC: RoleBindings & ClusterRoleBindings
** Service Principal / Managed Identity
*** Cluster provisioning identity (SP or MI)
*** Permissions: VNet Contributor, Load Balancer Contributor
** Pod Authentication
*** Workload Identity (see 4.2)
@endmindmap
```

## 5. API Management. API Management

```puml
@startmindmap
* Azure API Management
** Authentication
*** Subscription Key (header/query)
*** OAuth 2.0 (Auth Code, Client Credentials)
*** JWT Validation (validate-jwt policy)
*** Client Certificates (mTLS)
*** Basic Auth
** Authorization
*** Products & Subscriptions
*** Scopes & Quotas
** Pass-Through
*** Forward Authorization header
*** Certificate forwarding
*** set-header policy
** Policy Engine
*** Inbound, Backend, Outbound, Error handling
** Integration
*** Azure AD, OpenID Connect, AAD B2C
*** Backend APIs (REST, SOAP, GraphQL)
@endmindmap
```

---

## 6. Azure Data Platform Authentication

### 6.1 Azure Database for PostgreSQL

```puml
@startmindmap
* Azure PostgreSQL Authentication
** Client Stage
*** Username & Password: native auth
*** SSL/TLS Enforcement: sslmode=require
*** Azure AD Token Credential
** Network Stage
*** Firewall rules, VNet endpoints, Private Link
** Authentication Stage
*** Native vs Azure AD (JWT) validation
** Token Acquisition Stage
*** ManagedIdentityCredential, InteractiveBrowserCredential, DeviceCodeCredential
*** Audience: https://ossrdbms-aad.database.windows.net/.default
** Connection Stage
*** Connection string components
**** Host, Port, Database, SSL mode, Access token
*** Client libraries: psycopg2 + azure.identity, pg8000
** Monitoring & Audit
*** AAD Sign-In logs, pgaudit extension
@endmindmap
```

### 6.2 Azure SQL & Hyperscale

```puml
@startmindmap
* Azure SQL Server Authentication
** Methods: SQL Auth, Azure AD Auth (users, MIs)
** Flow: credentials/token → engine validation → RBAC
** Network: TLS, firewall, VNet, Private Link

* Azure SQL Hyperscale
** Primary: control plane for auth
** Secondary replicas: read-only workloads
** Token propagation via listener endpoints
** Connectivity: read-write vs read-only listeners
@endmindmap
```

### 6.3 Azure SQL Data Warehouse

```puml
@startmindmap
* Azure SQL Data Warehouse Authentication
** Methods: SQL Auth, Azure AD Auth
** Connectivity: firewall, VNet, Private Link
** Flow: token or password validation
** Scale: dedicated pool endpoints, Data Movement auth
@endmindmap
```

### 6.4 Azure Synapse Analytics

```puml
@startmindmap
* Azure Synapse Analytics Authentication
** Methods: SQL Auth, Azure AD Auth, Managed Identities
** Components: SQL pools, Spark pools, Integration Runtimes
** Flow: OAuth2 token acquisition → endpoint validation
** Networking: firewall, Managed VNet, Private Endpoints
** Authorization: Azure RBAC, ACLs, SAS tokens
@endmindmap
```

### 6.5 Azure Databricks

```puml
@startmindmap
* Azure Databricks Authentication
** Methods: AAD OAuth token, Personal Access Token
** Identity sources: Service Principal, Managed Identity, Users/Groups
** Token acquisition: InteractiveBrowserCredential, ClientSecretCredential, ManagedIdentityCredential
** API/JDBC auth: Bearer token in header/conn string
** Credential passthrough: SCIM, Unity Catalog
** Governance: Conditional Access, RBAC, Audit logs
@endmindmap
```

### 6.6 Control Plane Sharing

```puml
@startmindmap
* Azure & Databricks Control Planes
** Azure Control Plane: ARM, Resource Providers, AAD, Portal/CLI/API
** Databricks Control Plane: metadata, clusters, jobs, notebooks, PATs
** Data Plane: customer VNet, compute, storage (DBFS, ADLS)
** Orchestration Flow: ARM → CP deploys workspace → CP orchestrates DP via REST/gRPC
@endmindmap
```

---

## 7. Sending Email via Microsoft Graph API

```puml
@startmindmap
* Graph Email Sending
** Delegated Flow (Authorization Code)
*** User signs in and consents to `Mail.Send`
*** Client receives auth code and exchanges for tokens
*** Access token includes user context
*** Graph API call: `POST /me/sendMail`
*** Use Case: User-triggered emails (e.g., “Send on behalf of me” in web app)
** Application Flow (Client Credentials)
*** App authenticates with its own identity (service principal or managed identity)
*** ClientSecretCredential / ManagedIdentityCredential fetches token with app-level `Mail.Send` permission
*** Access token without user context
*** Graph API call: `POST /users/{user-id}/sendMail`
*** Use Case: Automated notifications and system alerts
** Token Acquisition Methods
*** Delegated: InteractiveBrowserCredential, DeviceCodeCredential
*** Application: ClientSecretCredential, CertificateCredential, ManagedIdentityCredential
** Graph Endpoint & Payload
*** Endpoint:
**** Delegated: `https://graph.microsoft.com/v1.0/me/sendMail`
**** Application: `https://graph.microsoft.com/v1.0/users/{id}/sendMail`
*** Payload Structure:
**** `message` object with `subject`, `body`, `toRecipients`, `ccRecipients`, etc.
*** Headers:
**** `Authorization: Bearer <access_token>`
**** `Content-Type: application/json`
@endmindmap
```  

## 8. Choosing OAuth Flow for Microsoft Graph API

When integrating with Microsoft Graph, select the OAuth flow based on your application context and use case.

```puml
@startmindmap
* Selecting OAuth Flow for Graph API
** Delegated (Auth Code Flow)
*** Use when: User interaction required; web apps, SPAs
*** Why: Provides user context and user consent
** Client Credentials Flow
*** Use when: No user context; background services, daemons
*** Why: Uses application identity (SP/MI)
** Device Code Flow
*** Use when: CLI tools, IoT devices without embedded browsers
*** Why: Allows code-based device login on separate device
** On-Behalf-Of Flow
*** Use when: APIs calling Graph downstream on behalf of user
*** Why: Retains user context across service layers
** ROPC Flow
*** Use when: Legacy applications requiring username/password migration (not recommended)
** Example Use Cases
*** Send mail as the signed-in user → Delegated Flow
*** Automated reports/email notifications → Client Credentials
*** CLI admin tasks → Device Code
*** API orchestration across services → On-Behalf-Of
@endmindmap
```

### Python Sample: Delegated (Authorization Code) Flow
```python
from azure.identity import InteractiveBrowserCredential
from msgraph.core import GraphClient

# Acquire token interactively
dialect = InteractiveBrowserCredential(
    tenant_id="<TENANT_ID>",
    client_id="<CLIENT_ID>"
)
token = dialect.get_token("Mail.Send User.Read")

# Initialize Graph client
graph_client = GraphClient(credential=dialect)

# Send an email
message = {
    "message": {
        "subject": "Hello via Graph API",
        "body": {"contentType": "Text", "content": "This is a test email."},
        "toRecipients": [{"emailAddress": {"address": "user@example.com"}}]
    }
}
response = graph_client.post('/me/sendMail', json=message)
print(response.status_code)
```

### Python Sample: Client Credentials Flow
```python
from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient

# Acquire token with app identity
cred = ClientSecretCredential(
    tenant_id="<TENANT_ID>",
    client_id="<CLIENT_ID>",
    client_secret="<CLIENT_SECRET>"
)

graph_client = GraphClient(credential=cred)
# Send email on behalf of a specific user
message = {
    "message": {
        "subject": "Automated Report",
        "body": {"contentType": "Text", "content": "Report attached."},
        "toRecipients": [{"emailAddress": {"address": "admin@example.com"}}]
    }
}
response = graph_client.post(
    '/users/<USER_ID>/sendMail', json=message
)
print(response.status_code)
```

### Python Sample: Device Code Flow
```python
from azure.identity import DeviceCodeCredential
from msgraph.core import GraphClient

# Acquire token via device code
dev_cred = DeviceCodeCredential(
    client_id="<CLIENT_ID>",
    tenant_id="<TENANT_ID>"
)

graph_client = GraphClient(credential=dev_cred)
# List user mailbox folders
response = graph_client.get('/me/mailFolders')
print(response.json())
```

## References

- **RFC 6749**: OAuth 2.0 Authorization Framework  
- **RFC 6750**: OAuth 2.0 Bearer Token Usage  
- **RFC 7636**: Proof Key for Code Exchange (PKCE)


- **RFC 6749**: OAuth 2.0 Authorization Framework
- **RFC 6750**: OAuth 2.0 Bearer Token Usage
- **RFC 7636**: Proof Key for Code Exchange (PKCE)

