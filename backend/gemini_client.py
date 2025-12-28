import google.generativeai as genai
import os
import json

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self._configure()

    def update_api_key(self, new_key: str):
        self.api_key = new_key
        self._configure()
        # Update env var for current session
        os.environ["GEMINI_API_KEY"] = new_key
        # Persist to .env file
        self._save_key_to_env(new_key)

    def _save_key_to_env(self, key: str):
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                lines = f.readlines()
        
        # Remove existing key
        lines = [l for l in lines if not l.startswith("GEMINI_API_KEY=")]
        # Add new key
        lines.append(f"GEMINI_API_KEY={key}\n")
        
        with open(env_path, "w") as f:
            f.writelines(lines)

    def _configure(self):
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use gemini-1.5-flash as it is faster and broadly available in free tier
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not set.")

    def get_api_key_masked(self) -> str:
        if not self.api_key:
            return "Not Set"
        if len(self.api_key) < 8:
            return "******"
        return f"{self.api_key[:4]}...{self.api_key[-4:]}"

    def analyze_vulnerability(self, vulnerability_data: dict) -> dict:
        """
        Analyzes a single vulnerability finding and generates a description and patch advice.
        """
        if not self.model:
            # Fallback Logic: robust parsing
            output = vulnerability_data.get("output", "") or vulnerability_data.get("info", "")
            
            response = {
                "severity": "High",
                "description": "Vulnerability identified by automated script.",
                "impact": "Potential system compromise.",
                "patch_advice": "Check vendor documentation.",
                "is_confirmed": True
            }

            # Helper to extract section content
            def extract_section(header, end_marker=None):
                if header not in output: 
                    return None
                try:
                    part = output.split(header)[1]
                    if end_marker and end_marker in part:
                        return part.split(end_marker)[0].strip()
                    # If no end marker is found (or it's the last section), return everything except future tags
                    # A simple heuristic: split by next "[" if it looks like a tag start
                    return part.split("\n[")[0].strip()
                except:
                    return None

            fix = extract_section("[How to Fix]")
            exploit = extract_section("[How to Exploit]")
            explanation = extract_section("[Code Explanation]")

            if fix:
                response["patch_advice"] = fix
            
            impact_text = "Exploitation verified via script.\n"
            if exploit:
                impact_text += f"\n-- Steps --\n{exploit}"
            if explanation:
                impact_text += f"\n\n-- Why it works --\n{explanation}"
            
            if exploit or explanation:
                response["impact"] = impact_text

            # Adjust Description
            script_name = vulnerability_data.get("name", "")
            if script_name:
                response["description"] = f"Automated exploit verified: {script_name}"

            if "SUCCESS" in output or "VULNERABILITY DETECTED" in output or "pass" in output.lower():
                 return response
            
            # If we reached here without returning, maybe just return what we have if it has content
            if fix or exploit:
                return response

            return {"error": "Gemini API key not configured, and no structured output found."}

        prompt = f"""
        You are a Cyber Security Expert. Analyze the following vulnerability finding from a scanner (Nmap/Nuclei):
        {json.dumps(vulnerability_data, indent=2)}

        Provide a structured JSON response with the following fields:
        - "severity": "Level (Low/Medium/High/Critical)"
        - "description": "Concise explanation of the vulnerability"
        - "impact": "What can an attacker do?"
        - "patch_advice": "Step-by-step remediation instructions, specifically for Ubuntu/Linux or Code changes."
        - "is_confirmed": boolean (if the scan result strongly indicates a vulnerability)
        
        Do not include markdown code blocks, just raw JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Cleanup potential markdown formatting in response
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            return {"error": f"Gemini analysis failed: {str(e)}"}

    def generate_poc(self, vulnerability_data: dict, target_url: str) -> dict:
        """
        Generates a Python PoC script to verify the vulnerability.
        """
        if not self.model:
            return {"error": "Gemini API key not configured"}

        prompt = f"""
        You are a Red Team Operator. Write a standalone Python script to verify the following vulnerability:
        Target: {target_url}
        Vulnerability Data: {json.dumps(vulnerability_data, indent=2)}
        
        IMPORTANT:
        - If the target is DVWA based on the URL or name, use the following credentials for login/authentication:
          Username: admin
          Password: password
          Login URL: {target_url.rstrip('/')}/login.php
          (You must handle CSRF token 'user_token' during login if required, and set 'security' cookie to 'low')
        - This script must perform the login first, capture the session, and then exploit the vulnerability.

        The script must:
        1. Be self-contained (only use requests, sys, re, standard libs, bs4).
        2. Attempt to exploit or trigger the vulnerability safely (proof of concept).
        3. Print "[+] VULNERABILITY CONFIRMED" to stdout if successful.
        4. Print "[-] VULNERABILITY NOT FOUND" or "[-] EXPLOIT FAILED" if unsuccessful.
        5. Exit with code 0.

        Output ONLY the python code. No usage instructions.
        """
        
        try:
            response = self.model.generate_content(prompt)
            code = response.text.replace("```python", "").replace("```", "").strip()
            return {"poc_code": code}
        except Exception as e:
            return {"error": f"PoC generation failed: {str(e)}"}

    def generate_exploit_from_url(self, script_url: str, content: str) -> dict:
        """
        Generates a Python Exploit script based on the content of a referenced script URL.
        """
        if not self.model:
            return {"error": "Gemini API key not configured"}

        prompt = f"""
        You are a Red Team Operator. I have found a reference script or tutorial at: {script_url}
        Content:
        {content[:10000]} # Truncate to avoid limit
        
        Create a functional Python Exploit Script based on this content. 
        The script should be designed to run against a target URL provided as a command line argument or variable.
        Assume standard DVWA/Web targets.
        
        The script must:
        1. Be standalone Python.
        2. Accept target URL via variable 'TARGET_URL' at top of script (I will inject it later) or sys.argv.
        3. Print "[+] SUCCESS" if the exploit works.
        4. Print "[-] FAILED" if it fails.
        
        Output ONLY the python code.
        """
        
        try:
            response = self.model.generate_content(prompt)
            code = response.text.replace("```python", "").replace("```", "").strip()
            return {"code": code}
        except Exception as e:
            return {"error": f"Exploit generation failed: {str(e)}"}

gemini_client = GeminiClient()
