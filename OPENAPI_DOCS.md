# OpenAPI & Swagger Documentation

The backend API is now served using FastAPI. You can access the auto-generated OpenAPI and Swagger UI docs at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## How to Run the API Server

1. Install dependencies (if not already):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API server:
   ```bash
   uvicorn api_server:app --reload
   ```
3. Visit [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to view and interact with the API docs.

## Endpoints Implemented
- `GET /workflows` — List workflows
- `POST /workflows` — Create/import workflow
- `PUT /workflows/{id}` — Update workflow
- `DELETE /workflows/{id}` — Delete workflow
- `POST /workflows/export` — Export selected workflows
- `POST /workflows/backup` — Backup all workflows
- `POST /workflows/restore` — Restore workflows from backup
- `POST /workflows/pin` — Pin/unpin workflow
- `POST /workflows/favorite` — Add/remove favorite
- `POST /workflows/run` — Run workflow (local or NIM VM)

All endpoints and models are documented interactively in the Swagger UI.
