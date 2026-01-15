from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
from pathlib import Path
from datetime import datetime
import json
import uuid

# Database setup
DB_PATH = Path(__file__).parent / "data" / "aiccl.db"

def init_db():
    """Initialize SQLite database and create tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            key TEXT PRIMARY KEY,
            project_id INTEGER,
            created_at TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT,
            trace_data TEXT,
            created_at TEXT,
            FOREIGN KEY (api_key) REFERENCES api_keys(key)
        )
    """)
    
    conn.commit()
    return conn

# Initialize database
conn = init_db()

# Pydantic models
class ProjectCreate(BaseModel):
    project_name: str

class TraceCreate(BaseModel):
    api_key: str
    trace: dict

# FastAPI app
app = FastAPI(title="AICCL Tracing Backend")

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Allow both origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Explicit OPTIONS handler for all endpoints
@app.options("/{rest_of_path:path}")
async def preflight(rest_of_path: str):
    headers = {
        "Access-Control-Allow-Origin": "http://127.0.0.1:8080",  # Match the requesting origin
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true",
    }
    return JSONResponse(status_code=200, content={}, headers=headers)

@app.get("/")
async def root():
    return {"message": "AICCL Tracing Backend"}

# API key endpoints
@app.post("/api/keys")
async def create_api_key(project: ProjectCreate):
    """Create a new API key for a project."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (name) VALUES (?)", (project.project_name,))
    project_id = cursor.lastrowid
    api_key = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO api_keys (key, project_id, created_at) VALUES (?, ?, ?)",
        (api_key, project_id, created_at)
    )
    conn.commit()
    return {"key": api_key, "project_name": project.project_name, "created_at": created_at}

@app.get("/api/keys")
async def get_api_keys():
    """List all API keys with their project names."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ak.key, p.name, ak.created_at
        FROM api_keys ak
        JOIN projects p ON ak.project_id = p.id
    """)
    keys = [{"key": row[0], "project_name": row[1], "created_at": row[2]} for row in cursor.fetchall()]
    return keys

@app.get("/api/validate/{api_key}")
async def validate_api_key(api_key: str):
    """Validate an API key."""
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM api_keys WHERE key = ?", (api_key,))
    return {"valid": bool(cursor.fetchone()), "project_id": None}

# Trace endpoints
@app.post("/api/trace")
async def log_trace(trace: TraceCreate):
    """Log a trace for a given API key."""
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM api_keys WHERE key = ?", (trace.api_key,))
    if not cursor.fetchone():
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    cursor.execute(
        "INSERT INTO traces (api_key, trace_data, created_at) VALUES (?, ?, ?)",
        (trace.api_key, json.dumps(trace.trace), datetime.now().isoformat())
    )
    conn.commit()
    return {"status": "success"}

@app.get("/api/traces/{api_key}")
async def get_traces(api_key: str):
    """Retrieve all traces for a given API key."""
    cursor = conn.cursor()
    cursor.execute("SELECT trace_data FROM traces WHERE api_key = ?", (api_key,))
    traces = [json.loads(row[0]) for row in cursor.fetchall()]
    return traces