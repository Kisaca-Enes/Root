#!/bin/bash

echo "== İz Temizleyici Başlatıldı =="

# 1. Bash geçmişini temizle
echo "[*] Bash geçmişi temizleniyor..."
history -c && echo " - Anlık geçmiş temizlendi."
rm -f ~/.bash_history && echo " - .bash_history dosyası silindi."
unset HISTFILE
export HISTFILE=/dev/null
export HISTSIZE=0
export HISTFILESIZE=0
echo " - Gelecek komutlar kaydedilmeyecek."

# 2. Ubuntu / Debian log dosyalarını temizle
echo "[*] Ubuntu/Debian logları temizleniyor..."
files=("/var/log/auth.log" "/var/log/syslog" "/var/log/kern.log")
for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    sudo truncate -s 0 "$file" && echo " - $file sıfırlandı."
  fi
done

# 3. RHEL / CentOS log dosyalarını temizle
echo "[*] RHEL/CentOS logları temizleniyor..."
files=("/var/log/secure" "/var/log/messages" "/var/run/utmp" "/var/log/wtmp" "/var/log/btmp")
for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    sudo truncate -s 0 "$file" && echo " - $file sıfırlandı."
  fi
done

# 4. systemd journal loglarını temizle
echo "[*] journalctl logları döndürülüyor ve temizleniyor..."
sudo journalctl --rotate && echo " - journalctl döndürüldü."
sudo journalctl --vacuum-time=1s && echo " - journalctl temizlendi."

# 5. Kullanıcı oturum kayıtlarını temizle
echo "[*] Oturum kayıtları temizleniyor..."
sudo truncate -s 0 /var/log/wtmp && echo " - /var/log/wtmp sıfırlandı."
sudo truncate -s 0 /var/log/btmp && echo " - /var/log/btmp sıfırlandı."
sudo truncate -s 0 /var/run/utmp && echo " - /var/run/utmp sıfırlandı."

echo "== İz Temizleme İşlemi Tamamlandı! =="
