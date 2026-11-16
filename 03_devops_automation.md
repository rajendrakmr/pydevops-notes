# 03. Python for DevOps Automation

The 17 libraries every DevOps engineer should know, each with:
**what it is → install → key APIs → examples → practical script → pitfalls.**

| # | Library | Used for |
|---|---------|----------|
| 1 | [os](#1-os-module) | Env vars, files, processes |
| 2 | [platform](#2-platform) | OS / hardware identification |
| 3 | [subprocess](#3-subprocess) | Run shell commands, kubectl, git, docker |
| 4 | [sys](#4-sys) | Args, exit codes, interpreter info |
| 5 | [psutil](#5-psutil) | CPU, memory, disk, network, processes |
| 6 | [re](#6-re-regular-expressions) | Log parsing, extraction, validation |
| 7 | [python-crontab](#7-python-crontab) | Manage cron jobs from code |
| 8 | [scapy](#8-scapy) | Packet crafting, network diagnostics |
| 9 | [requests and urllib3](#9-requests-and-urllib3) | REST APIs, health checks, retries |
| 10 | [logging](#10-logging) | Production-grade logs |
| 11 | [getpass](#11-getpass) | Safe password prompts |
| 12 | [boto3](#12-boto3) | AWS automation |
| 13 | [paramiko](#13-paramiko) | SSH / SFTP |
| 14 | [json](#14-json) | APIs, AWS/Terraform/K8s output |
| 15 | [PyYAML](#15-pyyaml) | Kubernetes, Ansible, CI configs |
| 16 | [pandas](#16-pandas) | CSV/report analysis |
| 17 | [smtplib](#17-smtplib) | Email alerts and reports |

Then: [Capstone project](#capstone-server-health-and-report-tool), [cheat sheet](#cheat-sheet), [DevOps script best practices](#devops-script-best-practices).

Setup:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install psutil python-crontab scapy requests boto3 paramiko pyyaml pandas
```
Standard library (no install): `os, platform, subprocess, sys, re, logging, getpass, json, smtplib`.

---

## 1. os module

**What:** Portable interface to the operating system: environment variables, files and directories, process info.
**Docs:** https://docs.python.org/3/library/os.html

### Key APIs

```python
import os

# Environment variables (the main DevOps use)
os.environ["HOME"]                       # KeyError if absent
os.environ.get("ENV", "dev")             # default
os.getenv("DEBUG") == "1"
os.environ["MY_VAR"] = "x"               # affects this process + children only
os.environ.pop("MY_VAR", None)
dict(os.environ)                          # copy of the whole environment

# Paths and directories
os.getcwd(); os.chdir("/tmp")
os.listdir("/etc")
os.makedirs("/tmp/a/b/c", exist_ok=True)
os.remove("file"); os.rmdir("emptydir"); os.rename("old", "new")
os.path.join("/var", "log", "app.log")
os.path.exists(p); os.path.isfile(p); os.path.isdir(p)
os.path.basename(p); os.path.dirname(p); os.path.splitext("a.tar.gz")  # ('a.tar', '.gz')
os.path.abspath("."); os.path.expanduser("~/x"); os.path.getsize(p)

# Walk a tree
for root, dirs, files in os.walk("/var/log"):
    for f in files:
        full = os.path.join(root, f)

# Fast directory scan with metadata
with os.scandir("/var/log") as it:
    for e in it:
        if e.is_file():
            print(e.name, e.stat().st_size)

# Permissions and ownership
os.chmod("deploy.sh", 0o750)
os.access("/etc/shadow", os.R_OK)        # can I read it?
os.stat(p).st_mode, os.stat(p).st_mtime, os.stat(p).st_uid

# Process info
os.getpid(); os.getppid(); os.getuid(); os.cpu_count()
os.uname()                               # Unix: sysname, nodename, release...
os.getloadavg()                          # (1, 5, 15 minute load) Unix
os.kill(pid, 15)                         # send SIGTERM
os.system("ls")                          # avoid: use subprocess
```

`pathlib` is nicer for path manipulation; `os` remains essential for `environ`, `walk`, `scandir`, `chmod`, `kill`, `getpid`.

### Practical A: environment validator (fail fast on missing config)

```python
#!/usr/bin/env python3
import os, sys

REQUIRED = ["AWS_REGION", "DEPLOY_ENV", "APP_VERSION"]
OPTIONAL = {"LOG_LEVEL": "INFO", "TIMEOUT": "30"}

missing = [k for k in REQUIRED if not os.environ.get(k)]
if missing:
    print(f"ERROR: missing env vars: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)

cfg = {k: os.environ[k] for k in REQUIRED}
cfg.update({k: os.environ.get(k, d) for k, d in OPTIONAL.items()})
print(cfg)
```
Run: `AWS_REGION=eu-west-1 DEPLOY_ENV=prod APP_VERSION=1.4.2 python validate_env.py`

### Practical B: find the biggest files under a directory

```python
import os, sys

def biggest(root: str, top: int = 10):
    sizes = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            p = os.path.join(dirpath, f)
            try:
                if not os.path.islink(p):
                    sizes.append((os.path.getsize(p), p))
            except OSError:
                continue                   # file vanished / permission denied
    return sorted(sizes, reverse=True)[:top]

for size, path in biggest(sys.argv[1] if len(sys.argv) > 1 else "."):
    print(f"{size/1e6:10.1f} MB  {path}")
```

### Practical C: old-log cleanup (with dry run)

```python
import os, time, sys

def cleanup(root, days=14, dry_run=True):
    cutoff = time.time() - days * 86400
    removed = 0
    for dirpath, _, files in os.walk(root):
        for f in files:
            if not f.endswith(".log"):
                continue
            p = os.path.join(dirpath, f)
            if os.path.getmtime(p) < cutoff:
                print(("[dry-run] " if dry_run else "") + "remove", p)
                if not dry_run:
                    os.remove(p)
                removed += 1
    return removed

if __name__ == "__main__":
    print(cleanup(sys.argv[1], dry_run="--apply" not in sys.argv), "files")
```

### Pitfalls
- `os.environ` values are always strings: `int(os.environ["PORT"])`.
- Changing `os.environ` doesn't change your parent shell.
- `os.system` and `os.popen` invite shell injection. Use `subprocess`.
- `os.getloadavg`, `getuid`, `uname`, `kill` signals differ or don't exist on Windows.

---

## 2. platform

**What:** Identify the OS, architecture and Python build you're running on, so a script can branch correctly.
**Docs:** https://docs.python.org/3/library/platform.html

### Key APIs

```python
import platform

platform.system()          # 'Linux', 'Darwin', 'Windows'
platform.release()         # kernel version e.g. '6.5.0-35-generic'
platform.version()         # build/version string
platform.machine()         # 'x86_64', 'arm64', 'aarch64'
platform.processor()       # may be '' on Linux; prefer machine()
platform.node()            # hostname
platform.platform()        # 'Linux-6.5.0-x86_64-with-glibc2.35'
platform.python_version()  # '3.12.1'
platform.python_implementation()  # 'CPython'
platform.architecture()    # ('64bit', 'ELF')
platform.uname()           # namedtuple: system, node, release, version, machine
platform.freedesktop_os_release()   # 3.10+, Linux: dict from /etc/os-release
```

### Practical A: OS-aware package installer chooser

```python
import platform, shutil

def package_manager() -> str:
    system = platform.system()
    if system == "Darwin":
        return "brew"
    if system == "Windows":
        return "choco" if shutil.which("choco") else "winget"
    if system == "Linux":
        try:
            osr = platform.freedesktop_os_release()
        except OSError:
            osr = {}
        ids = {osr.get("ID", "")} | set(osr.get("ID_LIKE", "").split())
        if ids & {"debian", "ubuntu"}:
            return "apt"
        if ids & {"rhel", "fedora", "centos"}:
            return "dnf" if shutil.which("dnf") else "yum"
        if "alpine" in ids:
            return "apk"
        if "arch" in ids:
            return "pacman"
    raise RuntimeError("unsupported platform")

print(package_manager())
```

### Practical B: inventory info as JSON

```python
import platform, json, socket

info = {
    "hostname": platform.node(),
    "fqdn": socket.getfqdn(),
    "os": platform.system(),
    "kernel": platform.release(),
    "arch": platform.machine(),
    "python": platform.python_version(),
}
print(json.dumps(info, indent=2))
```

### Pitfalls
- `platform.linux_distribution()` was removed (3.8). Use `freedesktop_os_release()` or parse `/etc/os-release`.
- `platform.node()` may return a short name. Use `socket.getfqdn()` for the full name.
- On Apple Silicon under Rosetta, `machine()` can report `x86_64`.

---

## 3. subprocess

**What:** Start external programs (git, kubectl, docker, terraform, systemctl) and capture their output and exit codes. This is the glue of DevOps scripting.
**Docs:** https://docs.python.org/3/library/subprocess.html

### Key APIs

```python
import subprocess

# The modern default: subprocess.run
r = subprocess.run(
    ["kubectl", "get", "pods", "-n", "prod", "-o", "json"],
    capture_output=True,    # collect stdout/stderr
    text=True,              # str instead of bytes
    timeout=30,             # raises TimeoutExpired
    check=True,             # raises CalledProcessError on non-zero exit
    cwd="/tmp",             # working dir
    env={**os.environ, "KUBECONFIG": "/path"},  # custom environment
)
r.returncode; r.stdout; r.stderr; r.args
```

Handling failure:

```python
try:
    r = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True, timeout=60)
except subprocess.CalledProcessError as e:
    print("exit", e.returncode, "stderr:", e.stderr)
except subprocess.TimeoutExpired:
    print("timed out")
except FileNotFoundError:
    print("git is not installed")
```

Shortcuts:

```python
out = subprocess.check_output(["hostname"], text=True).strip()
subprocess.run(["echo", "hi"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
subprocess.run(["wc", "-l"], input="a\nb\n", text=True, capture_output=True)  # feed stdin
```

Streaming output live (long-running commands: builds, deploys):

```python
with subprocess.Popen(
    ["ping", "-c", "4", "8.8.8.8"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
) as proc:
    for line in proc.stdout:
        print(">>", line.rstrip())
    rc = proc.wait()
print("exit code", rc)
```

Pipelines without a shell:

```python
p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
p2 = subprocess.run(["grep", "python"], stdin=p1.stdout, capture_output=True, text=True)
p1.stdout.close()
```

`shell=True` only when you truly need shell features (globs, pipes, `&&`), and **never** with user-supplied data. Otherwise use a list of args.

### Practical A: reusable command runner

```python
import logging, subprocess
from dataclasses import dataclass

log = logging.getLogger(__name__)

@dataclass
class CmdResult:
    rc: int
    out: str
    err: str
    @property
    def ok(self) -> bool:
        return self.rc == 0

def run(cmd: list[str], timeout: int = 60, check: bool = False, **kw) -> CmdResult:
    log.info("$ %s", " ".join(cmd))
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)
    except subprocess.TimeoutExpired:
        log.error("timeout after %ss: %s", timeout, cmd[0])
        res = CmdResult(124, "", f"timeout after {timeout}s")
    except FileNotFoundError:
        res = CmdResult(127, "", f"command not found: {cmd[0]}")
    else:
        res = CmdResult(p.returncode, p.stdout.strip(), p.stderr.strip())
    if check and not res.ok:
        raise RuntimeError(f"{' '.join(cmd)} failed ({res.rc}): {res.err}")
    return res

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run(["uname", "-a"]).out)
    print(run(["nonexistent-tool"]).err)
```

### Practical B: Kubernetes, find non-Running pods

```python
import json, subprocess

out = subprocess.run(
    ["kubectl", "get", "pods", "-A", "-o", "json"],
    capture_output=True, text=True, check=True, timeout=30,
).stdout

for item in json.loads(out)["items"]:
    phase = item["status"]["phase"]
    if phase != "Running" and phase != "Succeeded":
        ns, name = item["metadata"]["namespace"], item["metadata"]["name"]
        print(f"{ns}/{name}: {phase}")
```

### Practical C: git release helper

```python
import subprocess, sys

def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()

if git("status", "--porcelain"):
    sys.exit("working tree dirty, commit or stash first")

branch = git("rev-parse", "--abbrev-ref", "HEAD")
sha = git("rev-parse", "--short", "HEAD")
print(f"releasing {branch}@{sha}")
git("tag", "-a", f"v{sys.argv[1]}", "-m", f"release {sys.argv[1]}")
```

### Pitfalls
- A string with `shell=False` fails: `run("ls -l")` raises `FileNotFoundError`. Use `["ls", "-l"]` (or `shlex.split`).
- A non-zero exit does **not** raise unless `check=True`.
- Reading both PIPEs from `Popen` incorrectly can deadlock. Use `run()` or `communicate()`.
- Commands can hang: always set `timeout`.
- Output decoding errors: pass `errors="replace"` for messy output.

---

## 4. sys

**What:** Access to the interpreter and the runtime environment: command-line arguments, exit codes, standard streams, module search path.
**Docs:** https://docs.python.org/3/library/sys.html

### Key APIs

```python
import sys

sys.argv                 # ['script.py', 'arg1', 'arg2']
sys.exit(0)              # 0 ok, non-zero error; sys.exit("msg") prints to stderr, exits 1
sys.stdin; sys.stdout; sys.stderr
print("error!", file=sys.stderr)
sys.version              # long string
sys.version_info         # (3, 12, 1, 'final', 0)
sys.platform             # 'linux', 'darwin', 'win32'
sys.executable           # path to current python
sys.path                 # module search path list
sys.modules              # loaded modules
sys.getsizeof(obj)       # bytes of one object
sys.getrecursionlimit()
sys.prefix != sys.base_prefix   # True when inside a venv
sys.stdout.isatty()      # is output a terminal? (colour decisions)
sys.excepthook           # global handler for uncaught exceptions
```

Reading piped input:

```python
# cat access.log | python count.py
import sys
count = sum(1 for line in sys.stdin if " 500 " in line)
print(count)
```

Global exception hook (log every crash):

```python
import sys, logging
def hook(exc_type, exc, tb):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc, tb); return
    logging.critical("Uncaught", exc_info=(exc_type, exc, tb))
sys.excepthook = hook
```

### Practical A: minimal CLI with correct exit codes

```python
#!/usr/bin/env python3
import sys

USAGE = "usage: check_disk.py <path> <max_percent>"

def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(USAGE, file=sys.stderr)
        return 2                       # 2 = usage error (convention)
    import shutil
    path, limit = argv[1], float(argv[2])
    u = shutil.disk_usage(path)
    pct = u.used / u.total * 100
    print(f"{path}: {pct:.1f}% used")
    return 1 if pct > limit else 0     # 1 = problem found

if __name__ == "__main__":
    sys.exit(main(sys.argv))
```
Works as a Nagios/CI/cron check: `python check_disk.py / 90 || notify`.

### Practical B: ensure the right Python and a venv

```python
import sys
if sys.version_info < (3, 10):
    sys.exit(f"Python 3.10+ required, found {sys.version.split()[0]}")
if sys.prefix == sys.base_prefix:
    print("warning: not running inside a virtualenv", file=sys.stderr)
```

### Pitfalls
- `sys.exit()` raises `SystemExit`; a bare `except:` or `except BaseException` swallows it.
- Print errors to `stderr`, data to `stdout`.
- For real CLIs prefer `argparse`/Typer over hand-parsing `sys.argv`.

---

## 5. psutil

**What:** Cross-platform library for system monitoring: CPU, memory, disks, network, processes, sensors, boot time. The Python equivalent of `top`, `free`, `df`, `ps`, `netstat` in one API.
**Install:** `pip install psutil` · **Docs:** https://github.com/giampaolo/psutil

### Key APIs

```python
import psutil

# CPU
psutil.cpu_percent(interval=1)                 # % overall (blocks 1s to measure)
psutil.cpu_percent(interval=1, percall=True)   # per core
psutil.cpu_count(logical=False), psutil.cpu_count()
psutil.cpu_freq(); psutil.getloadavg()

# Memory
vm = psutil.virtual_memory()
vm.total, vm.available, vm.percent, vm.used
psutil.swap_memory().percent

# Disk
psutil.disk_partitions()                      # mounts
psutil.disk_usage("/")                        # total, used, free, percent
psutil.disk_io_counters()

# Network
psutil.net_io_counters()                      # bytes_sent, bytes_recv, errin, dropout...
psutil.net_io_counters(pernic=True)
psutil.net_if_addrs(); psutil.net_if_stats()
psutil.net_connections(kind="tcp")            # may need root; filter by status == "LISTEN"

# System
psutil.boot_time()                            # epoch
psutil.users()
psutil.sensors_temperatures()                 # Linux/FreeBSD
psutil.sensors_battery()

# Processes
for p in psutil.process_iter(["pid", "name", "username", "cpu_percent", "memory_percent"]):
    print(p.info)

p = psutil.Process(1234)
p.name(); p.cmdline(); p.status(); p.create_time()
p.cpu_percent(interval=0.5); p.memory_info().rss; p.num_threads()
p.open_files(); p.connections(); p.children(recursive=True)
p.terminate()      # SIGTERM
p.kill()           # SIGKILL
p.wait(timeout=5)
```

Exceptions to handle when iterating processes: `psutil.NoSuchProcess`, `psutil.AccessDenied`, `psutil.ZombieProcess`.

### Practical A: resource monitor with thresholds and exit codes

```python
#!/usr/bin/env python3
import psutil, sys, socket
from datetime import datetime

THRESH = {"cpu": 85, "mem": 85, "disk": 90}

def snapshot() -> dict:
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }

def main() -> int:
    s = snapshot()
    host = socket.gethostname()
    print(f"[{datetime.now():%F %T}] {host}", " ".join(f"{k}={v:.1f}%" for k, v in s.items()))
    alerts = [f"{k} {v:.1f}% > {THRESH[k]}%" for k, v in s.items() if v > THRESH[k]]
    for a in alerts:
        print("ALERT:", a, file=sys.stderr)
    return 1 if alerts else 0

if __name__ == "__main__":
    sys.exit(main())
```

### Practical B: top memory consumers

```python
import psutil

procs = []
for p in psutil.process_iter(["pid", "name", "memory_info", "cmdline"]):
    try:
        procs.append((p.info["memory_info"].rss, p.info["pid"], p.info["name"]))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

for rss, pid, name in sorted(procs, reverse=True)[:10]:
    print(f"{rss/1e6:8.1f} MB  pid={pid:<7} {name}")
```

### Practical C: network throughput meter

```python
import psutil, time

prev = psutil.net_io_counters()
while True:
    time.sleep(1)
    cur = psutil.net_io_counters()
    print(f"↓ {(cur.bytes_recv-prev.bytes_recv)/1024:8.1f} KB/s   "
          f"↑ {(cur.bytes_sent-prev.bytes_sent)/1024:8.1f} KB/s", end="\r")
    prev = cur
```

### Practical D: kill a runaway process gracefully

```python
import psutil

def stop_by_name(name: str, wait: int = 10):
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            p.terminate()
            try:
                p.wait(wait)
            except psutil.TimeoutExpired:
                p.kill()          # last resort
```

### Pitfalls
- First call of `cpu_percent()` without `interval` returns 0.0. Pass `interval=` or call twice.
- Containers: psutil reports the **host's** CPU/memory in many cases, not the cgroup limit. Read `/sys/fs/cgroup` for container limits.
- Processes disappear mid-iteration; always wrap in try/except.
- Some data needs root (e.g. `net_connections` for all users on some OSes).

---

## 6. re (Regular Expressions)

**What:** Pattern matching for text: parse logs, extract IPs/versions/IDs, validate input, bulk-edit config.
**Docs:** https://docs.python.org/3/library/re.html

### Syntax cheat sheet

| Pattern | Meaning |
|---------|---------|
| `.` | any char (not newline) |
| `\d \w \s` | digit, word char, whitespace (capital = negation) |
| `^ $` | start / end of line (with `re.M`) or string |
| `* + ?` | 0+, 1+, 0 or 1 |
| `{n} {n,m}` | exact count / range |
| `[abc] [a-z] [^abc]` | set / range / negated set |
| `(...)` | capture group |
| `(?:...)` | non-capturing group |
| `(?P<name>...)` | named group |
| `a\|b` | alternation |
| `\b` | word boundary |
| `*? +?` | lazy (non-greedy) |
| `(?=...) (?<=...)` | lookahead / lookbehind |

Use **raw strings** `r"..."` so `\d` isn't treated as a string escape.

### Key functions

```python
import re

re.search(r"\d+", "port 8080 open")        # first match anywhere -> Match or None
re.match(r"\d+", "8080 open")              # must match at START
re.fullmatch(r"\d{1,3}", "123")            # must match the WHOLE string
re.findall(r"\d+", "a1 b22 c333")          # ['1', '22', '333']
list(re.finditer(r"\d+", "a1 b22"))        # match objects with positions
re.sub(r"\s+", " ", "a   b \t c")          # 'a b c'
re.split(r"[,;]\s*", "a, b;c")             # ['a', 'b', 'c']

m = re.search(r"(?P<user>\w+)@(?P<host>[\w.]+)", "mail bob@example.com now")
m.group(0); m.group("user"); m.groupdict(); m.start(); m.end()

pat = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")      # compile once, reuse in loops
pat.match("10.0.0.1")
```

Flags: `re.I` (ignore case), `re.M` (multiline), `re.S` (dot matches newline), `re.X` (verbose, allows comments).

### Practical A: parse an nginx access log

```python
import re
from collections import Counter

LOG = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<bytes>\d+|-)'
)

line = '203.0.113.9 - - [10/Oct/2025:13:55:36 +0000] "GET /api/users HTTP/1.1" 500 123'
m = LOG.match(line)
print(m.groupdict())

def summarize(path: str):
    ips, errors = Counter(), Counter()
    with open(path, encoding="utf-8", errors="replace") as f:
        for ln in f:
            m = LOG.match(ln)
            if not m:
                continue
            ips[m["ip"]] += 1
            if m["status"].startswith("5"):
                errors[m["path"]] += 1
    return ips.most_common(5), errors.most_common(5)
```

### Practical B: extract IPs and validate them

```python
import re, ipaddress

text = "failed from 192.168.1.10, 999.1.1.1 and 10.0.0.7"
candidates = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", text)

valid = []
for c in candidates:
    try:
        valid.append(str(ipaddress.ip_address(c)))   # regex finds, ipaddress validates
    except ValueError:
        pass
print(valid)    # ['192.168.1.10', '10.0.0.7']
```

### Practical C: SSH brute-force detector from auth.log

```python
import re
from collections import Counter

pat = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)")
hits = Counter()
with open("/var/log/auth.log", errors="replace") as f:
    for line in f:
        if m := pat.search(line):
            hits[m.group(2)] += 1

for ip, n in hits.most_common():
    if n >= 5:
        print(f"{ip} had {n} failed logins")
```

### Practical D: bump a version in a config file

```python
import re
from pathlib import Path

p = Path("deploy.env")
s = p.read_text()
s = re.sub(r"^(APP_VERSION=).*$", r"\g<1>2.4.1", s, flags=re.M)
p.write_text(s)
```

### Pitfalls
- `match` vs `search` vs `fullmatch`. Most "my regex doesn't match" bugs are this.
- Greedy `.*` eats too much; use `.*?` or a negated class `[^"]*`.
- Don't parse HTML/JSON/YAML with regex. Use a real parser.
- Catastrophic backtracking on nested quantifiers like `(a+)+`, which is a ReDoS risk on untrusted input.
- Regexes for emails/IPs get complicated. Combine a simple regex with a validator (`ipaddress`, `urllib.parse`).

---

## 7. python-crontab

**What:** Read, create and modify cron jobs from Python instead of hand-editing `crontab -e`.
**Install:** `pip install python-crontab` · **Docs:** https://pypi.org/project/python-crontab/
Works on Unix-like systems.

### Cron syntax reminder

```
┌ minute (0-59)
│ ┌ hour (0-23)
│ │ ┌ day of month (1-31)
│ │ │ ┌ month (1-12)
│ │ │ │ ┌ day of week (0-6, Sun=0)
* * * * *  command

*/5 * * * *      every 5 minutes
0 2 * * *        daily at 02:00
0 9 * * 1-5      weekdays 09:00
30 3 1 * *       1st of month 03:30
@reboot          at startup
```

### Key APIs

```python
from crontab import CronTab

cron = CronTab(user=True)               # current user's crontab
# CronTab(user="root")                  # needs privileges
# CronTab(tabfile="/etc/cron.d/myapp", user=False)   # a system cron file
# CronTab(tab="* * * * * echo hi")      # from a string (great for tests)

for job in cron:                        # list jobs
    print(job.minute, job.hour, job.command, job.comment, job.is_enabled())

job = cron.new(command="/usr/bin/python3 /opt/backup.py >> /var/log/backup.log 2>&1",
               comment="nightly-backup")
job.setall("0 2 * * *")                 # raw expression
# or fluent:
job.minute.on(0); job.hour.on(2)
job.minute.every(5)                     # */5
job.dow.on("MON", "FRI")
job.enable(False)                       # comment out without deleting
cron.write()                            # SAVE. Nothing is persisted until this.

# find / remove
for j in cron.find_comment("nightly-backup"):
    cron.remove(j)
cron.remove_all(comment="nightly-backup")
cron.write()

job.is_valid()                          # syntax check
list(job.schedule().get_next() for _ in range(1))   # needs croniter installed
```

### Practical A: idempotent job installer

Running it twice must not create duplicates. Identify jobs by comment.

```python
#!/usr/bin/env python3
from crontab import CronTab

def ensure_job(command: str, schedule: str, comment: str) -> str:
    cron = CronTab(user=True)
    existing = list(cron.find_comment(comment))
    if existing:
        job = existing[0]
        if job.command == command and str(job.slices) == schedule:
            return "unchanged"
        job.set_command(command)
        job.setall(schedule)
        state = "updated"
    else:
        job = cron.new(command=command, comment=comment)
        job.setall(schedule)
        state = "created"
    if not job.is_valid():
        raise ValueError(f"invalid cron schedule: {schedule}")
    cron.write()
    return state

if __name__ == "__main__":
    print(ensure_job("/usr/bin/python3 /opt/ops/disk_check.py", "*/10 * * * *", "ops:disk-check"))
    print(ensure_job("/usr/bin/python3 /opt/ops/backup.py >> /var/log/backup.log 2>&1",
                     "0 2 * * *", "ops:nightly-backup"))
```

### Practical B: list and audit all jobs

```python
from crontab import CronTab
for job in CronTab(user=True):
    state = "ON " if job.is_enabled() else "OFF"
    print(f"{state} {job.slices!s:<18} {job.command}  # {job.comment}")
```

### Practical C: remove all jobs managed by your tool

```python
import re
cron = CronTab(user=True)
for job in list(cron.find_comment(re.compile(r"^ops:"))):   # regex match on comment
    cron.remove(job)
cron.write()
```

### Pitfalls
- **Forgetting `cron.write()`.**
- Cron's environment is minimal. Use **absolute paths** for the interpreter, scripts and files, and set env vars in the command or the script.
- Redirect output (`>> log 2>&1`) or you'll get silent failures or mail spam.
- Jobs run in the system timezone (usually UTC on servers).
- Overlapping runs: protect long jobs with a lock (`flock -n /tmp/job.lock cmd`).
- For container/Kubernetes workloads use a CronJob instead of crond.

---

## 8. scapy

**What:** Build, send, sniff and dissect network packets. Useful for network diagnostics, firewall rule verification, custom pings/traceroutes and learning how protocols work.
**Install:** `pip install scapy` · **Docs:** https://github.com/secdev/scapy/

> ⚠️ **Authorized use only.** Craft and sniff packets only on networks and hosts you own or have written permission to test. Most operations need **root/Administrator**, and sniffing on Windows needs Npcap.

### Key concepts

Packets are stacked with `/`: `Ether()/IP()/TCP()`. Fields are set as arguments.

```python
from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP, DNS, DNSQR, Raw
from scapy.all import sr1, sr, send, sendp, srp, sniff, conf, traceroute

pkt = IP(dst="8.8.8.8") / ICMP()
pkt.show()                       # show all fields
pkt.summary()
```

Send/receive functions:

| Function | Layer | Returns |
|----------|-------|---------|
| `sr1(pkt)` | 3 | first answer |
| `sr(pkt)` | 3 | (answered, unanswered) |
| `send(pkt)` | 3 | nothing |
| `srp(pkt)` | 2 | answers at layer 2 (ARP etc.) |
| `sendp(pkt)` | 2 | nothing |
| `sniff()` | | captured packets |

### Practical A: ICMP ping

```python
from scapy.all import IP, ICMP, sr1

def ping(host: str, timeout: float = 2.0) -> bool:
    reply = sr1(IP(dst=host) / ICMP(), timeout=timeout, verbose=0)
    if reply is None:
        return False
    print(f"{host} replied, ttl={reply.ttl}")
    return True

ping("8.8.8.8")          # run with sudo
```

### Practical B: TCP port probe (SYN check) on your own host

```python
from scapy.all import IP, TCP, sr1, send

def tcp_open(host: str, port: int, timeout: float = 2.0) -> str:
    resp = sr1(IP(dst=host) / TCP(dport=port, flags="S"), timeout=timeout, verbose=0)
    if resp is None:
        return "filtered"                              # no reply: firewall drop
    if resp.haslayer(TCP):
        flags = resp[TCP].flags
        if flags & 0x12 == 0x12:                       # SYN+ACK
            send(IP(dst=host) / TCP(dport=port, flags="R"), verbose=0)   # reset politely
            return "open"
        if flags & 0x04:                               # RST
            return "closed"
    return "unknown"

for p in (22, 80, 443):
    print(p, tcp_open("127.0.0.1", p))
```
This verifies what a firewall rule does, e.g. "is port 5432 really blocked from this subnet?"

### Practical C: ARP scan of your LAN (asset discovery)

```python
from scapy.all import ARP, Ether, srp

def arp_scan(cidr: str = "192.168.1.0/24"):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr), timeout=2, verbose=0)
    return [(rcv.psrc, rcv.hwsrc) for _, rcv in ans]

for ip, mac in arp_scan():
    print(f"{ip:<15} {mac}")
```

### Practical D: DNS query and sniffing

```python
from scapy.all import IP, UDP, DNS, DNSQR, sr1, sniff

r = sr1(IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com")), timeout=3, verbose=0)
if r and r.haslayer(DNS):
    for i in range(r[DNS].ancount):
        print(r[DNS].an[i].rdata)

# capture 10 packets on port 443 and print summaries
sniff(filter="tcp port 443", count=10, prn=lambda p: print(p.summary()))
# save/read pcap for Wireshark
from scapy.all import wrpcap, rdpcap
pkts = sniff(count=20); wrpcap("cap.pcap", pkts)
```

### Practical E: simple traceroute

```python
from scapy.all import IP, ICMP, sr1

def trace(dst: str, max_hops: int = 20):
    for ttl in range(1, max_hops + 1):
        r = sr1(IP(dst=dst, ttl=ttl) / ICMP(), timeout=2, verbose=0)
        if r is None:
            print(f"{ttl:>2}  *")
        else:
            print(f"{ttl:>2}  {r.src}")
            if r.type == 0:        # echo reply = destination reached
                break
trace("8.8.8.8")
```

### Pitfalls
- Needs privileges: `sudo python script.py` (or grant `CAP_NET_RAW`).
- The kernel may auto-RST scapy's SYN replies; that's why the example sends its own reset.
- Cloud networks (AWS/GCP) often block ICMP or spoofed packets via security groups.
- For ordinary connectivity checks, `socket.create_connection` or `requests` is simpler. Reach for scapy when you need raw control.

---

## 9. requests and urllib3

**What:** `requests` is the human-friendly HTTP client; `urllib3` is the engine under it and provides the **retry** and **connection pool** machinery.
**Install:** `pip install requests` (urllib3 comes with it)
**Docs:** https://pypi.org/project/requests/ · https://pypi.org/project/urllib3/

### Key APIs

```python
import requests

r = requests.get(
    "https://api.example.com/items",
    params={"limit": 50},
    headers={"Authorization": f"Bearer {token}"},
    timeout=(3.05, 10),          # connect, read. ALWAYS set
    verify=True,                 # TLS verification (default). Or path to CA bundle
    allow_redirects=True,
)
r.status_code; r.ok; r.reason
r.headers["Content-Type"]
r.text; r.content; r.json()
r.elapsed.total_seconds()
r.url; r.history              # redirects
r.raise_for_status()

requests.post(url, json={"name": "x"})           # JSON body
requests.post(url, data={"k": "v"})              # form-encoded
requests.post(url, files={"file": open("a.tgz", "rb")})
requests.put(url, json=...); requests.patch(url, json=...); requests.delete(url)
requests.head(url)

# Streaming a large download
with requests.get(url, stream=True, timeout=30) as r:
    r.raise_for_status()
    with open("big.iso", "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            f.write(chunk)
```

Session (connection reuse, shared headers/auth/cookies):

```python
s = requests.Session()
s.headers.update({"User-Agent": "devops-bot/1.0", "Accept": "application/json"})
s.auth = ("user", "pass")
s.get(url, timeout=10)
```

Exceptions hierarchy: `requests.RequestException` → `ConnectionError`, `Timeout` (`ConnectTimeout`, `ReadTimeout`), `HTTPError`, `TooManyRedirects`, `SSLError`.

### urllib3: retries

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def session_with_retries() -> requests.Session:
    retry = Retry(
        total=5,
        connect=3, read=3,
        backoff_factor=0.5,                       # sleep: 0, 1, 2, 4... *factor
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    s = requests.Session()
    ad = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    s.mount("https://", ad)
    s.mount("http://", ad)
    return s
```

Disabling TLS warnings (only for dev with self-signed certs; not for prod):

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.get(url, verify=False)                    # prefer verify="/path/to/ca.pem"
```

### Practical A: website health checker

```python
#!/usr/bin/env python3
import sys, time, requests
from concurrent.futures import ThreadPoolExecutor

SITES = {
    "homepage": "https://example.com",
    "api":      "https://httpbin.org/status/200",
    "broken":   "https://httpbin.org/status/503",
}

def check(item):
    name, url = item
    t = time.perf_counter()
    try:
        r = requests.get(url, timeout=(3, 8))
        ms = (time.perf_counter() - t) * 1000
        return name, r.status_code, ms, r.ok
    except requests.RequestException as e:
        return name, type(e).__name__, (time.perf_counter() - t) * 1000, False

with ThreadPoolExecutor(8) as ex:
    results = list(ex.map(check, SITES.items()))

failed = 0
for name, status, ms, ok in results:
    print(f"{'OK  ' if ok else 'FAIL'} {name:<10} {status!s:<20} {ms:7.0f} ms")
    failed += not ok
sys.exit(1 if failed else 0)
```

### Practical B: REST API automation (create, read, delete) with retries

```python
import os, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Api:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/")
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"
        self.s.mount("https://", HTTPAdapter(max_retries=Retry(
            total=4, backoff_factor=1, status_forcelist=[429, 502, 503, 504],
            allowed_methods=["GET", "PUT", "DELETE"])))

    def _req(self, method, path, **kw):
        r = self.s.request(method, f"{self.base}{path}", timeout=15, **kw)
        r.raise_for_status()
        return r.json() if r.content else None

    def list(self, path):  return self._req("GET", path)
    def create(self, path, body): return self._req("POST", path, json=body)
    def delete(self, path): return self._req("DELETE", path)

api = Api("https://api.example.com/v1", os.environ["API_TOKEN"])
```

### Pitfalls
- No timeout means infinite hang. Always pass `timeout=`.
- `r.json()` raises if the body isn't JSON; check `r.headers["Content-Type"]`/status first.
- Don't retry non-idempotent `POST` blindly (duplicate creates).
- `verify=False` in production defeats TLS.
- Use a `Session` for many calls to the same host.

---

## 10. logging

**What:** The standard library's logging framework: levels, formatters, handlers (console, file, syslog), hierarchy. Essential for any script that runs unattended (cron, CI, services).
**Docs:** https://docs.python.org/3/library/logging.html

> ⚠️ The PyPI link `pypi.org/project/logging` is an old, unrelated third-party package.
> **Do not `pip install logging`.** The real module is built in: just `import logging`.

### Concepts

- **Logger**: what you call (`log.info(...)`). Named hierarchically (`app.db` is a child of `app`).
- **Handler**: where records go (stream, file, rotating file, syslog, HTTP).
- **Formatter**: how a record looks.
- **Level**: `DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)`.

### Basic usage

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
log = logging.getLogger(__name__)      # one logger per module

log.info("deploy started version=%s env=%s", "1.4.2", "prod")   # use %s args, not f-strings
log.warning("retrying (%d/%d)", 2, 5)
try:
    risky()
except Exception:
    log.exception("deploy failed")      # logs ERROR + traceback
```

Useful format fields: `%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d %(funcName)s %(process)d %(threadName)s`.

### File logging with rotation

```python
import logging, sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SysLogHandler

def setup(name: str = "ops", logfile: str = "ops.log", level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()                      # avoid duplicate handlers on re-import
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)

    fileh = RotatingFileHandler(logfile, maxBytes=10_000_000, backupCount=5)   # 10MB x 5
    fileh.setFormatter(fmt)

    # daily rotation, keep 14 days
    # fileh = TimedRotatingFileHandler(logfile, when="midnight", backupCount=14)
    # syslog = SysLogHandler(address="/dev/log")

    logger.addHandler(console)
    logger.addHandler(fileh)
    logger.propagate = False
    return logger

log = setup()
log.info("hello")
```

### JSON logs (for ELK / Loki / CloudWatch)

```python
import json, logging

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        payload.update(getattr(record, "extra_fields", {}))
        return json.dumps(payload)

h = logging.StreamHandler()
h.setFormatter(JsonFormatter())
logging.getLogger().addHandler(h)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("x").info("deployed", extra={"extra_fields": {"service": "api", "version": "1.2"}})
```
In containers: log to **stdout/stderr** and let Docker/Kubernetes collect it.

### Practical A: script that logs to console and file, with levels from the CLI

```python
#!/usr/bin/env python3
import argparse, logging, sys
from logging.handlers import RotatingFileHandler

def configure(verbose: int, logfile: str | None):
    level = [logging.WARNING, logging.INFO, logging.DEBUG][min(verbose, 2)]
    handlers = [logging.StreamHandler(sys.stderr)]
    if logfile:
        handlers.append(RotatingFileHandler(logfile, maxBytes=5_000_000, backupCount=3))
    logging.basicConfig(level=level, handlers=handlers,
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")

log = logging.getLogger("backup")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="count", default=0)
    ap.add_argument("--logfile")
    a = ap.parse_args()
    configure(a.verbose, a.logfile)
    log.debug("args=%s", a)
    log.info("backup started")
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("backup failed")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
```
Try: `python backup.py -vv --logfile backup.log`

### Practical B: redact secrets from logs

```python
import logging, re

class RedactFilter(logging.Filter):
    PAT = re.compile(r"(?i)(password|token|secret|api[_-]?key)=\S+")
    def filter(self, record):
        record.msg = self.PAT.sub(r"\1=***", str(record.msg))
        return True

h = logging.StreamHandler()
h.addFilter(RedactFilter())
logging.basicConfig(level=logging.INFO, handlers=[h])
logging.info("connecting password=hunter2 token=abc123")   # -> password=*** token=***
```

### Pitfalls
- Calling `basicConfig` after handlers exist does nothing (unless `force=True`).
- Adding handlers inside functions called repeatedly yields duplicate lines.
- Libraries should **not** configure logging; only your application's entry point does.
- Use `log.info("x=%s", x)` rather than f-strings so formatting is skipped if the level is disabled.
- Never log secrets, tokens, or full request bodies with PII.

---

## 11. getpass

**What:** Prompt for a password without echoing it, and get the current username.
**Docs:** https://docs.python.org/3/library/getpass.html

```python
import getpass

pw = getpass.getpass("Password: ")            # nothing is displayed as you type
user = getpass.getuser()                       # login name (env LOGNAME/USER/..., or pwd db)
pw2 = getpass.getpass(prompt="Confirm: ", stream=None)
```

### Practical A: safe credential prompt with env var fallback (CI-friendly)

```python
import getpass, os, sys

def get_secret(env_name: str, prompt: str) -> str:
    val = os.environ.get(env_name)
    if val:
        return val                                  # automation: provided via environment
    if sys.stdin.isatty():
        return getpass.getpass(prompt)              # human: hidden prompt
    sys.exit(f"{env_name} not set and no TTY available for a prompt")

db_pw = get_secret("DB_PASSWORD", "Database password: ")
```

### Practical B: confirm + minimum-strength password change tool

```python
import getpass, sys

def new_password() -> str:
    while True:
        a = getpass.getpass("New password: ")
        b = getpass.getpass("Repeat: ")
        if a != b:
            print("Passwords differ, try again."); continue
        if len(a) < 12:
            print("Use at least 12 characters."); continue
        return a
```

### Pitfalls
- `input()` echoes. Never use it for secrets.
- Without a TTY (cron, CI, `docker run` without `-it`) `getpass` falls back and warns, so use env vars or a secret manager there.
- Never pass passwords as command-line arguments; they are visible in `ps`.
- Don't print or log what `getpass` returns.

---

## 12. boto3

**What:** The AWS SDK for Python: automate EC2, S3, IAM, RDS, Lambda, CloudWatch, SSM and everything else.
**Install:** `pip install boto3` · **Docs:** https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

### Authentication (order boto3 searches)

1. Explicit parameters in code (avoid)
2. Environment: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_PROFILE`, `AWS_REGION`
3. Shared files: `~/.aws/credentials` and `~/.aws/config` (`aws configure`)
4. SSO profiles (`aws sso login`)
5. IAM role (EC2 instance profile, ECS task role, EKS IRSA, Lambda role). **Best practice**, since no long-lived keys exist.

Never hard-code keys. Give the principal least privilege.

### Clients vs resources, sessions

```python
import boto3

session = boto3.Session(profile_name="dev", region_name="eu-west-1")
ec2 = session.client("ec2")          # low-level, 1:1 with API, returns dicts (full coverage)
s3 = session.resource("s3")          # object-oriented (older, in maintenance mode; clients are preferred)
sts = session.client("sts")
print(sts.get_caller_identity()["Arn"])      # "who am I?" Always a good first call
```

### Pagination, waiters, errors

```python
from botocore.exceptions import ClientError, NoCredentialsError, WaiterError

# Paginators: many APIs return max 1000/100 items per call
s3c = boto3.client("s3")
paginator = s3c.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket="my-bucket", Prefix="logs/"):
    for obj in page.get("Contents", []):
        print(obj["Key"], obj["Size"])

# Waiters: block until a state is reached
ec2.get_waiter("instance_running").wait(InstanceIds=["i-0abc"], WaiterConfig={"Delay": 5, "MaxAttempts": 40})

# Errors
try:
    boto3.client("s3").head_bucket(Bucket="nope")
except ClientError as e:
    code = e.response["Error"]["Code"]          # 'NoSuchBucket', '403', 'AccessDenied'...
    print(code, e.response["Error"]["Message"])
except NoCredentialsError:
    print("no AWS credentials found")
```

Retries/timeouts config:

```python
from botocore.config import Config
cfg = Config(retries={"max_attempts": 10, "mode": "adaptive"},
             connect_timeout=5, read_timeout=30, region_name="eu-west-1")
ec2 = boto3.client("ec2", config=cfg)
```

### Core examples

```python
import boto3
s3 = boto3.client("s3")

# S3
s3.upload_file("backup.tgz", "my-bucket", "backups/2025-10-10.tgz")       # handles multipart
s3.download_file("my-bucket", "backups/2025-10-10.tgz", "restore.tgz")
s3.put_object(Bucket="my-bucket", Key="hello.txt", Body=b"hi", ServerSideEncryption="AES256")
s3.delete_object(Bucket="my-bucket", Key="hello.txt")
url = s3.generate_presigned_url("get_object",
        Params={"Bucket": "my-bucket", "Key": "report.pdf"}, ExpiresIn=3600)

# EC2
ec2 = boto3.client("ec2")
resp = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
for res in resp["Reservations"]:
    for i in res["Instances"]:
        tags = {t["Key"]: t["Value"] for t in i.get("Tags", [])}
        print(i["InstanceId"], i["InstanceType"], tags.get("Name"))
ec2.stop_instances(InstanceIds=["i-0abc"])
ec2.create_tags(Resources=["i-0abc"], Tags=[{"Key": "Owner", "Value": "devops"}])

# SSM Parameter Store / Secrets Manager
ssm = boto3.client("ssm")
val = ssm.get_parameter(Name="/prod/db/password", WithDecryption=True)["Parameter"]["Value"]
sm = boto3.client("secretsmanager")
secret = sm.get_secret_value(SecretId="prod/db")["SecretString"]

# CloudWatch metric
cw = boto3.client("cloudwatch")
cw.put_metric_data(Namespace="MyApp", MetricData=[{"MetricName": "Deployments", "Value": 1, "Unit": "Count"}])

# Lambda
lam = boto3.client("lambda")
import json
out = lam.invoke(FunctionName="my-fn", Payload=json.dumps({"x": 1}).encode())
print(json.loads(out["Payload"].read()))
```

### Practical A: stop dev instances outside working hours (with safety)

```python
#!/usr/bin/env python3
"""Stop running EC2 instances tagged Env=dev and AutoStop=true."""
import argparse, boto3, logging
from botocore.exceptions import ClientError

log = logging.getLogger("autostop")

def find(ec2):
    pages = ec2.get_paginator("describe_instances").paginate(Filters=[
        {"Name": "tag:Env", "Values": ["dev"]},
        {"Name": "tag:AutoStop", "Values": ["true"]},
        {"Name": "instance-state-name", "Values": ["running"]},
    ])
    return [i["InstanceId"] for p in pages for r in p["Reservations"] for i in r["Instances"]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="eu-west-1")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    ec2 = boto3.client("ec2", region_name=a.region)
    ids = find(ec2)
    log.info("matched %d instance(s): %s", len(ids), ids)
    if not ids:
        return
    try:
        ec2.stop_instances(InstanceIds=ids, DryRun=not a.apply)     # AWS-native dry run
    except ClientError as e:
        if e.response["Error"]["Code"] == "DryRunOperation":
            log.info("dry-run OK. Re-run with --apply to stop them")
        else:
            raise
    else:
        log.info("stop requested")

if __name__ == "__main__":
    main()
```
Schedule it with cron (section 7) or EventBridge + Lambda.

### Practical B: S3 backup uploader with retention

```python
import boto3, datetime as dt, subprocess, tempfile, pathlib

BUCKET, PREFIX, KEEP_DAYS = "my-backups", "db/", 14
s3 = boto3.client("s3")

def backup():
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    with tempfile.TemporaryDirectory() as d:
        out = pathlib.Path(d) / f"db-{stamp}.sql.gz"
        with out.open("wb") as f:
            dump = subprocess.Popen(["pg_dump", "mydb"], stdout=subprocess.PIPE)
            gz = subprocess.Popen(["gzip", "-c"], stdin=dump.stdout, stdout=f)
            dump.stdout.close(); gz.wait(); dump.wait()
            if dump.returncode or gz.returncode:
                raise RuntimeError("dump failed")
        s3.upload_file(str(out), BUCKET, f"{PREFIX}{out.name}",
                       ExtraArgs={"ServerSideEncryption": "AES256"})

def prune():
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=KEEP_DAYS)
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        old = [{"Key": o["Key"]} for o in page.get("Contents", []) if o["LastModified"] < cutoff]
        if old:
            s3.delete_objects(Bucket=BUCKET, Delete={"Objects": old})

backup(); prune()
```
Prefer an S3 lifecycle rule for retention in real setups; this shows the API.

### Practical C: audit report: public S3 buckets and untagged instances

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
for b in s3.list_buckets()["Buckets"]:
    name = b["Name"]
    try:
        cfg = s3.get_public_access_block(Bucket=name)["PublicAccessBlockConfiguration"]
        blocked = all(cfg.values())
    except ClientError as e:
        blocked = False if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration" else None
    print(f"{name:<40} public-access-fully-blocked={blocked}")
```

### Practical D: multi-region sweep

```python
import boto3
regions = [r["RegionName"] for r in boto3.client("ec2", region_name="us-east-1").describe_regions()["Regions"]]
for region in regions:
    ec2 = boto3.client("ec2", region_name=region)
    n = sum(len(r["Instances"]) for p in ec2.get_paginator("describe_instances").paginate()
            for r in p["Reservations"])
    print(f"{region:<18} {n} instances")
```

### Testing boto3 code

```python
# pip install "moto[s3]"
import boto3
from moto import mock_aws

@mock_aws
def test_upload():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="b")
    s3.put_object(Bucket="b", Key="k", Body=b"x")
    assert s3.get_object(Bucket="b", Key="k")["Body"].read() == b"x"
```

### Pitfalls
- Forgetting **pagination**: you silently see only the first 1000 S3 keys or first page of instances.
- Region mismatch ("resource not found" often means wrong region).
- `ClientError` is the one exception for service errors; inspect `e.response["Error"]["Code"]`.
- Tests that hit real AWS cost money and are flaky. Use `moto` or stubs.
- Hard-coded credentials leak. Use roles/SSO.
- Use `DryRun=True` where supported (EC2) before destructive actions.

---

## 13. paramiko

**What:** Pure-Python SSHv2: run remote commands, transfer files via SFTP, tunnel ports. Good for agentless server automation when you don't want Ansible's overhead.
**Install:** `pip install paramiko` · **Docs:** https://www.paramiko.org/

> Authorized servers only. Use **key-based** auth, and verify host keys.

### Connecting

```python
import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()                                  # ~/.ssh/known_hosts
client.set_missing_host_key_policy(paramiko.RejectPolicy())     # secure: unknown host -> error

# For throwaway labs only:
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # blindly trusts: MITM risk

client.connect(
    hostname="10.0.0.12", port=22, username="deploy",
    key_filename="/home/me/.ssh/id_ed25519",     # or pkey=, or password= (avoid)
    timeout=10, banner_timeout=10, auth_timeout=10,
    allow_agent=True, look_for_keys=True,
)
```

### Running commands

```python
stdin, stdout, stderr = client.exec_command("uptime && df -h /", timeout=30)
out = stdout.read().decode()
err = stderr.read().decode()
rc = stdout.channel.recv_exit_status()          # remote exit code
print(rc, out, err)

# sudo needs a TTY unless NOPASSWD is configured
stdin, stdout, stderr = client.exec_command("sudo -n systemctl restart nginx", get_pty=False)

client.close()
```
Use a context manager for safety (`contextlib.closing`) or try/finally.

### SFTP

```python
sftp = client.open_sftp()
sftp.put("local.conf", "/tmp/app.conf")          # upload
sftp.get("/var/log/app.log", "app.log")          # download
for attr in sftp.listdir_attr("/var/log"):
    print(attr.filename, attr.st_size)
sftp.chmod("/tmp/app.conf", 0o640)
sftp.remove("/tmp/old"); sftp.mkdir("/tmp/newdir")
with sftp.open("/tmp/note.txt", "w") as f:
    f.write("hello\n")
sftp.close()
```

### Practical A: a small, reusable SSH helper

```python
import contextlib, paramiko
from dataclasses import dataclass

@dataclass
class Result:
    host: str
    rc: int
    out: str
    err: str

@contextlib.contextmanager
def ssh(host: str, user: str, key: str, port: int = 22):
    c = paramiko.SSHClient()
    c.load_system_host_keys()
    c.set_missing_host_key_policy(paramiko.RejectPolicy())
    c.connect(host, port=port, username=user, key_filename=key, timeout=10)
    try:
        yield c
    finally:
        c.close()

def run(host: str, cmd: str, user="deploy", key="~/.ssh/id_ed25519") -> Result:
    import os
    with ssh(host, user, os.path.expanduser(key)) as c:
        _, so, se = c.exec_command(cmd, timeout=60)
        out, err = so.read().decode(), se.read().decode()
        return Result(host, so.channel.recv_exit_status(), out.strip(), err.strip())

if __name__ == "__main__":
    r = run("10.0.0.12", "hostname; uptime")
    print(r.rc, r.out)
```

### Practical B: run a command on many servers in parallel

```python
from concurrent.futures import ThreadPoolExecutor

HOSTS = ["10.0.0.11", "10.0.0.12", "10.0.0.13"]

def safe(host):
    try:
        return run(host, "systemctl is-active nginx")
    except Exception as e:
        return Result(host, -1, "", f"{type(e).__name__}: {e}")

with ThreadPoolExecutor(10) as pool:
    for r in pool.map(safe, HOSTS):
        status = "OK " if r.rc == 0 else "BAD"
        print(f"{status} {r.host:<14} {r.out or r.err}")
```

### Practical C: push a config and reload a service

```python
def deploy_config(host: str, local: str, remote: str, service: str):
    with ssh(host, "deploy", "/home/me/.ssh/id_ed25519") as c:
        sftp = c.open_sftp()
        tmp = remote + ".new"
        sftp.put(local, tmp)
        sftp.close()
        for cmd in (
            f"sudo -n nginx -t -c {tmp}" if service == "nginx" else "true",   # validate first
            f"sudo -n mv {tmp} {remote}",
            f"sudo -n systemctl reload {service}",
        ):
            _, so, se = c.exec_command(cmd, timeout=30)
            if so.channel.recv_exit_status() != 0:
                raise RuntimeError(f"{host}: '{cmd}' failed: {se.read().decode()}")
```

### Practical D: collect log tails from servers into local files

```python
import pathlib
out_dir = pathlib.Path("collected"); out_dir.mkdir(exist_ok=True)
for h in HOSTS:
    r = run(h, "sudo -n tail -n 200 /var/log/syslog")
    (out_dir / f"{h}.log").write_text(r.out)
```

### Pitfalls
- `AutoAddPolicy` accepts any host key (man-in-the-middle risk). Keep `RejectPolicy` and manage `known_hosts`.
- Without `timeout`, a dead host blocks your script.
- Read both stdout and stderr; huge output on one can block the channel. For large output stream it or redirect on the remote side.
- Each `exec_command` is a **new shell**: `cd` and `export` don't persist across calls. Chain with `&&`.
- Passwords in code are a bad idea. Use keys and an agent.
- For fleets and idempotent config management, Ansible (which itself is Python) is usually better; paramiko is for custom glue.

---

## 14. JSON

**What:** The universal data format for APIs, `aws ... --output json`, `kubectl -o json`, `terraform show -json`, `docker inspect`, and config files.
**Docs:** https://docs.python.org/3/library/json.html

### Key APIs

```python
import json

obj = json.loads('{"a": 1, "b": [true, null, 3.5], "c": {"d": "x"}}')   # str  -> Python
text = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)     # Python -> str
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(obj, f, indent=2)                                          # Python -> file
with open("data.json", encoding="utf-8") as f:
    obj = json.load(f)                                                   # file -> Python
```

Type mapping: object↔dict, array↔list, string↔str, number↔int/float, true/false↔True/False, null↔None.

Errors and custom types:

```python
try:
    json.loads("{bad json}")
except json.JSONDecodeError as e:
    print(e.msg, "line", e.lineno, "col", e.colno)

import datetime as dt
def default(o):
    if isinstance(o, (dt.datetime, dt.date)): return o.isoformat()
    if isinstance(o, set): return sorted(o)
    raise TypeError(f"not serializable: {type(o)}")
json.dumps({"when": dt.datetime.now(), "tags": {"a", "b"}}, default=default)
```

JSON Lines (one JSON object per line, ideal for logs and big streams):

```python
with open("events.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({"event": "deploy", "ok": True}) + "\n")

with open("events.jsonl", encoding="utf-8") as f:
    events = [json.loads(line) for line in f if line.strip()]
```

CLI pretty-printer: `curl -s api | python -m json.tool`.

### Practical A: parse `aws ec2 describe-instances` output

```python
import json, subprocess

raw = subprocess.run(
    ["aws", "ec2", "describe-instances", "--output", "json"],
    capture_output=True, text=True, check=True, timeout=60).stdout
data = json.loads(raw)

rows = []
for res in data["Reservations"]:
    for i in res["Instances"]:
        tags = {t["Key"]: t["Value"] for t in i.get("Tags", [])}
        rows.append((i["InstanceId"], i["State"]["Name"], i["InstanceType"], tags.get("Name", "-")))

for r in sorted(rows, key=lambda r: r[3]):
    print("{:<20} {:<10} {:<12} {}".format(*r))
```

### Practical B: safely read nested data (a `jq` substitute)

```python
def dig(obj, path: str, default=None):
    """dig(data, "spec.containers.0.image")"""
    cur = obj
    for key in path.split("."):
        try:
            cur = cur[int(key)] if isinstance(cur, list) else cur[key]
        except (KeyError, IndexError, ValueError, TypeError):
            return default
    return cur

pod = json.loads(subprocess.check_output(["kubectl", "get", "pod", "mypod", "-o", "json"], text=True))
print(dig(pod, "spec.containers.0.image"))
```

### Practical C: merge and validate configuration files

```python
import json
from pathlib import Path

def deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out

base = json.loads(Path("base.json").read_text())
env = json.loads(Path("prod.json").read_text())
final = deep_merge(base, env)

required = {"host", "port", "db"}
if missing := required - final.keys():
    raise SystemExit(f"config missing keys: {sorted(missing)}")
Path("final.json").write_text(json.dumps(final, indent=2, sort_keys=True))
```

### Pitfalls
- JSON keys must be strings. `{1: "a"}` becomes `{"1": "a"}` after a round trip.
- No comments or trailing commas in JSON (use JSON5/YAML if you need comments).
- Big integers and floats may lose precision in other languages.
- Don't `eval()` JSON-like text; use `json.loads`.
- Large files: stream as JSONL or use `ijson` instead of loading everything.

---

## 15. PyYAML

**What:** Parse and generate YAML: Kubernetes manifests, Docker Compose, Ansible playbooks, GitHub Actions, Helm values, Prometheus rules.
**Install:** `pip install pyyaml` · **Docs:** https://pyyaml.org/wiki/PyYAMLDocumentation

### Key APIs

```python
import yaml

doc = yaml.safe_load("""
name: web
replicas: 3
ports: [80, 443]
env:
  LOG_LEVEL: info
enabled: true
""")
# {'name': 'web', 'replicas': 3, 'ports': [80, 443], 'env': {'LOG_LEVEL': 'info'}, 'enabled': True}

with open("values.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

# Multi-document files (--- separated), e.g. k8s manifests
with open("all.yaml", encoding="utf-8") as f:
    docs = [d for d in yaml.safe_load_all(f) if d]

# Writing
text = yaml.safe_dump(cfg, sort_keys=False, default_flow_style=False, indent=2)
with open("out.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(cfg, f, sort_keys=False)
yaml.safe_dump_all(docs, open("multi.yaml", "w"), sort_keys=False)

# Errors
try:
    yaml.safe_load("a: [1, 2")
except yaml.YAMLError as e:
    print("bad YAML:", e)        # includes line/column
```

### Always `safe_load`

`yaml.load()` / `yaml.unsafe_load()` can construct arbitrary Python objects, which means **code execution** from a malicious file. Use `safe_load` / `safe_load_all` / `safe_dump` for anything you didn't write yourself.

### YAML gotchas (YAML 1.1 as implemented by PyYAML)

```python
yaml.safe_load("country: no")        # {'country': False}   "Norway problem": quote it: "no"
yaml.safe_load("version: 1.10")      # {'version': 1.1}     quote: "1.10"
yaml.safe_load("id: 0123")           # {'id': 83}           leading 0 = octal; quote it
yaml.safe_load("on: push")           # {True: 'push'}       "on" is boolean! (GitHub Actions)
```
Always quote ambiguous strings. Comments are lost on a load/dump round trip. Use `ruamel.yaml` if you must preserve comments and ordering.

### Practical A: modify image tags in all Kubernetes manifests

```python
import sys, yaml
from pathlib import Path

NEW_TAG = sys.argv[1]               # e.g. 1.5.0
for path in Path("k8s").glob("*.y*ml"):
    docs = list(yaml.safe_load_all(path.read_text()))
    changed = False
    for d in docs:
        if d and d.get("kind") == "Deployment":
            for c in d["spec"]["template"]["spec"]["containers"]:
                if c["image"].startswith("myrepo/api:"):
                    c["image"] = f"myrepo/api:{NEW_TAG}"
                    changed = True
    if changed:
        path.write_text(yaml.safe_dump_all(docs, sort_keys=False))
        print("updated", path)
```

### Practical B: validate manifests against policy (CI gate)

```python
import sys, yaml
from pathlib import Path

errors = []
for p in Path("k8s").rglob("*.yaml"):
    for d in yaml.safe_load_all(p.read_text()):
        if not d or d.get("kind") != "Deployment":
            continue
        name = d["metadata"]["name"]
        for c in d["spec"]["template"]["spec"]["containers"]:
            if c["image"].endswith(":latest") or ":" not in c["image"]:
                errors.append(f"{p}:{name}: image must be pinned, got {c['image']}")
            if "resources" not in c or "limits" not in c["resources"]:
                errors.append(f"{p}:{name}: container {c['name']} has no resource limits")
            sc = c.get("securityContext", {})
            if sc.get("privileged"):
                errors.append(f"{p}:{name}: privileged container")
print("\n".join(errors) or "policy OK")
sys.exit(1 if errors else 0)
```

### Practical C: generate an inventory/config from data

```python
import yaml

servers = [{"name": f"web{i}", "ip": f"10.0.1.{i}"} for i in range(1, 4)]
inventory = {"all": {"children": {"web": {"hosts": {s["name"]: {"ansible_host": s["ip"]} for s in servers}}}}}
print(yaml.safe_dump(inventory, sort_keys=False))
```

### Practical D: docker-compose to environment overrides

```python
import yaml
compose = yaml.safe_load(open("docker-compose.yml"))
for svc, spec in compose["services"].items():
    print(svc, "->", spec.get("image"), spec.get("ports", []))
```

### Pitfalls
- `yaml.load` without a Loader is unsafe and deprecated.
- Indentation is meaningful. Never use tabs.
- Booleans/versions/octals mis-typed (see above).
- Round-tripping loses comments; use `ruamel.yaml` for that.
- For validation beyond "is it valid YAML", add a schema check (`jsonschema`, `pydantic`).

---

## 16. pandas

**What:** Tabular data analysis. In DevOps: crunch CSV/JSON/Excel exports (cloud cost reports, inventory, access logs, test results), build reports, find anomalies.
**Install:** `pip install pandas openpyxl` (openpyxl for Excel) · **Docs:** https://pandas.pydata.org/

### Core ideas
- **DataFrame** = table, **Series** = one column.
- Think in columns/vectorised operations, not loops.

### Key APIs

```python
import pandas as pd

df = pd.read_csv("servers.csv", parse_dates=["created"])     # also read_json, read_excel, read_sql
df.head(); df.tail(); df.shape; df.columns; df.dtypes; df.info(); df.describe()

# Select
df["cpu"]; df[["host", "cpu"]]
df.loc[df["cpu"] > 80]                       # filter rows
df.query("cpu > 80 and env == 'prod'")
df.loc[0, "host"]; df.iloc[0, 1]

# Create / modify
df["mem_gb"] = df["mem_mb"] / 1024
df["state"] = df["cpu"].apply(lambda v: "hot" if v > 80 else "ok")
df = df.rename(columns={"hostname": "host"}).drop(columns=["junk"])
df["env"] = df["env"].str.lower().str.strip()
df = df.fillna({"owner": "unknown"}).dropna(subset=["host"]).drop_duplicates("host")
df["cpu"] = pd.to_numeric(df["cpu"], errors="coerce")

# Sort, group, aggregate
df.sort_values("cpu", ascending=False)
df.groupby("env")["cpu"].mean()
df.groupby("env").agg(count=("host", "count"), avg_cpu=("cpu", "mean"), max_mem=("mem_gb", "max"))
df.pivot_table(index="env", columns="region", values="cost", aggfunc="sum", fill_value=0)
df["env"].value_counts()

# Combine
pd.merge(servers, owners, on="host", how="left")
pd.concat([df1, df2], ignore_index=True)

# Time series
df.set_index("ts").resample("1h")["cpu"].mean()

# Write
df.to_csv("out.csv", index=False)
df.to_excel("report.xlsx", index=False, sheet_name="servers")
df.to_json("out.json", orient="records", indent=2)
df.to_markdown()                   # needs `tabulate`
```

### Practical A: cloud cost report from a CSV export

Assume `costs.csv` with columns `date,service,team,cost_usd`.

```python
import pandas as pd

df = pd.read_csv("costs.csv", parse_dates=["date"])
df["month"] = df["date"].dt.to_period("M")

by_service = (df.groupby("service")["cost_usd"].sum().sort_values(ascending=False).round(2))
by_team_month = df.pivot_table(index="team", columns="month", values="cost_usd", aggfunc="sum", fill_value=0).round(2)
top_day = df.groupby("date")["cost_usd"].sum().idxmax()

print("Top services:\n", by_service.head(5))
print("\nTeam x month:\n", by_team_month)
print("\nMost expensive day:", top_day.date())

with pd.ExcelWriter("cost_report.xlsx") as xw:
    by_service.to_frame().to_excel(xw, sheet_name="by_service")
    by_team_month.to_excel(xw, sheet_name="team_month")
```

### Practical B: analyze an access-log CSV for error spikes

```python
import pandas as pd
logs = pd.read_csv("access.csv", names=["ts", "ip", "method", "path", "status", "ms"], parse_dates=["ts"])

logs["is_5xx"] = logs["status"].between(500, 599)
per_min = logs.set_index("ts").resample("1min").agg(requests=("status", "size"), errors=("is_5xx", "sum"))
per_min["error_rate"] = (per_min["errors"] / per_min["requests"]).round(3)
print(per_min[per_min["error_rate"] > 0.05])                      # minutes with >5% errors

print(logs.groupby("path")["ms"].describe(percentiles=[.5, .95, .99]).sort_values("95%", ascending=False).head(10))
print(logs["ip"].value_counts().head(10))                         # noisy clients
```

### Practical C: inventory diff (what is in the CMDB but not running?)

```python
import pandas as pd

cmdb = pd.read_csv("cmdb.csv")                 # host,owner
live = pd.read_csv("live_hosts.csv")           # host
m = cmdb.merge(live, on="host", how="outer", indicator=True)
print("In CMDB only (decommissioned?):\n", m[m["_merge"] == "left_only"][["host", "owner"]])
print("Running but untracked (shadow IT):\n", m[m["_merge"] == "right_only"][["host"]])
```

### Practical D: JSON from an API to a CSV report

```python
import pandas as pd, requests
data = requests.get("https://api.github.com/orgs/python/repos?per_page=100", timeout=15).json()
df = pd.json_normalize(data)[["name", "stargazers_count", "open_issues_count", "pushed_at"]]
df.sort_values("stargazers_count", ascending=False).to_csv("repos.csv", index=False)
```

### Pitfalls
- Chained assignment (`df[df.a > 1]["b"] = 0`) doesn't modify `df`; use `df.loc[mask, "b"] = 0`.
- Mixed dtypes from CSVs: pass `dtype=`/`parse_dates=` or use `pd.to_numeric(errors="coerce")`.
- Memory: files larger than RAM need `chunksize=` or tools like Polars/DuckDB.
- It's a heavy dependency; for a 20-line CSV job, the `csv` module is enough.

---

## 17. smtplib

**What:** Send email via SMTP, used for alerts, reports and notifications. Pair with `email.message.EmailMessage` to build messages.
**Docs:** https://docs.python.org/3/library/smtplib.html

### Key APIs

```python
import smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "alerts@example.com"
msg["To"] = "oncall@example.com, team@example.com"
msg["Subject"] = "[ALERT] Disk 93% on web-01"
msg.set_content("Plain text body")
msg.add_alternative("<h2>Disk alert</h2><p><b>93%</b> used</p>", subtype="html")

# Attachment
from pathlib import Path
p = Path("report.csv")
msg.add_attachment(p.read_bytes(), maintype="text", subtype="csv", filename=p.name)

# Option 1: STARTTLS on port 587 (most common)
with smtplib.SMTP("smtp.example.com", 587, timeout=15) as s:
    s.starttls(context=ssl.create_default_context())
    s.login("alerts@example.com", os.environ["SMTP_PASSWORD"])
    s.send_message(msg)

# Option 2: implicit TLS on port 465
with smtplib.SMTP_SSL("smtp.example.com", 465, context=ssl.create_default_context(), timeout=15) as s:
    s.login(user, password)
    s.send_message(msg)
```

Port 25 is for server-to-server relay, typically unauthenticated and blocked by many ISPs/clouds.
Never send mail with plain `SMTP` and `login` without `starttls()` first (credentials would be in clear text).

Local debugging server: `python -m smtpd -c DebuggingServer -n localhost:1025` was removed in 3.12; use `aiosmtpd`:
`pip install aiosmtpd && python -m aiosmtpd -n -l localhost:1025`.

### Gmail / Microsoft 365 notes
- Gmail requires an **App Password** (with 2FA) or OAuth2; "less secure apps" no longer exists.
- Microsoft 365 basic auth for SMTP is being disabled; OAuth2 is the long-term path.
- For production alerting consider a transactional email service (SES, SendGrid, Mailgun) or a proper alert manager.

### Practical A: reusable alert sender

```python
import os, smtplib, ssl, logging
from email.message import EmailMessage

log = logging.getLogger("mail")

def send_mail(subject: str, body: str, to: list[str], html: str | None = None,
              attachments: list[str] = ()) -> None:
    host = os.environ.get("SMTP_HOST", "smtp.example.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]              # never hard-code

    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = user, ", ".join(to), subject
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")
    from pathlib import Path
    for a in attachments:
        p = Path(a)
        msg.add_attachment(p.read_bytes(), maintype="application", subtype="octet-stream", filename=p.name)

    try:
        with smtplib.SMTP(host, port, timeout=20) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(user, password)
            s.send_message(msg)
        log.info("mail sent to %s", to)
    except (smtplib.SMTPException, OSError) as e:
        log.error("mail failed: %s", e)
        raise
```

### Practical B: disk monitor that emails only when a threshold is crossed

```python
import shutil, socket

host = socket.gethostname()
usage = shutil.disk_usage("/")
pct = usage.used / usage.total * 100
if pct > 85:
    send_mail(
        subject=f"[ALERT] {host}: disk {pct:.0f}%",
        body=f"Root filesystem on {host} is {pct:.1f}% full.\nFree: {usage.free/1e9:.1f} GB",
        to=["oncall@example.com"],
    )
```
Run it from cron every 10 minutes. Add a state file to avoid emailing every run (alert fatigue).

### Practical C: daily report with the pandas output attached

```python
import pandas as pd
df = pd.read_csv("costs.csv")
df.groupby("service")["cost_usd"].sum().sort_values(ascending=False).to_csv("daily_cost.csv")
send_mail("Daily cost report", "See attached.", ["finance@example.com"], attachments=["daily_cost.csv"])
```

### Pitfalls
- Always use TLS (`starttls()`/`SMTP_SSL`). Set a `timeout`.
- Header injection: validate any user-provided `Subject`/`To` (reject newlines). `EmailMessage` helps by raising on invalid headers.
- Credentials from env/secret manager, never from source.
- Providers rate-limit and spam-filter. Set a proper `From`, SPF/DKIM on your domain.
- Email is not guaranteed delivery. For critical alerts add a second channel (Slack webhook, PagerDuty).

---

## Capstone: server health and report tool

Combine **os, platform, psutil, subprocess, json, logging, requests, argparse, smtplib, sys**.

```python
#!/usr/bin/env python3
"""
healthcheck.py: collect host health, check URLs and services,
write JSON, optionally email if anything is wrong.

  python healthcheck.py --url https://example.com --service nginx --email ops@example.com -v
"""
from __future__ import annotations
import argparse, json, logging, os, platform, shutil, smtplib, socket, ssl, subprocess, sys
from datetime import datetime, timezone
from email.message import EmailMessage

import psutil
import requests

log = logging.getLogger("healthcheck")
THRESHOLDS = {"cpu": 85.0, "mem": 85.0, "disk": 90.0}

def host_info() -> dict:
    return {"hostname": socket.gethostname(), "os": platform.platform(),
            "python": platform.python_version(), "pid": os.getpid()}

def metrics() -> dict:
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "load1": os.getloadavg()[0] if hasattr(os, "getloadavg") else None,
    }

def check_url(url: str) -> dict:
    try:
        r = requests.get(url, timeout=(3, 8))
        return {"url": url, "status": r.status_code, "ms": round(r.elapsed.total_seconds() * 1000), "ok": r.ok}
    except requests.RequestException as e:
        return {"url": url, "status": type(e).__name__, "ms": None, "ok": False}

def check_service(name: str) -> dict:
    if not shutil.which("systemctl"):
        return {"service": name, "active": None, "ok": True, "note": "systemctl unavailable"}
    p = subprocess.run(["systemctl", "is-active", name], capture_output=True, text=True, timeout=10)
    state = p.stdout.strip()
    return {"service": name, "active": state, "ok": state == "active"}

def evaluate(report: dict) -> list[str]:
    problems = []
    for k, limit in THRESHOLDS.items():
        if report["metrics"][k] > limit:
            problems.append(f"{k} {report['metrics'][k]:.1f}% > {limit}%")
    problems += [f"URL {u['url']} -> {u['status']}" for u in report["urls"] if not u["ok"]]
    problems += [f"service {s['service']} is {s['active']}" for s in report["services"] if not s["ok"]]
    return problems

def send_email(to: str, subject: str, body: str) -> None:
    user, pw = os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"]
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = user, to, subject
    msg.set_content(body)
    with smtplib.SMTP(os.environ.get("SMTP_HOST", "smtp.example.com"), 587, timeout=20) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(user, pw)
        s.send_message(msg)

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--service", action="append", default=[])
    ap.add_argument("--email")
    ap.add_argument("--out", default="-", help="JSON output file, '-' for stdout")
    ap.add_argument("-v", "--verbose", action="count", default=0)
    a = ap.parse_args(argv)

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(a.verbose, 2)],
                        format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)

    report = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "host": host_info(),
        "metrics": metrics(),
        "urls": [check_url(u) for u in a.url],
        "services": [check_service(s) for s in a.service],
    }
    problems = evaluate(report)
    report["problems"] = problems
    log.info("collected report with %d problem(s)", len(problems))

    text = json.dumps(report, indent=2)
    if a.out == "-":
        print(text)
    else:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)

    if problems and a.email:
        try:
            send_email(a.email, f"[ALERT] {report['host']['hostname']}: {len(problems)} problem(s)",
                       "\n".join(problems) + "\n\n" + text)
        except Exception:
            log.exception("could not send email")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
```

**Install it on a schedule** with python-crontab:

```python
from crontab import CronTab
cron = CronTab(user=True)
if not list(cron.find_comment("ops:healthcheck")):
    j = cron.new(command="/opt/venv/bin/python /opt/ops/healthcheck.py "
                         "--url https://example.com --service nginx --email ops@example.com "
                         "--out /var/log/health.json >> /var/log/healthcheck.log 2>&1",
                 comment="ops:healthcheck")
    j.minute.every(5)
    cron.write()
```

**Extension ideas:** push the metrics to CloudWatch with `boto3`, run it on many hosts using `paramiko`, summarise a week of `health.json` files with `pandas`, write tests with `pytest` + `unittest.mock`.

---

## Cheat sheet

| Task | Tool |
|------|------|
| Read env var | `os.environ.get("X", default)` |
| Walk a directory tree | `os.walk()` / `Path.rglob()` |
| What OS/arch am I on? | `platform.system()`, `platform.machine()` |
| Run a command | `subprocess.run([...], capture_output=True, text=True, timeout=, check=)` |
| Exit with status | `sys.exit(code)` |
| CPU / RAM / disk | `psutil.cpu_percent(1)`, `virtual_memory().percent`, `disk_usage("/").percent` |
| Extract with regex | `re.compile(r"...").search(line)` + named groups |
| Schedule a job | `CronTab(user=True).new(...)`, `.setall("*/5 * * * *")`, `cron.write()` |
| Craft packets | `sr1(IP(dst=h)/ICMP())` (root) |
| HTTP with retries | `Session` + `HTTPAdapter(max_retries=Retry(...))` + `timeout=` |
| Structured logs | `logging` + `RotatingFileHandler` |
| Hidden password prompt | `getpass.getpass()` |
| AWS | `boto3.client("s3")`, paginators, waiters, `ClientError` |
| SSH | `paramiko.SSHClient()` + `RejectPolicy` + `exec_command` / `open_sftp` |
| Parse / emit JSON | `json.loads` / `json.dumps(indent=2)` |
| YAML | `yaml.safe_load` / `yaml.safe_dump` |
| Tabular analysis | `pd.read_csv` → `groupby` → `to_excel` |
| Send email | `EmailMessage` + `SMTP.starttls()` + `login` + `send_message` |

---

## DevOps script best practices

1. **Idempotent**: running twice gives the same result (check-then-change, e.g. the cron installer).
2. **Dry-run first**: `--apply` flag for anything destructive; use native dry-runs (`DryRun=True`).
3. **Exit codes**: 0 success, non-zero failure, so cron/CI/monitoring can react.
4. **Timeouts everywhere**: HTTP, SSH, subprocess, sockets.
5. **Log, don't print**: logs to stderr/file with levels; results to stdout.
6. **No secrets in code or logs**: env vars, secret managers, IAM roles.
7. **No `shell=True` with variable data**; validate input.
8. **Least privilege**: don't run as root unless needed; scoped IAM policies.
9. **Handle failure**: retries with backoff for transient errors; fail loudly for permanent ones.
10. **Test**: pytest, mock external systems (`moto`, `unittest.mock`), run linters in CI.
11. **Pin dependencies** (`pip-compile`) and scan them (`pip-audit`).
12. **Document**: a `--help`, a README, and comments that explain *why*.
