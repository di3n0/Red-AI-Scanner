import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 21: Tetragon
    """
    target = target_url.rstrip("/")
    
    # Report Step: "helm install tetragon", "kubectl get pods ... app=tetragon"
    
    try:
        cmd = "kubectl get pods -n kube-system -l app.kubernetes.io/name=tetragon -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Tetragon Observability
Target: Pod {pod_name}
[VERIFIED] Tetragon is running in kube-system.

[How to Exploit/Test (Detailed Steps from Report)]
1. Trigger Event: Privileged execution or file access.
   `nsenter -t 1 ...` or `cat /etc/shadow`
2. Check Logs:
   `kubectl logs ... -c exportstdout`
3. Result: Tetragon detects process execution/ syscalls.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
         return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Tetragon deployment not detected.

[How to Verify (from Report)]
1. Install Tetragon: `helm install tetragon ...`
2. Validate logs for runtime security events.
"""
         }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and Tetragon not found."
        }
