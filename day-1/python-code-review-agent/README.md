# Python Code Review Agent - Simple Self-Reflecting Demo

A minimal, working demonstration of a **self-reflecting AI code review agent** that analyzes Python code using AST and uses Claude Haiku to iteratively improve its suggestions.

**Build time:** 45 minutes | **Complexity:** Minimal | **Learning value:** High

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│   Frontend (HTML + Vanilla JS)      │
│  ┌─────────────────────────────────┐│
│  │ Code Input | Review Button      ││
│  │ AI Suggestions (Self-Reflected) ││
│  └─────────────────────────────────┘│
└──────────────┬──────────────────────┘
               │ HTTP POST /review
               ↓
┌──────────────────────────────────────────┐
│     Backend (Express + TypeScript)       │
│  ┌──────────────────────────────────────┐│
│  │ Step 1: Subprocess call to analyzer  ││
│  │  (Python AST → JSON findings)        ││
│  │                                      ││
│  │ Step 2: Claude API (Initial review)  ││
│  │  (Code + AST findings → suggestions) ││
│  │                                      ││
│  │ Step 3: Claude API (Self-reflection) ││
│  │  (Code + suggestions → improved)     ││
│  │                                      ││
│  │ Step 4: Return results to frontend   ││
│  └──────────────────────────────────────┘│
└──────────────────────────────────────────┘
```

---

## Project Structure

```
python-code-review-agent/
├── backend/
│   ├── src/
│   │   └── server.ts           # Express server + API endpoints
│   ├── analyzer.py             # Python AST analyzer (subprocess)
│   ├── package.json            # Node dependencies
│   └── tsconfig.json           # TypeScript config
├── frontend/
│   └── index.html              # Single HTML file with inline JS
├── .env.example                # Environment template
└── README.md                   # This file
```

---

## Installation (5 minutes)

### Prerequisites
- Node.js 18+ (`node --version`)
- Python 3.8+ (`python --version`)
- Claude API key from [console.anthropic.com](https://console.anthropic.com)

### Setup

```bash
# Backend
cd backend
npm install

# Copy env template
cp ../.env.example ../.env

# Edit .env and add your ANTHROPIC_API_KEY
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

### Start Backend
```bash
cd backend
npm run dev
# Output: ✅ Python Code Review Agent running on http://localhost:5000
```

### Open Frontend
In a browser:
```
http://localhost:5000/frontend/index.html
```

---

## How It Works: The Self-Reflection Loop

### Step-by-Step Workflow

```
1. User Input
   └─ Python code in textarea

2. Frontend sends POST /review
   └─ { code: "def hello():\n    print('world')" }

3. Backend Step 1: AST Analysis
   └─ Calls Python subprocess (analyzer.py)
   └─ Returns: { syntax_valid: true, functions: [...], issues: [...] }

4. Backend Step 2: Initial Claude Review
   └─ Prompt: "You are a Python code reviewer. Analyze this code..."
   └─ Sends: Code + AST findings
   └─ Returns: 3-5 suggestion points

5. Backend Step 3: SELF-REFLECTION (The Key)
   └─ Prompt: "Review your suggestions critically and improve them..."
   └─ Sends: Code + previous suggestions
   └─ Returns: Prioritized, refined suggestions

6. Frontend displays results
   └─ AST findings + final improved suggestions
```

---

## Key Components

### 1. Backend Server (`backend/src/server.ts`)

```typescript
// Receives code from frontend
POST /review
Input:  { code: "python code string" }
Output: {
  astFindings: { ... },           // From Python analyzer
  initialSuggestions: "...",      // First Claude pass
  improvedSuggestions: "..."      // Second Claude pass (self-reflection)
}
```

**Key functions:**
- `runPythonAnalyzer()` - Spawns Python subprocess, captures JSON
- `getInitialReview()` - First Claude pass (model: claude-haiku-4-5-20251001)
- `reflectAndImprove()` - Second Claude pass (self-reflection)

### 2. Python Analyzer (`backend/analyzer.py`)

Uses Python's built-in `ast` module (no external dependencies):

```python
# Detects:
✓ Syntax errors
✓ Function/class definitions
✓ Imports
✓ Code quality issues (bare except, unused vars, etc.)

# Returns JSON to stdout for Node.js to parse
```

Example output:
```json
{
  "syntax_valid": true,
  "functions": [{"name": "hello", "line": 1, "args": []}],
  "imports": [],
  "issues": []
}
```

### 3. Frontend (`frontend/index.html`)

Single HTML file with:
- Code textarea input
- Output box for results
- Vanilla JavaScript (no frameworks)
- Real-time UI updates

---

## The Two Claude Prompts

### Prompt 1: Initial Analysis

```
You are an expert Python code reviewer. Analyze this Python code and provide 
clear, practical improvement suggestions.

STATIC ANALYSIS FINDINGS:
[AST results: functions, imports, issues]

PYTHON CODE:
```python
[User's code here]
```

Provide 3-5 specific, actionable suggestions focusing on:
- Code clarity and readability
- Performance improvements
- Best practices
- Error handling

Format each suggestion with a title and explanation.
```

### Prompt 2: Self-Reflection (The Improvement)

```
You are a senior Python architect reviewing code suggestions.

ORIGINAL CODE:
```python
[User's code here]
```

YOUR PREVIOUS SUGGESTIONS:
[Suggestions from prompt 1]

TASK:
1. Review your previous suggestions critically
2. Identify the most impactful improvements
3. Refine any vague or unclear suggestions
4. Reorganize by priority (most important first)
5. Add 1-2 additional improvements if you spot important issues

OUTPUT:
Provide improved, prioritized suggestions. Be more specific and actionable than before.
```

---

## Example: Input → Output

### Input Python Code
```python
def process_data(items):
    result = []
    for i in range(len(items)):
        if items[i] > 0:
            result.append(items[i] * 2)
    return result
```

### Step 1: AST Analysis
```
✅ Syntax Valid
📍 Functions: process_data
⚠️  Issues: None
```

### Step 2: Initial Claude Suggestions
```
1. Use list comprehension for better performance
   - Your loop-append pattern is slower than a single list comprehension

2. Add type hints
   - def process_data(items: list[int]) -> list[int]:

3. Add docstring
   - Document what the function does
```

### Step 3: Self-Reflected Suggestions (Improved)
```
PRIORITY 1 - Performance (Quick Win):
Replace loop with list comprehension:
  result = [x * 2 for x in items if x > 0]
This is 3-5x faster and more Pythonic.

PRIORITY 2 - Type Safety:
Add type hints for clarity:
  def process_data(items: list[int]) -> list[int]:

PRIORITY 3 - Documentation:
Add a docstring explaining parameters and return value.

PRIORITY 4 - Flexibility:
Consider parameterizing the multiplier (currently hardcoded as 2).
```

---

## Environment Variables

Create `backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxx
PORT=5000
```

**Where to get:**
- ANTHROPIC_API_KEY: [console.anthropic.com](https://console.anthropic.com) → API Keys
- PORT: Optional, defaults to 5000

---

## Claude Model Used

**Model:** `claude-haiku-4-5-20251001`

This is the lightweight Haiku model optimized for:
- Fast inference (ideal for iterative passes)
- Lower cost (2x cheaper than Sonnet)
- Excellent code analysis capabilities

```typescript
const response = await client.messages.create({
  model: "claude-haiku-4-5-20251001",  // DO NOT CHANGE
  max_tokens: 800,                      // Adjust as needed
  messages: [...]
});
```

---

## How Node Talks to Python

```typescript
// In server.ts:
const python = spawn("python", ["analyzer.py", codeString], {
  cwd: __dirname,  // Run from backend/ directory
});

// Python outputs JSON to stdout
python.stdout.on("data", (data) => {
  const findings = JSON.parse(data);  // Parse JSON
});
```

This approach:
- ✅ No external Python dependencies (uses built-in `ast` module)
- ✅ Secure (Python code runs as subprocess)
- ✅ Fast (Python AST is instantaneous)
- ✅ Simple (just spawn + read stdout)

---

## Dependencies

### Backend (`package.json`)
- `express` - Web framework
- `cors` - Cross-origin requests (frontend access)
- `dotenv` - Load environment variables
- `@anthropic-ai/sdk` - Claude API client
- `typescript` - Type safety
- `ts-node` - Run TypeScript directly

### Frontend
- None! (Pure HTML + vanilla JavaScript)

### Python
- None! (Uses only built-in `ast` module)

---

## Quick Start Commands

```bash
# Terminal 1: Backend
cd backend
npm install
npm run dev

# Terminal 2: Frontend
# Just open in browser:
http://localhost:5000/frontend/index.html

# Test with example Python code:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| "Cannot find module 'express'" | `cd backend && npm install` |
| "ANTHROPIC_API_KEY not configured" | Check `backend/.env` file exists |
| Python analyzer not found | Ensure `analyzer.py` is in `backend/` directory |
| Port 5000 in use | Change `PORT` in `.env` |
| CORS error | Ensure backend is running before opening frontend |

---

## API Reference

### POST /review

**Request:**
```bash
curl -X POST http://localhost:5000/review \
  -H "Content-Type: application/json" \
  -d '{"code":"def hello():\n    print(\"world\")"}'
```

**Response (200 OK):**
```json
{
  "astFindings": {
    "syntax_valid": true,
    "functions": [
      {"name": "hello", "line": 1, "args": []}
    ],
    "classes": [],
    "imports": [],
    "issues": []
  },
  "initialSuggestions": "1. Add docstring...",
  "improvedSuggestions": "PRIORITY 1 - Documentation...",
  "finalOutput": "..."
}
```

---

## Extension Ideas

1. **Support multiple languages** - Add JavaScript, TypeScript analyzers
2. **Persistent history** - Store reviews in JSON/SQLite
3. **Batch processing** - Review multiple files
4. **Streaming responses** - Real-time suggestion generation
5. **Web UI** - Deploy frontend separately
6. **Custom prompts** - Let users define review focus areas

---

## Learning Outcomes

After building this, you'll understand:

✓ How to spawn Python subprocesses from Node.js
✓ How to use Python's `ast` module for code analysis
✓ How Claude API works with streaming/non-streaming
✓ The self-reflection agent pattern (AI improving its own output)
✓ Building a full-stack agent in 45 minutes
✓ CORS, Express routing, TypeScript basics

---

## Production Checklist

Before deploying:

- [ ] Add rate limiting
- [ ] Input validation (max code length)
- [ ] Error logging (Sentry/LogRocket)
- [ ] HTTPS only
- [ ] API key rotation
- [ ] Cost monitoring (Claude API usage)
- [ ] Tests (Jest for TypeScript)

---

## File Reference

| File | Purpose |
|------|---------|
| `backend/src/server.ts` | Express API + orchestration |
| `backend/analyzer.py` | Python AST analysis |
| `frontend/index.html` | UI + client-side logic |
| `.env.example` | Environment template |

---

## Support

1. Check that `backend/` is running (port 5000)
2. Verify ANTHROPIC_API_KEY in `.env`
3. Ensure Python is installed (`python --version`)
4. Check browser console for errors

---

**Ready to go!** Start with the Backend setup above. You'll have a working code review agent in ~45 minutes. 🚀
