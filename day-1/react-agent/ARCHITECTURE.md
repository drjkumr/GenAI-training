# Architecture & Design Deep Dive

This document explains the architectural decisions and how the ReAct pattern is implemented.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + Vite)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ ChatWindow   │  │Reasoning     │  │ Tools                │   │
│  │ (Message     │  │Panel (Thought│  │ Panel (Tool calls)   │   │
│  │ history)    │  │/Action/Obs)  │  │                      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                   │
│                           App.tsx                                │
│                    (State management)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                      HTTP (REST API)
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
    POST /api/chat   GET /api/history   POST /api/reset
                             │
┌────────────────────────────┴───────────────────────────────────┐
│                    BACKEND (Express + TS)                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    index.ts (Server)                     │   │
│  │  - Define REST endpoints                                │   │
│  │  - Parse incoming messages                              │   │
│  │  - Call agent.runAgent()                                │   │
│  │  - Return formatted response                            │   │
│  └──────────────────────────┬────────────────────────────┬─┘   │
│                             │                            │      │
│  ┌──────────────────────────▼──────┐  ┌────────────────▼──┐   │
│  │     agent.ts (ReAct Loop)       │  │   prompts.ts      │   │
│  │                                  │  │                  │   │
│  │  executeReActStep():             │  │ System prompt    │   │
│  │  1. Parse thought/action         │  │ (teaches pattern)│   │
│  │  2. Execute tool if action       │  │                  │   │
│  │  3. Get observation              │  │ Conversation fmt │   │
│  │  4. Loop (max 5 iterations)      │  │                  │   │
│  │  5. Return final response        │  │ Prompt creation  │   │
│  │                                  │  │                  │   │
│  │  runAgent():                     │  └──────────────────┘   │
│  │  - Initialize Gemini client      │                         │
│  │  - Call executeReActStep()      │  ┌──────────────────┐   │
│  │  - Return formatted response     │  │   tools.ts       │   │
│  └──────────────────────────────────┘  │                  │   │
│                                         │ calculatorTool   │   │
│  ┌──────────────────────────────────┐  │ webSearchTool    │   │
│  │        types.ts                  │  │ fileReaderTool   │   │
│  │                                  │  │                  │   │
│  │ Tool interface                   │  │ getTool(name)    │   │
│  │ ReActStep interface              │  │                  │   │
│  │ AgentResponse interface          │  └──────────────────┘   │
│  │ ChatMessage interface            │                         │
│  └──────────────────────────────────┘  ┌──────────────────┐   │
│                                         │   Gemini API     │   │
│                                         │   (external)     │   │
│                                         └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: User Message → Agent Response

### 1. Message Submission
```javascript
User types: "What is 25 * 4?"
↓
User clicks "Send"
↓
Frontend sends HTTP POST to /api/chat
  {
    message: "What is 25 * 4?"
  }
```

### 2. Backend Receipt
```typescript
// index.ts - POST /api/chat handler
- Parse JSON body
- Extract: message = "What is 25 * 4?"
- Call: runAgent(message, apiKey, conversationHistory)
```

### 3. Agent Loop (Core ReAct Pattern)
```typescript
// agent.ts - executeReActStep()

ITERATION 1:
┌─────────────────────────────────┐
│ 1. Build Prompt                 │
│    - System prompt (defines ReAct pattern)
│    - Conversation history       │
│    - User message               │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 2. Call Gemini API              │
│    Gemini returns:              │
│    "Thought: User wants...      │
│     Action: calculator          │
│     Input: {"expression"..."    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 3. Parse Response               │
│    Extract:                     │
│    - thought = "User wants..."  │
│    - action = "calculator"      │
│    - input = {expression: ...}  │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 4. Execute Tool                 │
│    Tool: calculator             │
│    Run: eval("25 * 4")          │
│    Result: "Result: 100"        │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 5. Add Observation              │
│    Loop condition:              │
│    - Max 5 iterations: CONTINUE │
│    - Tool result provided: YES  │
│                                 │
│    Add to history:              │
│    - Agent response             │
│    - Tool result                │
└────────────────┬────────────────┘
                 │
                 ▼
        ITERATION 2 (or STOP?)
```

### 4. Response Formatting
```typescript
// Still in agent.ts - after loop completes

Return AgentResponse:
{
  success: true,
  steps: [
    {
      thought: "User wants calculation",
      action: { tool: "calculator", input: {expression: "25 * 4"} },
      observation: "Result: 100"
    }
  ],
  finalResponse: "The result of 25 * 4 is 100.",
  toolCalls: [
    {
      tool: "calculator",
      input: {expression: "25 * 4"},
      result: "Result: 100"
    }
  ]
}
```

### 5. Backend Returns Response
```typescript
// index.ts - API response

HTTP 200 OK with JSON:
{
  id: "msg-1234567890-assistant",
  role: "assistant",
  content: "The result of 25 * 4 is 100.",
  agentData: {
    steps: [...],
    toolCalls: [...]
  }
}
```

### 6. Frontend Receives & Displays
```typescript
// App.tsx
- Store message in state
- Render ChatWindow with new message
- Populate ReasoningPanel with steps
- Populate ToolsPanel with toolCalls
- User can click message to see details
```

## The ReAct Prompt Pattern

### How It Works

The system prompt teaches Gemini to think step-by-step:

```
You are a helpful AI using the ReAct (Reasoning + Acting) pattern.

Your decision-making process MUST follow this structure:
1. Thought: Think about what the user is asking...
2. Action: Choose a tool to help...
3. Observation: Receive the tool's result
4. Response: Provide the final answer

Available tools:
- calculator: Performs mathematical calculations
  Parameters:
    - expression (string): A mathematical expression (e.g., '2 + 2')
...

Format tool calls EXACTLY like:
Action: [tool_name]
Input: {"param1": "value1"}
```

### Why This Works

1. **Clear Structure**: The template gives Gemini a clear format to follow
2. **Tool Awareness**: Gemini sees all available tools and their descriptions
3. **Parseable Output**: The consistent format makes it easy to extract Thought/Action/Input
4. **Reasoning Transparency**: Shows HOW the agent thinks, not just WHAT it answers

## Tool System Design

### Tool Interface
```typescript
interface Tool {
  name: string;                              // ID for selection
  description: string;                       // What it does (for Gemini)
  inputSchema: {                             // Input contract
    type: "object";
    properties: Record<string, unknown>;     // Parameter descriptions
    required: string[];                      // Required parameters
  };
  execute: (input: Record<string, unknown>) => Promise<string>;
}
```

### Adding Tools
Tools are defined once and automatically:
- Show up in the system prompt
- Can be called by Gemini
- Have inputs validated by schema
- Execute in a sandbox-like manner

To add a tool:
1. Create a `Tool` object in `tools.ts`
2. Add to `tools` array
3. That's it! Gemini learns to use it automatically

## Error Handling Strategy

### Tool Execution Errors
```typescript
// In executeReActStep:
try {
  const toolResult = await tool.execute(input);
} catch (error) {
  // Return error message as observation
  step.observation = `Error executing tool: ${error.message}`;
  // Agent loops again with error info
}
```

**Design**: Errors become observations
- Agent sees failure
- Can try alternative approach
- No hard crashes

### API Errors
```typescript
// In runAgent:
try {
  const response = await executeReActStep(...);
} catch (error) {
  return {
    success: false,
    error: `Agent error: ${error.message}`
  };
}
```

**Design**: API failures return gracefully
- Frontend gets error message
- User sees what went wrong
- No backend crash

## Iteration Limits

The agent runs max 5 iterations:
```typescript
while (iteration < maxIterations) { // maxIterations = 5
  // One ReAct step
}
```

**Why?**
- Prevents infinite loops
- Saves API costs
- Keeps responses fast
- Most queries solve in 1-2 steps

## Conversation Memory

Currently: **In-Memory Only**
```typescript
// index.ts
const messageStore: ChatMessage[] = [];

// On each chat request:
const conversationHistory = messageStore.map(msg => ({
  role: msg.role,
  content: msg.content
}));
// Send to agent
```

**Limitation**: Restarts server = lose history

**To Persist**: Replace with database like SQLite/PostgreSQL

## State Management Design

### Frontend (React)
```typescript
// App.tsx

const [messages, setMessages] = useState<Message[]>([]);
// All messages: user + assistant
// Each has agentData (steps, toolCalls)

const [selectedMessageId, setSelectedMessageId] = useState<string | null>(null);
// Click message to view its reasoning/tools

const [isLoading, setIsLoading] = useState(false);
// Show "thinking" state during API call

const [error, setError] = useState<string | null>(null);
// Display errors to user
```

All state local. No global state manager needed (keep it simple!).

### Backend
```typescript
// index.ts

const messageStore: ChatMessage[] = [];
// Simple array - not optimal but works for demo

// For production:
// - Use database
// - Add session/user management
// - Add rate limiting
```

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Cold Start | 1-2s | Gemini API latency |
| Tool Call | 1-2s | Depends on tool |
| Full Response | 2-5s | Typical: 1 tool call |
| Max Latency | ~15s | 5 iterations × 3s avg |
| Message Store | In-memory | Limited by RAM |
| Concurrent Users | Limited | Single-threaded JS |

## Scalability Considerations

### Current Limitations
- Single process (`npm run dev`)
- In-memory message store
- No database
- No rate limiting
- No authentication

### To Scale To Production
1. **Database**: Add PostgreSQL for message persistence
2. **Sessions**: User IDs, authentication
3. **Rate Limiting**: Prevent API spam
4. **Clustering**: Run multiple backend processes
5. **Caching**: Cache tool results
6. **Monitoring**: Add logging, error tracking

## Extension Points

Where to add features:

| Feature | Edit File | Notes |
|---------|-----------|-------|
| New tool | `tools.ts` | Add Tool object |
| New prompt | `prompts.ts` | Edit system prompt |
| Different model | `agent.ts` | Change model name |
| Tool validation | `tools.ts` | Add input validation |
| Response formatting | `index.ts` | Modify response shape |
| UI changes | `components/*.tsx` | React components |
| Database | Create new file | Add data layer |

## Design Philosophy

✅ **Do**: Keep it simple, explicit, understandable
❌ **Don't**: Add abstraction layers for abstraction's sake

Key decisions:
- No framework overhead (raw Express)
- No state management library (React hooks)
- No CSS-in-JS (inline styles)
- No ORMs (raw queries if DB added)
- Comments over clever code
- Modular files over monolithic ones

This makes it educational and easy to extend.
