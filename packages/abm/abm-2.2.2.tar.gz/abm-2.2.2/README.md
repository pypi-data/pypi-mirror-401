# ABM Python client

This is a Python client for the Applied BioMath platform. It is useless alone and must be
installed in an environment with a valid access token to a deployed Applied BioMath server.

## Configuration

The client searches the following paths for a configuration file:

```
${XDG_CONFIG_HOME:-~/.config}/abm/client.toml

/etc/abm/client.toml
```

Example configuration file:

```toml
api_origin = 'https://services-blue.dev-abm.com'
auth_token_path = '/home/jovyan/.jupyterhub/services-blue/auth_token'
```

- `api_origin`: The protocol and host for ABM server API. All requests will be made against this API. By
  default, the client will request against `http://localhost:5100`
- `auth_token_path`: Path to a file containing a bearer token that will be used to authenticate
  requests. By default, the client will attempt requests with no authentication.

The search stops at the first configuration file found. If no configuration file is found, the defaults for
all values are used.
