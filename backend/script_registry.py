
import os
import importlib.util
import sys
from typing import List, Dict, Optional

class ScriptRegistry:
    def __init__(self):
        self.scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
        self.scripts = {
            "k8s_goat": [],
            "custom": []
        }
        self._load_scripts()

    def _load_scripts(self):
        """
        Dynamically loads scripts from the backend/scripts directory.
        """
        # Load K8s Scripts
        k8s_path = os.path.join(self.scripts_dir, "k8s")
        if os.path.exists(k8s_path):
            self.scripts["k8s_goat"] = self._scan_directory(k8s_path, "k8s_goat")



    def _get_k8s_name_mapping(self) -> Dict[str, str]:
        return {
            "sensitive_keys.py": "Sensitive keys in codebases",
            "dind_exploitation.py": "DIND (docker-in-docker) exploitation",
            "ssrf_k8s.py": "SSRF in the Kubernetes (K8S) world",
            "container_escape.py": "Container escape to the host system",
            "docker_cis.py": "Docker CIS benchmarks analysis",
            "k8s_cis.py": "Kubernetes CIS benchmarks analysis",
            "private_registry.py": "Attacking private registry",
            "nodeport_services.py": "NodePort exposed services",
            "helm_v2.py": "Helm v2 tiller to PwN the cluster - Deprecated",
            "crypto_miner.py": "Analyzing crypto miner container",
            "namespace_bypass.py": "Kubernetes namespaces bypass",
            "env_info.py": "Gaining environment information",
            "dos_resources.py": "DoS the Memory/CPU resources",
            "hacker_container.py": "Hacker container preview",
            "hidden_layers.py": "Hidden in layers",
            "rbac_misconfig.py": "RBAC least privileges misconfiguration",
            "kubeaudit.py": "KubeAudit - Audit Kubernetes clusters",
            "falco.py": "Falco - Runtime security monitoring & detection",
            "popeye.py": "Popeye - A Kubernetes cluster sanitizer",
            "nsp_boundary.py": "Secure Network Boundaries using NSP",
            "tetragon.py": "Cilium Tetragon - eBPF-based Security Observability and Runtime Enforcement",
            "kyverno.py": "Securing Kubernetes Clusters using Kyverno Policy Engine"
        }

    def _scan_directory(self, path: str, category_key: str) -> List[Dict]:
        results = []
        name_map = {}
        if category_key == "k8s_goat":
            name_map = self._get_k8s_name_mapping()

        for filename in os.listdir(path):
            if filename.endswith(".py") and filename != "__init__.py":
                
                # Use mapped name if available, else prettify filename
                if filename in name_map:
                    name_human = name_map[filename]
                else:
                    name_human = filename.replace(".py", "").replace("_", " ").title()
                
                script_id = f"{category_key}_{filename.replace('.py', '')}"
                
                # Check for description docstring
                file_path = os.path.join(path, filename)
                description = "No description available."
                try:
                    with open(file_path, "r") as f:
                        content = f.read()
                        # Very basic docstring extraction
                        if '"""' in content:
                           parts = content.split('"""')
                           if len(parts) >= 3:
                               description = parts[1].strip()
                except:
                    pass

                results.append({
                    "id": script_id,
                    "name": name_human,
                    "category": category_key.upper().replace("_", " "),
                    "description": description,
                    "file_path": file_path
                })
        # Sort by Name for easier checking
        results.sort(key=lambda x: x['name'])
        return results

    def get_all_scripts(self) -> Dict[str, List[Dict]]:
        # Refresh potentially? For now static after init
        return self.scripts

    def add_custom_script(self, name: str, code: str, source_url: str):
        script_id = f"custom_{len(self.scripts['custom']) + 1}"
        entry = {
            "id": script_id,
            "name": name,
            "category": "Custom",
            "description": f"Imported from {source_url}",
            "code": code,
            "source_url": source_url
        }
        self.scripts["custom"].append(entry)
        return entry

    def get_script_code(self, script_id: str) -> Optional[str]:
        # Check custom first
        for s in self.scripts["custom"]:
            if s["id"] == script_id:
                return s.get("code")
        
        # Check file-based
        for category in ["k8s_goat"]:
            for s in self.scripts[category]:
                if s["id"] == script_id:
                    path = s.get("file_path")
                    if path and os.path.exists(path):
                        with open(path, "r") as f:
                            return f.read()
        return None

registry = ScriptRegistry()
