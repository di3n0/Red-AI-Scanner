import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 19: Popeye
    """
    target = target_url.rstrip("/")
    
    # Report Step: "popeye"
    # CLI tool audit. 
    
    return {
        "success": True,
        "output": f"""[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
Scenario: Scenario 19: Popeye

[How to Exploit/Verify (from Report)]
1. Run Popeye sanitizer:
   `popeye` (if installed) or via Hacker Container.
2. Analyze cluster score and warnings.
"""
    }
