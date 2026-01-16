# Clever Cloud Python SDK

A Python SDK for the [Clever Cloud](https://clever-cloud.com) API.

## Installation

```bash
pip install clevercloud-sdk
```

## Usage

### With API Token

```python
from clever_cloud import CleverCloudClient, ApiTokenCredentials

async with CleverCloudClient(ApiTokenCredentials(token="...")) as client:
    profile = await client.get_profile()
    print(f"Hello, {profile.name}!")
```

### With OAuth

```python
from clever_cloud import CleverCloudClient, OAuthCredentials

credentials = OAuthCredentials(
    consumer_key="...",
    consumer_secret="...",
    token="...",
    secret="...",
)

async with CleverCloudClient(credentials) as client:
    app = await client.create_application(
        owner_id="...",
        name="my-app",
        instance_slug="node"
    )
```

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.
