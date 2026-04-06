from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Vaultwares Workflow API", description="API for managing workflows, favorites, backup, and NIM integration.", version="0.1.0")

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

# --- In-memory store (for demo) ---
workflows = {}

# --- Endpoints ---
@app.get("/workflows", response_model=List[Workflow])
def list_workflows():
    return list(workflows.values())

@app.post("/workflows", response_model=Workflow)
def create_workflow(wf: Workflow):
    workflows[wf.id] = wf
    return wf

@app.put("/workflows/{id}", response_model=Workflow)
def update_workflow(id: str, wf: Workflow):
    if id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflows[id] = wf
    return wf

@app.delete("/workflows/{id}")
def delete_workflow(id: str):
    if id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    del workflows[id]
    return {"ok": True}

@app.post("/workflows/export")
def export_workflows(req: WorkflowsExportRequest):
    return [workflows[wid] for wid in req.ids if wid in workflows]

@app.post("/workflows/backup")
def backup_workflows(_: WorkflowsBackupRequest):
    return list(workflows.values())

@app.post("/workflows/restore")
def restore_workflows(req: WorkflowsRestoreRequest):
    for wf in req.data:
        workflows[wf.id] = wf
    return {"ok": True}

@app.post("/workflows/pin")
def pin_workflow(req: WorkflowPinRequest):
    if req.id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflows[req.id].pinned = req.pin
    return workflows[req.id]

@app.post("/workflows/favorite")
def favorite_workflow(req: WorkflowFavoriteRequest):
    if req.id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflows[req.id].favorite = req.favorite
    return workflows[req.id]

@app.post("/workflows/run")
def run_workflow(req: WorkflowRunRequest):
    if req.id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    # Simulate run
    return {"id": req.id, "mode": req.mode, "status": "started"}

# --- OpenAPI/Swagger UI available at /docs and /openapi.json ---
