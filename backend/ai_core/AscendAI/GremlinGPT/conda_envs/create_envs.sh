#!/bin/zsh

echo "[GremlinGPT] Creating conda environments..."

cd "$(dirname "$0")" # Always run from conda_envs/

ENV_NAMES=(
  "gremlin-nlp"
  "gremlin-dashboard"
  "gremlin-scraper"
  "gremlin-memory"
  "gremlin-orchestrator"
)

for ENV in "${ENV_NAMES[@]}"; do
  YAML_FILE="${ENV}.yml"
  REQ_FILE="${ENV}.txt"

  echo "[INFO] Checking environment: $ENV"

  if conda info --envs | awk '{print $1}' | grep -qx "$ENV"; then
    echo "[SKIP] Environment '$ENV' already exists."
    continue
  fi

  if [ ! -f "$YAML_FILE" ]; then
    echo "[ERROR] YAML file '$YAML_FILE' not found. Skipping '$ENV'."
    continue
  fi

  echo "[CREATE] Creating '$ENV' from '$YAML_FILE'..."
  conda env create -f "$YAML_FILE"
  if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create environment: $ENV"
    exit 1
  fi

  if [ -f "$REQ_FILE" ]; then
    echo "[PIP] Installing pip requirements for $ENV from $REQ_FILE..."
    conda run -n "$ENV" pip install -r "$REQ_FILE"
    if [ $? -ne 0 ]; then
      echo "[ERROR] Pip requirements failed for $ENV"
      exit 1
    fi
  fi
  # Always ensure flask and chromadb are installed for VS Code and runtime compatibility
  conda run -n "$ENV" pip install --upgrade flask chromadb
done

echo "[GremlinGPT] ✅ All environments checked, created, and pip-requirements installed if present."
