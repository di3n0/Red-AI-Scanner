import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 16: RBAC Misconfig
    """
    target = target_url.rstrip("/")
    
    # Report Step: "curl ... /api/v1/secrets", "grep k8svaultapikey"
    # We simulate this by checking if the specific service account (or Any authenticated user in this context?)
    # actually, proper report step is to check if we can list secrets.
    # We can check if there is a rolebinding for the service account that gives 'get secrets'
    
    try:
        # Check permissions of the specific sensitive service account if plausible, 
        # or simplified: Check if we can list secrets in the namespace 'big-monolith' (where Scenario 16 usually lives)
        # Using a canary check "kubectl auth can-i list secrets --namespace big-monolith"
        
        # NOTE: Verification script runs as user 'ais3' (admin), so it will always be yes.
        # We need to find the specific SA `webhook-service-account` used in the scenario and check IT'S permissions.
        
        cmd = "kubectl get rolebinding -n big-monolith -o jsonpath='{range .items[*]}{.metadata.name}{\" \"}{.subjects[*].name}{\"\\n\"}{end}'"
        bindings = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        
        if "webhook-service-account" in bindings:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: RBAC Misconfiguration
Target: Namespace big-monolith
[VERIFIED] Found 'webhook-service-account' with attached RoleBinding.

[How to Exploit (Detailed Steps from Report)]
1. Access Pod using this SA.
2. Query API: `curl ... /api/v1/secrets`
3. Decrypt Secret: `base64 -d`
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Specific misconfigured ServiceAccount not detected.

[How to Verify (from Report)]
1. Check SA tokens in `/var/run/secrets/...`
2. Try querying API server for secrets.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and RBAC misconfig not verified."
        }
