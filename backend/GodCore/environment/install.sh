#!/usr/bin/env zsh

set -eu

ENV_NAME="runmistral"

if ! command -v conda &>/dev/null; then
    echo "[ERROR] conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

echo "\n[*] Checking if conda env '$ENV_NAME' exists..."
if conda info --envs | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    echo "[*] Conda env '$ENV_NAME' already exists. Activating and upgrading packages..."
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate $ENV_NAME
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
else
    echo "[*] Conda env '$ENV_NAME' not found. Creating from conda_env.yml..."
    conda env create -f conda_env.yml
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate $ENV_NAME
fi

# --- REMOVE ALL SYSTEM CUDA TOOLKIT (APT) ---
echo "[*] Removing ALL system CUDA from apt (if any present, may take 2 min)..."

sudo apt-get remove --purge -y '^cuda.*' nvidia-cuda-toolkit nvidia-cuda-dev || true
sudo apt-get autoremove -y
sudo apt-get update

# --- REQUIRED SYSTEM LIBS ---
echo "[*] Installing build-essential and python3-dev..."
sudo apt-get install -y build-essential python3-dev

# --- ENSURE CUDA TOOLKIT IS PRESENT ---
if [ ! -x /usr/local/cuda-12.4/bin/nvcc ]; then
    echo "[ERROR] /usr/local/cuda-12.4/bin/nvcc not found! Install official NVIDIA CUDA 12.4 toolkit first!"
    exit 99
fi

export CUDA_HOME=/usr/local/cuda-12.4
export PATH=/usr/local/cuda-12.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH

echo "[*] CUDA version:"
nvcc --version

# --- Download Mistral-13B Model if missing ---
MODEL_DIR="/path/to/GodCore/models/Mistral-13B-Instruct"
MODEL_PATH="$MODEL_DIR/mistral-13b-instruct-v0.1.Q5_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/Mistral-13B-Instruct-v0.1-GGUF/resolve/main/mistral-13b-instruct-v0.1.Q5_K_M.gguf"

echo "[*] Checking for Mistral-13B model..."
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_PATH" ]; then
    echo "[*] Downloading Mistral-13B-Instruct Q5_K_M GGUF model..."
    curl -L --output "$MODEL_PATH" "$MODEL_URL" || { echo "Model download failed!"; exit 2; }
    echo "[*] Model downloaded to $MODEL_PATH"
else
    echo "[*] Model already exists at $MODEL_PATH"
fi

# --- Install/Upgrade GPU PyTorch stack (PIP ONLY) ---
pip install torch==2.2.2+cu121 torchvision==0.17.2+cu121 torchaudio==2.2.2+cu121 --index-url https://download.pytorch.org/whl/cu121

# --- Build llama-cpp-python from local source with GGML_CUDA+LLaVA ---
cd ../llama-cpp-python

[ ! -f README.md ] && touch README.md

if [ -f pyproject.toml ]; then
    echo "[*] Uninstalling previous llama-cpp-python wheel (if any)..."
    pip uninstall llama-cpp-python -y || true
    rm -rf build/ dist/ llama_cpp_python.egg-info/
    export CUDA_HOME=/usr/local/cuda-12.4
    export PATH=/usr/local/cuda-12.4/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH
    echo "[*] Building llama-cpp-python with GGML_CUDA=on..."
    CMAKE_ARGS="-DGGML_CUDA=on -DLLAVA_BUILD=on -DCMAKE_CUDA_ARCHITECTURES=86" pip install . --force-reinstall --no-cache-dir
    echo "[*] Wheel built, testing system info:"
    python -c "from llama_cpp import llama_print_system_info; llama_print_system_info()"
else
    echo "[ERROR] No pyproject.toml in $(pwd). Are you in the llama-cpp-python source directory?"
    exit 1
fi

cd ../frontend

if ! command -v npm &>/dev/null; then
    echo "[ERROR] npm not found. Please install Node.js and npm."
    exit 1
fi

npm install

conda install -c conda-forge gxx -y # installs latest GCC toolchain (may be called gxx_linux-64)
conda install -c conda-forge libstdcxx-ng=13.2.0 -y
conda install -c conda-forge gcc=13.2.0 gxx=13.2.0 -y

# Remove any broken conda libstdc++ copy (will re-link)
rm -f $CONDA_PREFIX/lib/libstdc++.so.*

# Link system libstdc++.so.6 into the env
ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6 $CONDA_PREFIX/lib/libstdc++.so.6

# Confirm link
ls -l $CONDA_PREFIX/lib/libstdc++.so.6

pip install pyngrok fastapi uvicorn

sudo apt install qrencode

npm install --save-dev cross-env

sudo apt install libgtk-3-bin

conda deactivate

echo "\n[*] Install complete. Activate with: conda activate $ENV_NAME"
