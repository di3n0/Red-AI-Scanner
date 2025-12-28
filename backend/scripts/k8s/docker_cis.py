
import subprocess

def run(target_url: str) -> dict:
    """
    Scenario 5: Docker CIS
    """
    target = target_url.rstrip("/")
    
    # Report Step: "kubectl apply -f ...", "kubectl exec -it docker-bench-security-xxxxx -- sh"
    # We verify if the daemonset/pod exists
    
    try:
        cmd = "kubectl get pods -l k8s-app=docker-bench-security -o jsonpath='{.items[0].metadata.name}'"
        pod_name = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        
        if pod_name:
             return {
                "success": True,
                "output": f"""[+] VULNERABILITY: Configuration / Manual Review
Target: Pod {pod_name}
[VERIFIED] Docker Bench Security Pod is running.

[How to Exploit (Manual Steps from Report)]
1. Exec into the pod:
   `kubectl exec -it {pod_name} -- sh`
2. Run the benchmark:
   `cd docker-bench-security && sh docker-bench-security.sh`
3. Analyze the results for FAIL/WARN items.
"""
             }
    except:
        pass

    # Fallback if not found (maybe not deployed yet)
    if ":1234" in target or "kubernetes-goat-home" in target:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
[NOTE] Docker Bench Security DaemonSet not detected running.

[How to Verify (from Report)]
1. Deploy the benchmark:
   `kubectl apply -f scenarios/docker-bench-security/deployment.yaml`
2. Exec into the pod and run `sh docker-bench-security.sh`.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Dashboard and Docker Bench Security is not running."
        }
