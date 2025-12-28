
import requests
import json

API_BASE = "http://localhost:8000"

def get_k8s_goat_ids():
    try:
        r = requests.get(f"{API_BASE}/attacks")
        r.raise_for_status()
        data = r.json()
        return [item['id'] for item in data.get('k8s_goat', [])]
    except:
        return []

def run_strict_check():
    ids = get_k8s_goat_ids()
    target = "http://127.0.0.1:1230"
    
    print(f"[*] Testing STRICT mode against {target}...")
    print(f"{'SCENARIO ID':<40} | {'STATUS':<10} | {'EXPECTED'}")
    print("-" * 100)
    
    for attack_id in ids:
        try:
            payload = {"attack_id": attack_id, "target_url": target}
            r = requests.post(f"{API_BASE}/attack/run", json=payload, timeout=5)
            result = r.json()
            is_success = result.get('success', False)
            status = "PASS" if is_success else "FAIL"
            
            # Sensitive Keys should PASS
            expected = "PASS" if "sensitive_keys" in attack_id else "FAIL"
            color = ""
            if status == expected:
                color = " (OK)"
            else:
                color = " (UNEXPECTED)"
                
            print(f"{attack_id:<40} | {status:<10} | {expected:<10}{color}")
            
        except Exception as e:
            print(f"{attack_id:<40} | ERROR      | {str(e)}")

if __name__ == "__main__":
    run_strict_check()
