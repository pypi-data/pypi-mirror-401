# Cegaware Python SDK

The Cegaware Python SDK provides programmatic access to the Cegaware platform, including authentication, market data access, and other core features.

---

## Installation

Install directly from PyPI:

```bash
pip install cegaware
```

Verify installation:

```python
import cegaware
print(cegaware.__version__)
```

---

## Quick Start

Authenticate and obtain an API token (valid for 60 minutes):

```python
import cegaware as cw

# Initialize logger
logger = cw.Logger()

# Prepare authentication request
results = cw.GetAPIToken_Results(
    Username="YOUR_USERNAME",
    Password="YOUR_PASSWORD"
)

# Perform authentication
if cw.GetAPIToken(results, logger):
    api_token = results.APIToken
    print("Authenticated successfully")
else:
    raise RuntimeError("Authentication failed")
```

> ⚠️ Note: API token expires in 60 minutes. Re-authenticate as needed.

---

## Documentation

For detailed instructions on installation, authentication, data configuration, and usage examples, see the **Client Installation Guide**:

```
CLIENT_INSTALLATION_GUIDE.md
```

---

## Support

For assistance, contact your Cegaware representative. Include logs from `cw.Logger()` when reporting issues.

---

© Cegaware – All rights reserved