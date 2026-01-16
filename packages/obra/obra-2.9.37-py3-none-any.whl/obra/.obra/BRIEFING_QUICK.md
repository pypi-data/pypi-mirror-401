# Obra Quick Start for AI Agents

**Version**: 1.1
**Read time**: ~2 minutes (~1,500 tokens)
**Purpose**: Essential input quality requirements before submitting tasks to Obra

---

## LLM Operator Fast Path (Deterministic)

Use this before you run the task:

- **Models**: `obra models` -> pick names. Use `obra run --model X --fast-model X --high-model X --impl-provider openai`.
  - Or env vars: `OBRA_MODEL`, `OBRA_FAST_MODEL`, `OBRA_HIGH_MODEL`, `OBRA_PROVIDER`.
- Do NOT use `obra config set llm.*.model` (unsupported).
- **Help**: `obra help run` for single-level help. Subcommand help uses `--help` (ex: `obra projects create --help`).
- **Windows paths**: map `C:\Projects\...` -> `/mnt/c/Projects/...` and pass with `obra run --dir /mnt/c/...`.
- **Native Windows**: use `C:\...` directly (no `/mnt/c` mapping).
- **Verbosity**: use `-v/-vv/-vvv` (not `--vvv`).
- **Monitoring**: capture `session_id` from run output, then `obra status <session_id>`.
- **Long-running runs**: do NOT use short timeouts that kill the process. If your tool enforces timeouts, start `obra run` in a separate terminal or background (tmux/screen/nohup) and monitor with `obra status` while it keeps running.
- **Config warnings**: if `obra config show` warns about auth metadata keys in `~/.obra/client-config.yaml`, ignore. Other unknown keys are real issues.

Example:
```
OBRA_PROVIDER=openai \
OBRA_MODEL=gpt-5.1-codex-mini \
OBRA_FAST_MODEL=gpt-5.1-codex-mini \
OBRA_HIGH_MODEL=gpt-5.1-codex-mini \
obra run --dir /mnt/c/Projects/obra-simulations/my-sim --stream -vvv \
"Objective with clear stack, features, and success criteria"
```

## ⚠️ REQUIRED BEFORE SUBMITTING

### Input Quality Gate

❌ **DON'T submit vague input:**
```
obra "build a website"
obra "add authentication"
obra "make it better"
obra "fix the bug"
```

✅ **DO submit specific, complete input:**
```
obra "E-commerce website for handmade crafts: React 18 + TypeScript frontend,
Node.js + Express backend, MongoDB database. Features: product catalog with
search/filter by category and price, shopping cart with session persistence,
Stripe checkout integration, JWT authentication. Docker Compose deployment.
Performance: <500ms response time. Testing: >80% code coverage."
```

---

## Minimum Required Information Checklist

Before running `obra "task"`, you MUST have:

- [ ] **Git repository** (project in a git repo, or use `--auto-init-git`)
- [ ] **Clear objective** (2-4 sentences, not just "build X")
- [ ] **Tech stack identified** (language, framework, database)
- [ ] **Specific features** (not "auth" → "JWT authentication with refresh tokens and RBAC")
- [ ] **Success criteria** (testable outcomes: "all tests pass", "API responds <200ms")

---

## If Input is Vague: STOP and Ask

**When user says vague things, HALT execution and ask clarifying questions:**

| User says... | You ask... |
|--------------|------------|
| "Build a website" | "What kind? E-commerce, blog, SaaS app, portfolio? What features?" |
| "Add authentication" | "What type? JWT with refresh tokens? OAuth2? Session-based? Social login?" |
| "Fix the bug" | "Which bug? What's the symptom? What file/component?" |
| "Make it faster" | "Which part? API response time? Page load? Database queries? What's the target?" |

---

## Required Information by Category

### 1. Tech Stack (ALWAYS REQUIRED)

**FIRST**: Check project files before asking:
- `package.json` → JavaScript/TypeScript, framework (React/Express/Next.js)
- `requirements.txt` or `pyproject.toml` → Python, framework (FastAPI/Django/Flask)
- `go.mod` → Go, framework (Gin/Echo)
- `Cargo.toml` → Rust
- `pom.xml` or `build.gradle` → Java

**If found**: Confirm with user ("I see Python + FastAPI, continue with that?")
**If not found**: Ask with smart defaults ("REST API → suggest FastAPI or Express. Preference?")

**Minimum to specify:**
- Language (python, javascript, go, rust, java, typescript)
- Framework if applicable (fastapi, express, django, react, nextjs)
- Database if needed (postgresql, mysql, mongodb, redis, sqlite, none)

### 2. Specific Features (ALWAYS REQUIRED)

**Be detailed. Push back on vague descriptions:**

| ❌ Vague | ✅ Specific |
|---------|------------|
| "Authentication" | "JWT authentication with refresh tokens, role-based access control (admin/user roles), password reset via email" |
| "Search" | "Product search by name/description with filters for category, price range ($0-$1000), and star rating (1-5)" |
| "Admin panel" | "Admin dashboard with user management (CRUD), order tracking table with filters, analytics charts (daily revenue, top products)" |

### 3. Success Criteria (ALWAYS REQUIRED)

**Testable outcomes that define "done":**

✅ Good examples:
- "All CRUD endpoints return correct HTTP status codes (201, 200, 204, 404)"
- "Authentication blocks unauthenticated requests with 401"
- "Tests achieve >80% code coverage and all pass"
- "API responds to all endpoints within 200ms (95th percentile)"
- "Docker Compose brings up all services without errors"

❌ Bad examples:
- "It works" (not testable)
- "Good performance" (not specific)
- "No bugs" (impossible to verify)

### 4. Constraints (OPTIONAL BUT VALUABLE)

**Ask if user mentions any of these:**
- **Deployment**: Docker, Kubernetes, AWS, Heroku, cloud-run?
- **Performance**: Response time limits? Concurrent user targets? Memory limits?
- **Integration**: Existing services to connect with? (e.g., "auth-service:8000", "legacy-db:5432")
- **Security**: OWASP compliance? No secrets in code? Specific encryption requirements?
- **Testing**: Coverage targets? Test types needed (unit, integration, E2E)?

### 5. Anti-Patterns (OPTIONAL BUT VALUABLE)

**Ask: "Any frameworks, libraries, or approaches you want to avoid?"**

Good examples:
- "Don't use Flask - team is standardizing on FastAPI"
- "Avoid Redux - prefer React Context for simpler state management"
- "No raw SQL queries - must use SQLAlchemy ORM"

---

## Complete Example: Good Input

```
User: "I need user management for my app"

You (LLM): [Check package.json → see FastAPI + PostgreSQL]

You: "I see you're using FastAPI and PostgreSQL. For user management, I need:
1. What operations? Just CRUD, or also authentication/authorization?
2. What user fields beyond email/password?
3. Any role-based access control (admin vs user)?
4. Performance requirements?"

User: "CRUD plus JWT auth. Fields: name, email, role. Admins can manage users.
Response time under 200ms."

You construct:
"User management API for FastAPI app with PostgreSQL: CRUD operations
(create, read, update, delete users), JWT authentication with refresh tokens,
role-based access control (admin and user roles). User fields: name, email,
password (bcrypt), role. Admin endpoints for user management. Success: All
endpoints respond <200ms, JWT blocks unauthorized access, tests >80% coverage."

You submit: obra "User management API for FastAPI..." --stream
```

---

## Quick Decision Tree

```
1. User request received
   ├─ Is objective clear? (2-4 sentence description)
   │  ├─ YES → Continue
   │  └─ NO → Ask: "Can you describe the goal in more detail?"
   │
   ├─ Tech stack specified OR inferable from files?
   │  ├─ YES → Confirm if inferred
   │  └─ NO → Ask: "Language and framework preference?"
   │
   ├─ Features specific? (not "auth", but "JWT auth with X, Y, Z")
   │  ├─ YES → Continue
   │  └─ NO → Push for details: "What kind of auth exactly?"
   │
   ├─ Success criteria defined?
   │  ├─ YES → Ready to submit
   │  └─ NO → Ask: "How do we know when this is done?"
   │
   └─ Submit to Obra with complete, specific input
```

---

## If You Encounter Issues

🐛 **Report bugs, request features, and provide feedback**:

```bash
obra feedback bug "description"     # Report a bug
obra feedback feature "title"       # Request a feature
obra feedback general "text"        # General feedback
```

**Common scenarios**:
```bash
# Orchestration stuck or looping
obra feedback bug "Orchestration repeating same task" --severity high

# Error during execution
obra feedback bug "Derive failed" --error "EmptyPlanError: No tasks" --severity critical

# Feature request with context
obra feedback feature "Support for X" --use-case "Need this for Y"
```

**For automation/non-interactive use**:
```bash
obra feedback bug "description" --non-interactive --format json
```

**Automatic reporting**: If Obra crashes or fails to complete, it will offer to file a bug report automatically with session logs and context already captured.

**Privacy controls**:
- `--privacy full` - Maximum diagnostic data (recommended for complex bugs)
- `--privacy standard` - Balanced data collection (default)
- `--privacy minimal` - Essential info only

**Your feedback helps improve Obra** - all submissions are automatically triaged and prioritized.

---

## Autonomous Workplan Execution

🤖 **For multi-story workplans**: Use `obra auto` for hands-off execution

```bash
obra auto --plan <WORK_ID>              # Execute all pending stories
obra auto --plan <WORK_ID> --dry-run    # Preview execution plan
```

**When to use**:
- You have a MACHINE_PLAN.json with multiple stories
- Want sequential story execution without continuous LLM attention
- Solving the completion bias problem (LLMs tend to stop before finishing)

**Features**:
- Automatic retry on transient failures
- Progress logged to obra-auto.log
- Graceful Ctrl+C (completes current story, saves state)
- Breakpoint escalation for manual intervention

---

## Next Steps

📚 **Need more guidance?**

- **Complex projects/integrations**: `obra briefing questions`
  ↳ Detailed question patterns for enterprise scenarios, legacy systems, non-technical users

- **Worked examples**: `obra briefing examples`
  ↳ 10 good/bad input comparisons across different project types

- **Autonomous long-running tasks**: `obra briefing protocol`
  ↳ 11 behaviors for unattended execution (checkpointing, progress reporting, escalation)

- **Complete reference**: `obra briefing full`
  ↳ Full 3,600-line guide (blueprint structure, all sections, advanced patterns)

🐛 **Report issues**: `obra feedback bug "description"` or `obra feedback feature "title"`

---

**Generated by Obra v2.1.0** | For updates: `pipx upgrade obra`
