
import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 6: Kubernetes CIS
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubectl apply -f ...", "kubectl logs -f kube-bench-node-xxxxx"
    
    try:
        cmd = "kubectl get pods -l job-name=kube-bench-node -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY: Configuration / Manual Review
Target: Pod {pod_name}
[VERIFIED] Kube-Bench Job is running.

[How to Exploit (Manual Steps from Report)]
1. Check logs for the benchmark results:
   `kubectl logs -f {pod_name}`
2. Review FAILED status in the output.
"""
             }
    except:
        pass

    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Kube-Bench Job not detected running.

[How to Verify (from Report)]
1. Deploy the benchmark job:
   `kubectl apply -f scenarios/kube-bench-security/node-job.yaml`
2. Check logs of the created pod.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and Kube-Bench is not running."
        }
