Authentication
==============

The PyGEAI SDK supports two authentication methods: **API Key** authentication and **OAuth 2.0** authentication. Both methods provide secure access to Globant Enterprise AI services, with OAuth offering enhanced security through token-based authentication and project-level access control.

API Key Authentication
----------------------

API Key authentication is the traditional method that uses a project-specific API token. This is the simplest authentication method and is suitable for most use cases.

Configuration
~~~~~~~~~~~~~

You can configure API Key authentication using the CLI:

.. code-block:: shell

    geai configure

When prompted, enter your API key and base URL:

.. code-block:: shell

    -> Select an alias (Leave empty to use 'default'): default
    -> Insert your GEAI_API_KEY: your_api_key_here
    GEAI API KEY for alias 'default' saved successfully!
    -> Insert your GEAI API BASE URL: https://api.saia.ai
    GEAI API BASE URL for alias 'default' saved successfully!

Usage in Code
~~~~~~~~~~~~~

**Using Configured Credentials:**

.. code-block:: python

    from pygeai.lab.clients import AILabClient
    
    # Uses credentials from configuration file
    client = AILabClient()

**Explicit API Key:**

.. code-block:: python

    from pygeai.lab.clients import AILabClient
    
    client = AILabClient(
        api_key="your_api_key_here",
        base_url="https://api.saia.ai"
    )

**With Project ID:**

.. code-block:: python

    from pygeai.lab.clients import AILabClient
    
    client = AILabClient(
        api_key="your_api_key_here",
        base_url="https://api.saia.ai",
        project_id="your-project-id"
    )

OAuth 2.0 Authentication
------------------------

OAuth 2.0 provides enhanced security by using temporary access tokens instead of long-lived API keys. This method requires both an ``access_token`` and a ``project_id``.

Prerequisites
~~~~~~~~~~~~~

Before using OAuth authentication, you need to:

1. Obtain OAuth credentials (client ID, username, password)
2. Get an access token
3. Know your project ID

Getting an Access Token
~~~~~~~~~~~~~~~~~~~~~~~

Use the Auth client to obtain an OAuth 2.0 access token:

.. code-block:: python

    from pygeai.auth.clients import AuthClient
    
    auth_client = AuthClient()
    
    # Get OAuth 2.0 access token
    response = auth_client.get_oauth2_access_token(
        client_id="your-client-id",
        username="your-username",
        password="your-password"
    )
    
    access_token = response["access_token"]
    project_id = "your-project-id"

Usage in Code
~~~~~~~~~~~~~

**Basic OAuth Authentication:**

.. code-block:: python

    from pygeai.lab.clients import AILabClient
    
    client = AILabClient(
        base_url="https://api.saia.ai",
        access_token="your_oauth_access_token",
        project_id="your-project-id"
    )

**With Other Clients:**

.. code-block:: python

    from pygeai.core.secrets.clients import SecretClient
    from pygeai.evaluation.clients import EvaluationClient
    
    # Secret Client with OAuth
    secret_client = SecretClient(
        base_url="https://api.saia.ai",
        access_token="your_oauth_access_token",
        project_id="your-project-id"
    )
    
    # Evaluation Client with OAuth
    eval_client = EvaluationClient(
        base_url="https://api.saia.ai",
        eval_url="https://eval.saia.ai",
        access_token="your_oauth_access_token",
        project_id="your-project-id"
    )

Complete OAuth Flow Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pygeai.auth.clients import AuthClient
    from pygeai.lab.clients import AILabClient
    from pygeai.lab.agents.clients import AgentClient
    
    # Step 1: Obtain OAuth access token
    auth_client = AuthClient()
    token_response = auth_client.get_oauth2_access_token(
        client_id="your-client-id",
        username="user@example.com",
        password="your-password"
    )
    
    access_token = token_response["access_token"]
    project_id = "your-project-id"
    
    # Step 2: Use OAuth token with clients
    lab_client = AILabClient(
        base_url="https://api.saia.ai",
        access_token=access_token,
        project_id=project_id
    )
    
    # Step 3: Use the client
    agents = lab_client.list_agents()
    print(f"Found {len(agents)} agents")

Authentication Comparison
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - API Key
     - OAuth 2.0
   * - **Security**
     - Long-lived key
     - Temporary access token
   * - **Setup Complexity**
     - Simple
     - Moderate
   * - **Project Isolation**
     - Optional
     - Required
   * - **Token Expiration**
     - Never (until revoked)
     - Yes (requires refresh)
   * - **Header Format**
     - ``Bearer {api_key}``
     - ``Bearer {access_token}``
   * - **Additional Headers**
     - None (ProjectId optional)
     - ``ProjectId`` header required
   * - **Use Case**
     - Development, testing
     - Production, multi-project

Implementation Details
----------------------

Header Injection
~~~~~~~~~~~~~~~~

The SDK automatically injects authentication headers:

**API Key:**

.. code-block:: python

    Authorization: Bearer your_api_key_here

**OAuth 2.0:**

.. code-block:: python

    Authorization: Bearer your_oauth_access_token
    ProjectId: your-project-id

Backward Compatibility
~~~~~~~~~~~~~~~~~~~~~~

OAuth parameters (``access_token`` and ``project_id``) are **keyword-only** parameters to maintain backward compatibility with existing code:

.. code-block:: python

    # Correct - keyword arguments
    client = AILabClient(
        base_url="https://api.saia.ai",
        access_token="token",
        project_id="project-123"
    )
    
    # Error - cannot pass as positional
    client = AILabClient("https://api.saia.ai", "token", "project-123")

Validation
~~~~~~~~~~

The SDK validates authentication parameters:

- **Missing OAuth parameters**: If ``access_token`` is provided without ``project_id``, a ``MissingRequirementException`` is raised.
- **Complete OAuth**: Both ``access_token`` and ``project_id`` must be provided together.

.. code-block:: python

    # Raises MissingRequirementException
    client = AILabClient(
        base_url="https://api.saia.ai",
        access_token="token_without_project"
    )
    
    # Correct
    client = AILabClient(
        base_url="https://api.saia.ai",
        access_token="token",
        project_id="project-123"
    )

Best Practices
--------------

1. **Use OAuth for Production**: OAuth provides better security through temporary tokens and project isolation.

2. **Store Credentials Securely**: Never hardcode API keys or access tokens in your source code. Use environment variables or secure credential storage.

3. **Token Refresh**: Implement token refresh logic when using OAuth to handle token expiration.

4. **Project Isolation**: Use ``project_id`` to ensure requests are scoped to the correct project, even when using API keys.

5. **Error Handling**: Implement proper error handling for authentication failures:

.. code-block:: python

    from pygeai.core.common.exceptions import MissingRequirementException, APIResponseError
    
    try:
        client = AILabClient(
            base_url="https://api.saia.ai",
            access_token=access_token,
            project_id=project_id
        )
        agents = client.list_agents()
    except MissingRequirementException as e:
        print(f"Configuration error: {e}")
    except APIResponseError as e:
        print(f"Authentication failed: {e}")

Related Resources
-----------------

- :doc:`quickstart` - Getting started with PyGEAI
- :doc:`api_reference/auth` - Auth client API reference
- :doc:`ai_lab` - AI Lab documentation
