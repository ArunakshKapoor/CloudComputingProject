# API Spec Summary

Base path: `/api/v1`

- `GET /health`
- `GET /connectors/status`
- `POST /workflows`
- `GET /workflows`
- `GET /workflows/{workflow_id}`
- `POST /workflows/{workflow_id}/plan`
- `POST /workflows/{workflow_id}/simulate`
- `POST /workflows/{workflow_id}/execute`
- `POST /workflows/{workflow_id}/cancel`
- `GET /workflows/{workflow_id}/approvals`
- `POST /approvals/{step_id}`
- `GET /workflows/{workflow_id}/trace`
- `GET /memory?user_id=demo-user`
- `POST /memory`
- `PATCH /memory/{memory_id}`
- `DELETE /memory/{memory_id}`
- `GET /policies`
- `POST /policies/evaluate`
- `GET /connectors`
- `POST /connectors/{connector}/test`
- `POST /evaluations/run`
- `GET /evaluations/{run_id}`
