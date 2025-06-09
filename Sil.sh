# Anlık geçmişi temizle
history -c
# Geçmiş dosyasını sil
rm -f ~/.bash_history
unset HISTFILE
# Ubuntu / Debian
sudo truncate -s 0 /var/log/auth.log
sudo truncate -s 0 /var/log/syslog
sudo truncate -s 0 /var/log/kern.log

# RHEL / CentOS
sudo truncate -s 0 /var/log/secure
sudo truncate -s 0 /var/log/messages
sudo truncate -s 0 /var/run/utmp
sudo truncate -s 0 /var/log/wtmp
sudo truncate -s 0 /var/log/btmp
sudo journalctl --rotate
sudo journalctl --vacuum-time=1s
export HISTFILE=/dev/null
export HISTSIZE=0
export HISTFILESIZE=0
