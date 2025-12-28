from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from scanner import scanner
from scanner import scanner
from ai_client import ai_client
from exploit_runner import exploit_runner
from script_registry import registry
import json
import os
import requests

app = FastAPI(title="Red-AI-Scanner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    target_url: str
    scan_type: str = "custom" # "dvwa", "k8s_goat", "custom"

class AnalysisRequest(BaseModel):
    vulnerability_data: Dict[str, Any]

class PoCRequest(BaseModel):
    target_url: str
    vulnerability_data: Dict[str, Any]

class RunPoCRequest(BaseModel):
    poc_code: str

class ImportScriptRequest(BaseModel):
    script_url: str

class RunAttackRequest(BaseModel):
    attack_id: str
    target_url: str

class ApiKeyRequest(BaseModel):
    key: str

@app.get("/")
def read_root():
    return {"message": "Red-AI-Scanner Backend is running"}

@app.post("/scan/nmap")
def run_nmap(request: ScanRequest):
    result = scanner.run_nmap_scan(request.target_url)
    return result

@app.post("/scan/nuclei")
def run_nuclei(request: ScanRequest):
    result = scanner.run_nuclei_scan(request.target_url)
    return result

@app.post("/scan/zap")
def run_zap(request: ScanRequest):
    result = scanner.run_zap_scan(request.target_url)
    return result

@app.post("/scan/stop")
def stop_scan():
    result = scanner.stop_active_scan()
    return result

@app.post("/analyze")
def analyze_results(request: AnalysisRequest):
    analysis = ai_client.analyze_vulnerability(request.vulnerability_data)
    return analysis

@app.post("/generate_poc")
def generate_poc(request: PoCRequest):
    result = ai_client.generate_poc(request.vulnerability_data, request.target_url)
    return result

@app.post("/run_poc")
def run_poc(request: RunPoCRequest):
    result = exploit_runner.run_poc(request.poc_code)
    return result

# --- V2 Features ---

@app.post("/script/import")
def import_script(request: ImportScriptRequest):
    """
    Fetches external script content, uses Gemini to generate a Python exploit,
    and saves it to the registry.
    """
    try:
        # 1. Fetch content
        resp = requests.get(request.script_url, timeout=10)
        resp.raise_for_status()
        content = resp.text
        
        # 2. Generate Exploit via AI
        gen_result = ai_client.generate_exploit_from_url(request.script_url, content)
        if "error" in gen_result:
             raise HTTPException(status_code=500, detail=gen_result["error"])
        
        code = gen_result["code"]
        name = request.script_url.split('/')[-1]
        
        # 3. Save to Registry
        entry = registry.add_custom_script(f"Imported: {name}", code, request.script_url)
        
        return {"status": "success", "entry": entry}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/attacks")
def list_attacks():
    return registry.get_all_scripts()

@app.get("/attack/{attack_id}")
def get_attack_details(attack_id: str):
    code = registry.get_script_code(attack_id)
    if not code:
        raise HTTPException(status_code=404, detail="Script code not found.")
    return {"id": attack_id, "code": code}

@app.post("/attack/run")
def run_attack(request: RunAttackRequest):
    # Retrieve code
    code = registry.get_script_code(request.attack_id)
    if not code:
        # If it's a built-in without code, we might generate it on fly (Mock for now if empty)
        # For this demo, let's assume we use Gemini to generate on fly if empty?
        # Or return error. Let's return error or mock.
        return {"success": False, "output": "Script code not available locally. Analyze & Generate first."}
    
    # Inject Target URL (Simple replacement or env var)
    # The generated script expects 'TARGET_URL' var or sys arg.
    # We'll prepend variable definition
    injected_code = f"TARGET_URL = '{request.target_url}'\n" + code
    
    result = exploit_runner.run_poc(injected_code)
    return result

@app.get("/config/ai")
def get_ai_config():
    """Returns the current masked API key."""
    return {"key": ai_client.get_api_key_masked()}

@app.post("/config/ai")
def update_ai_config(request: ApiKeyRequest):
    """Updates the AI API key."""
    ai_client.update_api_key(request.key)
    return {"status": "success", "message": "API Key updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
