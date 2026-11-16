# 01. Python Core Notes

Contents
1. [Python setup and syntax](#1-python-setup-and-syntax)
2. [Control flow and collections](#2-control-flow-and-collections)
3. [Functions and modules](#3-functions-and-modules)
4. [Files and data formats](#4-files-and-data-formats)
5. [Errors and debugging](#5-errors-and-debugging)
6. [Object-oriented Python](#6-object-oriented-python)

---

## 1. Python setup and syntax

### 1.1 The interpreter

Python is an interpreted language. `python3` reads your code, compiles it to bytecode, and runs it on the Python virtual machine.

```bash
python3 --version              # which version
which python3                  # where it lives
python3                        # interactive REPL (exit with Ctrl+D)
python3 script.py              # run a file
python3 -c "print('hi')"       # run one-liner
python3 -m http.server 8000    # run a module as a script (-m)
python3 -m json.tool data.json # pretty-print JSON (handy in DevOps)
```

Shebang for executable scripts (Linux/macOS):

```python
#!/usr/bin/env python3
print("hello")
```
```bash
chmod +x script.py && ./script.py
```

### 1.2 Virtual environments (venv)

A venv is an isolated folder with its own Python and packages, so projects don't clash.

```bash
python3 -m venv .venv            # create
source .venv/bin/activate        # activate (Linux/macOS)
.venv\Scripts\activate           # activate (Windows)
which python                     # now points inside .venv
deactivate                       # leave
```

Rules of thumb:
- One venv per project, kept in `.venv/`
- Add `.venv/` to `.gitignore`. Never commit it.
- Never `sudo pip install`; use a venv instead.

### 1.3 pip basics

```bash
pip install requests               # latest
pip install "requests==2.32.3"     # exact
pip install "requests>=2.30,<3"    # range
pip install -r requirements.txt    # from file
pip install -e .                   # editable install of your own project
pip uninstall requests
pip list                           # installed
pip list --outdated
pip show requests                  # details
pip freeze > requirements.txt      # snapshot
```

Always use `python -m pip ...` inside a venv; it guarantees the pip matches the active Python.

### 1.4 pyproject.toml basics

`pyproject.toml` is the modern single config file for a project (metadata, dependencies, and tool settings).

```toml
[project]
name = "opskit"
version = "0.1.0"
description = "Small DevOps helper tools"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31",
    "psutil>=5.9",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "ruff", "black", "mypy"]

[project.scripts]
opskit = "opskit.cli:main"      # creates an `opskit` command

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 100

[tool.black]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Install with extras: `pip install -e ".[dev]"`.

### 1.5 Variables and types

Variables are names bound to objects; no declaration needed. Python is dynamically typed but strongly typed (`"1" + 1` raises an error).

```python
name = "web-01"          # str
port = 8080              # int
cpu = 73.5               # float
healthy = True           # bool
nothing = None           # NoneType
tags = ["prod", "eu"]    # list
point = (10, 20)         # tuple
unique = {1, 2, 3}       # set
server = {"host": "web-01", "port": 80}   # dict

print(type(port))        # <class 'int'>
print(isinstance(port, int))  # True
```

Type conversion:

```python
int("42"); float("3.14"); str(99); bool(0)       # False
list("abc")        # ['a','b','c']
int("abc")         # ValueError
```

Falsy values: `0, 0.0, "", [], (), {}, set(), None, False`. Everything else is truthy.

Strings:

```python
s = "  Hello, DevOps  "
s.strip(); s.lower(); s.upper(); s.replace("DevOps", "World")
s.split(",")                 # ['  Hello', ' DevOps  ']
"-".join(["a", "b", "c"])    # 'a-b-c'
s.startswith("  H"); "Dev" in s
name = "web-01"; cpu = 73.456
f"{name} CPU={cpu:.1f}%"     # f-string: 'web-01 CPU=73.5%'
f"{1234567:,}"               # '1,234,567'
f"{name=}"                   # "name='web-01'" (debug form)
s[0]; s[-1]; s[2:7]; s[::-1] # indexing and slicing
```

Multi-line and raw strings:

```python
text = """line1
line2"""
path = r"C:\new\table"     # raw: backslashes literal (great for regex)
```

### 1.6 Operators

| Kind | Operators |
|------|-----------|
| Arithmetic | `+ - * / // % **` (`//` floor division, `%` modulo) |
| Comparison | `== != < > <= >=` |
| Logical | `and or not` |
| Membership | `in`, `not in` |
| Identity | `is`, `is not` (use `is None`, not `== None`) |
| Assignment | `= += -= *= /= //= %= **=`, walrus `:=` |

```python
7 / 2     # 3.5
7 // 2    # 3
7 % 2     # 1
2 ** 10   # 1024
1 < x < 10          # chained comparison
if (n := len(items)) > 10:   # walrus: assign and test
    print(f"too many: {n}")
```

### 1.7 Practical: system report skeleton

```python
#!/usr/bin/env python3
"""Print a tiny host report using only syntax from this chapter."""
import platform

host = platform.node()
os_name = platform.system()
py_ver = platform.python_version()
checks = {"disk": 71.2, "mem": 55.0, "cpu": 93.4}
limit = 90

print(f"Host: {host} | OS: {os_name} | Python: {py_ver}")
for name, value in checks.items():
    status = "ALERT" if value > limit else "ok"
    print(f"  {name:<5} {value:>5.1f}%  {status}")
```

### 1.8 Pitfalls
- Mutable default arguments (see section 3).
- `is` vs `==`: `is` checks identity, not equality.
- Indentation is syntax: use 4 spaces, never mix tabs and spaces.
- Floating-point: `0.1 + 0.2 != 0.3`; use `math.isclose` or `decimal`.

---

## 2. Control flow and collections

### 2.1 if / elif / else

```python
cpu = 85
if cpu > 90:
    level = "critical"
elif cpu > 70:
    level = "warning"
else:
    level = "ok"

state = "up" if cpu < 100 else "down"    # ternary
```

### 2.2 match (Python 3.10+)

```python
def handle(status: int) -> str:
    match status:
        case 200 | 201:
            return "success"
        case 301 | 302:
            return "redirect"
        case 404:
            return "not found"
        case code if 500 <= code < 600:
            return "server error"
        case _:
            return "other"
```

### 2.3 Loops

```python
for i in range(3):          # 0,1,2
    print(i)
for i, host in enumerate(["a", "b"], start=1):
    print(i, host)
for h, p in zip(["a", "b"], [80, 443]):
    print(h, p)

n = 0
while n < 3:
    n += 1

for x in range(10):
    if x == 3: continue     # skip this iteration
    if x == 6: break        # leave loop
else:
    print("only runs if no break")   # for-else
```

### 2.4 list: ordered, mutable

```python
servers = ["web1", "web2", "db1"]
servers.append("cache1")
servers.extend(["x", "y"])
servers.insert(0, "lb1")
servers.remove("x")          # by value
last = servers.pop()         # by index (default last)
servers.sort()               # in place
sorted(servers, reverse=True)  # new list
servers.index("db1"); servers.count("web1")
servers[1:3]; servers[::2]
copy = servers.copy()        # shallow copy (same as servers[:])
```

### 2.5 tuple: ordered, immutable

```python
point = (10, 20)
x, y = point                 # unpacking
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2,3,4]
single = (5,)                # trailing comma needed
```
Use tuples for fixed records and as dict keys.

### 2.6 set: unique, unordered

```python
a = {"web1", "web2", "db1"}
b = {"web2", "db1", "cache1"}
a | b      # union
a & b      # intersection
a - b      # only in a
a ^ b      # in exactly one
a.add("x"); a.discard("zzz")      # discard won't raise
dedup = list(set([1, 1, 2, 3, 3]))
```
Sets give O(1) membership tests. Great for "which servers are missing?" diffs.

### 2.7 dict: key to value

```python
srv = {"host": "web1", "port": 80}
srv["port"]                 # 80 (KeyError if missing)
srv.get("tls", False)       # default, no error
srv["env"] = "prod"
srv.update({"port": 443, "tls": True})
srv.pop("env")
for k, v in srv.items(): print(k, v)
list(srv.keys()); list(srv.values())
srv.setdefault("tags", []).append("eu")

merged = {**srv, "region": "eu"}   # merge (or srv | {...} on 3.9+)
```

`collections` helpers:

```python
from collections import Counter, defaultdict
Counter(["200","404","200"])          # Counter({'200': 2, '404': 1})
groups = defaultdict(list)
groups["prod"].append("web1")
```

### 2.8 Comprehensions

```python
squares = [n*n for n in range(10)]
evens = [n for n in range(10) if n % 2 == 0]
ports = {h: 80 for h in ["a", "b"]}          # dict comp
unique_codes = {line.split()[-1] for line in ["x 200", "y 404"]}   # set comp
total = sum(n for n in range(100))           # generator expr (lazy)
flat = [x for row in [[1,2],[3,4]] for x in row]
```
Keep them readable. If it needs more than one `if` plus a nested loop, use a normal loop.

### 2.9 Practical: count HTTP status codes from an access log

```python
from collections import Counter

log_lines = [
    '10.0.0.1 - - [10/Oct/2025:13:55:36] "GET /index.html HTTP/1.1" 200 2326',
    '10.0.0.2 - - [10/Oct/2025:13:55:40] "GET /missing HTTP/1.1" 404 512',
    '10.0.0.1 - - [10/Oct/2025:13:56:01] "POST /api HTTP/1.1" 500 87',
    '10.0.0.3 - - [10/Oct/2025:13:56:05] "GET /index.html HTTP/1.1" 200 2326',
]

codes = Counter(line.split('"')[2].split()[0] for line in log_lines)
ips = Counter(line.split()[0] for line in log_lines)

print("Status codes:", dict(codes))
print("Top IP:", ips.most_common(1))
errors = [l for l in log_lines if l.split('"')[2].split()[0].startswith("5")]
print("5xx lines:", len(errors))
```

### 2.10 Pitfalls
- Modifying a list while iterating it. Iterate over a copy or build a new list.
- `a = b = []` makes both names share one list.
- Shallow vs deep copy: use `copy.deepcopy` for nested structures.

---

## 3. Functions and modules

### 3.1 Defining functions, arguments, return

```python
def greet(name, greeting="Hello"):
    """Return a greeting. (This is a docstring.)"""
    return f"{greeting}, {name}!"

greet("Ana")                       # positional
greet(greeting="Hi", name="Ana")   # keyword
```

Argument kinds:

```python
def f(a, b, /, c, *, d):     # a,b positional-only; c either; d keyword-only
    ...

def total(*nums):            # *args -> tuple
    return sum(nums)

def connect(host, **opts):   # **kwargs -> dict
    print(host, opts)

total(1, 2, 3)
connect("db", port=5432, ssl=True)

args = [1, 2, 3]; total(*args)           # unpack list into args
cfg = {"port": 80}; connect("x", **cfg)   # unpack dict into kwargs
```

Return multiple values (really a tuple):

```python
def stats(nums):
    return min(nums), max(nums)
lo, hi = stats([3, 1, 9])
```
A function with no `return` returns `None`.

### 3.2 The mutable default trap

```python
def add(item, bucket=[]):      # BUG: one shared list across calls
    bucket.append(item); return bucket

def add(item, bucket=None):    # correct
    if bucket is None:
        bucket = []
    bucket.append(item); return bucket
```

### 3.3 Scope (LEGB)

Python looks up names in order: **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in.

```python
count = 0
def inc():
    global count      # rebind a module-level name
    count += 1

def outer():
    n = 0
    def inner():
        nonlocal n    # rebind enclosing variable
        n += 1
        return n
    return inner
```
Prefer passing values and returning results over `global`.

### 3.4 First-class functions, lambda, decorators

```python
servers = [{"n": "a", "cpu": 90}, {"n": "b", "cpu": 20}]
servers.sort(key=lambda s: s["cpu"], reverse=True)

import functools, time

def timed(fn):
    @functools.wraps(fn)          # keep name/docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__} took {time.perf_counter()-start:.3f}s")
    return wrapper

@timed
def slow(): time.sleep(0.2)
```

### 3.5 Modules, imports, packages

A module is a `.py` file. A package is a folder of modules (with `__init__.py`, optional in modern Python but still recommended).

```
opskit/
├── pyproject.toml
├── src/opskit/
│   ├── __init__.py
│   ├── disk.py
│   └── net/
│       ├── __init__.py
│       └── ping.py
└── tests/test_disk.py
```

```python
import os                           # whole module
import os.path as osp               # alias
from pathlib import Path            # specific name
from opskit.disk import usage       # absolute import (preferred)
from .disk import usage             # relative import (inside a package)
```

The main guard: code runs only when executed directly, not when imported.

```python
def main() -> int:
    print("running")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Avoid `from x import *`. Avoid circular imports by moving shared code to a third module.

### 3.6 Typing basics

Type hints don't change runtime behaviour; tools like `mypy` check them.

```python
from typing import Optional, Callable, Iterable, Any

def avg(nums: list[float]) -> float:
    return sum(nums) / len(nums)

def find(host: str) -> dict[str, int] | None:   # 3.10+; same as Optional[...]
    ...

Handler = Callable[[str], bool]
def process(items: Iterable[str], cb: Handler) -> None: ...

from typing import TypedDict
class Server(TypedDict):
    host: str
    port: int
```
Run: `mypy script.py`.

### 3.7 Practical: retry decorator for flaky operations

```python
import functools, logging, time

log = logging.getLogger(__name__)

def retry(times: int = 3, delay: float = 1.0, backoff: float = 2.0,
          exceptions: tuple[type[BaseException], ...] = (Exception,)):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == times:
                        raise
                    log.warning("%s failed (%s). retry %d/%d in %.1fs",
                                fn.__name__, exc, attempt, times, wait)
                    time.sleep(wait)
                    wait *= backoff
        return wrapper
    return deco

@retry(times=4, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def call_service():
    raise ConnectionError("refused")
```

---

## 4. Files and data formats

### 4.1 pathlib (use this instead of string paths)

```python
from pathlib import Path

p = Path("/var/log") / "nginx" / "access.log"   # / joins paths
p.name; p.stem; p.suffix; p.parent; p.parts
p.exists(); p.is_file(); p.is_dir()
Path.home(); Path.cwd()
Path("logs").mkdir(parents=True, exist_ok=True)
Path("a.txt").write_text("hello\n", encoding="utf-8")
Path("a.txt").read_text(encoding="utf-8")
Path("a.bin").read_bytes()
list(Path(".").glob("*.py"))            # non-recursive
list(Path(".").rglob("*.log"))          # recursive
Path("a.txt").rename("b.txt"); Path("b.txt").unlink(missing_ok=True)
Path("a.txt").stat().st_size            # bytes
Path("a.py").with_suffix(".bak")
```

### 4.2 open() and context managers

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()           # whole file

with open("big.log", encoding="utf-8") as f:
    for line in f:               # lazy, memory safe
        if "ERROR" in line:
            print(line.rstrip())

with open("out.txt", "w", encoding="utf-8") as f:   # "w" truncates, "a" appends
    f.write("line1\n")
    f.writelines(["a\n", "b\n"])
```

Modes: `r` read, `w` write (truncate), `a` append, `x` create-only, `b` binary, `+` read/write.
Always pass `encoding="utf-8"` for text.

### 4.3 CSV

```python
import csv

with open("servers.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):           # each row is a dict
        print(row["host"], row["cpu"])

rows = [{"host": "web1", "cpu": 40}, {"host": "web2", "cpu": 95}]
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["host", "cpu"])
    w.writeheader()
    w.writerows(rows)
```
Values read from CSV are always strings; convert with `int()`/`float()`.

### 4.4 JSON

```python
import json

data = json.loads('{"host":"web1","ports":[80,443]}')     # str -> dict
text = json.dumps(data, indent=2, sort_keys=True)          # dict -> str
with open("cfg.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
with open("cfg.json", encoding="utf-8") as f:
    data = json.load(f)
```
JSON has no tuples, sets, or datetimes. Use `default=str` or convert first.

### 4.5 YAML (PyYAML)

```python
import yaml          # pip install pyyaml

doc = yaml.safe_load("""
app:
  name: shop
  replicas: 3
  env: [prod, eu]
""")
print(doc["app"]["replicas"])      # 3

with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(doc, f, sort_keys=False, default_flow_style=False)
```
Always `safe_load`, never `yaml.load` on untrusted data.

### 4.6 Config files: INI, TOML, .env

```python
# INI
import configparser
cp = configparser.ConfigParser()
cp.read("app.ini")
port = cp.getint("server", "port", fallback=8080)

# TOML (read-only, stdlib in 3.11+)
import tomllib
with open("pyproject.toml", "rb") as f:     # note: binary mode
    cfg = tomllib.load(f)

# Environment variables
import os
db_url = os.environ.get("DB_URL", "sqlite:///local.db")
debug = os.getenv("DEBUG", "0") == "1"
```

`.env` files: load with `python-dotenv` (`pip install python-dotenv`) in development only. Never commit them.

### 4.7 Practical: layered config (defaults, then file, then env vars)

```python
import json, os
from pathlib import Path

DEFAULTS = {"host": "0.0.0.0", "port": 8080, "debug": False}

def load_config(path: str = "config.json") -> dict:
    cfg = dict(DEFAULTS)
    p = Path(path)
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    # env vars win: APP_HOST, APP_PORT, APP_DEBUG
    if "APP_HOST" in os.environ:
        cfg["host"] = os.environ["APP_HOST"]
    if "APP_PORT" in os.environ:
        cfg["port"] = int(os.environ["APP_PORT"])
    if "APP_DEBUG" in os.environ:
        cfg["debug"] = os.environ["APP_DEBUG"].lower() in {"1", "true", "yes"}
    return cfg

print(load_config())
```
Priority order (lowest to highest): defaults, file, environment, CLI flags. This matches the 12-factor approach.

---

## 5. Errors and debugging

### 5.1 Exceptions

```python
try:
    value = int(input("number: "))
    result = 10 / value
except ValueError:
    print("not a number")
except ZeroDivisionError as exc:
    print("cannot divide:", exc)
except (KeyError, IndexError):
    print("lookup failed")
else:
    print("no error, result =", result)       # runs only if no exception
finally:
    print("always runs (cleanup)")
```

Raising and chaining:

```python
def get_port(cfg: dict) -> int:
    try:
        return int(cfg["port"])
    except KeyError as exc:
        raise ValueError("config missing 'port'") from exc    # keeps original cause
```

Rules:
- Catch the **specific** exception. A bare `except:` hides bugs and swallows Ctrl+C.
- Don't use exceptions for normal flow when a simple `if` does it.
- Re-raise with a bare `raise` to preserve the traceback.

Common exceptions: `ValueError, TypeError, KeyError, IndexError, FileNotFoundError, PermissionError, OSError, TimeoutError, ConnectionError, KeyboardInterrupt`.

### 5.2 Custom exceptions

```python
class OpsError(Exception):
    """Base class for our app."""

class DeployError(OpsError):
    def __init__(self, service: str, reason: str):
        super().__init__(f"{service}: {reason}")
        self.service = service
        self.reason = reason

try:
    raise DeployError("api", "image not found")
except OpsError as e:
    print("handled:", e)
```
One base class lets callers catch everything from your library with a single `except OpsError`.

### 5.3 Logging (instead of print)

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

log.debug("detail")                 # hidden at INFO level
log.info("started %s", "job-1")     # lazy formatting: use %s, not f-strings
log.warning("disk at %d%%", 91)
log.error("failed")
try:
    1 / 0
except ZeroDivisionError:
    log.exception("math broke")     # ERROR + full traceback
```

Levels: `DEBUG < INFO < WARNING < ERROR < CRITICAL`.

### 5.4 Reading a traceback

```
Traceback (most recent call last):
  File "app.py", line 12, in <module>
    main()
  File "app.py", line 8, in main
    return load()["port"]
KeyError: 'port'
```
Read **bottom to top**: the last line is the error type and message, the line above it is where it happened, and the lines above that are how you got there.

```python
import traceback
try:
    risky()
except Exception:
    print(traceback.format_exc())
```

### 5.5 Debugging with pdb

```python
def total(items):
    s = 0
    for i in items:
        breakpoint()        # drops into pdb here (Python 3.7+)
        s += i
    return s
```
Or run `python -m pdb script.py`. Post-mortem: `python -m pdb -c continue script.py` jumps in on the crash.

| Command | Meaning |
|---------|---------|
| `n` | next line |
| `s` | step into a call |
| `c` | continue |
| `l` | list source |
| `p expr` | print value |
| `pp expr` | pretty print |
| `w` | where (stack) |
| `u` / `d` | up / down a frame |
| `b 25` | breakpoint at line 25 |
| `q` | quit |

Set `PYTHONBREAKPOINT=0` to disable all `breakpoint()` calls without editing code.

### 5.6 Practical: resilient file processor with logging

```python
import json, logging, sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("processor")

class BadRecord(Exception):
    pass

def parse(line: str) -> dict:
    try:
        rec = json.loads(line)
    except json.JSONDecodeError as exc:
        raise BadRecord(f"invalid JSON: {exc.msg}") from exc
    if "host" not in rec:
        raise BadRecord("missing 'host'")
    return rec

def process(path: Path) -> tuple[int, int]:
    ok = bad = 0
    with path.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                parse(line)
                ok += 1
            except BadRecord as exc:
                bad += 1
                log.warning("line %d skipped: %s", n, exc)
    return ok, bad

if __name__ == "__main__":
    p = Path(sys.argv[1])
    try:
        ok, bad = process(p)
    except FileNotFoundError:
        log.error("file not found: %s", p); sys.exit(2)
    log.info("done ok=%d bad=%d", ok, bad)
    sys.exit(1 if bad else 0)
```
Note the use of **exit codes**: 0 = success, non-zero = failure. CI systems and cron rely on them.

---

## 6. Object-oriented Python

### 6.1 Classes and objects

```python
class Server:
    default_port = 22                      # class attribute (shared)

    def __init__(self, host: str, port: int | None = None):
        self.host = host                   # instance attributes
        self.port = port or self.default_port
        self._up = False                   # _ = "internal, please don't touch"

    def start(self) -> None:
        self._up = True

    @property
    def status(self) -> str:               # accessed like an attribute
        return "up" if self._up else "down"

    @classmethod
    def from_url(cls, url: str) -> "Server":    # alternative constructor
        host, _, port = url.partition(":")
        return cls(host, int(port) if port else None)

    @staticmethod
    def valid_port(p: int) -> bool:        # no self/cls needed
        return 0 < p < 65536

    def __repr__(self) -> str:             # for developers (debug)
        return f"Server({self.host!r}, {self.port})"

    def __str__(self) -> str:              # for users (print)
        return f"{self.host}:{self.port} [{self.status}]"

s = Server.from_url("web1:2222")
s.start(); print(s); print(repr(s))
```

Useful dunder methods: `__eq__`, `__lt__`, `__len__`, `__iter__`, `__enter__/__exit__` (context manager), `__call__`.

### 6.2 Inheritance

```python
class Service:
    def __init__(self, name: str):
        self.name = name
    def health(self) -> bool:
        raise NotImplementedError

class HttpService(Service):
    def __init__(self, name: str, url: str):
        super().__init__(name)      # call parent
        self.url = url
    def health(self) -> bool:       # override
        return True

isinstance(HttpService("a", "u"), Service)    # True
```

Abstract base classes force subclasses to implement methods:

```python
from abc import ABC, abstractmethod

class Check(ABC):
    @abstractmethod
    def run(self) -> bool: ...
```

### 6.3 Composition (prefer "has-a" over "is-a")

```python
class Notifier:
    def send(self, msg: str) -> None:
        print("NOTIFY:", msg)

class Deployer:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier       # composed, easy to swap or mock in tests
    def deploy(self, svc: str) -> None:
        self.notifier.send(f"deploying {svc}")
```
Rule of thumb: use inheritance only when the child truly *is* a specialised parent; otherwise compose.

### 6.4 Dataclasses

Less boilerplate for classes that mostly hold data.

```python
from dataclasses import dataclass, field, asdict

@dataclass
class Host:
    name: str
    ip: str
    port: int = 22
    tags: list[str] = field(default_factory=list)   # never `= []`

h = Host("web1", "10.0.0.5")
print(h)                      # Host(name='web1', ip='10.0.0.5', port=22, tags=[])
asdict(h)                     # dict, ready for json.dumps

@dataclass(frozen=True, order=True)      # immutable, sortable, hashable
class Version:
    major: int
    minor: int
```
`__post_init__` lets you validate after construction:

```python
@dataclass
class Limits:
    cpu: int
    def __post_init__(self):
        if not 0 <= self.cpu <= 100:
            raise ValueError("cpu must be 0..100")
```

### 6.5 Protocols (structural typing)

"If it has the right methods, it fits," with no inheritance required. Checked by `mypy`.

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, msg: str) -> None: ...

class SlackNotifier:
    def send(self, msg: str) -> None: print("slack:", msg)

class EmailNotifier:
    def send(self, msg: str) -> None: print("email:", msg)

def alert(n: Notifier, msg: str) -> None:
    n.send(msg)

alert(SlackNotifier(), "disk full")    # both OK, neither inherits Notifier
alert(EmailNotifier(), "disk full")
```

### 6.6 Practical: pluggable health checker

```python
from dataclasses import dataclass
from typing import Protocol
import socket

@dataclass
class Result:
    name: str
    ok: bool
    detail: str = ""

class Check(Protocol):
    name: str
    def run(self) -> Result: ...

@dataclass
class TcpCheck:
    host: str
    port: int
    timeout: float = 2.0
    @property
    def name(self) -> str:
        return f"tcp://{self.host}:{self.port}"
    def run(self) -> Result:
        try:
            with socket.create_connection((self.host, self.port), self.timeout):
                return Result(self.name, True)
        except OSError as exc:
            return Result(self.name, False, str(exc))

@dataclass
class FileCheck:
    path: str
    @property
    def name(self) -> str:
        return f"file:{self.path}"
    def run(self) -> Result:
        from pathlib import Path
        return Result(self.name, Path(self.path).exists())

def run_all(checks: list[Check]) -> int:
    failed = 0
    for c in checks:
        r = c.run()
        print(("PASS" if r.ok else "FAIL"), r.name, r.detail)
        failed += not r.ok
    return failed

if __name__ == "__main__":
    raise SystemExit(run_all([TcpCheck("example.com", 443), FileCheck("/etc/hosts")]))
```
Adding a new kind of check means adding one small class; nothing else changes (open/closed principle).

### 6.7 Pitfalls
- Class attributes holding mutable values are shared by every instance.
- Forgetting `super().__init__()` in a subclass.
- Deep inheritance trees. Prefer composition and Protocols.
