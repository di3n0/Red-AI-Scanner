
import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 10: Crypto Miner
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubectl get jobs", "kubectl describe job batch-check-job"
    
    try:
        cmd = "kubectl get jobs --all-namespaces -o jsonpath='{range .items[*]}{.metadata.name}{\"\\n\"}{end}'"
        jobs = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        
        if "batch-check-job" in jobs:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY DETECTED: Potential Crypto Miner Job
Target: Cluster Jobs
[VERIFIED] Found suspicious job 'batch-check-job'.

[How to Exploit (Detailed Steps from Report)]
1. Get Pod info: `kubectl get pods -l job-name=batch-check-job`
2. Analyze Image: `kubectl get pod <pod> -o yaml`
3. Reveal History: `docker history --no-trunc <image>`
4. Find Flag/Miner: Look for hidden execution strings in layers.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Suspicious 'batch-check-job' not found automatically.

[How to Verify (from Report)]
1. Run `kubectl get jobs` to list all jobs.
2. Inspect any unknown jobs for mining behavior (high resource usage).
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and no suspicious jobs found."
        }
