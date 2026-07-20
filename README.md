# `GIT-FISHBOWL`

An asynchronous, zero-dependency command-line interface (CLI) telemetry tool designed for real-time monitoring of GitHub repository health. 

`git-fishbowl` delivers high-performance repository tracking by streaming clean, platform-agnostic ASCII dashboards directly to `stdout`. Built entirely on native Python libraries, it eliminates external dependency overhead, ensuring rapid execution and native compatibility with Unix-style shell pipeline operations such as `grep` or `findstr`.

---

## Technical Stack

*   **Runtime Environment:** Python 3.8+
*   **Asynchronous Engine:** `asyncio` (Event-loop driven concurrent task execution)
*   **Network Layer:** Native `urllib.request` and `urllib.error` (Non-blocking I/O execution via loop pools)
*   **Data Parsing:** Native `json`
*   **Code Quality Guardrails:** Strict compliance with PEP 8 standards enforced via `black` (88-character line configuration) and `flake8`

---

## Directory Architecture

```text
git-fishbowl/
│
├── .flake8                 # Linter override configuration (88-char limit)
├── run.py                  # CLI entrypoint and pipeline orchestrator
└── src/
    ├── __init__.py         # Package initialization marker
    ├── client.py           # Asynchronous network communication client
    └── dashboard.py        # Functional metrics processing and ASCII matrix rendering

```

---

## Installation & Setup

Clone the repository to your local workspace using Git:

```bash
git clone [https://github.com/Surendra571/git-fishbowl.git](https://github.com/Surendra571/git-fishbowl.git)
cd git-fishbowl

```

*(Optional)* For development, testing, or code-style validation, install the project's quality assurance utilities:

```bash
pip install black flake8

```

---

## Core Usage & Pipeline Operations

### 1. Default Telemetry Execution

Running the engine without arguments initiates real-time monitoring of the default target repository (`python/cpython`):

```cmd
git-fishbowl>python run.py
============================================================
GIT-FISHBOWL(1)       HEALTH SUMMARY       [ OK ]
============================================================
TARGET REPOSITORY : python/cpython
------------------------------------------------------------
  - Active Issues          : 37
  - Critical Unresolved   : 0
  - Open Pull Requests    : 100
  - Draft Pull Requests   : 4
------------------------------------------------------------
SYSTEM METRIC STATUS  : HEALTHY
============================================================

```

### 2. Custom Target Routing

To inspect a specific public GitHub repository, pass the repository name as a trailing command-line argument:

```cmd
python run.py encode/httpcore

```

### 3. Shell Pipeline Filtration

Because metrics stream directly to the standard output stream, data can be isolated instantly using text-filtering utilities:

```cmd
git-fishbowl>python run.py | findstr "Critical"
  - Critical Unresolved   : 0

```

---

## Code Quality Standards

The architecture strictly enforces a separation of concerns between I/O communication and presentation layers. Codebase integrity and styling compliance can be verified using the following directives:

```bash
# Execute static analysis and style linting
python -m flake8 src/ run.py

# Execute automated code reformatting
python -m black src/ run.py

```
