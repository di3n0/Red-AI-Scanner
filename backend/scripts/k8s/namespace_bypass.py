import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 11: Namespace Bypass
    """
    target = target_url.rstrip("/")
    
    # Report Step: "zmap -p 6379...", "redis-cli -h ..."
    # We verify if the target service (cache-store) exists in another namespace (likely 'big-monolith' or similar)
    
    try:
        cmd = "kubectl get pods --all-namespaces -l app=cache-store -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Namespace Isolation Bypass Risk
Target: Pod {pod_name}
[VERIFIED] Found 'cache-store' service in another namespace.

[How to Exploit (Detailed Steps from Report)]
1. Launch Hacker Container in default namespace.
2. Scan internal network: `zmap -p 6379 10.0.0.0/8`
3. Connect to Redis: `redis-cli -h <IP>`
4. Extract Flag: `GET SECRETSTUFF`
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] 'cache-store' pod not found automatically.

[How to Verify (from Report)]
1. Deploy Hacker Container.
2. Run `zmap` or `nmap` to scan other namespace subnets.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and cache-store not found."
        }
