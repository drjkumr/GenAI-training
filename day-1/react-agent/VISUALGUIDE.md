# 🎯 ReAct Agent - Visual Architecture & Reference Guide

Visual representations and quick references for the complete system.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           BROWSER (localhost:5173)                      │
│  ┌──────────────xxxxxx──────────────xxxxxx─────────────────────────┐  │
│  │ ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │  │
│  │ │   ChatWindow │  │  Reasoning   │  │ Tools Panel            │ │  │
│  │ │   (Messages) │  │   Panel      │  │ (Tool Executions)      │ │  │
│  │ │              │  │ (Thinking)   │  │                        │ │  │
│  │ │ • User msg   │  │              │  │ 🧮 calculator          │ │  │
│  │ │ • Bot resp   │  │ 💭 Thought   │  │   Input: {expr: "2*3"} │ │  │
│  │ │ • Clickable  │  │ 🎯 Action    │  │   Output: Result: 6    │ │  │
│  │ │              │  │ 👁️ Observe   │  │                        │ │  │
│  │ │ [msg1]       │  │              │  │ 🔍 web_search         │ │  │
│  │ │ [msg2] ← ← ←─┼──────┬─────────┼──┤   Input: {query: ...} │ │  │
│  │ │ [msg3]       │  │    │         │  │   Output: ...         │ │  │
│  │ │              │  │    │ (shows  │  │                        │ │  │
│  │ │              │  │    │ details)│  │                        │ │  │
│  │ └──────────────┘  └────┼─────────┘  └────────────────────────┘ │  │
│  │                        │                                         │  │
│  │  ┌──────────────────────┼────────────────────────────────────┐ │  │
│  │  │  Input Box                    [Send] [Reset]            │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────┬───────────────────────────────────┘  │
└─────────────────────────────────┼─────────────────────────────────────┘
        HTTP REST API
        POST /api/chat
        GET /api/history
        POST /api/reset
        (JSON over HTTP)
                 │
    ┌────────────▼────────────┐
    │                         │
    │ Backend Server          │
    │ (localhost:3001)        │
    │                         │
    │  ┌───────────────────┐  │
    │  │  index.ts         │  │
    │  │ (Express Server)  │  │
    │  │                   │  │
    │  │ POST /api/chat    │  │
    │  │  └─→ Extract msg  │  │
    │  │  └─→ Call agent   │  │
    │  │  └─→ Return resp  │  │
    │  └───────┬───────────┘  │
    │          │              │
    │  ┌───────▼───────────┐  │
    │  │  agent.ts         │  │
    │  │ (ReAct Loop)      │  │
    │  │                   │  │
    │  │  while loop < 5:  │  │
    │  │   1. Parse resp   │  │
    │  │   2. Get action   │  │
    │  │   3. Run tool     │  │
    │  │   4. Get obs      │  │
    │  │   5. Continue     │  │
    │  │                   │  │
    │  │ Uses:             │  │
    │  │ • prompts.ts      │  │
    │  │ • tools.ts        │  │
    │  │ • types.ts        │  │
    │  └──────┬────────────┘  │
    │         │               │
    │  ┌──────▼────────────┐  │
    │  │ Gemini API        │  │
    │  │ (Google Cloud)    │  │
    │  │                   │  │
    │  │ • Takes prompt    │  │
    │  │ • Returns thought │  │
    │  │ • Returns action  │  │
    │  │ • Returns input   │  │
    │  └───────────────────┘  │
    │                         │
    └─────────────────────────┘
```

---

## ReAct Agent Processing Flow

```
INPUT: "Calculate 50 * 3 then add 5"

                      ┌──────────────────┐
                      │  Agent Receives  │
                      │  User Message    │
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │ ITERATION 1      │
                      └────────┬─────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
      ┌────▼────┐         ┌────▼────┐        ┌────▼──────┐
      │ 💭      │         │ 🎯      │        │ 🧮        │
      │ THINK   │ ──────► │ ACTION  │ ─────► │ EXECUTE   │
      │         │         │         │        │ TOOL      │
      │ Need to │         │ Call    │        │           │
      │ calc    │         │ calc    │        │ "50 * 3"  │
      │         │         │ with    │        │ = 150     │
      │         │         │ "50*3"  │        │           │
      └─────────┘         └────┬────┘        └─────┬─────┘
                                │                   │
                      ┌─────────▼───────────────────▼──┐
                      │ 👁️ OBSERVATION                │
                      │ "Result: 150"                 │
                      └─────────┬──────────────────────┘
                                │
                      ┌─────────▼─────────┐
                      │ Loop check:       │
                      │ • Iteration < 5?  │ YES
                      │ • Has action?     │ YES
                      │ Continue loop     │
                      └─────────┬─────────┘
                                │
                      ┌────────▼─────────┐
                      │ ITERATION 2      │
                      └────────┬─────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
      ┌────▼────┐         ┌────▼────┐        ┌────▼──────┐
      │ 💭      │         │ 🎯      │        │ 🧮        │
      │ THINK   │ ──────► │ ACTION  │ ─────► │ EXECUTE   │
      │         │         │         │        │ TOOL      │
      │ Now add │         │ Call    │        │           │
      │ 5 to    │         │ calc    │        │ "150 + 5" │
      │ result  │         │ with    │        │ = 155     │
      │         │         │ "150+5" │        │           │
      └─────────┘         └────┬────┘        └─────┬─────┘
                                │                   │
                      ┌─────────▼───────────────────▼──┐
                      │ 👁️ OBSERVATION                │
                      │ "Result: 155"                 │
                      └─────────┬──────────────────────┘
                                │
                      ┌─────────▼─────────┐
                      │ Loop check:       │
                      │ • Has action?     │ NO
                      │ STOP LOOP         │
                      └─────────┬─────────┘
                                │
                      ┌────────▼─────────┐
                      │ Final Response   │
                      │                  │
                      │ "The first calc  │
                      │  gives 150, and  │
                      │  adding 5 equals │
                      │  155"            │
                      └──────────────────┘

OUTPUT: Message with reasoning + tool calls visible in UI
```

---

## ReAct Pattern Explained Visually

```
The ReAct Loop (simplified):

Step 1: USER PROMPT
┌────────────────────────┐
│ "What is 10 * 5?"      │
└────────────┬───────────┘
             │
Step 2: GEMINI THINKS + ACTS
┌────────────▼──────────────────────────────┐
│ Gemini Response (structured):             │
│                                           │
│ Thought: The user wants a calculation.    │
│ Action: calculator                        │
│ Input: {"expression": "10 * 5"}          │
└────────────┬──────────────────────────────┘
             │
Step 3: WE EXECUTE TOOL
┌────────────▼──────────────────┐
│ Execute tool: calculator       │
│ Result: "Result: 50"           │
└────────────┬──────────────────┘
             │
Step 4: WE PROVIDE OBSERVATION
┌────────────▼──────────────────────────────┐
│ User or Agent: "Tool gave us: Result: 50" │
└────────────┬──────────────────────────────┘
             │
Step 5: CHECK IF MORE NEEDED
┌────────────▼──────────────────┐
│ Does agent need more actions? │
│ • If YES → Loop back to 2     │
│ • If NO → Go to step 6        │
└────────────┬──────────────────┘
             │
Step 6: FINAL RESPONSE
┌────────────▼──────────────────────┐
│ Gemini responds to user:          │
│ "10 * 5 = 50"                    │
│                                  │
│ (with full reasoning shown)      │
└──────────────────────────────────┘
```

---

## Code Organization Flowchart

```
User Opens Browser
        ↓
React loads [main.tsx]
        ↓
Renders [App.tsx]
    ├─→ [ChatWindow.tsx]
    ├─→ [ReasoningPanel.tsx]
    └─→ [ToolsPanel.tsx]

┌─────── App.tsx handles all state ────────┐
│                                          │
│  state:                                  │
│  • messages[]                            │
│  • selectedMessageId                     │
│  • isLoading                             │
│  • error                                 │
│                                          │
│  functions:                              │
│  • handleSendMessage()  ◄─── calls API   │
│  • handleResetChat()                     │
│  • handleSelectMessage()                 │
└──────────────────────────────────────────┘

API Call to Backend:
        ↓
[index.ts] receives POST /api/chat
        ↓
Calls runAgent() from [agent.ts]
        ├─→ Uses [prompts.ts] for system prompt
        ├─→ Uses [tools.ts] for tools
        ├─→ Uses [types.ts] for types
        └─→ Calls Gemini API
        ↓
Returns AgentResponse
        ↓
API returns to Frontend
        ↓
App.tsx updates state
        ↓
Components re-render with new data
```

---

## Tool System Diagram

```
┌─────────────────────────────────────┐
│ Available Tools in tools.ts         │
├─────────────────────────────────────┤
│                                     │
│  ┌────────────────────────────────┐ │
│  │ calculatorTool                 │ │
│  │  ├─ name: "calculator"         │ │
│  │  ├─ description: "Calculates"  │ │
│  │  ├─ inputSchema: {...}         │ │
│  │  └─ execute: (input) => {...}  │ │
│  └────────────────────────────────┘ │
│                                     │
│  ┌────────────────────────────────┐ │
│  │ webSearchTool                  │ │
│  │  ├─ name: "web_search"         │ │
│  │  ├─ description: "Searches"    │ │
│  │  ├─ inputSchema: {...}         │ │
│  │  └─ execute: (input) => {...}  │ │
│  └────────────────────────────────┘ │
│                                     │
│  ┌────────────────────────────────┐ │
│  │ fileReaderTool                 │ │
│  │  ├─ name: "file_reader"        │ │
│  │  ├─ description: "Reads files" │ │
│  │  ├─ inputSchema: {...}         │ │
│  │  └─ execute: (input) => {...}  │ │
│  └────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
           ↓
    Exported in tools[] array
           ↓
    Available to agent at runtime
           ↓
    ┌──────────────────────┐
    │ getTool(name)        │
    │ → looks up tool      │
    │ → executes it        │
    │ → returns result     │
    └──────────────────────┘
```

---

## Type Flow Diagram

```
Communication Chain:

FRONTEND
┌─────────────────────────────────┐
│ Message {                       │
│   id: string                    │
│   role: "user" | "assistant"    │
│   content: string               │
│   timestamp: number             │
│   agentData?: {                 │
│     steps: ReActStep[]          │
│     toolCalls: ToolCall[]       │
│   }                             │
│ }                               │
└─────────────────────────────────┘
         ↓ (HTTP POST)
BACKEND
┌─────────────────────────────────┐
│ AgentResponse {                 │
│   success: boolean              │
│   steps: ReActStep[]            │
│   finalResponse: string         │
│   toolCalls: ToolCall[]         │
│   error?: string                │
│ }                               │
│                                 │
│ ReActStep {                     │
│   thought?: string              │
│   action?: {                    │
│     tool: string                │
│     input: Record<...>          │
│   }                             │
│   observation?: string          │
│ }                               │
└─────────────────────────────────┘
         ↓ (HTTP 200)
FRONTEND (re-render)
```

---

## UI Layout Percentages

```
┌─────────────────────────────────────────────┐
│            Header (Blue Bar)                 │
│  ReAct Agent Demo | Reasoning + Acting     │
├──────────┬──────────┬────────────┬─────────┤
│          │          │            │         │
│          │          │            │         │
│ CHAT     │REASONING │   TOOLS    │  (rest) │
│ WINDOW   │  PANEL   │   PANEL    │         │
│          │          │            │         │
│  30%     │  35%     │    35%     │         │
│          │          │            │         │
│          │          │            │         │
│          │          │            │         │
│          │          │            │         │
├──────────┴──────────┴────────────┴─────────┤
│          Input Box         [Send] [Reset]  │
│                       Footer (Gray Bar)    │
└─────────────────────────────────────────────┘
```

---

## State Management Flow

```
┌─────────────────────────────────────┐
│        App.tsx State                │
├─────────────────────────────────────┤
│                                     │
│  messages: Message[] = [            │
│    {id, role, content, agentData}   │
│    {id, role, content, agentData}   │
│    ...                              │
│  ]                                  │
│                                     │
│  selectedMessageId: string | null   │
│  (which message is being viewed)    │
│                                     │
│  inputValue: string                 │
│  (what user is typing)              │
│                                     │
│  isLoading: boolean                 │
│  (API call in progress?)            │
│                                     │
│  error: string | null               │
│  (error to show user)               │
│                                     │
└─────────────────────────────────────┘
       ↓ (passed as props)
   ┌───┴────┬────────┬───────┐
   ▼        ▼        ▼       ▼
ChatWin Reasoning Tools   Input
 Panel    Panel    Panel   Area

All updates trigger re-render
```

---

## Configuration Relationships

```
Environment Setup
├─ GEMINI_API_KEY
│  └─ Used by agent.ts
│     └─ Gemini API client init
├─ PORT
│  └─ Used by index.ts
│     └─ Express server listen
└─ NODE_ENV
   └─ Logged on startup

TypeScript Configuration
├─ tsconfig.json (backend)
│  └─ Compiles *.ts → dist/
├─ tsconfig.json (frontend)
│  └─ Type checking for React
└─ tsconfig.node.json (vite config)
   └─ Build tool config

Package Dependencies
├─ Backend
│  ├─ @google-ai/generativeai → agent.ts
│  ├─ express → index.ts
│  ├─ cors → index.ts
│  └─ dotenv → index.ts
└─ Frontend
   ├─ react → App.tsx + components
   ├─ vite → bundling
   └─ @vitejs/plugin-react → JSX
```

---

## Error Handling Paths

```
User Message
    ↓
API Call
    ├─ Network Error
    │   ↓
    │   Display "Cannot connect to backend"
    │   (check if server is running)
    │
    └─ Server Response
        ├─ Success (200)
        │   ↓
        │   Display response
        │   Show reasoning & tools
        │
        ├─ API Key Error (500)
        │   ↓
        │   Display "GEMINI_API_KEY not configured"
        │
        ├─ Agent Error (500)
        │   ↓
        │   Agent returns error in response
        │   Display error message
        │
        └─ Tool Execution Error
            ↓
            Tool catches error
            Returns error as observation
            Agent sees error & may retry

All errors caught, none crash the app!
```

---

## Extension Points (Easy to Hard)

```
EASY (5-10 min)
├─ Add new tool
│  Modify: tools.ts only
│  Add: Tool object + to array
│
├─ Change Gemini model
│  Modify: agent.ts (1 line)
│  Options: gemini-pro, gemini-1.5-flash, etc
│
└─ Modify system prompt
   Modify: prompts.ts
   Edit: generateSystemPrompt() function

MEDIUM (30-60 min)
├─ Add database persistence
│  Create: db.ts
│  Modify: index.ts (messageStore)
│
├─ Add streaming responses
│  Modify: index.ts, App.tsx
│  Integrate: Server-Sent Events
│
└─ Add request validation
   Create: validation middleware
   Modify: index.ts

HARD (2-4 hours)
├─ Multi-agent system
│  Create: agents/
│  Add: Agent communication layer
│
├─ Function calling instead of tools
│  Modify: agent.ts, prompts.ts
│  Study: Gemini function-calling API
│
└─ Real tool implementations
   Implement: Actual APIs
   Security: Add rate limiting, auth
```

---

## Quick Reference Tables

### File Responsibilities

| File | Purpose | Lines | Complexity |
|------|---------|-------|-----------|
| index.ts | REST API server | 113 | ⭐⭐ |
| agent.ts | ReAct loop core | 153 | ⭐⭐⭐ |
| tools.ts | Tool definitions | 102 | ⭐ |
| prompts.ts | Prompt templates | 62 | ⭐⭐ |
| types.ts | Type definitions | 48 | ⭐ |
| App.tsx | Main UI layout | 148 | ⭐⭐ |
| ChatWindow | Message display | 94 | ⭐ |
| ReasoningPanel | Reasoning display | 89 | ⭐ |
| ToolsPanel | Tools display | 88 | ⭐ |

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/chat | Send message |
| GET | /api/history | Get messages |
| POST | /api/reset | Clear history |
| GET | /api/health | Status check |

### React Components

| Component | Role | Props |
|-----------|------|-------|
| App | Orchestrator | - |
| ChatWindow | Display | messages, selectedId |
| ReasoningPanel | Display | steps, loading |
| ToolsPanel | Display | toolCalls, loading |

---

**This visual guide provides quick reference to the entire system architecture! 🎯**

Use alongside code comments and documentation for complete understanding.
