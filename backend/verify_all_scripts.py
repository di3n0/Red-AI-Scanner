
import sys
import os
import importlib.util

# Add backend directory to path so we can import scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_script(name):
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "k8s", name)
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

SCENARIOS = [
    # Active Scanners (Specific Ports)
    {"file": "sensitive_keys.py", "port": 1230, "name": "Scenario 1: Sensitive Keys"},
    {"file": "dind_exploitation.py", "port": 1231, "name": "Scenario 2: DIND Exploitation"},
    {"file": "ssrf_k8s.py", "port": 1232, "name": "Scenario 3: SSRF"},
    {"file": "container_escape.py", "port": 1233, "name": "Scenario 4: Container Escape"},
    {"file": "private_registry.py", "port": 1235, "name": "Scenario 7: Private Registry"},
    {"file": "dos_resources.py", "port": 1236, "name": "Scenario 13: DoS Resources"},

    # Manual/Config Scanners (Check against Dashboard/Home Port 1234)
    {"file": "docker_cis.py", "port": 1234, "name": "Scenario 5: Docker CIS"},
    {"file": "k8s_cis.py", "port": 1234, "name": "Scenario 6: K8s CIS"},
    {"file": "nodeport_services.py", "port": 1234, "name": "Scenario 8: NodePort Services"},
    {"file": "helm_v2.py", "port": 1234, "name": "Scenario 9: Helm v2"},
    {"file": "crypto_miner.py", "port": 1234, "name": "Scenario 10: Crypto Miner"},
    {"file": "namespace_bypass.py", "port": 1234, "name": "Scenario 11: Namespace Bypass"},
    {"file": "env_info.py", "port": 1234, "name": "Scenario 12: Env Info"},
    {"file": "hacker_container.py", "port": 1234, "name": "Scenario 14: Hacker Container"},
    {"file": "hidden_layers.py", "port": 1234, "name": "Scenario 15: Hidden Layers"},
    {"file": "rbac_misconfig.py", "port": 1234, "name": "Scenario 16: RBAC Misconfig"},
    {"file": "kubeaudit.py", "port": 1234, "name": "Scenario 17: KubeAudit"},
    {"file": "falco.py", "port": 1234, "name": "Scenario 18: Falco"},
    {"file": "popeye.py", "port": 1234, "name": "Scenario 19: Popeye"},
    {"file": "nsp_boundary.py", "port": 1234, "name": "Scenario 20: NSP Boundary"},
    {"file": "tetragon.py", "port": 1234, "name": "Scenario 21: Tetragon"},
    {"file": "kyverno.py", "port": 1234, "name": "Scenario 22: Kyverno"},
]

def verify_all():
    print("Starting Verification of 22 Scenarios...")
    print("="*60)
    
    failed_count = 0
    passed_count = 0

    for scenario in SCENARIOS:
        target_url = f"http://127.0.0.1:{scenario['port']}"
        try:
            module = load_script(scenario['file'])
            result = module.run(target_url)
            
            if result.get("success"):
                print(f"[PASS] {scenario['name']}")
                passed_count += 1
            else:
                print(f"[FAIL] {scenario['name']}") 
                print(f"       Target: {target_url}")
                print(f"       Reason: {result.get('output', 'Unknown')[:100]}...")
                failed_count += 1
        except Exception as e:
            print(f"[ERR ] {scenario['name']} - Exception: {e}")
            failed_count += 1

    print("="*60)
    print(f"Results: {passed_count} Passed, {failed_count} Failed.")
    
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    verify_all()
