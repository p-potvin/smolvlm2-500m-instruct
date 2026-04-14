## Starting the API Server (FastAPI)

You can run the API server using the provided `api_server.py` file. This will start a FastAPI server exposing all workflow endpoints.

### 1. Install dependencies (if not already done):
```bash
pip install -r requirements.txt
```

### 2. (Recommended) Activate your virtual environment:
```bash
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 3. Start the API server:
```bash
python api_server.py
```

- By default, the server will run on `http://127.0.0.1:9001`.
- The OpenAPI/Swagger UI will be available at `http://127.0.0.1:9001/docs`.
- You can configure CORS, authentication, and other settings via environment variables (see top of `api_server.py`).

---

**Note:** If you want to run the API with production features (e.g., hot reload, multiple workers), you can use `uvicorn`:
```bash
pip install uvicorn
uvicorn api_server:app --reload --port 9001
```

---

