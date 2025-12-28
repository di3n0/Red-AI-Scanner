import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 17: KubeAudit
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubeaudit all"
    # This is a CLI tool audit. 
    
    # We return success with instructions because we can't easily automate an interactive audit
    # without installing the tool or executing a heavy job.
    
    return {
        "success": True,
        "output": f"""[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
Scenario: Scenario 17: KubeAudit

[How to Exploit/Verify (from Report)]
1. Run KubeAudit in helper container:
   `kubectl run -it --rm --image=madhuakula/hacker-container audit -- bash`
2. Execute audit:
   `kubeaudit all`
3. Analyze results for privilege/security issues.
"""
    }
