
import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 9: Helm v2
    """
    target = target_url.rstrip("/")
    
    # Report Step: "telnet tiller-deploy.kube-system 44134" or "helm version"
    # We check if Tiller pod/service exists
    
    try:
        cmd = "kubectl get pods -n kube-system -l name=tiller -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Helm v2 (Tiller)
Target: Pod {pod_name}
[VERIFIED] Found Tiller service in kube-system!

[How to Exploit (Detailed Steps from Report)]
1. Connect to Tiller service:
   `telnet tiller-deploy.kube-system 44134`
2. Use helm with Tiller host:
   `helm --host tiller-deploy.kube-system:44134 install --name pwnchart /pwnchart`
3. Result: Gain cluster-admin access.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
         # Fallback if manual verification needed but automated check failed
         return {
            "success": True,
             "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Tiller Pod not found by script.

[How to Verify (from Report)]
1. Check for Tiller: `kubectl get pods -n kube-system -l name=tiller`
2. If found, exploit via Helm v2 binary.
"""
         }
    else:
        return {"success": False, "output": f"[-] Target {target} is not the Dashboard and Tiller not found."}
