# Denodo Platform: Security Features

The Denodo Platform offers robust features for managing data security and access, including integration with Active Directory, role-based data classification, and global policy implementation.

## 1. Entitlements Based on Active Directory:

Denodo can integrate with LDAP servers, such as Microsoft Windows Active Directory, to authenticate users and manage their privileges.[1, 2] This simplifies user management as it leverages existing corporate identity systems.[1, 3]

*   **Centralized Authentication:** Denodo can rely on Active Directory to validate user credentials, eliminating the need to manage users within Denodo itself.[1, 4]
*   **Role Mapping:** Denodo can retrieve user roles from Active Directory, which are then used to determine the user's access rights within Denodo.[1, 3, 4] You can configure Denodo to map Active Directory groups to Denodo roles.[1, 2]
*   **Simplified Management:** By integrating with Active Directory, managing user access and permissions becomes more efficient as changes in user roles within Active Directory can be automatically reflected in Denodo.[1]
*   **Pass-through Authentication:** Denodo can be configured to pass through user credentials to underlying data sources that also support Active Directory authentication.[5]
*   **Global LDAP Authentication:** Denodo allows setting up global LDAP authentication for the entire Virtual DataPort server.[1, 6]
*   **LDAP Data Source Configuration:** You need to define an LDAP data source in Denodo, providing the server URI and credentials to connect to the Active Directory.[2, 6] This data source is used to query user and role information.[7]
*   **Role Import:** Denodo allows importing roles directly from the LDAP server (Active Directory), which can then be assigned privileges within Denodo.[2, 6]
*   **Connection Pooling:** To optimize performance with LDAP authentication, it's recommended to configure clients to use connection pools against the Denodo server, reducing the need for repeated authentication.[2]

## 2. Role-Level Data Classification:

Denodo employs a Role-Based Access Control (RBAC) model to manage permissions and enforce security.[8, 9] This allows for classifying data access based on the roles assigned to users.

*   **Schema-Wide Permissions:** You can assign permissions (e.g., connect, create, read, write) to specific schemas (databases and views) based on roles.
*   **Fine-Grained Privileges:** Denodo supports defining privileges at a granular level:
    *   **Column Restrictions:** Limiting the columns a user or role can access in a query.
    *   **Row Restrictions:** Filtering the rows visible to a user or role, effectively implementing data masking or custom policies.
    *   **Custom Policies:** Using an API, developers can implement their own access control rules.
*   **Role Hierarchy:** Denodo supports hierarchical roles, where a role can inherit privileges from another role. This allows for creating a structure of permissions based on job functions or responsibilities.
*   **Cumulative Permissions:** A user's effective permissions are the combination of all privileges granted by all the roles assigned to them.
*   **Data Catalog Permissions:** Within the Denodo Data Catalog, you can define which tasks a role can perform, such as editing descriptions, creating endorsements, or assigning tags.
*   **Tags for Classification:** Tags can be used to label data elements (views, columns) for various purposes, including security and data privacy. These tags can then be used in global security policies to enforce access restrictions.

## 3. Global Policy Implementation:

Denodo allows the implementation of global security policies to enforce restrictions across all or specific data elements based on defined conditions.

*   **Centralized Policy Management:** Global security policies provide a single place to define and manage security rules that apply to multiple data objects.
*   **Tag-Based Policies:** Policies can be defined to apply to views or columns that are tagged with specific labels. This allows for easy application of security rules to groups of data based on their classification.
*   **Audience Specification:** You can define the audience to which a global security policy applies, such as all users, users with specific roles, or even based on user attributes (Attribute-Based Access Control - ABAC).
*   **Restriction Types:** Global security policies can implement various types of restrictions:
    *   **Denying Access:** Completely preventing access to certain data.
    *   **Filtering Rows:** Restricting the rows that users can see based on conditions.
    *   **Masking Data:** Obfuscating sensitive data by techniques like hiding, redacting, or substituting values. Denodo offers built-in masking expressions and allows for custom expressions.
*   **Session Roles:** Global security policies can leverage session attributes, including user roles, to dynamically enforce restrictions based on the user's context.
*   **VQL Commands:** Global security policies are managed using Denodo's Virtual Query Language (VQL) commands, such as `CREATE GLOBAL_SECURITY_POLICY`, `ALTER GLOBAL_SECURITY_POLICIES`, `DESC VQL GLOBAL_SECURITY_POLICY`, `LIST GLOBAL_SECURITY_POLICIES`, and `DROP GLOBAL_SECURITY_POLICY`.
*   **Policy Enforcement:** Once a global security policy is enabled, it is automatically applied at runtime to all queries accessing the specified data elements for the defined audience.

By combining these features, Denodo provides a comprehensive framework for securing data access and ensuring compliance with organizational policies and regulations.