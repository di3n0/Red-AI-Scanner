import requests
import os
import json
from dotenv import load_dotenv

class GroqClient:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        
    def update_api_key(self, new_key: str):
        self.api_key = new_key
        # Update env var
        os.environ["GROQ_API_KEY"] = new_key
        self._save_key_to_env(new_key)

    def get_api_key_masked(self) -> str:
        if not self.api_key:
            return "Not Set"
        if len(self.api_key) < 8:
            return "******"
        return f"{self.api_key[:4]}...{self.api_key[-4:]}"

    def _save_key_to_env(self, key: str):
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                lines = f.readlines()
        
        # Remove existing key
        lines = [l for l in lines if not l.startswith("GROQ_API_KEY=")]
        # Add new key
        lines.append(f"GROQ_API_KEY={key}\n")
        
        with open(env_path, "w") as f:
            f.writelines(lines)

    def _query(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            try:
                return response.json()
            except:
                return {"error": f"Invalid JSON. Status: {response.status_code}. Body: {response.text[:200]}"}
        except Exception as e:
            return {"error": str(e)}

    def analyze_vulnerability(self, vulnerability_data: dict) -> dict:
        """
        Analyzes a single vulnerability finding.
        """
        raw_output = vulnerability_data.get("output", "") or vulnerability_data.get("info", "")
        
        system_prompt = """You are a cybersecurity expert. Analyze the following vulnerability scan output.
Provide a JSON response with the following fields:
- severity: (High/Medium/Low)
- description: (Short summary)
- impact: (What can an attacker do?)
- patch_advice: (How to fix it?)"""

        user_prompt = f"Scan Output:\n{raw_output[:2000]}\n\nRespond ONLY with valid JSON."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._query(messages)
        
        # Simple fallback parsing
        default_res = {
            "severity": "Unknown",
            "description": "Analysis failed or model unavailable.",
            "impact": "Unknown",
            "patch_advice": "Check manual verification.",
        }
        
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            try:
                # Try to extract JSON
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != -1:
                    data = json.loads(content[start:end])
                    return {**default_res, **data}
            except:
                pass
        
        return default_res

    def generate_exploit_from_url(self, script_url: str, content: str) -> dict:
        """
        Generates a Python exploit script.
        """
        system_prompt = """You are an expert Offensive Security Engineer and Python Developer.
Your task is to convert the provided vulnerability information into a robust, standalone Python PoC (Proof of Concept) script.

STRICT REQUIREMENTS:
1. The script MUST be valid Python 3 code.
2. The script MUST import all necessary libraries (e.g. `requests`, `json`, `sys`).
3. The script MUST define a function with the exact signature: `def run(target_url: str) -> dict:`
4. The `run` function MUST return a dictionary with exactly two keys:
   - "success": boolean (True if vulnerability is confirmed/exploited, False otherwise)
   - "output": string (A detailed report including vulnerability name, target, exploit steps taken, and mitigation advice).
5. Do NOT use `input()` or interactive commands.
6. The script should be robust against network errors (use try/except).
7. Return ONLY the Python code. Wrap it in ```python``` blocks.

Example Structure:
```python
import requests

def run(target_url: str) -> dict:
    try:
        # validation logic here
        if vulnerabilities_found:
            return {"success": True, "output": "...details..."}
    except Exception as e:
        return {"success": False, "output": f"Error: {e}"}
    return {"success": False, "output": "Not vulnerable"}
```
"""
        user_prompt = f"Source info from {script_url}:\n{content[:3000]}\n\nGenerate the Python code now. Wrap code in ```python blocks."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._query(messages)
        
        if isinstance(response, dict) and "error" in response:
             return {"error": response["error"]}

        generated_text = ""
        if "choices" in response and len(response["choices"]) > 0:
            generated_text = response["choices"][0]["message"]["content"]
        
        # Extract Code
        code = ""
        if "```python" in generated_text:
            code = generated_text.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_text:
            code = generated_text.split("```")[1].split("```")[0].strip()
        else:
            code = "# Could not extract code block.\n# Raw Output:\n" + generated_text
            
        return {"code": code}

    def generate_poc(self, vulnerability_data: dict, target_url: str) -> dict:
        return {"code": "# Feature migrated to Script Import workflow."}

# Singleton
ai_client = GroqClient()
