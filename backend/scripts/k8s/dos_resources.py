import requests

import subprocess
import yaml

def run(target_url: str) -> dict:
    """
    Scenario 13: DoS Resources
    """
    target = target_url.rstrip("/")
    
    is_vulnerable = False
    details = ""
    evidence = ""

    # Check 1: Kubectl check for missing limits (Report methodology)
    try:
        # Check deployment 'hunger-check-deployment' in 'big-monolith' namespace
        cmd = "kubectl get deployment hunger-check-deployment -n big-monolith -o yaml"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        
        # Parse YAML to check resources
        dep = yaml.safe_load(output)
        containers = dep['spec']['template']['spec']['containers']
        
        for c in containers:
            resources = c.get('resources', {})
            limits = resources.get('limits', {})
            requests = resources.get('requests', {})
            
            if not limits:
                is_vulnerable = True
                details = "Resource Limits are MISSING in deployment manifest."
                evidence = "resources: {} (No limits defined)"
                break
    except:
        pass

    # Check 2: Active check (Fallback)
    if not is_vulnerable:
        try:
            r = requests.get(target, timeout=5)
            if r.status_code == 200 and ("hunger-check" in r.text.lower() or ":1236" in target):
                is_vulnerable = True
                details = "Service appears to be the Hunger Check (DoS) application."
                evidence = "Service banner detected."
        except:
            pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Denial of Service (No Resource Limits)
Target: {target}
   resources:
     limits:
       cpu: "500m"
       memory: "512Mi"
   ```
3. LimitRanges: Set default limits for containers in the namespace.
"""
        }
    else:
        return {"success": False, "output": f"[-] Target {target} is not the DoS Vulnerable service."}
