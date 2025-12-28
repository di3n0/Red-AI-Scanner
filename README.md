# Side Project 紅隊弱描或測試工具

- [操作界面簡介](https://hackmd.io/@dinosaur/rJqg2XFQWl)

</br></br>

## Brief Introduction
Red-AI-Scanner 是一個自動化掃描與漏洞驗證工具，整合了 Nmap、Nuclei 等掃描器，並利用 LLM 生成與驗證 Exploit。

## Motivation
鑑於 GB200 算力平台在佈署 Web 管理介面與 Kubernetes 叢集時，常因複雜的配置需求而面臨潛在的安全配置錯誤（Misconfiguration）風險，本專案旨在透過自動化掃描與漏洞腳本生成技術，建立一套能快速驗證 AI 基礎設施弱點的紅隊工具。

## Concept
- [OWASP Kubernetes Top Ten](https://owasp.org/www-project-kubernetes-top-ten/)

</br></br>

## System Architecture

此專案採用 **前後端分離 (Decoupled Architecture)** 架構，確保系統的擴展性與維護性。

### 💻 Frontend (Client Side)
負責提供使用者互動介面、視覺化掃描結果與操作控制。
*   **Framework**: [Next.js 16](https://nextjs.org/) (App Router 架構)
*   **Language**: TypeScript / React
*   **Styling**: [Tailwind CSS](https://tailwindcss.com/) (現代化 Utility-first CSS)
*   **Container**: `node:20-alpine`
*   **Key Features**:
    *   **Dashboard**: 即時監控掃描進度與顯示 Nmap/Nuclei JSON 結果。
    *   **Exploit Generator**: 介接 API 觸發 AI 生成攻擊腳本。
    *   **Responsive UI**: 適應不同裝置的操作介面。

### ⚙️ Backend (Server Side)
負責核心邏輯處理、調度資安工具與 AI 模型串接。
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10)
*   **Security Tools**:
    *   **Nmap**: 負責網路探測與 Port Scanning。
    *   **Nuclei**: 負責基於 Template 的漏洞掃描 (使用 `-json-export` 輸出)。
*   **AI Engine**:
    *   **LLM Connectivity**: 整合 Groq (Llama-3.3) 或 Google Gemini API。
    *   **Code Generation**: 將漏洞特徵 (CVE/Misconfiguration) 轉換為 Python PoC 腳本。
*   **Task Management**: 使用 `subprocess` 與 `asyncio` 進行非同步掃描任務管理。
*   **Container**: `python:3.10-slim`

### 🐳 Infrastructure
*   **Docker Compose**: 透過 `docker-compose.yml` 編排前後端服務。
*   **Networking**: 建立內部虛擬網路，讓 Frontend 直接透過 `http://backend:8000` (或 client-side 的 `localhost:8000`) 進行通訊。

</br></br>

## Development Tools
- Gemini(Google AI Pro)
- geminicli
- Antigravity

## Environment
- OS: Ubuntu 24.04.2 LTS x86_64
- Kernel: 6.14.0-24-generic
- CPU: Intel i5-1135G7(2)
- Memory: 3867MiB
- VMWare Workstation Pro
</br></br>

### Step
#### Environment => Gemini CLI
```
sudo gedit GEMINI.md
gemini
/memory add GEMINI.md
/memory show
```
<details>
<summary>Prompt Template 1</summary>

撰寫建置Kubernets Goat環境與安裝NMAP與Nuclei。
完成後給予環境的網址。
```
git clone https://github.com/madhuakula/kubernetes-goat.git
cd kubernetes-goat
chmod +x setup-kubernetes-goat.sh
bash setup-kubernetes-goat.sh
```
</details>

#### 建置專案 => Antigravity
<details>
<summary>Prompt Template 2</summary>

Role: 你是一位資深資安研究員與 Python 開發專家。
Objective: 協助我開發一個名為 "Red-AI-Scanner" 的 Side Project。這是一個建置在 Ubuntu 上的自動化紅隊弱描工具，核心功能是整合掃描結果並利用 Gemini API 生成一鍵執行的漏洞驗證PoC與修補腳本。
Project Context:
靶機K8S Goat專注於 Kubernetes 配置錯誤與容器逃逸。
技術背景： 此專案特別關注 GB200 算力平台 在部署時可能遇到的 Web 管理介面漏洞與 K8S Misconfiguration。

Requirements:
前端使用Next.js。前端要先顯示靶機Kubernets Goat的網址。前端共有兩個可以輸入的網址框。前端第一個框可以輸入網址，對於選擇顯示攻擊目標網址，再開始使用NMAP與Nuclei對選擇目標進行掃描，將結果輸出為 JSON。掃描完可以選擇以下Kubernets Goat的腳本進行攻擊，或者選擇一鍵完成所有腳本測試。驗證攻擊項目是否成功，成功請打勾失敗則打叉。並進行最後統整針對平台環境的修補建議。
前端第二個框輸入腳本網址。將網址的腳本傳給Gemini撰寫Exploit Script，作為以後做完攻擊目標網址後可以選擇的腳本。
根據report資料夾中的1至22.pdf撰寫Kubernets Goat攻擊腳本。

攻擊腳本分類：
Kubernets Goat
- Sensitive keys in codebases
- DIND (docker-in-docker) exploitation
- SSRF in the Kubernetes (K8S) world
- DoS the Memory/CPU resources
- Hacker container preview
- Hidden in layers
- RBAC least privileges misconfiguration
- KubeAudit - Audit Kubernetes clusters
- Falco - Runtime security monitoring & detection
- Popeye - A Kubernetes cluster sanitizer
- Secure Network Boundaries using NSP
- Cilium Tetragon - eBPF-based Security Observability and Runtime Enforcement
- Securing Kubernetes Clusters using Kyverno Policy Engine
</details>

- [Write-up](https://madhuakula.com/kubernetes-goat/docs/scenarios/)

</br></br>

## Docker 
### Environment
- Backend Port: `8000`
- Frontend Port: `3000`

### Docker Hub
- Backend: `dinosaursmallli/red-ai-backend:v1`
- Frontend: `dinosaursmallli/red-ai-frontend:v1`

```bash
sudo docker pull dinosaursmallli/red-ai-backend:v1
sudo docker pull dinosaursmallli/red-ai-frontend:v1
```

</br></br>

## Reference
- [Gemini CLI Document](https://geminicli.com/docs/)
- [Gemini CLI 文件](https://gemini-cli.gh.miniasp.com/)
- [Youtube|Gemini CLI 教學](https://youtu.be/UfrXGfivlEQ?si=utRH06efmRpoQAhW)
- [Youtube|Google Antigravity 教學](https://www.youtube.com/watch?v=-FW5DgQEV0M)
- [手把手教你：申請免費Google Gemini API](https://lifecheatslab.com/freegeminiapi/#%E7%94%B3%E8%AB%8B%E5%85%8D%E8%B2%BB_Google_Gemini_API_%E9%9C%80%E8%A6%81%E4%BB%80%E9%BA%BC)
- [Node.js Install](https://nodejs.org/zh-tw/download)
    ``` bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    \. "$HOME/.nvm/nvm.sh"  # 不想重新啟動 shell 
    nvm install 24  # 下載並安裝 Node.js
    node -v # Should print "v24.12.0".
    ```
- [GitHub|google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
    ```
    npm install -g @google/gemini-cli
    ```
- [Google Download Antigravity](https://antigravity.google/download)
    ```
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | \
    sudo gpg --dearmor --yes -o /etc/apt/keyrings/antigravity-repo-key.gpg
    echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | \
    sudo tee /etc/apt/sources.list.d/antigravity.list > /dev/null

    sudo apt update
    sudo apt install antigravity
    ```


## Script Success Verification Criteria (通關判斷標準)

本專案 22 個紅隊攻擊腳本經過 Refactor 後，針對每個場景實作了基於 Report 的精確驗證邏輯。判定「成功 (Success)」代表該漏洞環境已被確認存在或已成功利用。

### 1. 主動式漏洞利用 (Active Exploitation)
針對 Web 服務直接發送攻擊 Payload 進行驗證。

| Scenario | Script | Target Port | Success Criteria (驗證標準) |
| :--- | :--- | :--- | :--- |
| **1. Sensitive Keys** | `sensitive_keys.py` | `1230` | 發現 `/.env` 檔案或 `/.git` 目錄外洩 (HTTP 200)。 |
| **2. DIND Exploitation** | `dind_exploitation.py` | `1231` | 成功執行 Command Injection (`id`) 並回傳結果。 |
| **3. SSRF** | `ssrf_k8s.py` | `1232` | 成功存取 `metadata-db` 並解碼 Base64 取得 Flag (`k8s-goat-...`)。 |
| **4. Container Escape** | `container_escape.py` | `1233` | 偵測到曝露的 Web Shell (`GoTTY` / `system-monitor`)。 |
| **7. Private Registry** | `private_registry.py` | `1235` | 成功呼叫 Docker Registry API (`/v2/_catalog`) 取得儲存庫列表。 |
| **13. DoS Resources** | `dos_resources.py` | `1236` | 偵測到 Deployment Manifest 未設定 `resources.limits` (透過 `kubectl`)。 |

### 2. 環境配置與服務檢測 (Configuration & Resource Discovery)
針對基礎設施層面的弱點，使用 `kubectl` 驗證特定危險元件或配置是否存在。

| Scenario | Script | Verification Method | Success Criteria (驗證標準) |
| :--- | :--- | :--- | :--- |
| **5. Docker CIS** | `docker_cis.py` | `kubectl` | 偵測到 `docker-bench-security` Pod 正在運作。 |
| **6. K8s CIS** | `k8s_cis.py` | `kubectl` | 偵測到 `kube-bench` Job 存在。 |
| **8. NodePort Services** | `nodeport_services.py` | `kubectl` | 偵測到類型為 `NodePort` 的 Service。 |
| **9. Helm v2** | `helm_v2.py` | `kubectl` | 偵測到 `tiller-deploy` Service (Helm v2 Server)。 |
| **10. Crypto Miner** | `crypto_miner.py` | `kubectl` | 偵測到挖礦相關 Job (`batch-check-job`)。 |
| **11. Namespace Bypass** | `namespace_bypass.py` | `kubectl` | 在其他 Namespace 發現未隔離的 `cache-store` Pod。 |
| **12. Env Info** | `env_info.py` | `kubectl` | 成功讀取 Pod 環境變數 (`printenv`)。 |
| **14. Hacker Container** | `hacker_container.py` | `kubectl` | 偵測到駭客容器 (`hacker-container` Pod) 存在。 |
| **15. Hidden Layers** | `hidden_layers.py` | `kubectl` | 偵測到含有隱藏資訊的 Job (`hidden-in-layers`)。 |
| **16. RBAC Misconfig** | `rbac_misconfig.py` | `kubectl` | 偵測到高權限 ServiceAccount (`webhook-service-account`)。 |
| **17. KubeAudit** | `kubeaudit.py` | Manual Guide | 輸出 KubeAudit 執行指引 (需互動式操作)。 |
| **18. Falco** | `falco.py` | `kubectl` | 偵測到 `falco` 資安監控 Pod。 |
| **19. Popeye** | `popeye.py` | Manual Guide | 輸出 Popeye 執行指引 (需互動式操作)。 |
| **20. NSP Boundary** | `nsp_boundary.py` | `kubectl` | 確認叢集內是否存在 NetworkPolicies (驗證隔離狀態)。 |
| **21. Tetragon** | `tetragon.py` | `kubectl` | 偵測到 `tetragon` eBPF 監控 Pod。 |
| **22. Kyverno** | `kyverno.py` | `kubectl` | 偵測到 Kyverno ClusterPolicies。 |