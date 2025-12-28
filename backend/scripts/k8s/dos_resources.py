
import requests

def run(target_url: str) -> dict:
    """
    Scenario 13: DoS the Memory/CPU resources
    """
    target = target_url.rstrip('/')
    
    is_vulnerable = False
    details = ""

    try:
        r = requests.get(target, timeout=5)
        # Port 1236 check
        if r.status_code == 200 and ("hunger-check" in r.text.lower() or ":1236" in target):
             is_vulnerable = True
             details = "Service appears to be the Hunger Check (DoS) application."
    except:
        pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Unbounded Resource Consumption (DoS)
Target: {target}
Details: {details}

[How to Exploit]
1. Stress Test: Use stress-generation tools (like `stress-ng` inside the container or generic HTTP flooding if app supports it).
2. Resource Hog: The application likely does not have ResourceLimits.
   Action: Send requests that trigger high CPU/Memory computation.
3. Observability: Watch the node status. `kubectl get nodes`.
   Result: The node might become NotReady, or other pods might be evicted (OOMKilled).

[How to Fix]
1. Resource Quotas: Apply ResourceQuotas to namespaces.
2. Limits: Define `resources.requests` and `resources.limits` in the Pod spec.
   Example:
   ```yaml
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
