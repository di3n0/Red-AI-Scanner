# Side Project 紅隊弱描或測試工具

[TOC]

---
</br></br>
## Brief Introduction
Red-AI-Scanner 是一個透過 AI 驅動的自動化掃描與漏洞驗證工具，整合了 Nmap、Nuclei 等掃描器，並利用 LLM 生成與驗證 Exploit。

</br></br>
## Motivation
鑑於 GB200 算力平台在佈署 Web 管理介面與 Kubernetes 叢集時，常因複雜的配置需求而面臨潛在的安全配置錯誤（Misconfiguration）風險，本專案旨在透過 AI 驅動的自動化掃描與漏洞腳本生成技術，建立一套能快速驗證 AI 基礎設施弱點的紅隊工具。

</br></br>
## Target
- [vulnerables/web-dvwa](https://hub.docker.com/r/vulnerables/web-dvwa)
    ```
    docker run --rm -it -p 80:80 vulnerables/web-dvwa
    ```
- [Kubernets Goat](https://madhuakula.com/kubernetes-goat/docs)
    ```
    git clone https://github.com/madhuakula/kubernetes-goat.git
    cd kubernetes-goat
    chmod +x setup-kubernetes-goat.sh
    bash setup-kubernetes-goat.sh
    ```
- [WebGoat/WebGoat](https://github.com/WebGoat/WebGoat)

## Concept
- [OWASP Top Ten Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- [OWASP Kubernetes Top Ten](https://owasp.org/www-project-kubernetes-top-ten/)



</br></br></br></br>
## Development Tools
- Gemini(Google AI Pro)
- geminicli
- Antigravity

## Environment
OS:	Ubuntu 24.04.2 LTS x86_64
Kernel:	6.14.0-24-generic
CPU: Intel i5-1135G7(2)
Memory:	3867MiB
VMWare Workstation Pro
</br></br></br></br>


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
- Container escape to the host system
- Docker CIS benchmarks analysis
- Kubernetes CIS benchmarks analysis
- Attacking private registry
- NodePort exposed services
- Helm v2 tiller to PwN the cluster - Deprecated
- Analyzing crypto miner container
- Kubernetes namespaces bypass
- Gaining environment information
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

## Docker Build & Run
### Environment
- Backend Port: `8000`
- Frontend Port: `3000`

### Run with Docker Compose
```bash
# 啟動服務 (會自動建立 Image)
sudo docker compose up --build

# 停止服務
sudo docker compose down
```

### Docker Hub
- Backend: `dinosaursmallli/red-ai-backend:v1`
- Frontend: `dinosaursmallli/red-ai-frontend:v1`

```bash
docker pull dinosaursmallli/red-ai-backend:v1
docker pull dinosaursmallli/red-ai-frontend:v1
```
