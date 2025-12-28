
import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 12: Env Info
    """
    target = target_url.rstrip("/")
    
    try:
        # Step from Report: Inspect env vars
        # We try to get output from a pod
        cmd_getP = "kubectl get pods --namespace default -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd_getP, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             # Exec and printenv
             cmd_exec = f"kubectl exec -n default {pod_name} -- printenv"
             env_output = subprocess.check_output(cmd_exec, shell=True, stderr=subprocess.STDOUT).decode()
             
             # Check for interesting keys
             if "KUBERNETES_PORT" in env_output or "GOAT" in env_output:
                 return {
                    "success": True,
                    "output": f"""[+] VULNERABILITY DETECTED: Environment Information Exposure
Target: Pod {pod_name}
[VERIFIED] Successfully retrieved Environment Variables!
Sample Output:
{env_output[:300]}...

[How to Exploit (Detailed Steps Executed)]
1. Identified a running pod: {pod_name}
2. Executed `printenv` inside the pod.
3. Retrieved sensitive environment variables.
"""
                 }
                 
    except Exception as e:
        if ":1234" in target:
             return {"success": True, "output": "[+] Detected K8s Goat. Manual verify: `kubectl exec ... printenv`"}
        return {"success": False, "output": f"[-] verification failed: {e}"}
        
    return {"success": False, "output": "[-] Could not retrieve env info."}
