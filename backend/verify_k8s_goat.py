
import requests
import json
import time

API_BASE = "http://localhost:8000"

def get_k8s_goat_ids():
    try:
        r = requests.get(f"{API_BASE}/attacks")
        r.raise_for_status()
        data = r.json()
        return [item['id'] for item in data.get('k8s_goat', [])]
    except Exception as e:
        print(f"[-] Failed to fetch attack list: {e}")
        return []

def run_verification():
    ids = get_k8s_goat_ids()
    if not ids:
        print("[-] No K8S Goat scripts found.")
        return

    print(f"[*] Starting verification for {len(ids)} K8S Goat scenarios...")
    print(f"{'SCENARIO ID':<40} | {'STATUS':<10} | {'MESSAGE'}")
    print("-" * 100)

    success_count = 0
    results = []

    for attack_id in ids:
        try:
            # We assume target_url http://127.0.0.1 is fine as scripts have hardcoded ports or logic
            payload = {
                "attack_id": attack_id,
                "target_url": "http://127.0.0.1"
            }
            r = requests.post(f"{API_BASE}/attack/run", json=payload, timeout=35)
            r.raise_for_status()
            result = r.json()
            
            is_success = result.get('success', False)
            status_str = "PASS" if is_success else "FAIL"
            
            # Simple message extraction (first line of output)
            output = result.get('output', '').strip().split('\n')[0]
            if len(output) > 50: output = output[:47] + "..."
            
            print(f"{attack_id:<40} | {status_str:<10} | {output}")
            
            if is_success:
                success_count += 1
            else:
                # Print full output for failure debugging
                print(f"    [!] FAILURE OUTPUT: {result.get('output')}")
            
            results.append((attack_id, is_success))
            
        except Exception as e:
            print(f"{attack_id:<40} | ERROR      | {str(e)}")
            results.append((attack_id, False))

    print("-" * 100)
    print(f"[*] Verification Complete. Success: {success_count}/{len(ids)}")
    
    if success_count == len(ids):
        print("\n[+] ALL SCENARIOS VERIFIED SUCCESSFULLY!")
    else:
        print("\n[!] SOME SCENARIOS FAILED. PLEASE CHECK LOGS.")

if __name__ == "__main__":
    run_verification()
