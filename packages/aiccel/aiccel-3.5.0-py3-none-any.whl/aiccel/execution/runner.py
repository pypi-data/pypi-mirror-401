# aiccel/execution/runner.py
"""
AICCEL Isolated Runner Service
==============================

A standalone FastAPI service for executing potentially unsafe code
in an isolated environment.
"""

import os
import json
import base64
import io
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional
import contextlib
import time

app = FastAPI(title="AICCEL Isolated Runner")

class ExecutionRequest(BaseModel):
    code: str
    dataframe_json: Optional[str] = None  # Base64 encoded parquet or json
    context: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    dataframe_json: Optional[str] = None
    execution_time_ms: float

def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    allowed = ["pandas", "numpy", "re", "random", "string", "datetime", "math", "json", "pd", "np"]
    if name in allowed or any(a in name for a in allowed):
        return __import__(name, globals, locals, fromlist, level)
    raise ImportError(f"Module '{name}' is not allowed")

SAFE_BUILTINS = {
    "abs": abs, "all": all, "any": any, "bool": bool,
    "dict": dict, "enumerate": enumerate, "filter": filter, 
    "float": float, "int": int, "isinstance": isinstance, 
    "len": len, "list": list, "map": map, "max": max, 
    "min": min, "print": print, "range": range, "round": round,
    "set": set, "str": str, "sum": sum, "tuple": tuple, "type": type,
    "zip": zip, "None": None, "True": True, "False": False,
    "__import__": restricted_import
}

@app.post("/execute", response_model=ExecutionResponse)
async def execute_code(req: ExecutionRequest):
    start_time = time.perf_counter()
    output_buffer = io.StringIO()
    
    # 1. Prepare DataFrame
    df = None
    if req.dataframe_json:
        try:
            # We use JSON for simplicity in this demo, but Parquet is better for prod
            df = pd.read_json(io.StringIO(req.dataframe_json))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid DataFrame format: {e}")
            
    # 2. Prepare Scope
    execution_scope = {
        "df": df,
        "pd": pd,
        "np": np,
        "__builtins__": SAFE_BUILTINS
    }
    if req.context:
        execution_scope.update(req.context)
        
    # 3. Execute
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(req.code, execution_scope)
        
        # 4. Handle Result
        result_df = execution_scope.get("df")
        result_df_json = None
        if isinstance(result_df, pd.DataFrame):
            result_df_json = result_df.to_json()
            
        return ExecutionResponse(
            success=True,
            output=output_buffer.getvalue(),
            execution_time_ms=(time.perf_counter() - start_time) * 1000,
            dataframe_json=result_df_json
        )
        
    except Exception as e:
        return ExecutionResponse(
            success=False,
            output=output_buffer.getvalue(),
            error=f"{type(e).__name__}: {str(e)}",
            execution_time_ms=(time.perf_counter() - start_time) * 1000
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
