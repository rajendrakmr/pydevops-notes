# Python for DevOps --- Complete Practical Learning Guide

A hands-on, production-minded Python curriculum for DevOps, Cloud, SRE,
and infrastructure automation.

This repository covers **all 17 requested modules/libraries** with
concepts, important APIs, runnable examples, real-world use cases,
exercises, security guidance, and an integrated capstone project.

> **Learning approach:** Understand the concept → run the example →
> modify it → handle errors → add logging/tests → use it in a realistic
> workflow. Do not just copy and paste code.

------------------------------------------------------------------------

## Table of contents

-   [1. Learning outcomes](#1-learning-outcomes)
-   [2. Prerequisites](#2-prerequisites)
-   [3. Environment setup](#3-environment-setup)
-   [4. Suggested repository
    structure](#4-suggested-repository-structure)
-   [5. Module 1 --- os](#5-module-1--os-operating-system-interaction)
-   [6. Module 2 ---
    platform](#6-module-2--platform-and-system-identification)
-   [7. Module 3 ---
    subprocess](#7-module-3--subprocess-system-command-execution)
-   [8. Module 4 ---
    sys](#8-module-4--sys-python-runtime-and-cli-basics)
-   [9. Module 5 ---
    psutil](#9-module-5--psutil-system-and-process-monitoring)
-   [10. Module 6 ---
    re](#10-module-6--re-regular-expressions-and-log-parsing)
-   [11. Module 7 ---
    python-crontab](#11-module-7--python-crontab-scheduling-linux-jobs)
-   [12. Module 8 ---
    Scapy](#12-module-8--scapy-network-packet-analysis)
-   [13. Module 9 --- Requests and
    urllib3](#13-module-9--requests-and-urllib3-http-api-automation)
-   [14. Module 10 ---
    logging](#14-module-10--logging-production-logging)
-   [15. Module 11 ---
    getpass](#15-module-11--getpass-secure-interactive-input)
-   [16. Module 12 --- Boto3](#16-module-12--boto3-aws-automation)
-   [17. Module 13 ---
    Paramiko](#17-module-13--paramiko-ssh-and-sftp-automation)
-   [18. Module 14 --- JSON](#18-module-14--json-data-interchange)
-   [19. Module 15 ---
    PyYAML](#19-module-15--pyyaml-yaml-configuration-automation)
-   [20. Module 16 ---
    pandas](#20-module-16--pandas-csv-and-operational-reporting)
-   [21. Module 17 ---
    smtplib](#21-module-17--smtplib-email-notifications)
-   [22. Integrated capstone
    project](#22-integrated-capstone-project--devops-operations-toolkit)
-   [23. Testing, quality, and security
    checklist](#23-testing-quality-and-security-checklist)
-   [24. Troubleshooting](#24-troubleshooting)
-   [25. Practical exercises and portfolio
    milestones](#25-practical-exercises-and-portfolio-milestones)
-   [26. Suggested 15-day study plan](#26-suggested-15-day-study-plan)
-   [27. Official documentation](#27-official-documentation)

------------------------------------------------------------------------

## 1. Learning outcomes

After completing this guide, you should be able to:

1.  Inspect operating-system and Python runtime information.
2.  Create directories, inspect files, and manage environment variables.
3.  Execute Linux commands safely from Python and interpret exit codes.
4.  Monitor CPU, memory, disk, network counters, and processes.
5.  Parse application logs and extract errors, timestamps, and IP-like
    values.
6.  Schedule recurring jobs on Linux using cron.
7.  Inspect network packets in an authorized lab.
8.  Call REST APIs, handle authentication, retries, timeouts, and HTTP
    errors.
9.  Write useful application and automation logs.
10. Accept secrets interactively without echoing them to the terminal.
11. Inventory and operate AWS resources with Boto3 and least-privilege
    IAM.
12. Connect to authorized Linux hosts using SSH/SFTP.
13. Read and write JSON and YAML configuration.
14. Process CSV inventory and monitoring exports with pandas.
15. Send operational email notifications.
16. Combine these skills into a maintainable DevOps automation project.

### Priority for a DevOps job

Learn these especially well:

-   **High priority:** `os`, `subprocess`, `psutil`, `requests`,
    `logging`, JSON, PyYAML, Boto3.
-   **Important:** `platform`, `sys`, `re`, Paramiko, `smtplib`,
    `getpass`.
-   **Specialist / learn fundamentals:** `python-crontab`, Scapy,
    pandas.

------------------------------------------------------------------------

## 2. Prerequisites

You should know basic Python before starting:

-   Variables and data types
-   Strings, numbers, booleans
-   Lists, tuples, sets, dictionaries
-   `if`, `elif`, `else`
-   `for` and `while` loops
-   Functions and return values
-   Imports and modules
-   Exceptions: `try`, `except`, `finally`
-   File handling with `open()`
-   Basic classes and objects
-   Virtual environments and `pip`

You should also be comfortable with basic Linux commands:

``` bash
pwd
ls -la
cd
mkdir
cp
mv
rm
cat
less
grep
find
chmod
chown
ps
top
df -h
free -h
ip addr
curl
systemctl
journalctl
```

------------------------------------------------------------------------

## 3. Environment setup

### 3.1 Linux / Ubuntu

``` bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
python3 --version
pip3 --version

mkdir -p ~/python-for-devops
cd ~/python-for-devops

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
```

### 3.2 Windows PowerShell

``` powershell
py --version
mkdir python-for-devops
cd python-for-devops

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
```

If PowerShell blocks activation, use an approved execution-policy
setting for your environment or activate the environment from Command
Prompt:

``` cmd
.venv\Scripts\activate.bat
```

### 3.3 Install third-party dependencies

``` bash
python -m pip install psutil python-crontab scapy requests urllib3 boto3 paramiko PyYAML pandas
```

Optional development tools:

``` bash
python -m pip install pytest ruff
```

Save dependencies:

``` bash
python -m pip freeze > requirements.txt
```

Install later:

``` bash
python -m pip install -r requirements.txt
```

### 3.4 Standard library versus external packages

These are included with Python and do **not** need `pip install`:

`os`, `platform`, `subprocess`, `sys`, `re`, `logging`, `getpass`,
`json`, `smtplib`, `datetime`, `argparse`, `pathlib`, `shutil`.

Third-party packages in this guide:

`psutil`, `python-crontab`, `scapy`, `requests`, `urllib3`, `boto3`,
`paramiko`, `PyYAML`, `pandas`.

> `logging` is part of Python's standard library. Do not install the
> unrelated package named `logging` from PyPI for normal Python logging.

------------------------------------------------------------------------

## 4. Suggested repository structure

Start with one file per module. As the project grows, separate reusable
code into packages.

``` text
python-for-devops/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── config/
│   └── config.example.yaml
├── examples/
│   ├── 01_os/
│   ├── 02_platform/
│   ├── 03_subprocess/
│   ├── 04_sys/
│   ├── 05_psutil/
│   ├── 06_regex/
│   ├── 07_crontab/
│   ├── 08_scapy/
│   ├── 09_http/
│   ├── 10_logging/
│   ├── 11_getpass/
│   ├── 12_boto3/
│   ├── 13_paramiko/
│   ├── 14_json/
│   ├── 15_yaml/
│   ├── 16_pandas/
│   └── 17_email/
├── src/
│   └── devops_toolkit/
│       ├── __init__.py
│       ├── system_info.py
│       ├── health_check.py
│       ├── command_runner.py
│       ├── log_analyzer.py
│       ├── aws_inventory.py
│       ├── ssh_manager.py
│       ├── report_generator.py
│       └── notifications.py
├── data/
│   └── sample_servers.csv
├── reports/
├── logs/
└── tests/
```

Example `.gitignore`:

``` gitignore
.venv/
__pycache__/
*.py[cod]
.env
*.pem
*.key
.aws/
logs/
reports/
.pytest_cache/
.ruff_cache/
```

Never commit real credentials, private keys, access tokens, production
logs, or sensitive inventory data.

------------------------------------------------------------------------

# 5. Module 1 --- `os`: Operating-system interaction

## What is it?

The `os` module provides operating-system-related functionality. It lets
a Python program inspect the current working directory, list files,
create directories, read environment variables, and interact with paths
and processes.

### Important functions and attributes

  ------------------------------------------------------------------------------------
  API                                  What it does            DevOps example
  ------------------------------------ ----------------------- -----------------------
  `os.getcwd()`                        Returns current working Find where a script is
                                       directory               running

  `os.chdir(path)`                     Changes working         Move to a workspace
                                       directory               

  `os.listdir(path)`                   Lists directory entries Inspect deployment
                                                               files

  `os.scandir(path)`                   Efficient directory     Inventory files
                                       iteration with metadata 

  `os.mkdir(path)`                     Creates one directory   Create a single folder

  `os.makedirs(path, exist_ok=True)`   Creates parent          Create nested
                                       directories too         deployment paths

  `os.remove(path)`                    Deletes a file          Remove a known
                                                               temporary file

  `os.rmdir(path)`                     Removes an empty        Remove an empty
                                       directory               workspace

  `os.rename(src, dst)`                Renames/moves a path    Rename a report

  `os.replace(src, dst)`               Replaces destination    Atomically replace a
                                       where permitted         config file

  `os.path.exists(path)`               Checks whether a path   Check a config file
                                       exists                  

  `os.path.isfile(path)`               Checks whether it is a  Validate an input
                                       file                    

  `os.path.isdir(path)`                Checks whether it is a  Validate a backup
                                       directory               directory

  `os.path.getsize(path)`              Returns file size in    Check log size
                                       bytes                   

  `os.path.abspath(path)`              Returns absolute path   Resolve a path

  `os.path.join(a, b)`                 Joins path components   Build portable paths

  `os.walk(path)`                      Recursively traverses   Find log files
                                       directories             

  `os.getenv(name)`                    Reads an environment    Read environment
                                       variable                configuration

  `os.environ`                         Mapping of environment  Set/read process
                                       variables               configuration

  `os.cpu_count()`                     Logical CPU count, if   Basic host inventory
                                       available               

  `os.getpid()`                        Current process ID      Identify automation
                                                               process
  ------------------------------------------------------------------------------------

### Example 1: Inspect the working directory

``` python
import os

print("Current directory:", os.getcwd())
print("Directory entries:", os.listdir("."))
```

`getcwd()` reports the process's current working directory. It is not
necessarily the directory containing the Python script.

### Example 2: Create a deployment directory tree

``` python
import os

base_dir = os.path.abspath("deployment")

for folder in ("logs", "backup", "config", "scripts"):
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
    print("Ready:", path)
```

`exist_ok=True` prevents an error if the directory already exists. It
does not make an existing file into a directory.

### Example 3: Validate a configuration file

``` python
import os

config_path = os.path.abspath("config/app.yaml")

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration not found: {config_path}")

if not os.path.isfile(config_path):
    raise ValueError(f"Expected a file: {config_path}")

print("Configuration file exists:", os.path.getsize(config_path), "bytes")
```

### Example 4: Read environment variables safely

``` python
import os

environment = os.getenv("APP_ENV", "development")
region = os.getenv("AWS_REGION", "ap-south-1")

print("Environment:", environment)
print("AWS region:", region)
```

Do not print secret environment variables such as passwords or tokens.

### Example 5: Find log files recursively

``` python
import os

log_root = "/var/log"

for root, directories, files in os.walk(log_root):
    for filename in files:
        if filename.endswith(".log"):
            print(os.path.join(root, filename))
```

You may need permission to inspect some system log directories.

### Real-world task

Write a script that creates `/opt/myapp/{logs,backup,config}`, verifies
that each path is a directory, and writes a deployment timestamp to a
log file. Use a test directory first; do not change system directories
without permission.

### Practice

1.  Print the current directory and process ID.
2.  List all entries in a chosen directory.
3.  Create nested directories without failing on a second run.
4.  Find all `.log` files under a sample directory.
5.  Read `APP_ENV` with a default value.
6.  Check whether a path is a file, directory, or missing.
7.  Report the size of each file in a test folder.

### Safety notes

-   Validate paths before deletion or replacement.
-   Avoid running destructive scripts against `/`, `/etc`, `/var`, or
    production paths during practice.
-   Use `pathlib` for many modern path-manipulation tasks; it
    complements `os`.
-   Do not store credentials in source code.

Documentation: https://docs.python.org/3/library/os.html

------------------------------------------------------------------------

# 6. Module 2 --- `platform`: Platform and system identification

## What is it?

The `platform` module identifies the operating system, release, machine
architecture, processor information, hostname, and Python version.

Use it when an automation tool must behave differently on Linux,
Windows, or macOS.

### Important functions

  API                           What it returns
  ----------------------------- -------------------------------------------
  `platform.system()`           OS family, such as Linux, Windows, Darwin
  `platform.release()`          OS release
  `platform.version()`          OS version details
  `platform.platform()`         Combined platform string
  `platform.machine()`          Machine architecture
  `platform.processor()`        Processor description, if available
  `platform.node()`             Network name/hostname
  `platform.python_version()`   Python version
  `platform.architecture()`     Interpreter architecture information

### Example 1: Print system inventory

``` python
import platform

print("OS:", platform.system())
print("Release:", platform.release())
print("Version:", platform.version())
print("Architecture:", platform.machine())
print("Processor:", platform.processor())
print("Hostname:", platform.node())
print("Python:", platform.python_version())
```

### Example 2: Select an OS-specific command

``` python
import platform
import subprocess

system = platform.system()

commands = {
    "Linux": ["uname", "-a"],
    "Darwin": ["uname", "-a"],
    "Windows": ["cmd", "/c", "ver"],
}

command = commands.get(system)

if command is None:
    raise RuntimeError(f"Unsupported operating system: {system}")

result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)

print(result.stdout)
```

### Real-world task

Build a system inventory script that records hostname, OS, release,
architecture, Python version, and timestamp in JSON.

### Practice

1.  Identify whether a script is running on Linux, Windows, or macOS.
2.  Print the architecture and Python version.
3.  Choose a safe read-only command based on the OS.
4.  Save the inventory to a JSON file.

Documentation: https://docs.python.org/3/library/platform.html

------------------------------------------------------------------------

# 7. Module 3 --- `subprocess`: System command execution

## What is it?

`subprocess` runs external programs and commands from Python. It is
essential for automating existing command-line tools such as Git,
Docker, kubectl, Terraform, and Linux utilities.

Prefer `subprocess.run()` for ordinary command execution. Use `Popen()`
when you need more advanced process interaction.

### Important APIs and concepts

  -----------------------------------------------------------------------
  API / option                        Purpose
  ----------------------------------- -----------------------------------
  `subprocess.run()`                  Runs a command and waits for it

  `subprocess.Popen()`                Starts and manages a process

  `capture_output=True`               Captures stdout and stderr

  `text=True`                         Returns text rather than bytes

  `check=True`                        Raises `CalledProcessError` on
                                      non-zero exit

  `timeout=seconds`                   Limits command execution time

  `result.args`                       Command arguments

  `result.returncode`                 Exit status

  `result.stdout`                     Standard output

  `result.stderr`                     Standard error

  `subprocess.PIPE`                   Pipe process input/output

  `subprocess.DEVNULL`                Discard output

  `subprocess.CalledProcessError`     Command failed with non-zero status

  `subprocess.TimeoutExpired`         Command exceeded timeout

  `subprocess.list2cmdline()`         Windows command-line quoting
                                      helper; not a security validator
  -----------------------------------------------------------------------

### Example 1: Run a read-only command

``` python
import subprocess

result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)

print(result.stdout)
print("Exit code:", result.returncode)
```

On Windows, use a Windows-appropriate command such as
`["cmd", "/c", "dir"]`. A command must exist on the host where the
script runs.

### Example 2: Check Docker containers

``` python
import subprocess

try:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )

    containers = result.stdout.splitlines()
    print("Running containers:", containers)

except FileNotFoundError:
    print("Docker CLI is not installed or not on PATH")
except subprocess.CalledProcessError as exc:
    print("Docker command failed:", exc.stderr)
except subprocess.TimeoutExpired:
    print("Docker command timed out")
```

### Example 3: Understand exit codes

``` python
import subprocess

result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    timeout=10,
)

print("Exit code:", result.returncode)
print("Output:", result.stdout or result.stderr)

if result.returncode == 0:
    print("Command succeeded")
else:
    print("Command failed")
```

Conventionally, exit code `0` means success and a non-zero code means
failure.

### Example 4: Fail a CI step on command failure

``` python
import subprocess
import sys

try:
    subprocess.run(
        ["python", "-m", "pytest", "-q"],
        check=True,
        timeout=120,
    )
except subprocess.CalledProcessError as exc:
    print(f"Tests failed with exit code {exc.returncode}")
    sys.exit(exc.returncode)
except subprocess.TimeoutExpired:
    print("Tests timed out")
    sys.exit(124)
```

### Example 5: Use Popen for a long-running process

``` python
import subprocess

process = subprocess.Popen(
    ["python", "-u", "-c", "import time; print('started'); time.sleep(2); print('finished')"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

for line in process.stdout:
    print("CHILD:", line.rstrip())

return_code = process.wait(timeout=10)
print("Exit code:", return_code)
```

For long-running processes, consider output buffering, process cleanup,
timeouts, and how you handle termination.

### Real-world task

Create a deployment checker that runs `git --version`,
`docker --version`, and `kubectl version --client`, records each
command's exit status, and exits non-zero if a required tool is missing.

### Practice

1.  Run `df -h` and print the output.
2.  Run a command that does not exist and handle `FileNotFoundError`.
3.  Run a command with `check=True` and handle failure.
4.  Add a timeout.
5.  Check Docker CLI availability.
6.  Run a test command and propagate its exit code to a CI pipeline.

### Security rules

-   Pass commands as a list, for example `["git", "status"]`.
-   Avoid `shell=True` unless there is a clear, reviewed requirement.
-   Never concatenate untrusted user input into shell commands.
-   Use timeouts and check return codes.
-   Run with the least privileges necessary.

Documentation: https://docs.python.org/3/library/subprocess.html

------------------------------------------------------------------------

# 8. Module 4 --- `sys`: Python runtime and CLI basics

## What is it?

The `sys` module provides access to Python interpreter details and
runtime behavior.

### Important APIs

  API                    Purpose
  ---------------------- ----------------------------------
  `sys.version`          Python version string
  `sys.version_info`     Structured version information
  `sys.executable`       Current Python executable
  `sys.argv`             Command-line arguments
  `sys.exit(code)`       Exit with a status
  `sys.path`             Module search paths
  `sys.platform`         Platform identifier
  `sys.stdin`            Standard input
  `sys.stdout`           Standard output
  `sys.stderr`           Standard error
  `sys.getsizeof(obj)`   Approximate object size in bytes

### Example 1: Check interpreter and version

``` python
import sys

print("Python:", sys.version)
print("Executable:", sys.executable)
print("Platform:", sys.platform)
print("Module paths:", sys.path)
```

Avoid dumping `sys.path` in routine production logs if it exposes
internal filesystem details unnecessarily.

### Example 2: Read command-line arguments

Create `hello.py`:

``` python
import sys

print("Script:", sys.argv[0])
print("Arguments:", sys.argv[1:])
```

Run:

``` bash
python hello.py production ap-south-1
```

For production-grade command-line interfaces, prefer `argparse` (covered
in the Python standard library, though not one of the 17 requested
modules).

### Example 3: Return a failure status

``` python
import sys

deployment_successful = False

if not deployment_successful:
    print("Deployment failed", file=sys.stderr)
    sys.exit(1)

sys.exit(0)
```

### Real-world task

Create a CLI script that accepts an environment name, validates it,
prints a result, and returns exit code `1` for invalid input.

### Practice

1.  Print the Python executable.
2.  Check the Python major/minor version.
3.  Accept two command-line arguments.
4.  Print errors to stderr.
5.  Return non-zero when a required argument is missing.

Documentation: https://docs.python.org/3/library/sys.html

------------------------------------------------------------------------

# 9. Module 5 --- `psutil`: System and process monitoring

## What is it?

`psutil` (process and system utilities) provides information about CPU,
memory, disks, network counters, boot time, users, and processes.

Install:

``` bash
python -m pip install psutil
```

### Important APIs

  API                                Purpose
  ---------------------------------- -----------------------------
  `psutil.cpu_percent(interval=1)`   CPU utilization
  `psutil.cpu_count()`               CPU count
  `psutil.cpu_times()`               CPU time statistics
  `psutil.virtual_memory()`          RAM statistics
  `psutil.swap_memory()`             Swap statistics
  `psutil.disk_usage(path)`          Disk usage
  `psutil.disk_partitions()`         Mounted partitions
  `psutil.disk_io_counters()`        Disk I/O counters
  `psutil.net_io_counters()`         Network I/O counters
  `psutil.net_if_addrs()`            Network interface addresses
  `psutil.net_if_stats()`            Network interface status
  `psutil.process_iter()`            Iterate over processes
  `psutil.pids()`                    Process IDs
  `psutil.boot_time()`               System boot timestamp
  `psutil.users()`                   Logged-in users

### Example 1: CPU monitoring

``` python
import psutil

cpu_percent = psutil.cpu_percent(interval=1)
print(f"CPU usage: {cpu_percent}%")

if cpu_percent > 80:
    print("WARNING: CPU usage is above 80%")
else:
    print("CPU usage is within the configured threshold")
```

The `interval=1` parameter measures utilization over a one-second
interval. A first non-blocking measurement may not be meaningful.

### Example 2: Memory and swap

``` python
import psutil

memory = psutil.virtual_memory()
swap = psutil.swap_memory()

print(f"Total RAM: {memory.total / (1024 ** 3):.2f} GiB")
print(f"Available RAM: {memory.available / (1024 ** 3):.2f} GiB")
print(f"RAM used: {memory.percent}%")
print(f"Swap used: {swap.percent}%")
```

Use `available` to understand memory that can be made available to
applications; `used` and `free` have OS-specific interpretation.

### Example 3: Disk utilization

``` python
import psutil

for partition in psutil.disk_partitions(all=False):
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print(
            partition.mountpoint,
            f"used={usage.percent}%",
            f"free={usage.free / (1024 ** 3):.2f} GiB",
        )
    except PermissionError:
        print("Permission denied:", partition.mountpoint)
```

### Example 4: Network counters

``` python
import psutil

counters = psutil.net_io_counters()

print("Bytes sent:", counters.bytes_sent)
print("Bytes received:", counters.bytes_recv)
print("Packets sent:", counters.packets_sent)
print("Packets received:", counters.packets_recv)
```

These are cumulative counters since boot or interface initialization. To
calculate throughput, take two samples and divide the byte difference by
elapsed seconds.

### Example 5: Inspect processes

``` python
import psutil

for process in psutil.process_iter(["pid", "name", "username", "memory_info"]):
    try:
        info = process.info
        print(info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
```

Processes can exit while being inspected. Always handle `NoSuchProcess`
and `AccessDenied`.

### Example 6: A simple health report

``` python
import psutil

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent
root_disk = psutil.disk_usage("/").percent

print("SERVER HEALTH")
print(f"CPU: {cpu}%")
print(f"Memory: {memory}%")
print(f"Root disk: {root_disk}%")

problems = []

if cpu > 80:
    problems.append("High CPU")
if memory > 85:
    problems.append("High memory")
if root_disk > 90:
    problems.append("High root disk usage")

if problems:
    print("ALERT:", ", ".join(problems))
else:
    print("Status: OK")
```

### Real-world task

Create a monitoring script that samples CPU, memory, disk, and network
counters every 30 seconds, logs threshold breaches, and exits cleanly on
Ctrl+C.

### Practice

1.  Print CPU count and CPU percentage.
2.  Report RAM and swap usage.
3.  Check every mounted disk.
4.  List the top processes by memory use.
5.  Calculate network bytes per second from two samples.
6.  Write a health report to JSON.
7.  Add warning thresholds through a YAML configuration file.

Documentation: https://github.com/giampaolo/psutil

------------------------------------------------------------------------

# 10. Module 6 --- `re`: Regular expressions and log parsing

## What is it?

Regular expressions (regex) describe text patterns. Use the `re` module
to search logs, extract fields, validate simple formats, and replace
sensitive values.

### Common regex syntax

  Pattern     Meaning
  ----------- -----------------------------------------
  `\d`        Digit
  `\D`        Non-digit
  `\w`        Word character
  `\W`        Non-word character
  `\s`        Whitespace
  `\S`        Non-whitespace
  `.`         Any character except newline by default
  `*`         Zero or more
  `+`         One or more
  `?`         Zero or one
  `{3}`       Exactly three repetitions
  `[0-9]`     One digit from 0 to 9
  `^`         Start of string/line
  `$`         End of string/line
  `(...)`     Capturing group
  `(?:...)`   Non-capturing group
  `\b`        Word boundary
  `|`         Alternation

### Important APIs

  API                Purpose
  ------------------ ------------------------------------
  `re.search()`      Find first match anywhere
  `re.match()`       Match from the start
  `re.fullmatch()`   Require the entire string to match
  `re.findall()`     Return all matches
  `re.finditer()`    Iterate over match objects
  `re.sub()`         Replace matches
  `re.split()`       Split using a pattern
  `re.compile()`     Compile a reusable pattern
  `re.escape()`      Escape literal text for a regex

Use raw strings such as `r"\d+"` to avoid confusion with Python string
escapes.

### Example 1: Find errors in application logs

``` python
import re

logs = """
2026-11-16 INFO Application started
2026-11-16 ERROR Database connection failed
2026-11-16 INFO Health check passed
2026-11-16 ERROR Payment service unavailable
"""

for line in logs.splitlines():
    if re.search(r"\bERROR\b", line):
        print(line)
```

### Example 2: Extract HTTP status codes

``` python
import re

log_line = '10.0.0.8 - - "GET /api/orders HTTP/1.1" 500 120'

match = re.search(r'"\s(\d{3})\s', log_line)

if match:
    status_code = int(match.group(1))
    print("HTTP status:", status_code)
```

### Example 3: Extract IPv4-looking values

``` python
import re

text = "Clients: 192.168.1.10 and 10.0.0.5"

pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
print(re.findall(pattern, text))
```

This identifies IPv4-shaped strings, not necessarily valid IP addresses.
Use Python's `ipaddress` module for actual validation:

``` python
import ipaddress

candidate = "192.168.1.10"
address = ipaddress.ip_address(candidate)
print(address.is_private)
```

### Example 4: Redact a token in logs

``` python
import re

message = "Authorization: Bearer abc123secret"
redacted = re.sub(
    r"(?i)(Bearer\s+)\S+",
    r"\1[REDACTED]",
    message,
)

print(redacted)
```

Do not rely only on regex to prevent secrets from entering logs. Avoid
logging credentials in the first place.

### Example 5: Parse multiple log lines

``` python
import re

pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<level>INFO|WARNING|ERROR) "
    r"(?P<message>.*)"
)

with open("application.log", encoding="utf-8") as file:
    for line in file:
        match = pattern.fullmatch(line.rstrip("\n"))
        if match:
            print(match.groupdict())
```

### Real-world task

Build a log analyzer that counts INFO/WARNING/ERROR entries, extracts
HTTP 4xx/5xx responses, and writes a summary report. Test it with sample
logs containing malformed lines.

### Practice

1.  Extract every ERROR line.
2.  Count HTTP 500 responses.
3.  Extract dates from a sample log.
4.  Redact bearer tokens from test data.
5.  Validate a simple version string.
6.  Explain the difference between `match`, `search`, and `fullmatch`.

Documentation: https://docs.python.org/3/library/re.html

------------------------------------------------------------------------

# 11. Module 7 --- `python-crontab`: Scheduling Linux jobs

## What is cron?

Cron is a Unix-like operating-system scheduler. It runs commands at
specified times. The `python-crontab` package allows Python code to
inspect and manage a user's crontab.

Install:

``` bash
python -m pip install python-crontab
```

On Linux, a cron service/daemon must be available. This package does not
itself provide a scheduler service.

### Cron expression format

``` text
MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK command
```

  Expression      Schedule
  --------------- --------------------------------------
  `* * * * *`     Every minute
  `*/5 * * * *`   Every five minutes
  `0 * * * *`     At the start of every hour
  `0 0 * * *`     Daily at midnight
  `30 2 * * *`    Daily at 02:30
  `0 0 * * 0`     Sunday at midnight
  `0 9 1 * *`     09:00 on the first day of each month

Cron uses the server's configured timezone. Verify it with `timedatectl`
where available.

### Important package APIs

  API                    Purpose
  ---------------------- -------------------------------
  `CronTab(user=True)`   Access current user's crontab
  `cron.new()`           Create a job
  `job.setall()`         Set schedule
  `job.minute.every()`   Set minute interval
  `job.hour.on()`        Set hour
  `job.enable()`         Enable a job
  `job.enable(False)`    Disable a job
  `cron.remove(job)`     Remove a job
  `cron.write()`         Save changes
  `cron.crons`           Iterate over jobs

### Example 1: Create a scheduled health check

``` python
from crontab import CronTab

cron = CronTab(user=True)

job = cron.new(
    command="/home/ubuntu/python-for-devops/.venv/bin/python "
            "/home/ubuntu/python-for-devops/health_check.py "
            ">> /home/ubuntu/python-for-devops/health.log 2>&1",
    comment="python-devops-health-check",
)

job.setall("*/5 * * * *")
cron.write()

print("Health-check cron job saved")
```

Use absolute paths because cron jobs often have a minimal `PATH` and a
different working directory from an interactive shell.

### Example 2: List current user's jobs

``` python
from crontab import CronTab

cron = CronTab(user=True)

for job in cron:
    print(job)
```

### Example 3: Avoid creating duplicate jobs

``` python
from crontab import CronTab

cron = CronTab(user=True)
comment = "python-devops-health-check"

for job in list(cron):
    if job.comment == comment:
        cron.remove(job)

job = cron.new(
    command="/usr/bin/python3 /opt/devops/health_check.py",
    comment=comment,
)
job.setall("*/10 * * * *")

cron.write()
```

### Real-world task

Schedule a health check every five minutes. Log output, prevent
duplicate entries, document how to disable/remove the job, and verify
the job actually ran.

### Practice

1.  Create a job that runs every five minutes.
2.  List existing jobs.
3.  Create a daily backup job.
4.  Prevent duplicate jobs using a comment.
5.  Disable and remove a test job.
6.  Investigate a cron job that works manually but fails under cron.

### Operational cautions

-   Test with a harmless command first.
-   Be careful: `cron.write()` changes the user's actual crontab.
-   Use absolute paths and redirect logs.
-   Consider locking if jobs must not overlap.
-   For complex production workflows, consider systemd timers or an
    orchestrator.

Documentation: https://pypi.org/project/python-crontab/

------------------------------------------------------------------------

# 12. Module 8 --- Scapy: Network packet analysis

## What is it?

Scapy is a Python packet manipulation and analysis library. It can
construct, dissect, send, receive, and inspect network packets.

Use it for authorized troubleshooting labs and packet analysis---not for
scanning or interacting with networks without permission.

Install:

``` bash
python -m pip install scapy
```

### Important functions and layers

  API                  Purpose
  -------------------- -------------------------------
  `Ether()`            Ethernet layer
  `IP()`               IPv4 layer
  `IPv6()`             IPv6 layer
  `TCP()`              TCP layer
  `UDP()`              UDP layer
  `ICMP()`             ICMP layer
  `DNS()`              DNS layer
  `DNSQR()`            DNS question record
  `packet.show()`      Detailed packet structure
  `packet.summary()`   Short packet summary
  `sniff()`            Capture packets
  `sr1()`              Send and receive one response
  `rdpcap()`           Read a PCAP file
  `wrpcap()`           Write packets to PCAP

### Example 1: Construct and inspect a packet (does not send it)

``` python
from scapy.all import IP, TCP

packet = IP(dst="192.0.2.10") / TCP(dport=443, flags="S")

packet.show()
print(packet.summary())
```

`192.0.2.0/24` is a documentation-only IPv4 range. This example
constructs a packet but does not transmit it.

### Example 2: Read an existing PCAP file

``` python
from scapy.all import rdpcap

packets = rdpcap("sample.pcap")

print("Packet count:", len(packets))

for packet in packets[:10]:
    print(packet.summary())
```

Use a PCAP file captured in your own lab or supplied for training.

### Example 3: Capture a small amount of authorized lab traffic

``` python
from scapy.all import sniff

packets = sniff(
    count=5,
    timeout=10,
)

packets.summary()
```

Packet capture may require elevated privileges and the correct network
interface. Captured traffic may contain sensitive information.

### Example 4: Inspect TCP packets in a PCAP

``` python
from scapy.all import rdpcap, TCP, IP

for packet in rdpcap("sample.pcap"):
    if IP in packet and TCP in packet:
        print(
            packet[IP].src,
            "->",
            packet[IP].dst,
            "destination port:",
            packet[TCP].dport,
        )
```

### Real-world task

Use a provided lab PCAP to count TCP and UDP packets, list destination
ports, and summarize DNS queries. Do not capture third-party traffic.

### Practice

1.  Construct an IP/TCP packet without sending it.
2.  Read a PCAP file.
3.  Count TCP, UDP, and ICMP packets.
4.  Extract source and destination IP addresses.
5.  Extract DNS query names.
6.  Explain why packet capture requires authorization.

Documentation: https://github.com/secdev/scapy/

------------------------------------------------------------------------

# 13. Module 9 --- Requests and urllib3: HTTP API automation

## What is an API?

An API allows programs to communicate. DevOps engineers use APIs to
automate GitHub, Jenkins, monitoring platforms, cloud services, and
internal applications.

### HTTP methods

  Method   Common purpose
  -------- -----------------------------
  GET      Retrieve a resource
  POST     Create or submit data
  PUT      Replace a resource
  PATCH    Partially update a resource
  DELETE   Delete a resource

### Common HTTP status codes

  Code   Meaning
  ------ ---------------------------------
  200    OK
  201    Created
  202    Accepted for processing
  204    No content
  400    Bad request
  401    Authentication required/invalid
  403    Forbidden
  404    Not found
  409    Conflict
  429    Rate limited
  500    Internal server error
  502    Bad gateway
  503    Service unavailable
  504    Gateway timeout

Install:

``` bash
python -m pip install requests urllib3
```

## 13.1 Requests

### Important Requests APIs

  API                             Purpose
  ------------------------------- ----------------------------------------
  `requests.get()`                GET request
  `requests.post()`               POST request
  `requests.put()`                PUT request
  `requests.patch()`              PATCH request
  `requests.delete()`             DELETE request
  `requests.Session()`            Reuse connections and session settings
  `response.status_code`          HTTP status
  `response.headers`              Response headers
  `response.text`                 Response text
  `response.json()`               Parse JSON response
  `response.raise_for_status()`   Raise for unsuccessful HTTP status
  `timeout=`                      Set request timeout
  `params=`                       Query-string parameters
  `json=`                         Send JSON body
  `headers=`                      Send HTTP headers
  `auth=`                         Configure supported authentication

### Example 1: GET a public API

``` python
import requests

url = "https://api.github.com"

try:
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()

    print("Status:", response.status_code)
    print("API response:", response.json())

except requests.exceptions.Timeout:
    print("The API request timed out")
except requests.exceptions.HTTPError as exc:
    print("HTTP error:", exc)
except requests.exceptions.RequestException as exc:
    print("Network/request error:", exc)
```

The tuple `(3, 10)` sets connect and read timeouts. It is not a
guaranteed total wall-clock deadline.

### Example 2: Send a POST request

``` python
import requests

url = "https://httpbin.org/post"

payload = {
    "application": "payment-service",
    "environment": "staging",
}

response = requests.post(
    url,
    json=payload,
    timeout=10,
)

response.raise_for_status()
print(response.json())
```

Use test endpoints for learning. Do not send sample data to a production
endpoint.

### Example 3: Use a session and headers

``` python
import os
import requests

token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise RuntimeError("Set GITHUB_TOKEN in the environment")

with requests.Session() as session:
    session.headers.update({
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    })

    response = session.get(
        "https://api.github.com/user",
        timeout=(3, 10),
    )
    response.raise_for_status()

    user = response.json()
    print("Authenticated GitHub user:", user.get("login"))
```

Do not print the token or commit it to Git.

### Example 4: Retry transient failures with urllib3 Retry

Requests uses urllib3 internally. A retry policy can be configured
through an HTTP adapter:

``` python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_policy = Retry(
    total=3,
    connect=3,
    read=2,
    status=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=frozenset(["GET", "HEAD", "OPTIONS"]),
    respect_retry_after_header=True,
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_policy)
session.mount("https://", adapter)
session.mount("http://", adapter)

response = session.get(
    "https://api.github.com",
    timeout=(3, 10),
)
response.raise_for_status()

print(response.status_code)
```

Retry only operations where repeating the request is safe. Retrying a
non-idempotent POST can create duplicate operations unless the API
supports idempotency keys or another deduplication mechanism.

## 13.2 urllib3 directly

### Important concepts

-   `PoolManager`: manages reusable connection pools.
-   `Timeout`: configures connect/read timeouts.
-   `Retry`: configures retry behavior.
-   `HTTPResponse`: contains response status, headers, and body.
-   `request()`: sends an HTTP request.

### Example 5: Direct urllib3 GET request

``` python
import urllib3

http = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=3, read=10),
    retries=urllib3.Retry(
        total=2,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET"]),
    ),
)

response = http.request("GET", "https://api.github.com")

print("Status:", response.status)
print(response.data.decode("utf-8"))
```

### Real-world task

Build a GitHub repository inventory tool that retrieves repository
names, visibility, default branch, and update time. Handle pagination,
authentication, rate limits, timeouts, and errors.

### Practice

1.  Make a GET request.
2.  Send a JSON POST request to a test endpoint.
3.  Add headers and query parameters.
4.  Handle 401, 403, 404, 429, and 500 responses.
5.  Configure a session.
6.  Add safe retries for GET.
7.  Implement pagination.
8.  Store the API response in JSON.

Documentation: - Requests: https://requests.readthedocs.io/ - urllib3:
https://urllib3.readthedocs.io/ - Requests on PyPI:
https://pypi.org/project/requests/ - urllib3 on PyPI:
https://pypi.org/project/urllib3/

------------------------------------------------------------------------

# 14. Module 10 --- `logging`: Production logging

## What is logging?

Logging records what an application or automation script is doing. It is
more useful than scattered `print()` statements because it supports
severity levels, timestamps, formatting, handlers, and rotation.

`logging` is part of Python's standard library.

### Logging levels

  Level      When to use
  ---------- ----------------------------------------------
  DEBUG      Detailed diagnostic information
  INFO       Normal operations
  WARNING    Unexpected condition that may need attention
  ERROR      An operation failed
  CRITICAL   A severe failure affecting the application

### Important APIs

  API                          Purpose
  ---------------------------- --------------------------------
  `logging.getLogger(name)`    Create/get a logger
  `logging.basicConfig()`      Configure basic logging
  `logger.debug()`             Debug message
  `logger.info()`              Informational message
  `logger.warning()`           Warning
  `logger.error()`             Error
  `logger.exception()`         Error plus exception traceback
  `logger.critical()`          Critical failure
  `logging.FileHandler`        Write to a file
  `logging.StreamHandler`      Write to a stream
  `RotatingFileHandler`        Rotate based on file size
  `TimedRotatingFileHandler`   Rotate based on time
  `logging.Formatter`          Format log records

### Example 1: Configure basic logging

``` python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger("deployment")

logger.debug("Detailed diagnostic information")
logger.info("Deployment started")
logger.warning("Disk usage is above 80%")
logger.error("Deployment command failed")
```

DEBUG is not shown because the configured level is INFO.

### Example 2: Write logs to a file

``` python
import logging

logging.basicConfig(
    filename="deployment.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("deployment")
logger.info("Build started")
logger.info("Tests passed")
logger.info("Deployment completed")
```

`basicConfig()` generally configures logging once. For more advanced
applications, explicitly configure handlers and formatters.

### Example 3: Record exceptions

``` python
import logging

logger = logging.getLogger("backup")

logging.basicConfig(level=logging.INFO)

try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Backup calculation failed")
```

`logger.exception()` should normally be called inside an exception
handler.

### Example 4: Rotate log files

``` python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("devops")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "application.log",
    maxBytes=1_000_000,
    backupCount=5,
)

handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
))

logger.addHandler(handler)
logger.info("Application started")
```

This keeps a current log and up to five rotated backup files. Avoid
adding duplicate handlers each time a reusable setup function is called.

### Real-world task

Add structured, timestamped logging to the health-check and API scripts.
Log command names, durations, outcomes, and error details---but never
passwords, access tokens, or private keys.

### Practice

1.  Use all five logging levels.
2.  Log to both console and file.
3.  Log an exception with traceback.
4.  Rotate a log by size.
5.  Add module and function names to the format.
6.  Ensure secrets are not written to logs.

Documentation: https://docs.python.org/3/library/logging.html

------------------------------------------------------------------------

# 15. Module 11 --- `getpass`: Secure interactive input

## What is it?

`getpass` reads a password or secret from an interactive terminal
without echoing the typed characters.

It is useful for local administrative tools and learning exercises. For
unattended CI/CD jobs, use a secrets manager or protected environment/CI
secret mechanism instead of interactive prompts.

### Important APIs

  API                         Purpose
  --------------------------- --------------------------
  `getpass.getpass(prompt)`   Read a hidden password
  `getpass.getuser()`         Get the current username

### Example 1: Read a hidden password

``` python
import getpass

username = getpass.getuser()
password = getpass.getpass("Enter password: ")

print("Current user:", username)
print("Password received; value will not be displayed.")
```

### Example 2: Validate a secret without printing it

``` python
import getpass

secret = getpass.getpass("Enter deployment token: ")

if not secret:
    raise SystemExit("A token is required")

print("A non-empty token was provided")
```

This checks only that a value was entered. It does not verify whether
the token is valid.

### Real-world task

Create an interactive local tool that asks for a database password and
uses it to connect to a disposable test database. Never print or save
the password.

### Practice

1.  Read a password without echoing it.
2.  Reject an empty value.
3.  Explain why `getpass` is unsuitable for unattended pipelines.
4.  Compare interactive secrets with environment variables and cloud
    secret managers.

Documentation: https://docs.python.org/3/library/getpass.html

------------------------------------------------------------------------

# 16. Module 12 --- Boto3: AWS automation

## What is Boto3?

Boto3 is the AWS SDK for Python. It allows Python applications to call
AWS APIs to inspect and manage services such as EC2, S3, IAM,
CloudWatch, and many others.

Install:

``` bash
python -m pip install boto3
```

### AWS credential setup

For local development, use an AWS CLI profile or another supported
credential provider:

``` bash
aws configure
aws sts get-caller-identity
```

For a named profile:

``` python
import boto3

session = boto3.Session(
    profile_name="dev",
    region_name="ap-south-1",
)

sts = session.client("sts")
print(sts.get_caller_identity())
```

For production, prefer temporary credentials through IAM roles or
workload identity, such as EC2 instance profiles, ECS task roles, or EKS
IAM integration. Never hardcode access keys in Python source code or
commit them to Git.

### Important Boto3 concepts

  -----------------------------------------------------------------------
  Concept/API                         Purpose
  ----------------------------------- -----------------------------------
  `boto3.Session()`                   Session with
                                      profile/region/credentials

  `session.client()`                  Low-level service client

  `session.resource()`                Higher-level resource interface
                                      where supported

  `describe_instances()`              Retrieve EC2 details

  `list_buckets()`                    List S3 buckets

  `upload_file()`                     Upload a local file

  `download_file()`                   Download an S3 object

  `get_object()`                      Retrieve an S3 object response

  `get_paginator()`                   Iterate through paginated results

  `get_waiter()`                      Wait for a supported resource state

  `ClientError`                       Handle AWS service errors
  -----------------------------------------------------------------------

### Example 1: Verify AWS identity

``` python
import boto3

session = boto3.Session(region_name="ap-south-1")
sts = session.client("sts")

identity = sts.get_caller_identity()

print("Account:", identity["Account"])
print("ARN:", identity["Arn"])
```

### Example 2: List EC2 instances with pagination

``` python
import boto3
from botocore.exceptions import BotoCoreError, ClientError

ec2 = boto3.client("ec2", region_name="ap-south-1")

try:
    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                print(
                    instance["InstanceId"],
                    instance["State"]["Name"],
                    instance.get("InstanceType"),
                )

except (BotoCoreError, ClientError) as exc:
    print("AWS request failed:", exc)
    raise
```

The IAM identity needs permission to call `ec2:DescribeInstances`.

### Example 3: List S3 buckets

``` python
import boto3

s3 = boto3.client("s3")
response = s3.list_buckets()

for bucket in response.get("Buckets", []):
    print(bucket["Name"], bucket["CreationDate"])
```

### Example 4: Upload a backup to S3

``` python
import boto3

s3 = boto3.client("s3")

s3.upload_file(
    Filename="backup.zip",
    Bucket="your-approved-backup-bucket",
    Key="daily/backup.zip",
)

print("Upload completed")
```

The bucket must exist, the file must exist, and the IAM identity must
have the required S3 permissions.

### Example 5: Read a small S3 object

``` python
import boto3

s3 = boto3.client("s3")

response = s3.get_object(
    Bucket="your-approved-bucket",
    Key="config/app.json",
)

content = response["Body"].read().decode("utf-8")
print(content)
```

For large objects, stream the body instead of loading the entire object
into memory.

### Example 6: Handle AWS API errors

``` python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

try:
    s3.head_bucket(Bucket="your-approved-bucket")
    print("Bucket is accessible")
except ClientError as exc:
    error_code = exc.response.get("Error", {}).get("Code", "Unknown")
    print("S3 request failed:", error_code)
    raise
```

Do not assume every AWS error code means the same thing. Handle expected
errors specifically and preserve useful diagnostics.

### Real-world task

Build an AWS inventory report that lists EC2 instance ID, state, type,
region, and tags. Add pagination, error handling, and CSV/JSON output.
Start with read-only IAM permissions.

### Practice

1.  Verify the active AWS identity.
2.  List EC2 instances in one region.
3.  List S3 buckets.
4.  Upload a sample file to a training bucket.
5.  Download a test object.
6.  Use a paginator.
7.  Handle `ClientError`.
8.  Explain IAM roles versus long-lived access keys.
9.  Add a region loop only for regions your organization authorizes you
    to inspect.

### AWS safety

-   Use least-privilege IAM permissions.
-   Begin with read-only inventory tasks.
-   Confirm account and region before changes.
-   Do not stop, start, terminate, or delete production resources during
    practice.
-   Never print secrets or commit credentials.
-   Consider AWS CloudTrail and change approvals for production
    operations.

Documentation: - Boto3:
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html -
PyPI: https://pypi.org/project/boto3/

------------------------------------------------------------------------

# 17. Module 13 --- Paramiko: SSH and SFTP automation

## What is Paramiko?

Paramiko is a Python implementation of SSHv2. It supports secure remote
command execution and SFTP file transfer.

Install:

``` bash
python -m pip install paramiko
```

### Important APIs

  API                               Purpose
  --------------------------------- -----------------------------------
  `paramiko.SSHClient()`            Create an SSH client
  `load_system_host_keys()`         Load known host keys
  `set_missing_host_key_policy()`   Define behavior for unknown hosts
  `RejectPolicy()`                  Reject unknown host keys
  `connect()`                       Connect to a remote server
  `exec_command()`                  Execute a remote command
  `open_sftp()`                     Open SFTP session
  `sftp.put()`                      Upload a file
  `sftp.get()`                      Download a file
  `close()`                         Close a connection

### Example 1: Connect with a verified host key

``` python
import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

try:
    ssh.connect(
        hostname="your-authorized-server.example",
        username="ubuntu",
        key_filename="/home/ubuntu/.ssh/id_ed25519",
        timeout=10,
        auth_timeout=10,
        banner_timeout=10,
    )
    print("SSH connection established")
finally:
    ssh.close()
```

The host must already have a trusted key in the known-hosts database.
Verify the server fingerprint through a trusted channel before trusting
it. Do not automatically trust unknown keys in production.

### Example 2: Execute a remote read-only command

``` python
import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

try:
    ssh.connect(
        hostname="your-authorized-server.example",
        username="ubuntu",
        key_filename="/home/ubuntu/.ssh/id_ed25519",
        timeout=10,
    )

    stdin, stdout, stderr = ssh.exec_command(
        "uptime",
        timeout=15,
    )

    exit_code = stdout.channel.recv_exit_status()

    print("STDOUT:")
    print(stdout.read().decode())

    print("STDERR:")
    print(stderr.read().decode())

    print("Exit code:", exit_code)

finally:
    ssh.close()
```

### Example 3: Upload a file using SFTP

``` python
import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

try:
    ssh.connect(
        hostname="your-authorized-server.example",
        username="ubuntu",
        key_filename="/home/ubuntu/.ssh/id_ed25519",
        timeout=10,
    )

    with ssh.open_sftp() as sftp:
        sftp.put(
            "local-config.yaml",
            "/home/ubuntu/local-config.yaml",
        )

    print("Upload completed")

finally:
    ssh.close()
```

### Example 4: Download a log file

``` python
import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

try:
    ssh.connect(
        hostname="your-authorized-server.example",
        username="ubuntu",
        key_filename="/home/ubuntu/.ssh/id_ed25519",
        timeout=10,
    )

    with ssh.open_sftp() as sftp:
        sftp.get(
            "/var/log/myapp/application.log",
            "application.log",
        )

finally:
    ssh.close()
```

The remote account needs permission to read the file.

### Real-world task

Build an authorized server health collector that connects to two lab
VMs, executes `uptime`, `df -h`, and `free -h`, and saves a separate
report for each host. Add host-key verification, timeouts, and error
handling.

### Practice

1.  Connect to your own Linux VM using a verified host key.
2.  Run `uptime`.
3.  Capture stdout, stderr, and exit code.
4.  Upload a test configuration file.
5.  Download a test log file.
6.  Handle connection failures and timeouts.
7.  Explain why disabling host-key checking is unsafe.

Documentation: - Paramiko: https://www.paramiko.org/ - API docs:
https://docs.paramiko.org/

------------------------------------------------------------------------

# 18. Module 14 --- JSON: Data interchange

## What is JSON?

JSON (JavaScript Object Notation) is a text format commonly used by APIs
and configuration systems. Python maps JSON objects to dictionaries,
arrays to lists, strings to strings, numbers to numeric types, booleans
to `True`/`False`, and `null` to `None`.

### Important APIs

  API                       Purpose
  ------------------------- ------------------------------------
  `json.loads(text)`        Parse a JSON string
  `json.load(file)`         Parse JSON from a file
  `json.dumps(data)`        Convert Python data to JSON string
  `json.dump(data, file)`   Write JSON to a file
  `indent=`                 Pretty-print output
  `sort_keys=True`          Sort object keys
  `ensure_ascii=False`      Keep non-ASCII characters readable
  `JSONDecodeError`         Handle invalid JSON

### Example 1: Parse a JSON string

``` python
import json

raw = """
{
  "application": "payment-service",
  "environment": "staging",
  "replicas": 3,
  "enabled": true
}
"""

config = json.loads(raw)

print(config["application"])
print(config["replicas"])
print(config["enabled"])
```

### Example 2: Write a JSON file

``` python
import json

report = {
    "hostname": "web-01",
    "status": "healthy",
    "cpu_percent": 34.5,
    "alerts": [],
}

with open("server-report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)
```

### Example 3: Read a JSON file

``` python
import json

with open("server-report.json", encoding="utf-8") as file:
    report = json.load(file)

print(report["hostname"])
print(report["status"])
```

### Example 4: Handle malformed JSON

``` python
import json

raw = '{"environment": "production",}'

try:
    data = json.loads(raw)
except json.JSONDecodeError as exc:
    print(f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
```

### Real-world task

Read an API response, validate required keys, and save only approved
non-sensitive fields to a timestamped JSON report.

### Practice

1.  Convert a dictionary to a JSON string.
2.  Write and read a JSON file.
3.  Handle invalid JSON.
4.  Pretty-print nested data.
5.  Extract EC2 fields from a sample JSON response.
6.  Never include passwords or tokens in reports.

Documentation: https://docs.python.org/3/library/json.html

------------------------------------------------------------------------

# 19. Module 15 --- PyYAML: YAML configuration automation

## What is YAML?

YAML is a human-readable serialization format widely used in Kubernetes
manifests, Ansible playbooks, Docker Compose files, and application
configuration.

Install:

``` bash
python -m pip install PyYAML
```

### Important APIs

  API                      Purpose
  ------------------------ ------------------------------------------
  `yaml.safe_load()`       Parse safe YAML types
  `yaml.safe_load_all()`   Parse multiple YAML documents
  `yaml.safe_dump()`       Serialize safe Python data
  `yaml.safe_dump_all()`   Write multiple YAML documents
  `yaml.YAMLError`         Handle YAML parsing/serialization errors

Prefer `safe_load()` for configuration from untrusted or external
sources. Avoid unsafe object construction.

### Example 1: Parse YAML text

``` python
import yaml

raw = """
application:
  name: payment-service
  port: 8080

environment: staging
replicas: 2
"""

config = yaml.safe_load(raw)

print(config["application"]["name"])
print(config["application"]["port"])
print(config["replicas"])
```

### Example 2: Read a configuration file

Create `config.yaml`:

``` yaml
app:
  name: payment-service
  port: 8080

monitoring:
  cpu_threshold: 80
  memory_threshold: 85
  disk_threshold: 90
```

Python:

``` python
import yaml

with open("config.yaml", encoding="utf-8") as file:
    config = yaml.safe_load(file) or {}

print("Application:", config["app"]["name"])
print("CPU threshold:", config["monitoring"]["cpu_threshold"])
```

### Example 3: Validate required configuration

``` python
import yaml

with open("config.yaml", encoding="utf-8") as file:
    config = yaml.safe_load(file) or {}

required_sections = ["app", "monitoring"]

for section in required_sections:
    if section not in config:
        raise ValueError(f"Missing required section: {section}")

if not 1 <= int(config["app"]["port"]) <= 65535:
    raise ValueError("Invalid application port")
```

For production, validate types, ranges, allowed values, and unknown keys
too.

### Example 4: Generate a Kubernetes-style manifest

``` python
import yaml

deployment = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "nginx"},
    "spec": {
        "replicas": 2,
        "selector": {"matchLabels": {"app": "nginx"}},
        "template": {
            "metadata": {"labels": {"app": "nginx"}},
            "spec": {
                "containers": [{
                    "name": "nginx",
                    "image": "nginx:1.27",
                    "ports": [{"containerPort": 80}],
                }]
            },
        },
    },
}

with open("deployment.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(deployment, file, sort_keys=False)

print("Manifest generated")
```

This generates a manifest file; it does not deploy it. Review it and
validate it with Kubernetes tooling before applying it to a cluster.

### Example 5: Read multiple YAML documents

``` python
import yaml

with open("resources.yaml", encoding="utf-8") as file:
    for document in yaml.safe_load_all(file):
        if document:
            print(document.get("kind"), document.get("metadata", {}).get("name"))
```

### Real-world task

Create a YAML-driven health checker. Thresholds, log path, and
environment name should come from YAML rather than being hardcoded.
Validate the configuration before running checks.

### Practice

1.  Parse YAML text.
2.  Read nested YAML configuration.
3.  Generate a YAML file from a dictionary.
4.  Read a multi-document Kubernetes YAML file.
5.  Handle malformed YAML.
6.  Validate required fields and allowed values.

Documentation: - PyYAML: https://pyyaml.org/wiki/PyYAMLDocumentation -
PyPI: https://pypi.org/project/PyYAML/

------------------------------------------------------------------------

# 20. Module 16 --- pandas: CSV and operational reporting

## What is pandas?

Pandas is a data analysis library. Its `DataFrame` structure is useful
for processing server inventories, monitoring exports, deployment
histories, and cloud-cost CSV files.

Install:

``` bash
python -m pip install pandas
```

### Important concepts and APIs

  API                         Purpose
  --------------------------- ---------------------------------------
  `pd.DataFrame(data)`        Create a table
  `pd.Series(data)`           Create a one-dimensional series
  `pd.read_csv(path)`         Read CSV
  `df.to_csv(path)`           Write CSV
  `df.head()` / `df.tail()`   Preview rows
  `df.info()`                 Column and type summary
  `df.describe()`             Statistical summary
  `df.shape`                  Row and column count
  `df.columns`                Column names
  `df.dtypes`                 Column data types
  `df.loc[]`                  Label-based selection
  `df.iloc[]`                 Position-based selection
  `df.isna()`                 Find missing values
  `df.dropna()`               Drop rows/columns with missing values
  `df.fillna()`               Fill missing values
  `df.groupby()`              Group and aggregate
  `df.sort_values()`          Sort data
  `pd.to_datetime()`          Parse dates
  `pd.merge()`                Join datasets

### Example 1: Create a DataFrame

``` python
import pandas as pd

data = {
    "server": ["web-01", "web-02", "db-01"],
    "cpu": [45, 90, 30],
    "memory": [50, 85, 40],
}

df = pd.DataFrame(data)
print(df)
```

### Example 2: Read a CSV file

Create `servers.csv`:

``` csv
server,environment,cpu,memory
web-01,production,45,50
web-02,production,90,85
db-01,staging,30,40
```

Python:

``` python
import pandas as pd

df = pd.read_csv("servers.csv")

print(df.head())
print(df.info())
print(df.describe(numeric_only=True))
```

### Example 3: Filter high-CPU servers

``` python
import pandas as pd

df = pd.read_csv("servers.csv")

high_cpu = df[df["cpu"] > 80]

print(high_cpu)
high_cpu.to_csv("high-cpu-report.csv", index=False)
```

### Example 4: Group by environment

``` python
import pandas as pd

df = pd.read_csv("servers.csv")

summary = (
    df.groupby("environment")
      .agg(
          server_count=("server", "count"),
          average_cpu=("cpu", "mean"),
          average_memory=("memory", "mean"),
      )
      .reset_index()
)

print(summary)
```

### Example 5: Handle missing data

``` python
import pandas as pd

df = pd.read_csv("servers.csv")

print("Missing values:")
print(df.isna().sum())

df["cpu"] = pd.to_numeric(df["cpu"], errors="coerce")
df["memory"] = pd.to_numeric(df["memory"], errors="coerce")

df = df.dropna(subset=["server", "cpu", "memory"])

print(df)
```

Choose a missing-value policy based on what the data means. Do not
silently replace missing CPU or memory measurements with zero unless
that is genuinely correct.

### Example 6: Parse dates

``` python
import pandas as pd

df = pd.read_csv("deployments.csv")
df["deployed_at"] = pd.to_datetime(
    df["deployed_at"],
    errors="coerce",
    utc=True,
)

print(df.sort_values("deployed_at"))
```

### Real-world task

Build a cloud-inventory report that reads EC2 inventory CSV data, counts
instances by environment, identifies missing tags, and exports a summary
CSV.

### Practice

1.  Read a CSV and inspect its columns.
2.  Filter CPU above 80%.
3.  Calculate average memory per environment.
4.  Find missing values.
5.  Sort servers by CPU usage.
6.  Merge two inventory CSV files.
7.  Export a clean report.

Documentation: - pandas: https://pandas.pydata.org/docs/ - PyPI:
https://pypi.org/project/pandas/

------------------------------------------------------------------------

# 21. Module 17 --- `smtplib`: Email notifications

## What is SMTP?

SMTP (Simple Mail Transfer Protocol) is used to send email. Python's
`smtplib` provides an SMTP client.

It is useful for deployment reports, backup notifications, and
operational alerts. For production systems, a managed email service or
approved organizational SMTP relay may be preferable.

### Important APIs

  API                       Purpose
  ------------------------- --------------------------------------
  `smtplib.SMTP()`          Connect to an SMTP server
  `smtplib.SMTP_SSL()`      Connect using SMTP over implicit TLS
  `server.starttls()`       Upgrade a connection to TLS
  `server.login()`          Authenticate
  `server.sendmail()`       Send a message
  `server.send_message()`   Send an email message object
  `server.quit()`           Close SMTP session

Use the standard library `email.message.EmailMessage` to construct
messages safely.

### Example 1: Send a plain-text email over TLS

Set credentials in your environment; do not place them in source code:

``` bash
export SMTP_HOST="smtp.example.com"
export SMTP_PORT="587"
export SMTP_USER="automation@example.com"
export SMTP_PASSWORD="replace-with-secret-from-your-secret-store"
export ALERT_TO="devops-team@example.com"
```

Python:

``` python
import os
import smtplib
import ssl
from email.message import EmailMessage

host = os.environ["SMTP_HOST"]
port = int(os.environ.get("SMTP_PORT", "587"))
username = os.environ["SMTP_USER"]
password = os.environ["SMTP_PASSWORD"]
recipient = os.environ["ALERT_TO"]

message = EmailMessage()
message["Subject"] = "DevOps deployment report"
message["From"] = username
message["To"] = recipient
message.set_content(
    "The staging deployment completed successfully.\n"
    "Check the deployment dashboard for details.\n"
)

context = ssl.create_default_context()

with smtplib.SMTP(host, port, timeout=20) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(username, password)
    server.send_message(message)

print("Email sent")
```

The SMTP server must support STARTTLS on the configured port. Some
providers use port 465 with `SMTP_SSL()` instead. Follow your provider's
configuration.

### Example 2: Send an email using SMTP_SSL

``` python
import os
import smtplib
import ssl
from email.message import EmailMessage

message = EmailMessage()
message["Subject"] = "Backup completed"
message["From"] = os.environ["SMTP_USER"]
message["To"] = os.environ["ALERT_TO"]
message.set_content("The scheduled backup completed.")

context = ssl.create_default_context()

with smtplib.SMTP_SSL(
    os.environ["SMTP_HOST"],
    int(os.environ.get("SMTP_PORT", "465")),
    context=context,
    timeout=20,
) as server:
    server.login(
        os.environ["SMTP_USER"],
        os.environ["SMTP_PASSWORD"],
    )
    server.send_message(message)
```

### Example 3: Send an alert based on health status

``` python
from email.message import EmailMessage
import os
import smtplib
import ssl

def send_alert(subject: str, body: str) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ["SMTP_USER"]
    message["To"] = os.environ["ALERT_TO"]
    message.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        os.environ["SMTP_HOST"],
        int(os.environ.get("SMTP_PORT", "465")),
        context=context,
        timeout=20,
    ) as server:
        server.login(
            os.environ["SMTP_USER"],
            os.environ["SMTP_PASSWORD"],
        )
        server.send_message(message)

send_alert(
    "ALERT: Production disk usage",
    "The production disk usage crossed the configured threshold.",
)
```

### Real-world task

Send an email when the health checker detects a threshold breach.
Include hostname, environment, metric, measured value, and
timestamp---but do not include credentials or sensitive log contents.

### Practice

1.  Send a test email to an address you control.
2.  Use TLS or SSL correctly.
3.  Read credentials from environment variables or a secret manager.
4.  Handle SMTP authentication and connection errors.
5.  Send a message with multiple recipients.
6.  Create an HTML email using `EmailMessage`.
7.  Avoid sending repeated alerts every minute; implement alert
    deduplication or cooldown.

Documentation: https://docs.python.org/3/library/smtplib.html

------------------------------------------------------------------------

# 22. Integrated capstone project --- DevOps Operations Toolkit

## Project goal

Build one maintainable Python CLI tool that collects local system
health, analyzes logs, reads configuration, optionally inventories AWS
resources, and produces reports with optional email notifications.

This project combines all 17 requested topics.

### High-level architecture

``` text
                  DevOps Operations Toolkit
                             |
                      CLI entry point
                             |
                 Configuration (YAML/JSON)
                             |
       +---------------------+----------------------+
       |                     |                      |
  Host inventory        Health monitoring       Log analysis
  os/platform/sys       psutil/subprocess       re
       |                     |                      |
       +---------------------+----------------------+
                             |
                      Report generation
                         pandas/JSON
                             |
              +--------------+--------------+
              |              |              |
          Local files      AWS API       Remote hosts
          os/shutil        Boto3          Paramiko
              |              |              |
              +--------------+--------------+
                             |
                       logging system
                             |
                    Email notification
                          smtplib
                             |
                    Cron scheduling
```

Scapy is an optional authorized network-diagnostics component.
Requests/urllib3 can integrate external APIs such as GitHub or an
internal monitoring endpoint. `getpass` can support a local interactive
prompt, but unattended runs should use managed secrets.

### 22.1 Configuration file

Create `config/config.yaml`:

``` yaml
app:
  name: devops-operations-toolkit
  environment: staging

monitoring:
  cpu_threshold: 80
  memory_threshold: 85
  disk_threshold: 90
  disk_path: /

report:
  output_directory: reports

aws:
  enabled: false
  region: ap-south-1

notifications:
  email_enabled: false
```

Do not put passwords, tokens, private keys, or AWS access keys in this
YAML file.

### 22.2 Example health-check module

Create `src/devops_toolkit/health_check.py`:

``` python
from datetime import datetime, timezone
import platform
import psutil


def collect_health(disk_path: str = "/") -> dict:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(disk_path)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "os": platform.system(),
        "cpu_percent": cpu,
        "memory_percent": memory.percent,
        "disk_path": disk_path,
        "disk_percent": disk.percent,
    }


def evaluate_health(
    report: dict,
    cpu_threshold: float,
    memory_threshold: float,
    disk_threshold: float,
) -> list[str]:
    alerts = []

    if report["cpu_percent"] > cpu_threshold:
        alerts.append("CPU threshold exceeded")

    if report["memory_percent"] > memory_threshold:
        alerts.append("Memory threshold exceeded")

    if report["disk_percent"] > disk_threshold:
        alerts.append("Disk threshold exceeded")

    return alerts
```

### 22.3 Example main program

Create `main.py`:

``` python
import argparse
import json
import logging
from pathlib import Path

import yaml

from src.devops_toolkit.health_check import (
    collect_health,
    evaluate_health,
)


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    required = ["monitoring", "report"]
    for section in required:
        if section not in config:
            raise ValueError(f"Missing configuration section: {section}")

    return config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Python DevOps Operations Toolkit"
    )
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Path to YAML configuration",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger("devops-toolkit")

    try:
        config = load_config(args.config)
        monitoring = config["monitoring"]

        report = collect_health(
            disk_path=monitoring.get("disk_path", "/")
        )

        alerts = evaluate_health(
            report,
            cpu_threshold=float(monitoring["cpu_threshold"]),
            memory_threshold=float(monitoring["memory_threshold"]),
            disk_threshold=float(monitoring["disk_threshold"]),
        )

        report["alerts"] = alerts
        report["status"] = "unhealthy" if alerts else "healthy"

        output_dir = Path(config["report"]["output_directory"])
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "health-report.json"
        output_file.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        logger.info("Health report written to %s", output_file)

        if alerts:
            for alert in alerts:
                logger.warning("%s", alert)
            return 1

        logger.info("System health is within configured thresholds")
        return 0

    except Exception:
        logger.exception("Toolkit execution failed")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

Run:

``` bash
python main.py --config config/config.yaml
```

This is a learning baseline. Before production use, add unit tests,
stricter configuration validation, safe report permissions, alert
cooldowns, and platform-aware disk paths. The `src` package also needs
`__init__.py` files for the package layout shown above.

### 22.4 Capstone milestones

  Milestone   Deliverable                     Topics
  ----------- ------------------------------- -------------------
  1           System inventory                os, platform, sys
  2           Command runner                  subprocess
  3           Health checker                  psutil
  4           Log analyzer                    re
  5           Scheduled execution             python-crontab
  6           Authorized packet analysis      Scapy
  7           API integration                 Requests, urllib3
  8           Centralized logs                logging
  9           Secure interactive mode         getpass
  10          AWS inventory                   Boto3
  11          Remote host collector           Paramiko
  12          JSON reports                    JSON
  13          Configuration-driven behavior   PyYAML
  14          CSV reports                     pandas
  15          Email alerts                    smtplib

### 22.5 Expected portfolio demonstration

Your GitHub repository should demonstrate:

-   Clear README and setup instructions.
-   Example YAML configuration without secrets.
-   Sample input data and sample output.
-   One command to run a local health check.
-   A JSON health report.
-   A log-analysis report.
-   Unit tests.
-   Safe AWS read-only inventory mode.
-   Optional SSH and email integrations disabled by default.
-   Screenshots or terminal output showing successful execution.

------------------------------------------------------------------------

# 23. Testing, quality, and security checklist

## Code quality

-   [ ] Use meaningful variable and function names.
-   [ ] Break large scripts into reusable functions.
-   [ ] Use `pathlib` for portable path operations where appropriate.
-   [ ] Add type hints to reusable functions.
-   [ ] Handle expected exceptions.
-   [ ] Use logging instead of relying only on print statements.
-   [ ] Keep configuration separate from code.
-   [ ] Add unit tests for parsing and threshold logic.
-   [ ] Pin and review dependencies for repeatable builds.

## Security

-   [ ] Never hardcode AWS access keys, passwords, tokens, or SMTP
    credentials.
-   [ ] Never commit `.env`, `.pem`, `.key`, or private configuration
    files.
-   [ ] Use IAM roles and least-privilege policies.
-   [ ] Verify SSH host keys.
-   [ ] Avoid `shell=True` for subprocess calls.
-   [ ] Validate file paths before destructive operations.
-   [ ] Use TLS certificate verification for HTTP.
-   [ ] Set network and subprocess timeouts.
-   [ ] Do not log secrets or sensitive personal data.
-   [ ] Capture packets only on networks you own or are authorized to
    inspect.
-   [ ] Require approval for production-changing operations.
-   [ ] Test destructive operations only in disposable environments.

## Testing commands

Install test tools:

``` bash
python -m pip install pytest ruff
```

Run tests:

``` bash
python -m pytest -v
```

Lint:

``` bash
ruff check .
```

Format:

``` bash
ruff format .
```

Compile Python files:

``` bash
python -m compileall .
```

------------------------------------------------------------------------

# 24. Troubleshooting

  -------------------------------------------------------------------------------
  Problem                 Likely cause            What to check
  ----------------------- ----------------------- -------------------------------
  `ModuleNotFoundError`   Package missing or      Activate venv; run
                          wrong interpreter       `python -m pip show PACKAGE`

  `PermissionError`       User lacks              Check ownership and
                          filesystem/process      permissions; avoid unnecessary
                          permission              root

  `FileNotFoundError`     Command missing or PATH Use `shutil.which()` and
  from subprocess         differs                 inspect environment

  Command works in        Cron has limited        Use absolute paths and redirect
  terminal but not cron   PATH/environment        logs

  `psutil.AccessDenied`   Process information     Handle exception; use permitted
                          restricted              access

  Scapy capture fails     Missing privileges or   Use an authorized lab and
                          wrong interface         inspect interfaces

  API timeout             Network/server latency  Set timeouts; inspect
                                                  DNS/firewall; use safe retries

  HTTP 401/403            Credentials or          Verify token, scopes, IAM/API
                          permissions issue       permissions

  HTTP 429                Rate limit              Respect `Retry-After` and
                                                  backoff

  Boto3                   No usable AWS           Check profile/role and
  `NoCredentialsError`    credentials             `aws sts get-caller-identity`

  Boto3 `AccessDenied`    IAM policy does not     Request the minimum required
                          allow action            permission

  Paramiko host key error Host is unknown or key  Verify fingerprint through a
                          changed                 trusted channel

  Paramiko authentication Wrong user/key or       Check authorized key and SSH
  failure                 server policy           server configuration

  YAML parsing error      Invalid indentation or  Validate spaces and YAML
                          syntax                  structure

  JSON decode error       Invalid JSON input      Inspect exact line/column and
                                                  source payload

  SMTP authentication     Wrong provider settings Check TLS mode, port, app
  failure                 or credentials          password, relay policy

  pandas parser error     Malformed CSV           Inspect delimiter, quoting,
                                                  encoding, and source rows
  -------------------------------------------------------------------------------

------------------------------------------------------------------------

# 25. Practical exercises and portfolio milestones

Complete these in order. Keep your code in Git and document what you
learned.

## Beginner

-   [ ] System information reporter using `os`, `platform`, and `sys`.
-   [ ] Directory and file inventory script.
-   [ ] Safe command runner using `subprocess`.
-   [ ] JSON read/write utility.
-   [ ] YAML configuration reader.
-   [ ] Basic logging setup.

## Intermediate

-   [ ] CPU/RAM/disk monitor using `psutil`.
-   [ ] Nginx or application log analyzer using `re`.
-   [ ] API health checker using Requests.
-   [ ] CSV server inventory report using pandas.
-   [ ] Scheduled backup checker using cron.
-   [ ] SMTP notification for failed health checks.

## Advanced

-   [ ] AWS EC2 and S3 inventory using Boto3.
-   [ ] Authorized multi-server health collector using Paramiko.
-   [ ] PCAP analysis report using Scapy.
-   [ ] Configurable CLI tool with JSON and CSV output.
-   [ ] Unit-tested DevOps Operations Toolkit.
-   [ ] CI workflow that runs lint and tests on every pull request.

------------------------------------------------------------------------

# 26. Suggested 15-day study plan

  Day   Topics             Daily practical output
  ----- ------------------ -----------------------------------------------
  1     os, platform       System inventory script
  2     subprocess, sys    Safe CLI command runner
  3     psutil             Server resource monitor
  4     re                 Application log analyzer
  5     python-crontab     Scheduled health check
  6     Scapy              Analyze an authorized sample PCAP
  7     Requests           REST API health checker
  8     urllib3, logging   Retry-enabled API client with logs
  9     getpass            Interactive secure-input utility
  10    JSON, PyYAML       Configuration and report manager
  11    Boto3              Read-only AWS resource inventory
  12    Paramiko           Authorized remote health collector
  13    pandas             CSV inventory and utilization report
  14    smtplib            Email notification
  15    All modules        Complete capstone, tests, README, GitHub push

### Daily learning routine

1.  Read the concept and documentation.
2.  Type the example yourself.
3.  Run it and understand the output.
4.  Change at least two inputs.
5.  Introduce one failure and handle it.
6.  Write one small practical script.
7.  Commit working code to Git.

A realistic goal is to understand and demonstrate the core use cases in
15 days---not to become an expert in every library. Continue improving
the capstone as you learn.

------------------------------------------------------------------------

# 27. Official documentation

  --------------------------------------------------------------------------------------------------------------------
  \#                      Topic                   Documentation
  ----------------------- ----------------------- --------------------------------------------------------------------
  1                       os                      https://docs.python.org/3/library/os.html

  2                       platform                https://docs.python.org/3/library/platform.html

  3                       subprocess              https://docs.python.org/3/library/subprocess.html

  4                       sys                     https://docs.python.org/3/library/sys.html

  5                       psutil                  https://github.com/giampaolo/psutil

  6                       re                      https://docs.python.org/3/library/re.html

  7                       python-crontab          https://pypi.org/project/python-crontab/

  8                       Scapy                   https://github.com/secdev/scapy/

  9                       Requests                https://requests.readthedocs.io/

  9                       urllib3                 https://urllib3.readthedocs.io/

  10                      logging                 https://docs.python.org/3/library/logging.html

  11                      getpass                 https://docs.python.org/3/library/getpass.html

  12                      Boto3                   https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

  13                      Paramiko                https://www.paramiko.org/

  14                      JSON                    https://docs.python.org/3/library/json.html

  15                      PyYAML                  https://pyyaml.org/wiki/PyYAMLDocumentation

  16                      pandas                  https://pandas.pydata.org/docs/

  17                      smtplib                 https://docs.python.org/3/library/smtplib.html
  --------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## Final learning principle

**A DevOps engineer should not learn Python only as a programming
language. Learn it as an automation tool.**

For every module, be able to answer:

1.  What problem does this module solve?
2.  Which functions are most useful?
3.  Can I write a working script without copying?
4.  Can I handle errors, timeouts, and permissions?
5.  Can I use it safely in a CI/CD or cloud environment?
6.  Can I explain the design in an interview?

Build small scripts, combine them into the capstone, test them, and
publish the work in your GitHub portfolio.
