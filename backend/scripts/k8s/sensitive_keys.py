
import requests
import time

def run(target_url: str) -> dict:
    """
    Scenario 1: Sensitive keys in codebases
    Target Logic: strict check against provided target_url
    """
    target = target_url.rstrip('/')
    
    # helper: detect if we are in docker and target is localhost, try gateway
    def get_accessible_target(t):
        if "127.0.0.1" in t or "localhost" in t:
            # Try original
            try:
                requests.get(t, timeout=2)
                return t
            except:
                # Try Gateway
                t_alt = t.replace("127.0.0.1", "172.17.0.1").replace("localhost", "172.17.0.1")
                try:
                    requests.get(t_alt, timeout=2)
                    return t_alt
                except:
                    return t
        return t

    target = get_accessible_target(target)
    
    # Check 1: Direct .env access
    env_url = f"{target}/.env"
    env_exposed = False
    env_content = ""
    
    # Retry logic for robustness
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            r_env = requests.get(env_url, timeout=5)
            if r_env.status_code == 200 and ("=" in r_env.text or "AWS" in r_env.text or "KEY" in r_env.text):
                env_exposed = True
                env_content = r_env.text
                break
        except Exception:
            time.sleep(1)
            pass

    # Check 2: Exposed .git directory
    git_url = f"{target}/.git/config"
    git_exposed = False
    details = ""
    last_status = "N/A"
    preview = ""

    for attempt in range(max_retries):
        try:
            r = requests.get(git_url, timeout=5)
            last_status = str(r.status_code)
            preview = r.text[:50] if r.text else "Empty"
            
            if r.status_code == 200 and ("[core]" in r.text or "repositoryformatversion" in r.text):
                git_exposed = True
                details = f"Found exposed .git configuration at {git_url}"
                break
            elif r.status_code == 200 and not env_exposed: 
                 # Fallback for lax environments, but warn
                 # If we see 200 but not obvious git config, it might be a false positive or custom page.
                 # We'll valid if text is effectively what we saw in curl: "[core]"
                 # If not found, we won't claim success unless strictly matching to avoid noise.
                 pass
        except Exception as e:
            last_status = f"Error: {str(e)}"
            time.sleep(1)

    if env_exposed:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Sensitive Keys (Direct .env Access)
Target: {target}
[CRITICAL] Found .env file directly accessible!
Content Preview:
{env_content[:200]}...
"""
        }
    elif git_exposed:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Sensitive Keys (Exposed .git)
Target: {target}
Details: {details}
Preview: {preview}

[How to Exploit]
1. Use `git-dumper` to download: `git-dumper {target}/.git output_dir`
2. Check `git log` and diffs for secrets.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} failed. .git/config Status: {last_status}, Content Preview: '{preview}'"
        }
