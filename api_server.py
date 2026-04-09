
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import os
import json
from threading import Lock
from pydantic import BaseModel
from typing import List, Optional

# --- Configurable Settings ---
AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "1") == "1"
DEFAULT_MODELS_DIR = os.environ.get("DEFAULT_MODELS_DIR", r"D:\\comfyui\\resources\\comfyui\\models")

app = FastAPI(title="Vaultwares Workflow API", description="API for managing workflows, favorites, backup, NIM integration, and storage.", version="0.2.0")

# --- CORS ---
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:4173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not AUTH_ENABLED:
        return
    # Placeholder: Replace with real user/pass check
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

# --- Models ---
class Workflow(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    steps: Optional[list] = []
    pinned: Optional[bool] = False
    favorite: Optional[bool] = False

class WorkflowsExportRequest(BaseModel):
    ids: List[str]

class WorkflowsBackupRequest(BaseModel):
    pass

class WorkflowsRestoreRequest(BaseModel):
    data: List[Workflow]

class WorkflowPinRequest(BaseModel):
    id: str
    pin: bool

class WorkflowFavoriteRequest(BaseModel):
    id: str
    favorite: bool

class WorkflowRunRequest(BaseModel):
    id: str
    mode: str  # 'local' or 'nim'

# --- Persistent JSON Storage ---
VAULTWARES_HOME_CSS = """
body {{ background: #181c24; color: #f3f6fa; font-family: 'Segoe UI', Arial, sans-serif; text-align: center; margin: 0; padding: 0; }}
.logo {{ margin-top: 48px; }}
.vault {{
    display: inline-block;
    margin: 0 auto 24px auto;
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, #2e3a4e 60%, #4e7ad2 100%);
    border-radius: 50%;
    box-shadow: 0 4px 32px #0008;
    position: relative;
}}
.vault:before {{
    content: '';
    display: block;
    position: absolute;
    left: 50%; top: 50%;
    width: 60px; height: 60px;
    background: #232b3a;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 8px #4e7ad2;
}}
h1 {{ font-size: 2.5rem; margin: 24px 0 8px 0; letter-spacing: 2px; }}
.subtitle {{ color: #b0c4e7; font-size: 1.2rem; margin-bottom: 32px; }}
.links a {{
    display: inline-block;
    margin: 12px 16px;
    padding: 12px 28px;
    background: #4e7ad2;
    color: #fff;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1.1rem;
    transition: background 0.2s;
}}
.links a:hover {{ background: #355a8a; }}
.apidoc-link {{
    margin-top: 40px;
    color: #b0c4e7;
    font-size: 0.95rem;
}}
.apidoc-link a {{
    color: #fff;
    text-decoration: underline;
}}
"""
WORKFLOWS_FILE = os.environ.get("WORKFLOWS_FILE", "workflows.json")
FRONTEND_URL = "https://vaultwares-frontend.example.com"  # TODO: Replace with actual frontend URL
API_KEY_REG_URL = "https://vaultwares.example.com/register"  # TODO: Replace with actual registration URL
_storage_lock = Lock()


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>Vaultwares Pipelines</title>
        <style>{css}</style>
    </head>
    <body>
        <div class="logo">
            <div class="vault"></div>
        </div>
        <h1>Vaultwares Pipelines</h1>
        <div class="subtitle">Multi-Agent AI Workflow Platform</div>
        <p>Welcome to <b>Vaultwares</b>!<br>
        Access the full dashboard, explore workflows, and manage your AI pipelines.</p>
        <div class="links">
            <a href="{frontend_url}" target="_blank">Go to Frontend Dashboard</a>
            <a href="{api_key_url}" target="_blank">Register for an API Key</a>
        </div>
        <p class="apidoc-link">API documentation: <a href='/docs'>/docs</a></p>
    </body>
    </html>
    """.format(css=VAULTWARES_HOME_CSS, frontend_url=FRONTEND_URL, api_key_url=API_KEY_REG_URL)

def load_workflows():
    if not os.path.exists(WORKFLOWS_FILE):
        return {}
    with _storage_lock:
        with open(WORKFLOWS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return {k: Workflow(**v) for k, v in data.items()}
            except Exception:
                return {}

def save_workflows(workflows):
    with _storage_lock:
        with open(WORKFLOWS_FILE, "w", encoding="utf-8") as f:
            json.dump({k: v.dict() for k, v in workflows.items()}, f, indent=2)


# --- Endpoints ---
@app.get("/workflows", response_model=List[Workflow])
def list_workflows(credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    return list(workflows.values())

@app.post("/workflows", response_model=Workflow)
def create_workflow(wf: Workflow, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    workflows[wf.id] = wf
    save_workflows(workflows)
    return wf

@app.put("/workflows/{id}", response_model=Workflow)
def update_workflow(id: str, wf: Workflow, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    if id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflows[id] = wf
    save_workflows(workflows)
    return wf

@app.delete("/workflows/{id}")
def delete_workflow(id: str, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    if id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    del workflows[id]
    save_workflows(workflows)
    return {"ok": True}

@app.post("/workflows/export")
def export_workflows(req: WorkflowsExportRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    return [workflows[wid] for wid in req.ids if wid in workflows]

@app.post("/workflows/backup")
def backup_workflows(_: WorkflowsBackupRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    return list(workflows.values())

@app.post("/workflows/restore")
def restore_workflows(req: WorkflowsRestoreRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    for wf in req.data:
        workflows[wf.id] = wf
    save_workflows(workflows)
    return {"ok": True}

@app.post("/workflows/pin")
def pin_workflow(req: WorkflowPinRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    if req.id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflows[req.id].pinned = req.pin
    save_workflows(workflows)
    return workflows[req.id]

@app.post("/workflows/favorite")
def favorite_workflow(req: WorkflowFavoriteRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    if req.id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflows[req.id].favorite = req.favorite
    save_workflows(workflows)
    return workflows[req.id]

@app.post("/workflows/run")
def run_workflow(req: WorkflowRunRequest, credentials: HTTPBasicCredentials = Depends(check_auth)):
    workflows = load_workflows()
    if req.id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    # NIM VM integration placeholder
    if req.mode == "nim":
        # --- NIM VM Integration Placeholder ---
        # Here you would add logic to connect to the NIM VM, send workflow data, and receive results.
        # Example (pseudo):
        # nim_result = nim_vm_client.run_workflow(workflows[req.id])
        # return {"id": req.id, "mode": req.mode, "status": "nim_vm_started", "result": nim_result}
        return {"id": req.id, "mode": req.mode, "status": "nim_vm_placeholder", "message": "NIM VM integration not yet implemented."}
    # Simulate local run
    return {"id": req.id, "mode": req.mode, "status": "started"}

# --- Persistent Storage Placeholders ---
@app.post("/storage/google-drive/upload")
def upload_google_drive(credentials: HTTPBasicCredentials = Depends(check_auth)):
    # Placeholder for Google Drive upload
    return {"status": "placeholder", "message": "Google Drive upload not implemented."}

@app.post("/storage/dropbox/upload")
def upload_dropbox(credentials: HTTPBasicCredentials = Depends(check_auth)):
    # Placeholder for Dropbox upload
    return {"status": "placeholder", "message": "Dropbox upload not implemented."}

@app.post("/storage/icloud/upload")
def upload_icloud(credentials: HTTPBasicCredentials = Depends(check_auth)):
    # Placeholder for iCloud upload
    return {"status": "placeholder", "message": "iCloud upload not implemented."}

@app.post("/storage/other/upload")
def upload_other(credentials: HTTPBasicCredentials = Depends(check_auth)):
    # Placeholder for other storage providers
    return {"status": "placeholder", "message": "Other storage provider upload not implemented."}

# --- Models Directory Config ---
@app.get("/config/models-dir")
def get_models_dir(credentials: HTTPBasicCredentials = Depends(check_auth)):
    return {"models_dir": DEFAULT_MODELS_DIR}

@app.post("/config/models-dir")
def set_models_dir(dir_path: str, credentials: HTTPBasicCredentials = Depends(check_auth)):
    global DEFAULT_MODELS_DIR
    DEFAULT_MODELS_DIR = dir_path
    return {"models_dir": DEFAULT_MODELS_DIR}




# --- Script Entrypoint ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="127.0.0.1", port=8001, reload=True)
