#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo ""
    echo "Stopping Red-AI-Scanner..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Progress Bar Function
# Usage: progress_bar <percentage> <message>
progress_bar() {
    local width=40
    local percent=$1
    local message=$2
    local filled=$(($width * $percent / 100))
    local empty=$(($width - $filled))
    
    # Create the bar string, e.g., "####      "
    local bar=$(printf "%0.s#" $(seq 1 $filled))
    local pad=$(printf "%0.s " $(seq 1 $empty))
    
    # Print the bar: \r returns to start of line to overwrite
    printf "\r[%s%s] %3d%% - %s" "$bar" "$pad" "$percent" "$message"
}

# Initial State
progress_bar 0 "Initializing..."

# --- Step 1: Cleanup ---
# Kill anything running on port 8000 (Backend) and 3000 (Frontend)
fuser -k 8000/tcp 2>/dev/null
fuser -k 3000/tcp 2>/dev/null
pkill -f "python3 main.py" 2>/dev/null
pkill -f "next-server" 2>/dev/null
pkill -f "kubectl port-forward" 2>/dev/null

progress_bar 10 "Cleaning up old processes..."
sleep 0.5

# --- Step 2: K8s Goat Setup ---
progress_bar 20 "Starting K8s Goat Environment..."
if [ -f "kubernetes-goat/access-kubernetes-goat.sh" ]; then
    bash kubernetes-goat/access-kubernetes-goat.sh > /dev/null 2>&1 &
    GOAT_PID=$!
    echo ""
    echo "[*] K8s Goat is running in background (PID: $GOAT_PID)"
else
    echo ""
    echo "[!] Warning: K8s Goat script not found!"
fi

# --- Step 3: Backend Setup ---
# echo "[*] Setting up Backend..."
cd backend

# Create venv if not exists
if [ ! -d "venv" ]; then
    progress_bar 15 "Creating Python venv..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies major step
progress_bar 30 "Installing Backend deps..."
pip install -r requirements.txt > /dev/null 2>&1

progress_bar 50 "Starting Backend Server..."
python main.py > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..

# --- Step 3: Frontend Setup ---
progress_bar 60 "Checking Frontend..."
cd frontend
# Ensure dependencies are installed (fast check)
if [ ! -d "node_modules" ]; then
    progress_bar 65 "Installing Frontend deps (First run)..."
    npm install > /dev/null 2>&1
fi

progress_bar 85 "Launching Next.js..."
npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!
cd ..

# Finalize
progress_bar 100 "Startup Complete!"
echo ""


echo "------------------------------------------------"
echo "The project is ready."
echo "✅ System Running!"
echo "➡️  Frontend Console: http://localhost:3000"
echo "➡️  Backend API:      http://localhost:8000/docs"
echo "------------------------------------------------"
echo "Press Ctrl+C to stop all services."

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
