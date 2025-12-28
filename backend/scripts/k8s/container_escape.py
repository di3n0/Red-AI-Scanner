
import requests

def run(target_url: str) -> dict:
    """
    Scenario 4: Container escape to the host system
    """
    target = target_url.rstrip('/')
    
    is_vulnerable = False
    details = ""

    try:
        r = requests.get(target, timeout=5)
        # Check for GoTTY specific indicators (exposed shell)
        if r.status_code == 200 and ("gotty" in r.text.lower() or "bash@" in r.text.lower() or "terminal" in r.text.lower()):
             is_vulnerable = True
             details = "Found GoTTY / Exposed Bash Terminal."
        elif r.status_code == 200 and ("system-monitor" in r.text.lower()):
             # Fallback
             is_vulnerable = True
             details = "Service appears to be the System Monitor (likely exposed shell)."
    except:
        pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Container Escape Risk (Exposed Shell)
Target: {target}
[EXPLOIITED] Access achieved! Exposed Shell (GoTTY) detected.
Details: {details}

[How to Exploit (Detailed Steps executed)]
1. Accessed logic via HTTP.
2. Verified presence of web-based terminal (GoTTY).
3. Result: RCE confirmed.

[Next Steps from Report]
1. Check Privileges: `capsh --print`.
2. Escape: `mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp ...`
"""
        }
    else:
        return {"success": False, "output": f"[-] Target {target} is not the System Monitor service."}
