#!/bin/zsh

# ==========================
# Gremlin Auto Boot System
# ==========================

echo "[*] Syncing system time with BIOS..."
sudo timedatectl set-local-rtc 1 --adjust-system-clock
sudo hwclock --systohc

echo "[*] Creating daily RTC wake timer for 3:30 AM..."
cat <<EOF | sudo tee /usr/local/bin/set-wake-timer.sh > /dev/null
#!/bin/zsh
# Auto-schedule system wake at 3:30 AM tomorrow
rtcwake -m no -t $(date -d 'tomorrow 03:30' +%s)
EOF

sudo chmod +x /usr/local/bin/set-wake-timer.sh

echo "[*] Setting RTC timer to run on every reboot..."
(crontab -l 2>/dev/null; echo "@reboot /usr/local/bin/set-wake-timer.sh") | crontab -

# TWS & STT Auto-login Setup
echo "[*] Creating GUI login filler for TWS and STT..."

cat <<EOF > ~/tws_stt_autologin.sh
#!/bin/zsh

sleep 20  # Let GUI load

# TWS Auto-login
xdotool search --name "Trader Workstation" windowactivate --sync \
  key Tab key Tab type 'YOUR_TWS_USERNAME' key Tab \
  type 'YOUR_TWS_PASSWORD' key Return

# STT Auto-login (adjust title if needed)
xdotool search --name "StocksToTrade" windowactivate --sync \
  key Tab type 'YOUR_STT_USERNAME' key Tab \
  type 'YOUR_STT_PASSWORD' key Return
EOF

chmod +x ~/tws_stt_autologin.sh

echo "[*] Done. To finish setup:"
echo "1. Replace placeholders in ~/tws_stt_autologin.sh with your credentials."
echo "2. Add '~/tws_stt_autologin.sh &' to your existing auto-start script."
