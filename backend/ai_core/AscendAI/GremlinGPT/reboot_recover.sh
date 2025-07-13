#!/bin/zsh

echo "[RECOVERY] Initiating GremlinGPT reboot recovery..."

SNAPSHOT_DIR="run/checkpoints"
BACKUP_DIR="run/checkpoints/backup"
TODAY=$(date +%Y-%m-%d)
# For Linux, use: date -d "yesterday" +%Y-%m-%d
# For macOS, use: date -v-1d +%Y-%m-%d
if date -d "yesterday" +%Y-%m-%d >/dev/null 2>&1; then
  YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
else
  YESTERDAY=$(date -v-1d +%Y-%m-%d)
fi

mkdir -p "$BACKUP_DIR/$TODAY"

if [[ -f "$SNAPSHOT_DIR/state_snapshot.json" ]]; then
  cp "$SNAPSHOT_DIR/state_snapshot.json" "$BACKUP_DIR/$TODAY/state_snapshot.json"
  echo "[RECOVERY] Backup saved under: $BACKUP_DIR/$TODAY"
else
  echo "[RECOVERY] ERROR: Checkpoint file not found: $SNAPSHOT_DIR/state_snapshot.json"
fi

if [[ -d "$BACKUP_DIR/$YESTERDAY" ]]; then
  rm -rf "$BACKUP_DIR/$YESTERDAY"
  echo "[RECOVERY] Removed stale backup: $YESTERDAY"
fi

# Optionally restart FSM + Backend + Trainer
echo "[RECOVERY] Restarting core modules..."
pkill -f fsm.py
pkill -f server.py
pkill -f trainer.py

# Wait for processes to stop
for PROC in fsm.py server.py trainer.py; do
  while pgrep -f "$PROC" >/dev/null; do
    echo "[RECOVERY] Waiting for $PROC to stop..."
    sleep 1
  done
done

zsh run/start_all.sh

