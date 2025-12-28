import subprocess
import json
import shutil
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List

from urllib.parse import urlparse

class ScannerService:
    def __init__(self):
        self.nmap_path = shutil.which("nmap")
        self.nuclei_path = shutil.which("nuclei")
        self.dvwa_creds = ("admin", "password")
        self.current_process = None # Track active process

    def stop_active_scan(self):
        """Stops the currently running scan process if any."""
        if self.current_process:
            try:
                print("[*] Stopping active scan process...")
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                 self.current_process.kill()
            except Exception as e:
                 print(f"[-] Error stopping process: {e}")
            finally:
                 self.current_process = None
            return {"status": "stopped"}
        return {"status": "no_process_running"}

    # ... _login_dvwa skipped for brevity, not changing ...

    def run_nmap_scan(self, target: str) -> Dict[str, Any]:
        if not self.nmap_path:
            return {"error": "Nmap not found"}

        parsed = urlparse(target)
        if not parsed.netloc:
             if "//" not in target:
                 target = "http://" + target
             parsed = urlparse(target)
        nmap_target = parsed.hostname or target
        output_file = f"/tmp/nmap_{nmap_target}_{parsed.port or 'default'}.xml"
        
        command = [self.nmap_path, "-sV", "-F", "-T5", "-n", "--min-rate", "1000", "--open", "-oX", output_file, nmap_target]
        if parsed.port:
             command[2] = "-p"
             command.insert(3, str(parsed.port))
        
        try:
            # Use Popen to track process
            self.current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = self.current_process.communicate(timeout=300)
            
            self.current_process = None # Reset after done

            if self.current_process and self.current_process.returncode != 0:
                 # Check if it was stopped strictly?
                 pass 

            output_content = ""
            if shutil.os.path.exists(output_file):
                 with open(output_file, 'r') as f:
                     output_content = f.read()

            return {"status": "success", "file": output_file, "command": " ".join(command), "output": output_content}
        except subprocess.TimeoutExpired:
            self.stop_active_scan()
            return {"error": "Scan timed out", "status": "failed"}
        except Exception as e:
            self.current_process = None
            return {"error": str(e), "status": "failed"}

    def run_nuclei_scan(self, target: str) -> Dict[str, Any]:
        if not self.nuclei_path:
            return {"error": "Nuclei not found"}
        
        output_file = f"/tmp/nuclei_{target.replace('/', '_').replace(':', '_')}.json"
        
        # Updated command for Nuclei v3+ which uses -json-export for file output
        # -json flag is often for stdout, but -json-export is safer for file writing
        command = [self.nuclei_path, "-u", target, "-json-export", output_file]

        if "dvwa" in target.lower() or "localhost" in target:
            print("[*] Attempting authenicated scan for potential DVWA target...")
            cookies = self._login_dvwa(target)
            if cookies:
                command.extend(["-H", f"Cookie: {cookies}"])
        
        try:
            print(f"[DEBUG] Executing Nuclei command: {' '.join(command)}")
            self.current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = self.current_process.communicate(timeout=600)
            
            if stdout:
                print(f"[DEBUG] Nuclei STDOUT: {stdout.decode()[:500]}...") # Print first 500 chars
            if stderr:
                print(f"[DEBUG] Nuclei STDERR: {stderr.decode()[:500]}...")

            self.current_process = None 

            results = []
            if shutil.os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    # Nuclei JSON export might be a JSON array or JSON Lines. 
                    # v3 usually does JSON array if -json-export is used? Or JSONL?
                    # Let's check the file content structure.
                    # Based on standard usage, it might be JSON list. 
                    # But the previous code assumed JSONL (iterating lines).
                    # Let's try to read as JSON first, then fall back to lines.
                    content = f.read().strip()
                    if content.startswith('[') and content.endswith(']'):
                         results = json.loads(content)
                    else:
                         # Fallback to lines
                         for line in content.splitlines():
                             if line.strip():
                                 try:
                                     results.append(json.loads(line))
                                 except:
                                     pass
            
            return {"status": "success", "findings": results}
        except subprocess.TimeoutExpired:
            self.stop_active_scan()
            return {"error": "Scan timed out", "status": "failed"}
        except Exception as e:
            self.current_process = None
            return {"error": str(e), "status": "failed"}

    def run_zap_scan(self, target: str) -> Dict[str, Any]:
        """
        Runs a ZAP scan (Quick Scan) on the target using the ZAP API.
        Requires ZAP to be running on localhost:8080.
        """
        try:
            from zapv2 import ZAPv2
            # Connect to ZAP - default port 8080
            zap = ZAPv2(apikey='', proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})
            
            # Check if ZAP is available
            try:
                zap.core.version
            except Exception:
                return {"status": "skipped", "message": "ZAP daemon not found on localhost:8080"}

            print(f"[*] Accessing ZAP: {target}")
            zap.urlopen(target)
            
            # Spider
            scan_id = zap.spider.scan(target)
            import time
            time.sleep(5) # Short wait for demo spider
            
            # Active Scan (Quick)
            # Keeping it simple/safe: just return alerts from passive/spider
            alerts = zap.core.alerts(baseurl=target)
            
            return {"status": "success", "findings": alerts}

        except Exception as e:
            return {"status": "failed", "error": str(e)}

scanner = ScannerService()
