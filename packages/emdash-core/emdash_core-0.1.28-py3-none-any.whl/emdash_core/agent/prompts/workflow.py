"""Shared workflow patterns for agents.

These patterns can be embedded in different agent prompts to ensure
consistent behavior across agent types.
"""

# Core workflow for tackling complex tasks
WORKFLOW_PATTERNS = """
## Workflow for Complex Tasks

### 1. Understand Before Acting
- Read code before modifying it
- Search for similar patterns already in the codebase
- When requirements are ambiguous, use `ask_followup_question` tool (not text output)
  - ONLY after exploring the codebase first - questions should be informed by research
  - ONLY one question at a time - never ask multiple questions in parallel
  - Ask the most critical question first, then continue based on the answer

### 2. Break Down Hard Problems
When facing a task you don't immediately know how to solve:

a) **Decompose**: Split into smaller, concrete sub-tasks
b) **Explore**: Use sub-agents to gather context (can run in parallel)
c) **Plan**: Write out your approach before implementing
d) **Submit**: Use `exit_plan` tool when your plan is ready for user approval
e) **Execute**: Work through tasks one at a time
f) **Validate**: Check your work against requirements

### 3. Use Sub-Agents Strategically
Spawn sub-agents via the `task` tool when you need:
- **Explore**: Find files, patterns, or understand code structure
- **Plan**: Design implementation approach for complex features

Guidelines:
- Launch multiple Explore agents in parallel for independent searches
- Use sub-agents for focused work that would clutter your context
- Prefer sub-agents over doing 5+ search operations yourself

### 4. Track Progress
For multi-step tasks, mentally track what's done and what's next.
Update the user on progress for long-running work.
"""

# Exploration strategy for code navigation
EXPLORATION_STRATEGY = """
## Exploration Strategy

### Phase 1: Orient (Where to Start)
Before searching randomly, understand the codebase structure:

```
list_files("src")   → Understand directory structure
glob("**/*.py")     → Find all Python files
```

### Phase 2: Search (Find Relevant Code)
Use the right tool for the job:

| Tool | Searches | Use When | Example |
|------|----------|----------|---------|
| `glob` | File paths/names | Know filename pattern | `glob("**/auth*.py")` |
| `grep` | File contents | Know exact text | `grep("def authenticate")` |
| `semantic_search` | Conceptual meaning | Fuzzy/conceptual | `semantic_search("user login flow")` |

**Parallel searches**: Run 2-3 searches together when exploring:
```
# In one response, invoke all three:
grep("authenticate")
grep("login")
grep("session")
→ All run concurrently, results return together
```

### Phase 3: Understand (Deep Dive)
Once you find relevant code:

```
read_file("src/auth/manager.py")
→ Read the full file to understand implementation

read_file("src/auth/manager.py", offset=45, limit=30)
→ Read specific section (lines 45-75)
```

Follow imports and function calls manually by reading related files.

### Tool Selection Quick Reference

| Goal | Best Tool |
|------|-----------|
| Find by filename | `glob` |
| Find by content | `grep` |
| Find by concept | `semantic_search` |
| Read code | `read_file` |
| List directory | `list_files` |
| Web research | `web` |

### When Stuck
1. **Wrong results?** → Try `semantic_search` with different phrasing
2. **Too many results?** → Add more specific terms to grep
3. **Need context?** → Read imports at top of file, follow them
4. **Still lost?** → Ask user ONE focused question with `ask_followup_question` (after exhausting search options)

### Stopping Criteria
You have enough context when you can answer:
- What files/functions are involved?
- What patterns does the codebase use?
- What would need to change?

Stop exploring when you can confidently describe the implementation approach.
"""

# Output formatting guidelines
OUTPUT_GUIDELINES = """
## Output Guidelines
- Cite specific files and line numbers
- Show relevant code snippets
- Be concise but thorough
- Explain your reasoning for complex decisions
- NEVER provide time estimates (hours, days, weeks)
"""

# Parallel tool execution patterns
PARALLEL_EXECUTION = """
## Parallel Tool Execution

You can execute multiple tools concurrently by invoking them in a single response.

### How It Works
- Multiple tool invocations in one message execute concurrently, not sequentially
- Results return together before continuing

### Use Parallel Execution For:
- Reading multiple files simultaneously
- Running independent grep/glob searches
- Launching multiple sub-agents for independent exploration
- Any independent operations that don't depend on each other

### Use Sequential Execution When:
- One tool's output is needed for the next (dependencies)
- Example: read a file before editing it
- Example: mkdir before cp, git add before git commit

### Example
Instead of:
1. grep for "authenticate" → wait for results
2. grep for "login" → wait for results
3. grep for "session" → wait for results

Do this in ONE message:
- grep for "authenticate"
- grep for "login"
- grep for "session"
→ All three run concurrently, results return together
"""

# Efficiency rules for sub-agents with limited turns
EFFICIENCY_RULES = """
## Efficiency Rules
- If you find what you need, STOP - don't keep searching
- If 3 searches return nothing, try different terms or report "not found"
- Read only the parts of files you need (use offset/limit for large files)
- Don't read entire files when you only need a specific function
- Parallelize independent searches - invoke multiple tools in one response
"""

# Structured output format for exploration results
EXPLORATION_OUTPUT_FORMAT = """
## Output Format
Structure your final response as:

**Summary**: 1-2 sentence answer to the task

**Key Findings**:
- `file:line` - Description of what you found
- `file:line` - Another finding

**Files Explored**: [list of files you read]

**Confidence**: high/medium/low
"""

# Plan template for Plan sub-agents (returns to main agent)
PLAN_TEMPLATE = """
## Adaptive Plan Structure

Adapt your plan structure based on these factors:

| Factor | Simple Task | Complex Task |
|--------|-------------|--------------|
| **Complexity** | Checklist format | Phases with rollback points |
| **Risk** | Minimal detail | Detailed with edge cases |
| **Uncertainty** | Prescriptive steps | Exploratory phases first |
| **Scope** | Implicit boundaries | Explicit scope & non-goals |

### Required Sections (always include)

**Summary**: What and why (1-2 sentences)

**Critical Files**: Files to modify with line numbers - this bridges to execution
- `path/to/file.py:45-60` - What changes

### Conditional Sections (include only if needed)

**Files to Create**: Only if creating new files
**Phases**: Only for multi-phase work (each phase independently testable)
**Risks**: Only if non-trivial risks exist
**Open Questions**: Only if genuine unknowns - mark explicitly, don't hide uncertainty
**Testing**: Only if tests needed beyond obvious

### Principles
- Each section must "earn its place" - no empty boilerplate
- Detail scales with risk (logout button ≠ database migration)
- Follow existing codebase patterns, not novel approaches
- Mark unknowns explicitly rather than pretending certainty

### Anti-patterns to Avoid
- Over-planning simple tasks
- Under-planning complex/risky ones
- Hiding uncertainty behind confident language
- Ignoring existing patterns in the codebase

Your output will be reviewed by the main agent, who will consolidate findings and submit the final plan for user approval.
"""

# Guidelines (no time estimates)
SIZING_GUIDELINES = """
## Guidelines
- NEVER include time estimates (no hours, days, weeks, sprints, timelines)
- Focus on what needs to be done, not how long it takes
"""
