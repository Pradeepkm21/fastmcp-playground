# fastmcp-playground

This repository is a learning and practice playground for building a Model Context Protocol (MCP) server using **fastMCP**.  
The project follows a step-by-step learning plan (Phases 0 and 1) to understand MCP concepts, set up tooling, and build a minimal but functional MCP server.


## Goals
- Understand what MCP is (clients, servers, transports, tools, resources, prompts, notifications).
- Learn how an IDE/assistant discovers and interacts with MCP server tools.
- Set up a clean project environment with `uv`, Python 3.12, and dependencies.
- Build and test a minimal MCP server with example tools (`ping`, `whoami`, `time_now`, `health_check`).
- Configure environment variables, logging, and testing.
- Connect to an MCP-compatible client and demo the server.


## Checklist

### Phase 0 — Orientation
- Understand MCP basics (client, server, transports, tools, resources, prompts, notifications).
- Write 1-page summary in `docs/overview.md`.
- Create repo `fastmcp-playground` and commit `README.md`.

### Phase 1 — Beginner fastMCP with uv & environment
1. Install & Pin Tooling  
   - Install Python 3.12  
   - Install `uv` and confirm version  
   - Document versions in `docs/tooling.md`  

2. Project Init (uv)  
   - Run `uv init`  
   - Add dependencies (`fastmcp`, `pydantic-settings`, `httpx`, `ruff`, `pytest`)  
   - Lock dependencies (`uv lock`)  
   - Commit `pyproject.toml` and `uv.lock`  

3. Environment & Secrets  
   - Create `.env.example`  
   - Add `.env` locally (ignored in git)  
   - Document env handling in `docs/env.md`  

4. Hello Server (fastMCP minimal)  
   - Create minimal server with `ping()` and `whoami()` tools  
   - Provide start script  
   - Verify server starts on stdio  

5. Add a Pure Function Tool  
   - Implement `time_now(tz)` with validation  
   - Ensure error handling works  

6. Logging & Health  
   - Add structured logging  
   - Add `health_check()` tool  
   - Save log sample in `docs/logs.txt`  

7. Basic Tests & Lint  
   - Configure `ruff` and `pytest`  
   - Write unit tests  
   - Add `make test` or `uv run -m pytest`  

8. Client Demo  
   - Connect to MCP client (IDE/assistant)  
   - Call all tools and capture screenshots  
   - Write demo notes in `docs/demo.md`  

---

## 📂 Repo Structure (planned)

fastmcp-playground/
│── docs/
│ ├── overview.md
│ ├── tooling.md
│ ├── env.md
│ ├── logs.txt
│ └── demo.md
│
│── app/ # MCP server code
│── tests/ # Unit tests
│── pyproject.toml
│── uv.lock
│── .env.example
│── .gitignore
│── README.md



