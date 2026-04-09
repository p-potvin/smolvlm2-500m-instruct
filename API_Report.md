# API & Integration Report

---

## 1. State of the API & Exposed Endpoints

The backend API is implemented in `api_server.py` using FastAPI. The main endpoints are:

| Endpoint                        | Method | Description                                      |
|----------------------------------|--------|--------------------------------------------------|
| `/workflows`                    | GET    | List all workflows                               |
| `/workflows`                    | POST   | Create a new workflow                            |
| `/workflows/{id}`               | PUT    | Update a workflow                                |
| `/workflows/{id}`               | DELETE | Delete a workflow                                |
| `/workflows/export`             | POST   | Export selected workflows                        |
| `/workflows/backup`             | POST   | Backup all workflows                             |
| `/workflows/restore`            | POST   | Restore workflows from backup                    |
| `/workflows/pin`                | POST   | Pin/unpin a workflow                             |
| `/workflows/favorite`           | POST   | Mark/unmark a workflow as favorite               |
| `/workflows/run`                | POST   | Run a workflow (local or NIM VM mode)            |
| `/storage/google-drive/upload`  | POST   | Placeholder for Google Drive upload              |
| `/storage/dropbox/upload`       | POST   | Placeholder for Dropbox upload                   |
| `/storage/icloud/upload`        | POST   | Placeholder for iCloud upload                    |
| `/storage/other/upload`         | POST   | Placeholder for other storage providers          |
| `/config/models-dir`            | GET    | Get the models directory                         |
| `/config/models-dir`            | POST   | Set the models directory                         |

- **Authentication:** HTTP Basic (default user/pass: admin/admin, can be disabled via env)
- **Docs:** OpenAPI/Swagger UI is available at `/docs`

---

## 2. Integration of `examples/` Files

- The `examples/` folder contains **standalone demo scripts** for image, video, and text workflows, as well as the main Gradio GUI (`workflow_gui_gradio.py`).
- **These scripts are NOT exposed as API endpoints.** They are meant for local CLI or GUI use, not for direct API consumption.
- The API only exposes workflow CRUD and execution, not the individual demo scripts.

---

## 3. Frontend/Backend Coupling

- The frontend (`frontend/`) is a React SPA that communicates with the backend **only via the `/workflows` API** (see `frontend/src/api.js` and `api.ts`).
- The backend does **not depend on the frontend**. If you delete the `frontend/` folder, the backend (FastAPI and Gradio GUI) will continue to work without issues.
- The frontend is ready to be moved to a separate project/repo. The only requirement is to set the correct `VITE_API_URL` to point to the backend API.

---

## Summary Table

| Area                | State/Notes                                                                 |
|---------------------|------------------------------------------------------------------------------|
| API                 | Stable, CRUD for workflows, no direct access to `examples/` scripts          |
| Examples Integration| Not exposed via API, CLI/GUI only                                            |
| Frontend Coupling   | Decoupled; backend will not break if `frontend/` is removed                  |

---

**In short:**
- The API is workflow-centric, not example-script-centric.
- The `examples/` folder is for demos and local testing, not API exposure.
- The frontend can be safely split out; the backend is fully independent.

Let me know if you want a full endpoint list with request/response schemas or further details on any integration!
