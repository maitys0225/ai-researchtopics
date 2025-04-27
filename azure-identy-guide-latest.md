# Author & Contributor

---
`Name` : Siddhartha Maity  
`Email` : siddhartha.maity@ubs.com  
`Current Role` : Crew Architect  
`Team` : DPAS Data Mesh Team  
---


# Azure Identity & OAuth 2.0 Comprehensive Guide

Modern application development relies on robust identity and access management. OAuth 2.0 is the industry-standard protocol for authorization, enabling secure delegated access to resources without sharing sensitive user credentials. In the Microsoft ecosystem, Azure Identity (Microsoft Entra ID, formerly Azure AD) provides a comprehensive Identity as a Service (IDaaS) platform for managing and securing identities across cloud, on-premises, and hybrid scenarios.

This guide explores the fundamental principles of OAuth 2.0 within the context of Azure Identity, including core components, implementation flows supported by the Microsoft Identity Platform, and practical application using the Azure Identity Python library. It also covers integration with directory services, API management, Azure data platforms, and Microsoft Graph API. Key concepts are illustrated with PlantUML mind maps and Python code examples.

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [OAuth 2.0 Fundamentals](#oauth-20-fundamentals)
3. [OAuth Flows in Microsoft Identity Platform](#oauth-flows-in-microsoft-identity-platform)
4. [Directory Services](#directory-services)
5. [Azure Service Identities](#azure-service-identities)
6. [API Management](#api-management)
7. [Azure Data Platform Authentication](#azure-data-platform-authentication)
8. [Microsoft Graph API Integration](#microsoft-graph-api-integration)
9. [Best Practices](#best-practices)
10. [References](#references)

---

## 1. High-Level Architecture

```puml
@startmindmap
* OAuth 2.0 & Azure Identity Guide
** OAuth 2.0 Fundamentals
*** Protocol Components (Roles, Endpoints, Tokens)
*** Grant Types (Flows)
** Azure Identity Core (Entra ID)
*** Tenants & Subscriptions
*** Identity Objects (Users, Groups, SPs, MIs)
*** Protocols (OAuth2, OIDC, SAML)
*** Services (CA, IP, PIM, B2B/B2C)
** Directory Services
*** Windows Active Directory
*** Azure Active Directory (Entra)
*** Hybrid Identity
** Azure Service Identities
*** Service Principals
*** Managed Identities
*** Workload Identity (AKS)
** API Management
*** Authentication Methods
*** Policy Engine
*** Azure AD Integration
** Azure Data Platform Authentication
*** PostgreSQL
*** SQL / Hyperscale
*** Synapse Analytics
*** Databricks
** Microsoft Graph API Integration
*** Delegated Flow
*** Application Flow
*** Token Acquisition


@endmindmap
```

---

## 2. OAuth 2.0 Fundamentals

OAuth 2.0 is an authorization framework that allows a third-party application to obtain limited access to a protected resource on behalf of a resource owner.

### Protocol Components

- **Roles:** Resource Owner, Client, Authorization Server, Resource Server
- **Endpoints:** Authorization, Token, Redirection, Revocation
- **Grant Types:** Authorization Code, Implicit, Client Credentials, Device Code, ROPC, Refresh Token
- **Token Types:** Access Token, Refresh Token, ID Token

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

---

## 3. OAuth Flows in Microsoft Identity Platform

The Microsoft Identity Platform supports several OAuth 2.0 flows tailored for different application types and scenarios.

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
***** Web applications (e.NET Core)
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
```

#### Example: Client Credentials Flow

```python
from azure.identity import ClientSecretCredential

tenant_id = "<YOUR_TENANT_ID>"
client_id = "<YOUR_CLIENT_ID>"
client_secret = "<YOUR_CLIENT_SECRET>"

cred = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
scopes = ["https://graph.microsoft.com/.default"]
token = cred.get_token(*scopes)
print(f"Access Token: {token.token}")
```

#### Example: Device Code Flow

```python
from azure.identity import DeviceCodeCredential

client_id = "<YOUR_CLIENT_ID>"
tenant_id = "<YOUR_TENANT_ID>"

cred = DeviceCodeCredential(client_id=client_id, tenant_id=tenant_id)
scopes = ["User.Read"]
token = cred.get_token(*scopes)
print(f"Access Token: {token.token}")
```

#### Example: ROPC Flow (Not Recommended)

```python
from azure.identity import UsernamePasswordCredential

client_id = "<YOUR_CLIENT_ID>"
username = "<YOUR_USERNAME>"
password = "<YOUR_PASSWORD>"
tenant_id = "<YOUR_TENANT_ID>"

cred = UsernamePasswordCredential(
    client_id=client_id,
    username=username,
    password=password,
    tenant_id=tenant_id
)
scopes = ["User.Read"]
token = cred.get_token(*scopes)
print(f"Access Token: {token.token}")
```

---

## 4. Directory Services

Directory services manage identities and resources.

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

#### Example: Querying LDAP using ldap3

```python
from ldap3 import Server, Connection, ALL, SUBTREE

ldap_server = 'ldap://ad.example.com'
user_dn = 'CN=svc_account,OU=Service Accounts,DC=example,DC=com'
password = 'P@ssw0rd'
base_dn = 'DC=example,DC=com'
search_filter = '(objectClass=user)'
attributes = ['cn', 'mail', 'memberOf']

server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=user_dn, password=password, auto_bind=True)

if conn.bind():
    print("LDAP Bind successful")
    conn.search(
        search_base=base_dn,
        search_filter=search_filter,
        search_scope=SUBTREE,
        attributes=attributes
    )
    print(f"Found {len(conn.entries)} entries:")
    for entry in conn.entries:
        print('CN:', entry.cn)
        print('Email:', entry.mail)
        print('Groups:', entry.memberOf)
        print('---')
    conn.unbind()
    print("LDAP Unbind successful")
else:
    print(f"LDAP Bind failed: {conn.result}")
```

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

---

## 5. Azure Service Identities

Identities for applications and services to access Azure resources.

### Azure Service Identities

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

#### Example: Using DefaultAzureCredential

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
key_vault_url = "https://your-key-vault.vault.azure.net"
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

secret_name = "your-secret-name"
try:
    retrieved_secret = secret_client.get_secret(secret_name)
    print(f"Retrieved secret value: {retrieved_secret.value}")
except Exception as e:
    print(f"Error retrieving secret: {e}")
```

### Workload Identity (AKS)

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

### AKS Cluster Authentication

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

---

## 6. API Management

Azure API Management (APIM) provides authentication and authorization mechanisms for APIs.

```puml
@startmindmap
* Azure API Management
** Authentication
*** Subscription Key (header/query)
*** OAuth 2.0 (Auth Code, Client Credentials)
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

#### Example: Calling an API secured with a Subscription Key

```python
import requests

api_url = "https://your-api-management.azure-api.net/your-api-path"
subscription_key = "YOUR_SUBSCRIPTION_KEY"

headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/json"
}

try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    print(f"Response Status Code: {response.status_code}")
    print("Response Body:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error calling API: {e}")
```

#### Example: Calling an API secured with Azure AD (OAuth 2.0)

```python
import requests
from azure.identity import DefaultAzureCredential

api_url = "https://your-api-management.azure-api.net/your-api-path"
scopes = ["api://<YOUR_API_CLIENT_ID>/.default"]

credential = DefaultAzureCredential()

try:
    token = credential.get_token(*scopes).token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    print(f"Response Status Code: {response.status_code}")
    print("Response Body:")
    print(response.json())
except Exception as e:
    print(f"Error calling API: {e}")
```

---

## 7. Azure Data Platform Authentication

Azure data services offer various authentication methods, often integrating with Azure AD.

### Azure Database for PostgreSQL Authentication

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

### Azure SQL & Hyperscale

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

#### Example: Connecting to Azure SQL using Azure AD Token

```python
from azure.identity import DefaultAzureCredential
import pyodbc

server = "your_server.database.windows.net"
database = "your_database"
driver = "ODBC Driver 17 for SQL Server"

credential = DefaultAzureCredential()
try:
    token = credential.get_token("https://database.windows.net/.default").token
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Authentication=ActiveDirectoryAccessToken;"
        f"AccessToken={token}"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()
    cursor.close()
    conn.close()
    print("Connection to Azure SQL successful.")
except Exception as e:
    print(f"Error connecting to Azure SQL: {e}")
```

---

## 8. Microsoft Graph API Integration

The Microsoft Graph API provides access to Microsoft 365 data. Authentication uses OAuth 2.0.

```puml
@startmindmap
* Graph Email Sending
** Delegated Flow (Authorization Code)
*** User signs in and consents to `Mail.Send`
*** Client receives auth code and exchanges for tokens
*** Access token includes user context
*** Graph API call: `POST /me/sendMail`
*** Use Case: User-triggered emails (e.g., "Send on behalf of me" in web app)
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

#### Example: Sending Email via Microsoft Graph (Delegated Flow)

```python
from azure.identity import InteractiveBrowserCredential
from msgraph.core import GraphClient

tenant_id = "<YOUR_TENANT_ID>"
client_id = "<YOUR_CLIENT_ID>"

credential = InteractiveBrowserCredential(
    tenant_id=tenant_id,
    client_id=client_id
)
scopes = ["Mail.Send", "User.Read"]
token = credential.get_token(*scopes)

graph_client = GraphClient(credential=credential)
message = {
    "message": {
        "subject": "Hello from Microsoft Graph (Delegated Flow)",
        "body": {"contentType": "Text", "content": "This is a test email sent via the Microsoft Graph API using the Delegated Flow."},
        "toRecipients": [{"emailAddress": {"address": "recipient@example.com"}}]
    },
    "saveToSentItems": "true"
}
response = graph_client.post('/me/sendMail', json=message)
response.raise_for_status()
print(f"Email sent successfully. Response Status Code: {response.status_code}")
```

#### Example: Sending Email via Microsoft Graph (Application Flow)

```python
from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient

tenant_id = "<YOUR_TENANT_ID>"
client_id = "<YOUR_CLIENT_ID>"
client_secret = "<YOUR_CLIENT_SECRET>"

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)
graph_client = GraphClient(credential=credential)
sender_user_id = "<SENDER_USER_ID>"

message = {
    "message": {
        "subject": "Automated Notification from Microsoft Graph (Application Flow)",
        "body": {"contentType": "Text", "content": "This is an automated email sent via the Microsoft Graph API using the Application Flow."},
        "toRecipients": [{"emailAddress": {"address": "recipient@example.com"}}]
    },
    "saveToSentItems": "true"
}

try:
    response = graph_client.post(f'/users/{sender_user_id}/sendMail', json=message)
    response.raise_for_status()
    print(f"Email sent successfully. Response Status Code: {response.status_code}")
except Exception as e:
    print(f"Error sending email via Graph API: {e}")
    print("Please ensure the Service Principal has the application-level 'Mail.Send' permission granted.")
```

---

## 9. Best Practices

1. Always use Authorization Code + PKCE for public clients.
2. Avoid Implicit and ROPC flows.
3. Implement proper token caching and revocation.
4. Use Managed Identities where possible.
5. Rotate client secrets and certificates regularly.
6. Implement Conditional Access policies.
7. Use minimum required permissions (least privilege).

---

## 10. References

1. [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
2. [Azure Identity Documentation](https://docs.microsoft.com/azure/active-directory)
3. [Microsoft Graph API Documentation](https://docs.microsoft.com/graph)

---

_Document Author: Siddhartha Maity (siddhartha.maity@ubs.com)_