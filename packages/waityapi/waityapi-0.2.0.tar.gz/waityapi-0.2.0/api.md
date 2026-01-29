# Shared Types

```python
from waityapi.types import ErrorResponse
```

# Health

Types:

```python
from waityapi.types import HealthCheckResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/waityapi/resources/health.py">check</a>() -> <a href="./src/waityapi/types/health_check_response.py">HealthCheckResponse</a></code>

# Stores

Types:

```python
from waityapi.types import (
    CheckInRequest,
    CheckInResponse,
    CheckOutRequest,
    CheckOutResponse,
    QueueHistory,
    QueueStatus,
    Store,
    StoreListResponse,
    UpdateQueueRequest,
    UpdateWaitTimeRequest,
    WaitTime,
    StoreUpdateQueueResponse,
)
```

Methods:

- <code title="get /stores/{id}">client.stores.<a href="./src/waityapi/resources/stores.py">retrieve</a>(id) -> <a href="./src/waityapi/types/store.py">Store</a></code>
- <code title="get /stores">client.stores.<a href="./src/waityapi/resources/stores.py">list</a>() -> <a href="./src/waityapi/types/store_list_response.py">StoreListResponse</a></code>
- <code title="get /stores/{id}/queue">client.stores.<a href="./src/waityapi/resources/stores.py">queue</a>(id) -> <a href="./src/waityapi/types/queue_status.py">QueueStatus</a></code>
- <code title="post /stores/{id}/queue/check-in">client.stores.<a href="./src/waityapi/resources/stores.py">queue_check_in</a>(id, \*\*<a href="src/waityapi/types/store_queue_check_in_params.py">params</a>) -> <a href="./src/waityapi/types/check_in_response.py">CheckInResponse</a></code>
- <code title="post /stores/{id}/queue/check-out">client.stores.<a href="./src/waityapi/resources/stores.py">queue_check_out</a>(id, \*\*<a href="src/waityapi/types/store_queue_check_out_params.py">params</a>) -> <a href="./src/waityapi/types/check_out_response.py">CheckOutResponse</a></code>
- <code title="get /stores/{id}/queue/history">client.stores.<a href="./src/waityapi/resources/stores.py">queue_history</a>(id, \*\*<a href="src/waityapi/types/store_queue_history_params.py">params</a>) -> <a href="./src/waityapi/types/queue_history.py">QueueHistory</a></code>
- <code title="post /stores/{id}/queue">client.stores.<a href="./src/waityapi/resources/stores.py">update_queue</a>(id, \*\*<a href="src/waityapi/types/store_update_queue_params.py">params</a>) -> <a href="./src/waityapi/types/store_update_queue_response.py">StoreUpdateQueueResponse</a></code>
- <code title="post /stores/{id}/wait-time">client.stores.<a href="./src/waityapi/resources/stores.py">update_wait_time</a>(id, \*\*<a href="src/waityapi/types/store_update_wait_time_params.py">params</a>) -> <a href="./src/waityapi/types/wait_time.py">WaitTime</a></code>
- <code title="get /stores/{id}/wait-time">client.stores.<a href="./src/waityapi/resources/stores.py">wait_time</a>(id) -> <a href="./src/waityapi/types/wait_time.py">WaitTime</a></code>

# APIKeys

Types:

```python
from waityapi.types import (
    APIKey,
    APIKeyListResponse,
    CreateRequest,
    CreateResponse,
    UpdateRequest,
    Usage,
)
```

Methods:

- <code title="post /manager/c/{companyId}/api-keys">client.api_keys.<a href="./src/waityapi/resources/api_keys.py">create</a>(company_id, \*\*<a href="src/waityapi/types/api_key_create_params.py">params</a>) -> <a href="./src/waityapi/types/create_response.py">CreateResponse</a></code>
- <code title="patch /manager/c/{companyId}/api-keys/{keyId}">client.api_keys.<a href="./src/waityapi/resources/api_keys.py">update</a>(key_id, \*, company_id, \*\*<a href="src/waityapi/types/api_key_update_params.py">params</a>) -> <a href="./src/waityapi/types/api_key.py">APIKey</a></code>
- <code title="get /manager/c/{companyId}/api-keys">client.api_keys.<a href="./src/waityapi/resources/api_keys.py">list</a>(company_id) -> <a href="./src/waityapi/types/api_key_list_response.py">APIKeyListResponse</a></code>
- <code title="delete /manager/c/{companyId}/api-keys/{keyId}">client.api_keys.<a href="./src/waityapi/resources/api_keys.py">delete</a>(key_id, \*, company_id) -> None</code>
- <code title="get /manager/c/{companyId}/api-keys/{keyId}/usage">client.api_keys.<a href="./src/waityapi/resources/api_keys.py">usage</a>(key_id, \*, company_id) -> <a href="./src/waityapi/types/usage.py">Usage</a></code>
