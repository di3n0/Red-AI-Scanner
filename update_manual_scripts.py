
import os

# Template that enforces strict target check (must range 1234 or Goat Home)
strict_template = '''
def run(target_url: str) -> dict:
    """
    STRICT_NAME
    """
    target = target_url.rstrip("/")
    
    # Strict Check: This scenario should ONLY pass if we are scanning the Cluster/Dashboard (1234)
    # or if the user explicitly targets this scenario\'s verification endpoint.
    # Scanning http://127.0.0.1:1230 (Sensitive Keys) should FAIL this check.
    
    is_home = False
    if ":1234" in target or "kubernetes-goat-home" in target:
        is_home = True

    if is_home:
        return {
            "success": True,
            "output": """[+] VULNERABILITY: Configuration / Manual Review
Target: {target}
Scenario: STRICT_NAME

[How to Exploit/Verify]
STRICT_INSTRUCT

[How to Fix]
STRICT_FIX
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} is not the Kubernetes Goat Dashboard (Port 1234). This manual scenario is verified at the cluster level."
        }
'''

scripts_data = [
    ("Scenario 5: Docker CIS", "backend/scripts/k8s/docker_cis.py", "Run `docker-bench-security` on the node.", "Follow CIS Benchmark recommendations (Audit, Permissions, Logging)."),
    ("Scenario 6: Kubernetes CIS", "backend/scripts/k8s/k8s_cis.py", "Run `kube-bench` job.", "Remediate Failed items in kube-bench report."),
    ("Scenario 8: NodePort Services", "backend/scripts/k8s/nodeport_services.py", "Nmap ports 30000-32767 on nodes.", "Avoid NodePort for production. Use LoadBalancer or Ingress."),
    ("Scenario 9: Helm v2", "backend/scripts/k8s/helm_v2.py", "Check for 'tiller-deploy' deployment.", "Upgrade to Helm v3 (Tiller-less)."),
    ("Scenario 10: Crypto Miner", "backend/scripts/k8s/crypto_miner.py", "Check high CPU usage pods.", "Deploy Runtime Security (Falco) to block miner binaries."),
    ("Scenario 11: Namespace Bypass", "backend/scripts/k8s/namespace_bypass.py", "Test access to other namespace services.", "NetworkPolicies (Deny All by default)."),
    ("Scenario 12: Env Info", "backend/scripts/k8s/env_info.py", "Inspect env vars (printenv) in checking pods.", "Use K8s Secrets. Do not pass sensitive data in plain ENV."),
    ("Scenario 14: Hacker Container", "backend/scripts/k8s/hacker_container.py", "Identify malicious pods (hacker-container).", "Image Scanning, Admission Controllers (OPA Gatekeeper)."),
    ("Scenario 15: Hidden Layers", "backend/scripts/k8s/hidden_layers.py", "Analyze image layers (dive).", "Multi-stage builds. Do not include secrets in intermediate layers."),
    ("Scenario 16: RBAC Misconfig", "backend/scripts/k8s/rbac_misconfig.py", "Check permissions (kubectl auth can-i).", "Least Privilege Principle. Remove 'cluster-admin' from unnecessary SAs."),
    ("Scenario 17: KubeAudit", "backend/scripts/k8s/kubeaudit.py", "Run `kubeaudit all`.", "Apply KubeAudit recommendations."),
    ("Scenario 18: Falco", "backend/scripts/k8s/falco.py", "Verify Falco is running.", "Ensure Security Monitoring is active."),
    ("Scenario 19: Popeye", "backend/scripts/k8s/popeye.py", "Run `popeye`.", "Clean up sanitizer findings."),
    ("Scenario 20: NSP Boundary", "backend/scripts/k8s/nsp_boundary.py", "Verify NetworkPolicies.", "Implement default-deny NetworkPolicies."),
    ("Scenario 21: Tetragon", "backend/scripts/k8s/tetragon.py", "Check Tetragon events.", "Enforce process execution policies."),
    ("Scenario 22: Kyverno", "backend/scripts/k8s/kyverno.py", "Check Policy Reports.", "Enforce Pod Security Standards via Kyverno.")
]

for name, path, instruct, fix in scripts_data:
    content = strict_template.replace("STRICT_NAME", name).replace("STRICT_INSTRUCT", instruct).replace("STRICT_FIX", fix)
    abs_path = os.path.join("/home/ais3/Desktop/redteamTool", path)
    with open(abs_path, "w") as f:
        f.write(content)
    print(f"Updated {path}")
