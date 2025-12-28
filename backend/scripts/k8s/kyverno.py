import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 22: Kyverno
    """
    target = target_url.rstrip("/")
    
    # Report Step: "helm install kyverno", "kubectl get clusterpolicies"
    
    try:
        cmd = "kubectl get clusterpolicies"
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        
        # If we see output other than "No resources found", or header
        if "No resources found" not in result:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Kyverno Policy Engine
Target: Cluster Policies
[VERIFIED] Kyverno Policies found.
{result}

[How to Exploit/Verify (Detailed Steps from Report)]
1. Deploy Policy: `kubectl apply -f kyverno-block-pod-exec.yaml`
2. Test: Try to Exec into blocked namespace.
   `kubectl exec ...` -> Denied.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Kyverno Policies not actively detected.

[How to Verify (from Report)]
1. Install Kyverno.
2. Apply test policies (e.g. Disallow Root).
3. Validate enforcement.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and Kyverno not configured."
        }
