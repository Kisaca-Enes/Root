#!/bin/bash

log_files=(
    "/var/log/syslog"
    "/var/log/auth.log"
    "/var/log/kern.log"
    "/var/log/dmesg"
    "/var/log/messages"
    "/var/log/secure"
    "/var/log/wtmp"
    "/var/log/btmp"
    "/var/log/utmp"
    "/var/log/lastlog"
    "$HOME/.bash_history"
)

function wipe_log() {
    local file="$1"
    if [ -f "$file" ]; then
        if [ -w "$file" ]; then
            > "$file"
            echo "[✅] Temizlendi: $file"
        else
            sudo bash -c "> $file" 2>/dev/null && echo "[✅] Temizlendi (sudo): $file" || echo "[❌] Temizlenemedi (izin yok): $file"
        fi
    else
        echo "[⚠️] Dosya bulunamadı: $file"
    fi
}

echo "📛 Log Temizleme Başlatıldı..."
for logfile in "${log_files[@]}"; do
    wipe_log "$logfile"
done

# Geçmiş RAM'den de silinsin
history -c
unset HISTFILE
echo "[✅] Bash geçmiş RAM'den de silindi (history -c)"

echo -e "\n🎉 İşlem tamamlandı."
