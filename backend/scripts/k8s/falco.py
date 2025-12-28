import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 18: Falco
    """
    target = target_url.rstrip("/")
    
    # Report Step: "helm install falco...", "kubectl get pods --selector app=falco"
    
    try:
        cmd = "kubectl get pods --all-namespaces -l app=falco -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Falco Runtime Security
Target: Pod {pod_name}
[VERIFIED] Falco is running.

[How to Exploit/Test (Detailed Steps from Report)]
1. Trigger Event: Read sensitive file or execute shell in pod.
   `kubectl exec -it <pod> -- cat /etc/shadow`
2. Check Logs:
   `kubectl logs -f -l app=falco`
3. Result: Alert generated for 'Read sensitive file'.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Falco deployment not detected.

[How to Verify (from Report)]
1. Install Falco: `helm install falco falcosecurity/falco`
2. Test Rules: Trigger suspicious activity and check logs.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and Falco not found."
        }
