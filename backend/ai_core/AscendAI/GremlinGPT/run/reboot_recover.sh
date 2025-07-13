#!/bin/zsh

echo "[RECOVERY] Initiating GremlinGPT reboot recovery..."

SNAPSHOT_DIR="run/checkpoints"
BACKUP_DIR="run/checkpoints/backup"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

mkdir -p "$BACKUP_DIR/$TODAY"

# Delete previous day's backup if it exists
if [[ -d "$BACKUP_DIR/$YESTERDAY" ]]; then
  rm -rf "$BACKUP_DIR/$YESTERDAY"
  echo "[RECOVERY] Removed stale backup: $YESTERDAY"
fi

# Copy current checkpoint(s) to today's backup
if [[ -f "$SNAPSHOT_DIR/state_snapshot.json" ]]; then
  cp "$SNAPSHOT_DIR/state_snapshot.json" "$BACKUP_DIR/$TODAY/state_snapshot.json"
  echo "[RECOVERY] Backup saved under: $BACKUP_DIR/$TODAY"
else
  echo "[RECOVERY] No snapshot found to backup."
fi

# Optionally restart FSM + Backend + Trainer
echo "[RECOVERY] Restarting core modules..."
pkill -f "agent_core/fsm"
pkill -f "backend/server"
pkill -f "self_training/trainer"

zsh run/start_all.sh

