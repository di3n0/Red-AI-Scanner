#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root (sudo)"
  exit
fi

echo "[+] Step 1: Installing Nmap..."
apt-get update
apt-get install -y nmap wget unzip curl

echo "[+] Step 2: Installing Nuclei..."
NUCLEI_VERSION=3.3.6
wget -q https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip
unzip -o nuclei_${NUCLEI_VERSION}_linux_amd64.zip
mv nuclei /usr/local/bin/
rm nuclei_${NUCLEI_VERSION}_linux_amd64.zip
echo "Nuclei installed: $(nuclei -version)"

echo "[+] Step 3: Setting up Kubernetes Goat..."
if [ -d "kubernetes-goat" ]; then
    echo "Directory kubernetes-goat already exists, skipping clone."
else
    git clone https://github.com/madhuakula/kubernetes-goat.git
fi

cd kubernetes-goat
chmod +x setup-kubernetes-goat.sh
# Run setup script
bash setup-kubernetes-goat.sh

echo ""
echo "----------------------------------------------------"
echo "✅ Environment Setup Complete!"
echo "----------------------------------------------------"
echo ""
echo "To access Kubernetes Goat applications, run:"
echo "bash kubernetes-goat/access-kubernetes-goat.sh"
echo ""
echo "Access URL: http://127.0.0.1:1234 (Verify exact port in access script output)"
echo "----------------------------------------------------"
