 
# Python Notes: From Basics to DevOps Automation
python  devops  automation  sre  boto3  paramiko  psutil subprocess  pyyaml  pandas  scapy  cron  scripting  notes  learning


Complete, example-driven notes with a practical exercise for every topic.
Written for someone who wants to go from "I know a little Python" to
"I can automate real infrastructure tasks."

## Repository layout

| File | What's inside |
|------|---------------|
| [`01_python_core.md`](01_python_core.md) | Setup, syntax, control flow, collections, functions, modules, files and data formats, errors and debugging, OOP |
| [`02_python_for_engineers.md`](02_python_for_engineers.md) | Systems programming, HTTP and APIs, concurrency, testing and quality, CLI and packaging, secure practices |
| [`03_devops_automation.md`](03_devops_automation.md) | **DevOps track**: 17 libraries (os, platform, subprocess, sys, psutil, re, python-crontab, scapy, requests/urllib3, logging, getpass, boto3, paramiko, json, PyYAML, pandas, smtplib) with examples, practical scripts and a capstone |

## Suggested learning path

1. **Week 1**: `01_python_core.md` sections 1 to 4 (syntax, collections, functions, files)
2. **Week 2**: `01_python_core.md` sections 5 to 6 (errors, OOP), then `02` sections 1 to 2
3. **Week 3**: `02` sections 3 to 6 (concurrency, testing, CLI, security)
4. **Week 4+**: `03_devops_automation.md`, building one practical per library, then the capstone

## Quick environment setup

```bash
# 1. Check Python (3.10+ recommended, 3.11+ best)
python3 --version

# 2. Create a project and virtual environment
mkdir devops-py && cd devops-py
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Upgrade pip and install the libraries used in these notes
python -m pip install --upgrade pip
pip install requests httpx psutil boto3 paramiko pyyaml pandas \
            python-crontab scapy typer pytest pytest-cov \
            ruff black mypy pip-audit bandit

# 4. Freeze versions
pip freeze > requirements.txt
```

> Do **not** `pip install logging`. `logging` is part of the standard library.
> The PyPI package of that name is an obsolete third-party project and can break things.
 
