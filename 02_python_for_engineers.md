# 02. Python for Engineers

Contents
7. [Python for systems](#7-python-for-systems)
8. [HTTP and APIs](#8-http-and-apis)
9. [Concurrency](#9-concurrency)
10. [Testing and quality](#10-testing-and-quality)
11. [CLI and packaging](#11-cli-and-packaging)
12. [Secure Python practices](#12-secure-python-practices)

> The DevOps-specific deep dive on each library (os, subprocess, psutil, requests, ...)
> is in [`03_devops_automation.md`](03_devops_automation.md). This file gives the engineering
> foundation that those scripts build on.

---

## 7. Python for systems

### 7.1 os and sys: the quick tour

```python
import os, sys

os.getcwd(); os.chdir("/tmp")
os.environ["HOME"]; os.environ.get("X", "default")
os.getpid(); os.getuid()                    # Unix
os.cpu_count()
os.listdir("."); os.makedirs("a/b", exist_ok=True)
os.remove("f"); os.rmdir("empty"); os.rename("a", "b")
os.stat("f").st_mtime
os.chmod("script.sh", 0o755)
for root, dirs, files in os.walk("/var/log"):
    ...

sys.argv            # ['script.py', 'arg1', ...]
sys.exit(1)         # exit code
sys.stdout.write("x\n"); sys.stderr.write("err\n")
sys.version_info >= (3, 10)
sys.platform        # 'linux', 'darwin', 'win32'
sys.executable      # path of the running interpreter
```

### 7.2 shutil: high-level file operations

```python
import shutil

shutil.copy("a.txt", "b.txt")            # file + permissions
shutil.copy2("a.txt", "b.txt")           # also metadata (mtime)
shutil.copytree("src", "dst", dirs_exist_ok=True)
shutil.move("a", "/tmp/a")
shutil.rmtree("old_dir", ignore_errors=True)     # DANGEROUS: rm -rf
shutil.which("git")                       # find executable on PATH, or None
shutil.disk_usage("/")                    # total, used, free (bytes)
shutil.make_archive("backup", "gztar", root_dir="data")   # backup.tar.gz
shutil.unpack_archive("backup.tar.gz", "restore")
```

### 7.3 subprocess: run other programs

```python
import subprocess

r = subprocess.run(
    ["ls", "-l", "/tmp"],       # list of args, NOT a string (no shell)
    capture_output=True, text=True, timeout=10, check=False,
)
print(r.returncode, r.stdout, r.stderr)

subprocess.run(["false"], check=True)      # raises CalledProcessError on non-zero
```

Key ideas: pass a **list**, use `timeout`, check `returncode`, and avoid `shell=True` (see section 12).

### 7.4 signal: handle Ctrl+C and `kill`

```python
import signal, sys, time

running = True
def stop(signum, frame):
    global running
    print(f"signal {signum}, shutting down...")
    running = False

signal.signal(signal.SIGINT, stop)      # Ctrl+C
signal.signal(signal.SIGTERM, stop)     # `kill <pid>`, Docker stop, Kubernetes

while running:
    time.sleep(1)
print("cleanup complete")
```
Containers send SIGTERM and wait (default 30s on k8s/Docker) before SIGKILL. Handling it gives you graceful shutdown.

### 7.5 psutil: system metrics (third party)

```python
import psutil
psutil.cpu_percent(interval=1)
psutil.virtual_memory().percent
psutil.disk_usage("/").percent
for p in psutil.process_iter(["pid", "name", "memory_percent"]):
    print(p.info)
```
More in `03_devops_automation.md` section 5.

### 7.6 Practical: safe temp-file cleaner with dry-run

```python
#!/usr/bin/env python3
"""Delete files older than N days under a directory. Dry-run by default."""
import argparse, time
from pathlib import Path

def old_files(root: Path, days: int):
    cutoff = time.time() - days * 86400
    for p in root.rglob("*"):
        if p.is_file() and not p.is_symlink() and p.stat().st_mtime < cutoff:
            yield p

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--delete", action="store_true", help="really delete")
    a = ap.parse_args()

    if not a.root.is_dir() or str(a.root.resolve()) in {"/", str(Path.home())}:
        ap.error("refusing to operate on that path")

    freed = 0
    for f in old_files(a.root, a.days):
        size = f.stat().st_size
        freed += size
        print(("DELETE " if a.delete else "would delete ") + str(f))
        if a.delete:
            f.unlink()
    print(f"{'freed' if a.delete else 'reclaimable'}: {freed/1e6:.1f} MB")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

### 7.7 Practical: graceful long-running worker

```python
import signal, threading, logging

logging.basicConfig(level=logging.INFO)
stop = threading.Event()

def handler(sig, _):
    logging.info("received %s", signal.Signals(sig).name)
    stop.set()

for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, handler)

while not stop.is_set():
    logging.info("working...")
    stop.wait(2)                 # sleeps but wakes immediately on stop
logging.info("bye")
```

---

## 8. HTTP and APIs

### 8.1 REST in one minute

| Method | Use | Idempotent |
|--------|-----|-----------|
| GET | read | yes |
| POST | create / action | no |
| PUT | replace | yes |
| PATCH | partial update | no (usually) |
| DELETE | remove | yes |

Status classes: 2xx success, 3xx redirect, 4xx client error (401 unauth, 403 forbidden, 404 missing, 429 rate-limited), 5xx server error.

### 8.2 requests

```python
import requests

r = requests.get(
    "https://api.github.com/repos/python/cpython",
    headers={"Accept": "application/vnd.github+json"},
    params={"per_page": 10},          # becomes ?per_page=10
    timeout=(3.05, 10),               # (connect, read). ALWAYS set a timeout
)
r.raise_for_status()                  # raises HTTPError for 4xx/5xx
print(r.status_code, r.headers["Content-Type"])
data = r.json()

requests.post(url, json={"a": 1})              # JSON body
requests.post(url, data={"user": "x"})         # form body
requests.put(url, json=payload); requests.delete(url)
```
`requests` has **no default timeout**: without one, a hung server hangs your script forever.

### 8.3 Sessions, auth, headers

```python
s = requests.Session()               # reuses TCP connections, shares settings
s.headers.update({"User-Agent": "opskit/1.0"})
s.auth = ("user", "password")                        # Basic auth
s.headers["Authorization"] = f"Bearer {token}"       # Bearer/API token
s.get(url, timeout=10)
```

### 8.4 Pagination patterns

```python
# a) page numbers / link headers
def paginate(session, url, params=None):
    while url:
        r = session.get(url, params=params, timeout=10)
        r.raise_for_status()
        yield from r.json()
        url = r.links.get("next", {}).get("url")    # GitHub-style Link header
        params = None                               # next URL already has them

# b) cursor-based
def cursor_pages(session, url):
    cursor = None
    while True:
        r = session.get(url, params={"cursor": cursor} if cursor else {}, timeout=10)
        body = r.json()
        yield from body["items"]
        cursor = body.get("next_cursor")
        if not cursor:
            break
```

### 8.5 Retries and timeouts

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_session() -> requests.Session:
    retry = Retry(
        total=5,
        backoff_factor=0.5,                         # 0.5, 1, 2, 4 ...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD", "PUT", "DELETE", "OPTIONS"],  # not POST
        respect_retry_after_header=True,
    )
    s = requests.Session()
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s
```
Only retry idempotent methods unless the API supports idempotency keys.

### 8.6 httpx (modern alternative: sync and async)

```python
import httpx

with httpx.Client(timeout=10.0, headers={"User-Agent": "opskit"}) as c:
    r = c.get("https://example.com/api")
    r.raise_for_status()

import asyncio
async def main():
    async with httpx.AsyncClient(timeout=10) as c:
        rs = await asyncio.gather(*(c.get(u) for u in urls))
asyncio.run(main())
```
httpx has timeouts on by default (5s), HTTP/2 support, and native async.

### 8.7 Practical: paginated API client with retry and rate-limit handling

```python
import time, requests, logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger("gh")

class GitHub:
    BASE = "https://api.github.com"

    def __init__(self, token: str | None = None):
        self.s = requests.Session()
        self.s.headers["Accept"] = "application/vnd.github+json"
        if token:
            self.s.headers["Authorization"] = f"Bearer {token}"
        self.s.mount("https://", HTTPAdapter(max_retries=Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])))

    def _get(self, url, **kw):
        r = self.s.get(url, timeout=15, **kw)
        if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(r.headers["X-RateLimit-Reset"])
            wait = max(0, reset - time.time()) + 1
            log.warning("rate limited, sleeping %.0fs", wait)
            time.sleep(wait)
            return self._get(url, **kw)
        r.raise_for_status()
        return r

    def repos(self, org: str):
        url = f"{self.BASE}/orgs/{org}/repos"
        params = {"per_page": 100}
        while url:
            r = self._get(url, params=params)
            yield from r.json()
            url = r.links.get("next", {}).get("url")
            params = None

if __name__ == "__main__":
    import os
    gh = GitHub(os.environ.get("GITHUB_TOKEN"))
    for repo in gh.repos("python"):
        print(repo["name"], repo["stargazers_count"])
```

---

## 9. Concurrency

### 9.1 Choosing the right tool

| Workload | Tool | Why |
|----------|------|-----|
| Waiting on network/disk (I/O-bound), modest scale | `threading` / `ThreadPoolExecutor` | Simple; GIL released during I/O |
| I/O-bound, thousands of connections | `asyncio` | Lightweight tasks |
| CPU-bound (hashing, parsing, math) | `multiprocessing` / `ProcessPoolExecutor` | Bypasses the GIL |

The **GIL** (Global Interpreter Lock) lets only one thread run Python bytecode at a time, so threads don't speed up CPU-bound work (note: free-threaded builds exist in 3.13+ but are experimental).

### 9.2 Threads with ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

urls = ["https://example.com", "https://python.org", "https://github.com"]

def check(url: str) -> tuple[str, int | str]:
    try:
        return url, requests.get(url, timeout=5).status_code
    except requests.RequestException as e:
        return url, type(e).__name__

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(check, u) for u in urls]
    for fut in as_completed(futures):
        print(fut.result())

# or, keeping order:
with ThreadPoolExecutor(10) as pool:
    results = list(pool.map(check, urls))
```

Shared state needs a lock:

```python
import threading
counter = 0
lock = threading.Lock()
def inc():
    global counter
    with lock:
        counter += 1
```

### 9.3 Queues (producer/consumer)

```python
import queue, threading

q: "queue.Queue[str | None]" = queue.Queue(maxsize=100)

def worker():
    while True:
        item = q.get()
        if item is None:           # sentinel = stop
            q.task_done(); break
        print("processing", item)
        q.task_done()

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads: t.start()
for i in range(10): q.put(f"job-{i}")
for _ in threads: q.put(None)
q.join()
for t in threads: t.join()
```

### 9.4 multiprocessing (CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor
import hashlib

def sha(path: str) -> tuple[str, str]:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return path, h.hexdigest()

if __name__ == "__main__":          # REQUIRED on Windows/macOS (spawn)
    files = ["a.iso", "b.iso"]
    with ProcessPoolExecutor() as pool:
        for path, digest in pool.map(sha, files):
            print(digest, path)
```
Arguments and return values are pickled, so avoid passing huge objects.

### 9.5 asyncio, async/await

```python
import asyncio, httpx

async def fetch(client: httpx.AsyncClient, url: str) -> tuple[str, int]:
    r = await client.get(url)
    return url, r.status_code

async def main(urls: list[str]):
    async with httpx.AsyncClient(timeout=5) as client:
        results = await asyncio.gather(*(fetch(client, u) for u in urls),
                                       return_exceptions=True)
    for r in results:
        print(r)

asyncio.run(main(["https://example.com", "https://python.org"]))
```

Rules:
- `await` only works inside `async def`.
- Never call blocking code (`time.sleep`, `requests.get`) in a coroutine. Use `await asyncio.sleep`, `httpx`, or `await asyncio.to_thread(blocking_fn)`.
- Timeouts: `async with asyncio.timeout(5):` (3.11+) or `asyncio.wait_for(coro, 5)`.

Async queue:

```python
async def producer(q):
    for i in range(5):
        await q.put(i)
    await q.put(None)

async def consumer(q):
    while (item := await q.get()) is not None:
        print("got", item)

async def main():
    q = asyncio.Queue(maxsize=10)
    await asyncio.gather(producer(q), consumer(q))
asyncio.run(main())
```

### 9.6 Rate limiting

```python
# a) cap concurrency with a semaphore
sem = asyncio.Semaphore(5)
async def limited(coro_fn, *a):
    async with sem:
        return await coro_fn(*a)

# b) cap requests per second with a token bucket
import time, threading

class RateLimiter:
    def __init__(self, rate: float, burst: int = 1):
        self.rate, self.capacity = rate, burst
        self.tokens, self.t = float(burst), time.monotonic()
        self.lock = threading.Lock()

    def acquire(self):
        while True:
            with self.lock:
                now = time.monotonic()
                self.tokens = min(self.capacity, self.tokens + (now - self.t) * self.rate)
                self.t = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return
                wait = (1 - self.tokens) / self.rate
            time.sleep(wait)

limiter = RateLimiter(rate=5, burst=5)       # 5 req/s
def call(url):
    limiter.acquire()
    return requests.get(url, timeout=5)
```

### 9.7 Practical: concurrent TCP port checker (async)

```python
import asyncio, sys

async def check(host: str, port: int, timeout: float = 2.0) -> tuple[int, bool]:
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        w.close(); await w.wait_closed()
        return port, True
    except (OSError, asyncio.TimeoutError):
        return port, False

async def scan(host: str, ports: list[int], limit: int = 100):
    sem = asyncio.Semaphore(limit)
    async def guarded(p):
        async with sem:
            return await check(host, p)
    return await asyncio.gather(*(guarded(p) for p in ports))

if __name__ == "__main__":
    host = sys.argv[1]
    for port, ok in asyncio.run(scan(host, [22, 80, 443, 3306, 5432, 6379, 8080])):
        print(f"{host}:{port:<5} {'OPEN' if ok else 'closed'}")
```
Scan only hosts you are authorized to test.

---

## 10. Testing and quality

### 10.1 pytest basics

Layout:

```
project/
├── src/opskit/disk.py
└── tests/
    ├── conftest.py           # shared fixtures
    └── test_disk.py
```

```python
# src/opskit/disk.py
def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"

# tests/test_disk.py
import pytest
from opskit.disk import human

def test_human_bytes():
    assert human(512) == "512.0B"

@pytest.mark.parametrize("n, expected", [
    (0, "0.0B"), (1024, "1.0KB"), (1024**2, "1.0MB"), (1024**3, "1.0GB"),
])
def test_human_param(n, expected):
    assert human(n) == expected

def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```
Run: `pytest -v`, `pytest -k human`, `pytest -x` (stop at first failure), `pytest --lf` (last failed).

### 10.2 Fixtures

```python
import json, pytest

@pytest.fixture
def config_file(tmp_path):                # tmp_path = built-in temp dir
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"port": 8080}))
    return p

def test_load(config_file):
    from opskit.config import load
    assert load(config_file)["port"] == 8080

@pytest.fixture
def db():
    conn = connect_test_db()
    yield conn                 # test runs here
    conn.close()               # teardown
```
Fixture scopes: `function` (default), `class`, `module`, `session`. Put shared ones in `conftest.py`.
Other useful built-ins: `monkeypatch`, `capsys`, `caplog`, `tmp_path`.

### 10.3 Mocks

Mock things you don't control (network, clock, cloud) so tests are fast and deterministic.

```python
from unittest.mock import patch, MagicMock

# code under test
import requests
def is_up(url: str) -> bool:
    return requests.get(url, timeout=3).status_code == 200

# test
def test_is_up():
    fake = MagicMock(status_code=200)
    with patch("requests.get", return_value=fake) as get:
        assert is_up("http://x") is True
        get.assert_called_once_with("http://x", timeout=3)

def test_down():
    with patch("requests.get", side_effect=requests.ConnectionError):
        with pytest.raises(requests.ConnectionError):
            is_up("http://x")

def test_env(monkeypatch):
    monkeypatch.setenv("APP_PORT", "9000")
```
**Patch where it is used**, not where it is defined (`patch("mymodule.requests.get")` if `mymodule` does `import requests`).

For AWS, the `moto` library fakes boto3 services: `pip install "moto[s3,ec2]"`.

### 10.4 Coverage

```bash
pytest --cov=opskit --cov-report=term-missing
pytest --cov=opskit --cov-report=html          # open htmlcov/index.html
pytest --cov=opskit --cov-fail-under=80         # fail CI under 80%
```
Coverage tells you what code ran, not whether the tests are meaningful.

### 10.5 ruff, black, mypy

```bash
ruff check .            # lint (replaces flake8, isort, pyupgrade, many plugins)
ruff check . --fix
ruff format .           # formatter (black-compatible)
black .                 # formatter
black --check .         # CI mode
mypy src/               # static type check
```

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "S"]     # pycodestyle, pyflakes, isort, bugbear, upgrade, bandit-ish

[tool.mypy]
python_version = "3.11"
strict = false
warn_unused_ignores = true
disallow_untyped_defs = true
```

Use one formatter (ruff format **or** black). Add them to pre-commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### 10.6 Practical: test a disk-alert function end to end

```python
# src/opskit/alerts.py
import shutil

def disk_alert(path: str, limit: int = 90) -> str | None:
    u = shutil.disk_usage(path)
    pct = u.used / u.total * 100
    return f"{path} at {pct:.0f}%" if pct >= limit else None

# tests/test_alerts.py
from collections import namedtuple
from unittest.mock import patch
from opskit.alerts import disk_alert

Usage = namedtuple("Usage", "total used free")

def test_alert_triggers():
    with patch("opskit.alerts.shutil.disk_usage", return_value=Usage(100, 95, 5)):
        assert disk_alert("/") == "/ at 95%"

def test_no_alert():
    with patch("opskit.alerts.shutil.disk_usage", return_value=Usage(100, 10, 90)):
        assert disk_alert("/") is None
```

---

## 11. CLI and packaging

### 11.1 argparse

```python
import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="opskit", description="Ops helper")
    p.add_argument("--verbose", "-v", action="count", default=0)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("disk", help="check disk usage")
    d.add_argument("path", nargs="?", default="/")
    d.add_argument("--limit", type=int, default=90)

    h = sub.add_parser("http", help="check URL")
    h.add_argument("url")
    h.add_argument("--timeout", type=float, default=5)
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "disk":
        ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```
Taking `argv` as a parameter makes `main()` trivially testable: `main(["disk", "/tmp"])`.

### 11.2 Typer (type-hint based CLI)

```python
import typer            # pip install typer
app = typer.Typer(help="Ops helper")

@app.command()
def disk(path: str = "/", limit: int = typer.Option(90, help="Alert percent")):
    """Check disk usage."""
    typer.echo(f"checking {path} (limit {limit}%)")

@app.command()
def deploy(service: str, env: str = "staging", force: bool = False):
    if env == "prod" and not force:
        typer.confirm("Deploy to PROD?", abort=True)
    typer.secho(f"deploying {service} to {env}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
```
Gives `--help`, validation, and shell completion for free.

### 11.3 Logging configuration for CLIs

```python
import logging, sys

def setup_logging(verbosity: int = 0, logfile: str | None = None) -> None:
    level = {0: logging.WARNING, 1: logging.INFO}.get(verbosity, logging.DEBUG)
    handlers = [logging.StreamHandler(sys.stderr)]        # logs to stderr, data to stdout
    if logfile:
        from logging.handlers import RotatingFileHandler
        handlers.append(RotatingFileHandler(logfile, maxBytes=5_000_000, backupCount=3))
    logging.basicConfig(level=level, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
```
Rule: **results go to stdout, logs go to stderr** so output can be piped safely.

Dictionary config for larger apps:

```python
import logging.config
logging.config.dictConfig({
    "version": 1,
    "formatters": {"std": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "std"}},
    "root": {"level": "INFO", "handlers": ["console"]},
})
```

### 11.4 Packaging

Use the `src/` layout and `pyproject.toml` (see section 1.4).

```
opskit/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/opskit/
│   ├── __init__.py
│   └── cli.py          # def main(): ...
└── tests/
```

```bash
pip install -e ".[dev]"          # develop
pip install build twine
python -m build                  # dist/opskit-0.1.0.tar.gz and .whl
twine check dist/*
twine upload --repository testpypi dist/*
```
Entry point in `[project.scripts]` creates the `opskit` command after install.

### 11.5 Requirements locking

`pyproject.toml` lists **what you need** (ranges); a lock file records **exactly what was installed** (pins + hashes) for reproducible builds.

```bash
# pip-tools
pip install pip-tools
pip-compile pyproject.toml -o requirements.txt --generate-hashes
pip-compile --extra dev pyproject.toml -o requirements-dev.txt
pip-sync requirements.txt         # make the venv match exactly

# uv (fast, all-in-one)
pip install uv
uv venv && uv pip install -r requirements.txt
uv pip compile pyproject.toml -o requirements.txt
```
In CI/Docker install with `pip install --require-hashes -r requirements.txt`.

---

## 12. Secure Python practices

### 12.1 Secrets via environment

```python
import os, sys

def require(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        sys.exit(f"missing required env var: {name}")
    return v

DB_PASSWORD = require("DB_PASSWORD")      # fail fast, never hard-code
```

- Never commit secrets. Add `.env` to `.gitignore`; use a pre-commit scanner such as `gitleaks` or `detect-secrets`.
- Never log secrets. Mask them: `log.info("token=%s***", token[:4])` (or better, don't log at all).
- In production use a secret manager (AWS Secrets Manager, Vault, Kubernetes Secrets) instead of files.
- Prompt interactively with `getpass.getpass()` rather than command-line arguments (which show in `ps`).

### 12.2 Input validation

Treat everything from users, files, APIs and env vars as untrusted.

```python
import re, ipaddress
from pathlib import Path

HOSTNAME = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9-]+)*$")

def valid_host(h: str) -> str:
    if len(h) > 253 or not HOSTNAME.fullmatch(h):
        raise ValueError("invalid hostname")
    return h

def valid_ip(s: str) -> str:
    return str(ipaddress.ip_address(s))          # raises ValueError

def valid_port(p: int) -> int:
    if not 1 <= p <= 65535:
        raise ValueError("port out of range")
    return p

def safe_join(base: Path, user_path: str) -> Path:
    """Prevent path traversal like ../../etc/passwd."""
    target = (base / user_path).resolve()
    if not target.is_relative_to(base.resolve()):
        raise ValueError("path escapes base directory")
    return target
```
Allow-list (what is permitted) beats deny-list (what is forbidden). Libraries like `pydantic` handle structured validation well.

### 12.3 Safe subprocess

```python
import subprocess, shlex

host = user_input

# BAD: shell injection. host = "x; rm -rf ~" would run the second command
subprocess.run(f"ping -c1 {host}", shell=True)

# GOOD: list args, no shell
subprocess.run(["ping", "-c1", valid_host(host)], check=True, timeout=10,
               capture_output=True, text=True)

# If you absolutely must build a shell string, quote:
cmd = "ping -c1 " + shlex.quote(host)
```
Also: use absolute paths for executables in privileged scripts, pass a minimal `env=`, always set `timeout=`, and use `--` before user values if the tool supports it (`["grep", "--", pattern, file]`) so they can't be read as options.

### 12.4 Dangerous functions and defaults

| Avoid | Use instead |
|-------|-------------|
| `eval()`, `exec()` on input | `ast.literal_eval`, or parse explicitly |
| `pickle.load` on untrusted data | JSON |
| `yaml.load()` | `yaml.safe_load()` |
| `requests.get(..., verify=False)` | fix the CA bundle |
| `hashlib.md5` for passwords | `hashlib.scrypt`/`argon2`/`bcrypt` |
| `random` for tokens | `secrets.token_urlsafe(32)` |
| `tempfile.mktemp()` | `tempfile.NamedTemporaryFile` / `mkstemp` / `TemporaryDirectory` |
| `os.system(...)` | `subprocess.run([...])` |
| `paramiko AutoAddPolicy` in prod | known_hosts + `RejectPolicy` |

```python
import secrets, hmac, tempfile
token = secrets.token_urlsafe(32)
hmac.compare_digest(a, b)        # constant-time compare for tokens
with tempfile.TemporaryDirectory() as d: ...
```

Set restrictive permissions on files that hold secrets:

```python
import os
fd = os.open("secret.key", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
```

### 12.5 Dependency scanning

```bash
pip install pip-audit bandit safety
pip-audit                           # checks installed packages against the PyPI advisory DB
pip-audit -r requirements.txt
bandit -r src/                      # static analysis of YOUR code for insecure patterns
```
Also:
- Pin and hash dependencies (section 11.5).
- Enable Dependabot or Renovate on your repo.
- Typosquatting is real: double-check package names before `pip install`.
- Use `pip install --only-binary :all:` or a private index in locked-down environments.
- Generate SBOMs with `cyclonedx-py` if compliance requires it.

### 12.6 Practical: security checklist script for CI

```bash
#!/usr/bin/env bash
set -euo pipefail
ruff check src tests
mypy src
bandit -q -r src
pip-audit -r requirements.txt
pytest --cov=opskit --cov-fail-under=80
echo "all gates passed"
```
