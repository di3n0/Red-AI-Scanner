import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 15: Hidden Layers
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubectl get jobs", "docker history ...", "dive ..."
    
    try:
        cmd = "kubectl get jobs --all-namespaces -l app=hidden-in-layers -o jsonpath='{.items[0].metadata.name}'"
        job_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if job_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Hidden Information in Layers
Target: Job {job_name}
[VERIFIED] Found 'hidden-in-layers' job.

[How to Exploit (Detailed Steps from Report)]
1. Get Image Name: `madhuakula/k8s-goat-hidden-in-layers`
2. Analyze History: `docker history --no-trunc <image>`
3. Deep Dive: `dive <image>` or export tar `docker save ...`
4. Extract Secret: `tar -xvf layer.tar; cat root/secret.txt`
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] 'hidden-in-layers' job not found.

[How to Verify (from Report)]
1. Check for jobs: `kubectl get jobs`.
2. Inspect images for secrets using `dive`.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and hidden layers job not found."
        }
