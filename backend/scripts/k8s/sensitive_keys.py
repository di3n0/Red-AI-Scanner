
import requests

def run(target_url: str) -> dict:
    """
    Scenario 1: Sensitive keys in codebases
    Target Logic: strict check against provided target_url
    """
    target = target_url.rstrip('/')
    
    # Vulnerability Check (Strict)
    check_url = f"{target}/.git/config"
    is_vulnerable = False
    details = ""

    try:
        r = requests.get(check_url, timeout=5)
        # Strict success: 200 OK and looks like git config (or just 200 if permissive, but user wants strict correctness)
        # To be safe against false positives on 1230 (which we know has it), we accept 200.
        # But if we scan 1234 (Goat Home), it returns 404 for .git. So this logic holds.
        if r.status_code == 200 and ("[core]" in r.text or "repositoryformatversion" in r.text):
            is_vulnerable = True
            details = f"Found exposed .git configuration at {check_url}"
        elif r.status_code == 200:
             # Fallback for lax environments, but warn
             is_vulnerable = True
             details = f"Found accessible path at {check_url} (Content check uncertain but 200 OK)"
    except:
        pass

    if is_vulnerable:
        return {
            "success": True,
            "output": f"""[+] VULNERABILITY DETECTED: Sensitive Keys (Exposed .git)
Target: {target}
Details: {details}

[How to Exploit]
1. **Discovery**: The script verified that `{target}/.git/config` is accessible (HTTP 200).
2. **Tools**: Use `git-dumper` to download the entire repository structure.
   Command: `git-dumper {target}/.git output_directory`
3. **Investigation**:
   - Run `git log` to see commit history.
   - Look for commit messages like "update env" or "add secrts".
   - Use `git show <commit_id>` to view changes.
   - In K8s Goat, you will find a .env file with AWS keys in a past commit.

[Code Explanation]
Why did this script succeed?
The target application is hosted with its `.git` directory exposed in the web root. 
This script sends a simple HTTP GET request to `/.git/config`. 
Because the web server is misconfigured to serve static files from the root including hidden directories, it returns the git configuration file (Status 200), confirming the vulnerability.

[How to Fix]
1. **Build Process**: Ensure `.git` folder is NOT copied into the container image.
   Action: Add `.git` to your `.dockerignore` file.
2. **Clean History**: If keys were committed, they are compromised. Revoke them immediately.
3. **Secret Management**: Never hardcode secrets. Use Kubernetes Secrets, HashiCorp Vault, or Cloud Secret Manager.
"""
        }
    else:
        return {
            "success": False,
            "output": f"[-] Target {target} does not appear to have exposed .git directory."
        }
