
import requests

def run(target_url: str) -> dict:
    """
    Scenario 3: SSRF in the Kubernetes (K8S) world
    """
    target = target_url.rstrip('/')
    
    is_vulnerable = False
    details = ""

    try:
        # SSRF app (internal-proxy) on 1232 often reflects input or shows "K8S Goat" style
        r = requests.get(target, timeout=5)
        # Unique identifier for the SSRF scenario app
        if r.status_code == 200 and ("internal-proxy" in r.text.lower() or "galery" in r.text.lower() or ":1232" in target):
            is_vulnerable = True
            details = "Service appears to be the Internal Proxy application (SSRF Target)."
    except:
        pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: SSRF Potential
Target: {target}
Details: {details}

[How to Exploit]
1. Identification: Observe the application takes a URL verification parameter (e.g., `?url=...`).
2. Cloud Metadata: Attempt to access Cloud Metadata service.
   AWS: `?url=http://169.254.169.254/latest/meta-data/`
   GCP: `?url=http://metadata.google.internal/computeMetadata/v1/`
3. K8s Internal: Scan internal K8s services (e.g., Etcd, Kube-API).
   Payload: `?url=http://kubernetes.default.svc`

[How to Fix]
1. Input Validation: Whitelist allowed domains/protocols for the proxy.
2. Network Policy: Use Kubernetes NetworkPolicies to restrict the pod's egress traffic (deny access to 169.254.169.254 or internal CIDRs).
3. Service Mesh: Use Istio/Linkerd to control egress traffic.
"""
        }
    else:
        return {"success": False, "output": f"[-] Target {target} is not the SSRF Vulnerable service."}
