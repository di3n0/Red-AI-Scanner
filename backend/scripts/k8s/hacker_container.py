import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 14: Hacker Container
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubectl run -it hacker-container..."
    
    try:
        cmd = "kubectl get pods -l run=hacker-container -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Hacker Container Active
Target: Pod {pod_name}
[VERIFIED] Hacker Container is running.

[How to Exploit (Detailed Steps from Report)]
1. Exec into container: `kubectl exec -it {pod_name} -- sh`
2. Use tools: `amicontained`, `nikto`, `zmap`.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Hacker Container not currently running.

[How to Verify (from Report)]
1. Run: `kubectl run -it hacker-container --image=madhuakula/hacker-container -- sh`
2. Explore available tools.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and Hacker Container not found."
        }
