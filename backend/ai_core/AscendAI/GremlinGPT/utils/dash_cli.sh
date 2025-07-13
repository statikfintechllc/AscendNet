#!/usr/bin/env zsh

APPLOC="$HOME"
LOGDIR="$APPLOC/data/logs"

# Dash CLI for GremlinGPT
LOGFILE="$LOGDIR/dash_cli.log"
mkdir -p "$(dirname "$LOGFILE")"
exec > >(tee -a "$LOGFILE") 2>&1
set -e

# Guarantee login+interactive shell for environment, if not already started
if [[ -z "$LOGIN_SHELL_STARTED" && "$0" != "-bash" ]]; then
    export LOGIN_SHELL_STARTED=1
    exec "$SHELL" -l -i "$0" "$@"
    exit 1
fi

APP_TITLE="AscendAI: GremlinGPT v1.0.3"
SUB_TITLE="From: SFTi"

# Resolve script dir, fallback to home if not found
APPLOC="$HOME"
APPDIR="$HOME/.local/share/applications"
START_SCRIPT="$APPLOC/run/start_all.sh"
STOP_SCRIPT="$APPLOC/run/stop_all.sh"
CHAT_SCRIPT="$APPLOC/run/cli.py"
REBOOT_SCRIPT="$APPLOC/run/reboot_recover.sh"

# Detect preferred shell (get user's shell from /etc/passwd or $SHELL), fallback to /bin/bash
USER_SHELL="$(getent passwd "$USER" | cut -d: -f7 2>/dev/null || echo "${SHELL:-/bin/bash}")"

# List of popular emulators, in order of preference
# If none found, will prompt user to install one
# If multiple found, will use the first available one
# This list can be extended with more terminal emulators as needed
# Note: This list is not exhaustive and may vary by distribution.
# It includes common terminal emulators found in most Linux distributions.
EMULATORS=(x-terminal-emulator gnome-terminal konsole xfce4-terminal lxterminal tilix mate-terminal)

function relaunch_in_terminal() {
    for TERM_APP in "${EMULATORS[@]}"; do
        if command -v "$TERM_APP" &>/dev/null; then
            if [[ "$USER_SHELL" =~ (bash|zsh) ]]; then
                exec "$TERM_APP" -- "$USER_SHELL" -ilc "$0"
            else
                exec "$TERM_APP" -- "$USER_SHELL" -ic "$0"
            fi
            exit 0
        fi
    done
    echo "[ERROR] No graphical terminal emulator found. Exiting."
    exit 1
}

# Check if we're in a terminal, if not relaunch in a graphical one, if available
if ! [ -t 0 ]; then
    relaunch_in_terminal
fi

while true; do
    clear
    UPTIME=$(uptime -p | sed 's/^up //')
    echo -e "\033[1;36m$APP_TITLE\033[0m"
    echo -e "\033[0;32m$SUB_TITLE\033[0m"
    echo -e "Up-Time: \033[1;33m$UPTIME\033[0m"
    echo ""
    echo "Choose an action:"
    echo "1) ✅ Start GremlinGPT ✅"
    echo "2) 🚫 Stop GremlinGPT 🚫"
    echo "3) 🗣️ Chat Only 🗣️"
    echo "4) ⚠️ View GremlinGPT Logs ⚠️"
    echo "5) ✌️ Exit GremlinGPT ✌️"
    echo "6) ♻️ Reboot & Recover GremlinGPT ♻️"
    echo -n "Select> "
    read -r CHOICE
#    echo ""  # For better readability, can be uncommented if needed
    case $CHOICE in
        1)
            bash -l "$START_SCRIPT"
            echo -e "\nGremlinGPT Launched. Press enter to continue..."
            read -r
            ;;
        2)
            bash -l "$STOP_SCRIPT"
            echo -e "\nGremlinGPT has Stopped. Press enter to continue..."
            read -r
            ;;
        3)
            echo -e "\nLaunching CLI Chat (type 'Exit' in chat to return)...\n"
            python3 "$CHAT_SCRIPT"
            echo -e "\nExited Chat. Press enter to return to menu."
            read -r
            ;;
        4)
            while true; do
                clear
                echo -e "\033[1;34m[Log Menu]\033[0m"
                echo "Select a log to view (last 40 lines):"
                echo "Available logs:"
                LOG_NAMES=(
                    "runtime.log"
                    "nlp.out"
                    "memory.out"
                    "fsm.out"
                    "scraper.out"
                    "trainer.out"
                    "backend.out"
                    "frontend.out"
                    "ngrok.out"
                    "gremlin_boot_trace.log"
                )
                for i in "${!LOG_NAMES[@]}"; do
                    echo "$((i+1))) ${LOG_NAMES[$i]}"
                done
                echo "$(( ${#LOG_NAMES[@]} + 1 ))) Return to main menu"
                echo -n "Select log> "
                read -r LOG_CHOICE
                if (( LOG_CHOICE > 0 && LOG_CHOICE <= ${#LOG_NAMES[@]} )); then
                    LOG_FILE="$LOGDIR/${LOG_NAMES[$((LOG_CHOICE - 1))]}"
                    clear
                    echo -e "\n\033[1;36m[Viewing: ${LOG_NAMES[$((LOG_CHOICE - 1))]}]\033[0m"
                    echo -e "Press Enter to return to log menu...\n"
                    tail -n 40 "$LOG_FILE" 2>/dev/null || echo "[Error] Log file not found."
                    read -r
                elif (( LOG_CHOICE == ${#LOG_NAMES[@]} + 1 )); then
                    break
                else
                    echo "[!] Invalid input. Maybe choose a real Option."
                    read -r
                fi
            done
            ;;
        5)
            echo "Goodbye, MeatSpace operator."
            exit 0
            ;;
        6)
            bash -l "$REBOOT_SCRIPT"
            echo -e "\nGremlinGPT reboot & recovery triggered. Press enter to continue..."
            read -r
            ;;
        *)
            echo "[!] Invalid input. Maybe choose a real Option."
            read -r
            ;;
    esac
done
