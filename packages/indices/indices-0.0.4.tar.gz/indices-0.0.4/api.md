# Tasks

Types:

```python
from indices.types import Task, TaskListResponse, TaskStartManualSessionResponse
```

Methods:

- <code title="post /v1beta/tasks">client.tasks.<a href="./src/indices/resources/tasks.py">create</a>(\*\*<a href="src/indices/types/task_create_params.py">params</a>) -> <a href="./src/indices/types/task.py">Task</a></code>
- <code title="get /v1beta/tasks/{id}">client.tasks.<a href="./src/indices/resources/tasks.py">retrieve</a>(id) -> <a href="./src/indices/types/task.py">Task</a></code>
- <code title="get /v1beta/tasks">client.tasks.<a href="./src/indices/resources/tasks.py">list</a>() -> <a href="./src/indices/types/task_list_response.py">TaskListResponse</a></code>
- <code title="delete /v1beta/tasks/{id}">client.tasks.<a href="./src/indices/resources/tasks.py">delete</a>(id) -> object</code>
- <code title="post /v1beta/tasks/{id}/complete-manual-session">client.tasks.<a href="./src/indices/resources/tasks.py">complete_manual_session</a>(id) -> object</code>
- <code title="post /v1beta/tasks/{id}/start-manual-session">client.tasks.<a href="./src/indices/resources/tasks.py">start_manual_session</a>(id, \*\*<a href="src/indices/types/task_start_manual_session_params.py">params</a>) -> <a href="./src/indices/types/task_start_manual_session_response.py">TaskStartManualSessionResponse</a></code>

# Runs

Types:

```python
from indices.types import Run, RunListResponse
```

Methods:

- <code title="get /v1beta/runs/{run_id}">client.runs.<a href="./src/indices/resources/runs.py">retrieve</a>(run_id) -> <a href="./src/indices/types/run.py">Run</a></code>
- <code title="get /v1beta/runs">client.runs.<a href="./src/indices/resources/runs.py">list</a>(\*\*<a href="src/indices/types/run_list_params.py">params</a>) -> <a href="./src/indices/types/run_list_response.py">RunListResponse</a></code>
- <code title="post /v1beta/runs">client.runs.<a href="./src/indices/resources/runs.py">run</a>(\*\*<a href="src/indices/types/run_run_params.py">params</a>) -> <a href="./src/indices/types/run.py">Run</a></code>

# Secrets

Types:

```python
from indices.types import Secret, SecretListResponse, SecretDeleteResponse, SecretGetTotpResponse
```

Methods:

- <code title="post /v1beta/secrets">client.secrets.<a href="./src/indices/resources/secrets.py">create</a>(\*\*<a href="src/indices/types/secret_create_params.py">params</a>) -> <a href="./src/indices/types/secret.py">Secret</a></code>
- <code title="get /v1beta/secrets">client.secrets.<a href="./src/indices/resources/secrets.py">list</a>() -> <a href="./src/indices/types/secret_list_response.py">SecretListResponse</a></code>
- <code title="delete /v1beta/secrets/{uuid}">client.secrets.<a href="./src/indices/resources/secrets.py">delete</a>(uuid) -> <a href="./src/indices/types/secret_delete_response.py">SecretDeleteResponse</a></code>
- <code title="post /v1beta/secrets/{uuid}/totp">client.secrets.<a href="./src/indices/resources/secrets.py">get_totp</a>(uuid) -> <a href="./src/indices/types/secret_get_totp_response.py">SecretGetTotpResponse</a></code>
