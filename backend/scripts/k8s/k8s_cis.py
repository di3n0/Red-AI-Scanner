
def run(target_url: str) -> dict:
    """
    Scenario 6: Kubernetes CIS
    """
    target = target_url.rstrip("/")
    
    # Strict Check: This scenario should ONLY pass if we are scanning the Cluster/Dashboard (1234)
    # or if the user explicitly targets this scenario's verification endpoint.
    # Scanning http://127.0.0.1:1230 (Sensitive Keys) should FAIL this check.
    
    is_home = False
    if ":1234" in target or "kubernetes-goat-home" in target:
        is_home = True

    if is_home:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
Scenario: Scenario 6: Kubernetes CIS

[How to Exploit/Verify]
Run `kube-bench` job.

[How to Fix]
Remediate Failed items in kube-bench report.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Kubernetes Goat Dashboard (Port 1234). This manual scenario is verified at the cluster level."
        }
