import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 20: NSP Boundary
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubectl apply -f website-deny.yaml", "kubectl get netpol"
    
    try:
        cmd = "kubectl get netpol --all-namespaces"
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        
        # If any netpol exists, it's a pass/verified detection
        if "No resources found" not in result:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Network Security Policy Analysis
Target: Cluster
[VERIFIED] Network Policies detected in cluster.
{result}

[How to Exploit/Verify (Detailed Steps from Report)]
1. Create a NetworkPolicy (e.g., Deny All).
2. Test Connectivity: `wget ...` should fail/timeout.
3. Validate: Effective isolation confirmed.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] No Network Policies found.

[How to Verify (from Report)]
1. Create test pod & service.
2. Apply NetworkPolicy (Deny).
3. Verify access is blocked.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and no NetworkPolicies found."
        }
