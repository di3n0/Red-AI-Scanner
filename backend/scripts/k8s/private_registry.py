
import requests

def run(target_url: str) -> dict:
    """
    Scenario 7: Attacking private registry
    """
    target = target_url.rstrip('/')
    
    is_vulnerable = False
    details = ""

    try:
        # Registry usually responds at /v2/
        check_url = f"{target}/v2/"
        r = requests.get(check_url, timeout=5)
        
        # Registry returns 200 or 401 on /v2/ endpoint usually
        if r.status_code in [200, 401, 403] and ("docker" in r.headers.get("Docker-Distribution-Api-Version", "").lower() or ":1235" in target):
             is_vulnerable = True
             details = f"Service responded as a Docker Registry (Code {r.status_code})."
    except:
        pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Private Registry Exposure
Target: {target}
Details: {details}

[How to Exploit]
1. Enumeration: List repositories.
   Command: `curl {target}/v2/_catalog`
2. Tags: List tags for a repo.
   Command: `curl {target}/v2/<repo_name>/tags/list`
3. Pull: Pull the image locally to inspect.
   Command: `docker pull localhost:1235/<repo_name>:<tag>`
4. Inspect: `docker run -it <image> sh` or `dive <image>` to find hardcoded secrets.

[How to Fix]
1. Authentication: Enable TLS and Basic Auth for the registry.
2. Network access: Do not expose registry outside the cluster/VPN. Use `ClusterIP`.
3. Scanning: Regularly scan images for vulnerable packages and secrets.
"""
        }
    else:
        return {"success": False, "output": f"[-] Target {target} does not identify as a Docker Registry."}
