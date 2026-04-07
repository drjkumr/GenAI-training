# 📋 Project Structure & File Manifest

Complete reference for all files in the ReAct Agent application.

---

## Full Directory Tree

```
react-agent/
│
├── 📄 README.md                        Main guide (start here!)
├── 📄 SETUP.md                         Step-by-step setup instructions
├── 📄 ARCHITECTURE.md                  Technical architecture deep dive
├── 📄 EXAMPLES.md                      Example queries & expected output
├── 📄 INDEX.md                         Overview & learning path
├── 📄 MANIFEST.md                      This file
├── 🔧 .gitignore                       Git configuration
│
├── 📁 backend/                         Node.js + TypeScript Server
│   │
│   ├── 📁 src/
│   │   ├── 📄 index.ts                 Express server & REST API (113 lines)
│   │   │                                Exports:
│   │   │                                - Express app setup
│   │   │                                - POST /api/chat handler
│   │   │                                - GET /api/history handler
│   │   │                                - POST /api/reset handler
│   │   │                                - GET /api/health check
│   │   │
│   │   ├── 📄 agent.ts                 ReAct agent loop (153 lines)
│   │   │                                Exports:
│   │   │                                - runAgent(message, apiKey, history)
│   │   │                                - executeReActStep() [internal]
│   │   │                                - parseReActResponse() [internal]
│   │   │
│   │   ├── 📄 tools.ts                 Tool definitions (102 lines)
│   │   │                                Exports:
│   │   │                                - calculatorTool
│   │   │                                - webSearchTool
│   │   │                                - fileReaderTool
│   │   │                                - tools array
│   │   │                                - getTool(name)
│   │   │
│   │   ├── 📄 prompts.ts               Prompt templates (62 lines)
│   │   │                                Exports:
│   │   │                                - generateSystemPrompt(tools)
│   │   │                                - formatConversationHistory()
│   │   │                                - createPrompt()
│   │   │
│   │   └── 📄 types.ts                 TypeScript definitions (48 lines)
│   │                                    Exports:
│   │                                    - Tool interface
│   │                                    - ReActStep interface
│   │                                    - AgentResponse interface
│   │                                    - ChatMessage interface
│   │
│   ├── 📄 package.json                 NPM dependencies & scripts
│   │                                    Scripts:
│   │                                    - npm run dev (tsx with auto-reload)
│   │                                    - npm run build (compile to dist/)
│   │                                    - npm run start (run compiled)
│   │                                    - npm run type-check (TS check)
│   │
│   ├── 📄 tsconfig.json                TypeScript configuration
│   │                                    - Target: ES2020
│   │                                    - Strict: true
│   │                                    - Outdir: dist/
│   │
│   └── 📄 .env.example                 Environment variables template
│                                        - GEMINI_API_KEY (paste your key)
│                                        - PORT (default 3001)
│                                        - NODE_ENV (development/production)
│
├── 📁 frontend/                        React + Vite GUI Application
│   │
│   ├── 📁 src/
│   │   ├── 📄 App.tsx                  Main layout component (148 lines)
│   │   │                                Features:
│   │   │                                - 3-panel layout (chat, reasoning, tools)
│   │   │                                - Message send logic
│   │   │                                - Error display
│   │   │                                - Reset functionality
│   │   │
│   │   ├── 📄 main.tsx                 Entry point (10 lines)
│   │   │                                - React DOM render
│   │   │                                - Strict mode
│   │   │
│   │   └── 📁 components/              Reusable React components
│   │       │
│   │       ├── 📄 ChatWindow.tsx       Chat history display (94 lines)
│   │       │                            Features:
│   │       │                            - Message list
│   │       │                            - Click to select
│   │       │                            - Role colors
│   │       │                            - Tool call indicators
│   │       │                            - Timestamps
│   │       │
│   │       ├── 📄 ReasoningPanel.tsx   Reasoning display (89 lines)
│   │       │                            Features:
│   │       │                            - Show Thought steps
│   │       │                            - Show Action & Input
│   │       │                            - Show Observation
│   │       │                            - Loading state
│   │       │
│   │       └── 📄 ToolsPanel.tsx       Tools execution log (88 lines)
│   │                                    Features:
│   │                                    - Tool name & icon
│   │                                    - Input parameters
│   │                                    - Output results
│   │                                    - Tool call counter
│   │
│   ├── 📄 index.html                   HTML template
│   │                                    - Root div for React
│   │                                    - Vite script reference
│   │
│   ├── 📄 vite.config.ts               Vite build config
│   │                                    - React plugin
│   │                                    - Dev server port 5173
│   │                                    - Auto-open on start
│   │
│   ├── 📄 package.json                 NPM dependencies & scripts
│   │                                    Scripts:
│   │                                    - npm run dev (Vite dev server)
│   │                                    - npm run build (Production build)
│   │                                    - npm run preview (Preview build)
│   │
│   ├── 📄 tsconfig.json                TypeScript configuration
│   │                                    - React JSX support
│   │                                    - Strict mode
│   │
│   └── 📄 tsconfig.node.json           Config for Vite TS support
│
└── 📁 Documentation                    (Markdown guides)
    ├── README.md                       ~400 lines
    │                                    Main overview, quick start, how-to-extend
    ├── SETUP.md                        ~200 lines
    │                                    Step-by-step setup, troubleshooting
    ├── ARCHITECTURE.md                 ~500 lines
    │                                    System design, data flow, patterns
    ├── EXAMPLES.md                     ~400 lines
    │                                    Test queries, edge cases, debugging
    └── INDEX.md                        ~300 lines
                                         Learning path, concept overview
```

---

## File Count Summary

```
Backend Files:         5 (src) + 4 (config) = 9 total
Frontend Files:        5 (src + components) + 4 (config) = 9 total
Documentation Files:   6 (md files)
Config Files:          1 (.gitignore)

TOTAL FILES:           16 files
CODE FILES:            10 (TypeScript + React)
CONFIG FILES:          4 (package.json, tsconfig, etc.)
DOCS FILES:            6 (Markdown)
```

---

## Code Statistics

```
Backend Code:
  index.ts            113 lines
  agent.ts            153 lines
  tools.ts            102 lines
  prompts.ts           62 lines
  types.ts             48 lines
  ────────────────────────────
  SUBTOTAL:           478 lines

Frontend Code:
  App.tsx             148 lines
  ChatWindow.tsx       94 lines
  ReasoningPanel.tsx   89 lines
  ToolsPanel.tsx       88 lines
  main.tsx             10 lines
  ────────────────────────────
  SUBTOTAL:           429 lines

Configuration:
  Various:            ~50 lines total

TOTAL CODE:          ~957 lines

Documentation:
  README.md           ~400 lines
  SETUP.md            ~200 lines
  ARCHITECTURE.md     ~500 lines
  EXAMPLES.md         ~400 lines
  INDEX.md            ~300 lines
  MANIFEST.md         ~200 lines (this file)
  ────────────────────────────
  TOTAL DOCS:        ~2000 lines

GRAND TOTAL:        ~3000 lines (code + docs + config)
```

---

## Entry Points & Starting Files

### To Run Backend:
```bash
cd backend
npm install
npm run dev
# Uses: src/index.ts
```

### To Run Frontend:
```bash
cd frontend
npm install
npm run dev
# Uses: src/main.tsx → src/App.tsx
```

### To Read Code (learning order):
1. [backend/src/types.ts](../backend/src/types.ts) - Understand data structures
2. [backend/src/tools.ts](../backend/src/tools.ts) - See tool system
3. [backend/src/agent.ts](../backend/src/agent.ts) - ReAct loop (core!)
4. [backend/src/prompts.ts](../backend/src/prompts.ts) - Prompt engineering
5. [backend/src/index.ts](../backend/src/index.ts) - REST API
6. [frontend/src/App.tsx](../frontend/src/App.tsx) - Main UI
7. [frontend/src/components/*.tsx](../frontend/src/components/) - UI components

---

## Key Implementation Details

### Backend Flow

```
User Message
    ↓
[index.ts] POST /api/chat
    ↓
[agent.ts] runAgent()
    ├─→ Initialize Gemini client
    ├─→ Build prompt [prompts.ts]
    ├─→ Loop: executeReActStep()
    │    ├─→ Call Gemini API
    │    ├─→ Parse thought/action/input
    │    ├─→ If action: getTool() [tools.ts]
    │    ├─→ Execute tool
    │    ├─→ Get observation
    │    └─→ Loop again (max 5x)
    ├─→ Format response
    └─→ Return AgentResponse [types.ts]
        ↓
[index.ts] Return HTTP 200
    ↓
Response to Frontend
```

### Frontend Flow

```
User Input
    ↓
[App.tsx] handleSendMessage()
    ├─→ Add user message to state
    ├─→ POST to /api/chat
    ├─→ setIsLoading(true)
    ├─→ Wait for response
    ├─→ Add assistant message to state
    ├─→ setIsLoading(false)
    └─→ Re-render with:
        ├─→ New message in [ChatWindow.tsx]
        ├─→ Steps in [ReasoningPanel.tsx]
        └─→ Tools in [ToolsPanel.tsx]
```

---

## Dependencies

### Backend
```
@google-ai/generativeai  ^0.3.1  # Gemini API client
express                  ^4.18.2 # Web server
cors                     ^2.8.5  # CORS middleware
dotenv                   ^16.3.1 # Environment variables
typescript               ^5.2.2  # Type checking
tsx                      ^4.1.0  # Run TS directly
```

### Frontend
```
react                    ^18.2.0 # UI library
react-dom                ^18.2.0 # DOM rendering
@vitejs/plugin-react     ^4.0.0  # Vite React plugin
typescript               ^5.2.2  # Type checking
vite                     ^4.5.0  # Build tool
```

---

## Configuration Files Explained

### backend/.env.example
```bash
GEMINI_API_KEY=your_api_key_here    # Required: Get from aistudio.google.com
PORT=3001                            # Optional: Server port
NODE_ENV=development                # Optional: Environment
```

### backend/package.json
```json
{
  "scripts": {
    "dev": "tsx src/index.ts",          // Local dev with auto-reload
    "build": "tsc",                     // Build to dist/
    "start": "node dist/index.js",      // Run built code
    "type-check": "tsc --noEmit"        // Just check types
  }
}
```

### backend/tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",                 // Modern JS
    "strict": true,                     // Maximum type safety
    "module": "commonjs",               // Node.js modules
    "outDir": "./dist"                  // Build output
  }
}
```

### frontend/vite.config.ts
```typescript
{
  plugins: [react()],                   // React JSX support
  server: {
    port: 5173,                         // Dev server port
    open: true,                         // Auto-open browser
  },
}
```

---

## Environment Setup

### Required: Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy the key
4. Paste into `backend/.env` as `GEMINI_API_KEY`

### Optional: Custom Configuration
- Ports: Edit `SETUP.md` instructions and vite.config.ts
- Models: Edit `agent.ts` line ~85
- Tools: Add to `tools.ts` and export in array

---

## How Files Work Together

### Making a Request (Step by Step)

```
1. User types message in [App.tsx]
   ↓
2. Click Send → calls handleSendMessage()
   ↓
3. Fetch POST to http://localhost:3001/api/chat
   ↓
4. [index.ts] receives request
   ↓
5. Calls runAgent() from [agent.ts]
   ↓
6. Agent.ts calls generateSystemPrompt() from [prompts.ts]
   ↓
7. Agent.ts looks up tools from [tools.ts]
   ↓
8. Agent.ts uses types from [types.ts]
   ↓
9. Agent.ts calls Gemini API with prompt
   ↓
10. Parses Gemini response
   ↓
11. Executes tool from [tools.ts]
   ↓
12. Gets observation, loops if needed
   ↓
13. Returns AgentResponse to [index.ts]
   ↓
14. [index.ts] formats and returns HTTP response
   ↓
15. [App.tsx] receives response
   ↓
16. Updates state:
    - messages (chat)
    - selectedMessage (for panels)
    - isLoading
    ↓
17. Components re-render:
    - [ChatWindow.tsx] shows new message
    - [ReasoningPanel.tsx] shows steps
    - [ToolsPanel.tsx] shows tool calls
```

---

## Extension Points

Where to add new features:

| Feature | File(s) | Difficulty |
|---------|---------|-----------|
| New tool | tools.ts | Easy |
| API validation | index.ts | Easy |
| Different model | agent.ts | Easy |
| Custom prompt | prompts.ts | Easy |
| Streaming | index.ts, App.tsx | Medium |
| Database | new file | Medium |
| Authentication | index.ts, App.tsx | Medium |
| Tool schema validation | tools.ts | Medium |
| Multi-agent | new file | Hard |

---

## Testing Files

No test files included (keep it minimal), but these would test:

- `__tests__/tools.test.ts` → Tool execution
- `__tests__/agent.test.ts` → ReAct loop logic
- `__tests__/prompts.test.ts` → Prompt generation
- `__tests__/components.test.tsx` → React components

You can add these following Jest or Vitest patterns.

---

## Production Checklist

Before deploying, consider:

- [ ] Replace in-memory store with database
- [ ] Add user authentication
- [ ] Add rate limiting
- [ ] Add request validation
- [ ] Add error tracking (Sentry)
- [ ] Add logging
- [ ] Use environment variables for API keys
- [ ] Add input sanitization
- [ ] Add HTTPS (if public)
- [ ] Add monitoring/metrics

---

## File Modification Guide

### If You Want To...

**Add a new tool:**
→ Edit `backend/src/tools.ts`

**Change agent behavior:**
→ Edit `backend/src/agent.ts` (executeReActStep function)

**Change the system prompt:**
→ Edit `backend/src/prompts.ts` (generateSystemPrompt function)

**Change UI layout:**
→ Edit `frontend/src/App.tsx` (styles object at bottom)

**Add a new component:**
→ Create `frontend/src/components/MyComponent.tsx`

**Change API endpoint:**
→ Edit `frontend/src/App.tsx` (API_URL constant)

**Add database:**
→ Create `backend/src/db.ts` and import in `index.ts`

---

## Performance Notes

### Current Bottlenecks
1. Gemini API latency (1-3 seconds per call)
2. No caching (redundant API calls)
3. No streaming (wait for full response)

### Improvements Available
- Add response streaming
- Cache tool results
- Implement batch requests
- Use faster models (gemini-1.5-flash)

---

## Version Info

- **Version**: 1.0.0
- **Created**: 2024
- **Node**: 18+
- **React**: 18.2+
- **TypeScript**: 5.2+
- **API**: Gemini (Google AI Studio)

---

## Support Resources

- [README.md](../README.md) - Main guide
- [SETUP.md](../SETUP.md) - Setup instructions
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Technical details
- [EXAMPLES.md](../EXAMPLES.md) - Example queries
- [Google AI Studio](https://aistudio.google.com) - Get API key
- [Gemini API Docs](https://ai.google.dev) - API reference

---

**This manifest describes a complete, production-style ReAct agent implementation. Start with SETUP.md to get running! 🚀**
