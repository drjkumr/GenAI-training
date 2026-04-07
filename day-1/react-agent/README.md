# 🤖 ReAct Agent GUI Application

A minimal, educational ReAct (Reasoning + Acting) agent demo built with Node.js, TypeScript, React, and Gemini API.

## 📋 Overview

This application demonstrates the **ReAct pattern** in action:
- **Reason**: LLM thinks about the problem
- **Act**: Agent chooses and executes tools
- **Observe**: Agent sees the results
- **Respond**: Agent provides the answer

Perfect for learning how modern LLM agents work.

## 🏗️ Architecture

```
react-agent/
├── backend/                    # Node.js + Express server
│   ├── src/
│   │   ├── index.ts           # Express server & API routes
│   │   ├── agent.ts           # ReAct loop implementation
│   │   ├── tools.ts           # Tool definitions (calculator, search, file reader)
│   │   ├── prompts.ts         # Prompt templates
│   │   └── types.ts           # TypeScript interfaces
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.example
│
├── frontend/                   # React + Vite GUI
│   ├── src/
│   │   ├── App.tsx            # Main app layout
│   │   ├── main.tsx           # Entry point
│   │   └── components/
│   │       ├── ChatWindow.tsx      # Chat history display
│   │       ├── ReasoningPanel.tsx  # Thought/Action/Observation display
│   │       └── ToolsPanel.tsx      # Tool execution log
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── README.md                   # This file
```

**Key Design Principles:**
- ✅ Minimal: ~13 files, no databases, no auth
- ✅ Clean: Strict TypeScript, modular structure
- ✅ Educational: Clear comments, easy to extend
- ✅ Fast: Can be set up and running in minutes

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Gemini API key (get free at [AI Studio](https://aistudio.google.com))

### 1. Clone / Setup Backend

```bash
cd backend
npm install
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
npm run dev
# Server runs on http://localhost:3001
```

### 2. Setup Frontend (in another terminal)

```bash
cd frontend
npm install
npm run dev
# App opens at http://localhost:5173
```

### 3. Start Chatting!

Click on "Send" to send a message. The agent will:
1. Think about your question
2. Choose a tool if needed
3. Execute the tool
4. Provide an answer

Watch the reasoning and tool panels to see how it works!

## 🧠 ReAct Pattern Explained

### The Flow

```
User Input
    ↓
[Agent Thinks] → "I need to calculate this"
    ↓
[Agent Acts] → Calls calculator tool
    ↓
[Agent Observes] → Gets result "2+2=4"
    ↓
[Agent Responds] → "The answer is 4"
```

### Example Conversation

**User:** "What is 15 * 8?"

**Agent Thought:** "The user wants a calculation. I should use the calculator tool."

**Agent Action:** Calls `calculator` with `expression: "15 * 8"`

**Observation:** "Result: 120"

**Final Response:** "The result of 15 * 8 is 120."

## 🛠️ Available Tools

### 1. **Calculator** 🧮
- Performs mathematical operations
- Input: mathematical expression (e.g., "2 + 2 * 5")
- Output: numeric result

### 2. **Web Search** 🔍
- Searches for information
- Input: search query
- Output: mock search results
- *Note: This is a mock for demo purposes*

### 3. **File Reader** 📄
- Reads text files
- Input: filename
- Output: file contents
- *Note: Mock implementation with predefined files*

## 📂 Key Files Explained

### Backend

#### `src/agent.ts` - ReAct Loop
This is where the magic happens. The core logic:

```typescript
// 1. Send prompt with tools to Gemini
// 2. Parse response for Thought/Action/Input
// 3. If Action: execute tool and get observation
// 4. Loop back with observation (max 5 iterations)
// 5. Return final response when no more actions needed
```

**Key function:** `executeReActStep()` - runs one iteration of the loop

#### `src/tools.ts` - Tool Definitions
Each tool has:
- `name`: Identifier used in prompts
- `description`: Tells the LLM what the tool does
- `inputSchema`: JSON schema for inputs
- `execute()`: Function that runs the tool

Example:
```typescript
export const calculatorTool: Tool = {
  name: "calculator",
  description: "Performs mathematical calculations",
  inputSchema: { /* JSON schema */ },
  execute: async (input) => { /* run calculation */ }
};
```

#### `src/prompts.ts` - Prompt Engineering
The system prompt teaches the LLM the ReAct pattern:

```
You are a helpful AI using the ReAct pattern.
1. Thought: Think about the problem
2. Action: Choose a tool
3. Observation: Receive the result
4. Response: Provide the answer
```

#### `src/index.ts` - Express Server
REST API endpoints:
- `POST /api/chat` - Send message to agent
- `GET /api/history` - Get conversation history
- `POST /api/reset` - Clear history
- `GET /api/health` - Health check

### Frontend

#### `src/App.tsx` - Main Layout
Three-panel layout:
1. **Left (30%)**: Chat history
2. **Center (35%)**: Reasoning steps
3. **Right (35%)**: Tool executions

All components use local state with React hooks.

#### `src/components/` - Reusable Components
- **ChatWindow**: Displays all messages, click to view details
- **ReasoningPanel**: Shows Thought/Action/Observation for selected message
- **ToolsPanel**: Shows all tool calls and their inputs/outputs

## 🔧 How to Extend

### Add a New Tool

1. **Define the tool in `backend/src/tools.ts`:**

```typescript
export const myNewTool: Tool = {
  name: "my_tool",
  description: "Does something useful",
  inputSchema: {
    type: "object",
    properties: {
      param1: { type: "string", description: "..." },
    },
    required: ["param1"],
  },
  execute: async (input) => {
    // Your logic here
    return "Result: ...";
  },
};
```

2. **Add to tools array:**

```typescript
export const tools: Tool[] = [
  calculatorTool,
  webSearchTool,
  fileReaderTool,
  myNewTool, // ← Add here
];
```

3. **That's it!** The agent will automatically:
   - See the tool in the system prompt
   - Learn how to use it from the description
   - Call it when appropriate

### Modify the Prompt

Edit the system prompt in `backend/src/prompts.ts` in the `generateSystemPrompt()` function.

Example: Add instructions to be more concise:
```typescript
Remember:
- Be concise and direct
- Use tools only when necessary
- ...
```

### Change the Model

In `backend/src/agent.ts`:

```typescript
// Change this line:
const model = client.getGenerativeModel({ model: "gemini-pro" });

// To use Gemini 1.5 Flash (faster, cheaper):
const model = client.getGenerativeModel({ model: "gemini-1.5-flash" });

// Or Gemini 1.5 Pro (more capable):
const model = client.getGenerativeModel({ model: "gemini-1.5-pro" });
```

## 📊 Example Run

### Conversation

**User:** "Calculate 25 + 75 and tell me about the weather"

**Agent Response:**

The agent will:
1. **Think**: "User wants two things: a calculation and weather info"
2. **Act**: Call calculator with "25 + 75"
3. **Observe**: Get "Result: 100"
4. **Act**: Call web_search with "weather today"
5. **Observe**: Get mock weather results
6. **Respond**: "The sum of 25 + 75 is 100. Current weather is sunny with 72°F."

You'll see in the UI:
- Calendar shows messages in chat window
- Reasoning panel shows all steps and thoughts
- Tools panel shows both tool executions

## 🎓 Learning Resources

Inside the code:

1. **ReAct Pattern**: See `agent.ts` - the core loop
2. **Prompt Engineering**: See `prompts.ts` - how to guide the LLM
3. **Tool Calling**: See `tools.ts` - structured tool definitions
4. **React Patterns**: See `frontend/src/` - hooks, state management

## 🧪 Testing

### Test Calculator Tool
Send: "What is 2 to the power of 10?"

Expected: Agent recognizes this needs calculation and calls calculator with "2 ** 10"

### Test Web Search
Send: "What is the capital of France?"

Expected: Agent calls web_search tool

### Test Reasoning
Look at the **Reasoning Panel** while agent processes - you'll see:
- Agent's thought process
- Tools it decides to use
- Results from each tool

## ⚙️ Configuration

### Environment Variables (.env)

```bash
GEMINI_API_KEY=your_api_key_here   # Required
PORT=3001                           # Optional, default 3001
NODE_ENV=development               # Optional
```

### API Response Format

All agent responses include:

```json
{
  "id": "msg-timestamp-id",
  "role": "assistant",
  "content": "The final response text",
  "agentData": {
    "steps": [
      {
        "thought": "...",
        "action": { "tool": "...", "input": {...} },
        "observation": "Tool result"
      }
    ],
    "toolCalls": [...]
  }
}
```

## 🐛 Troubleshooting

### Backend won't start
- Check: Is port 3001 available?
- Check: Is `GEMINI_API_KEY` set in `.env`?
- Try: `npm run type-check` to find TypeScript errors

### Frontend can't reach backend
- Check: Is backend running on http://localhost:3001?
- Check: CORS is enabled in `backend/src/index.ts`
- Try: Open browser console (F12) to see network errors

### Agent not responding
- Check: Is `GEMINI_API_KEY` valid?
- Check: Do you have quota remaining on Gemini API?
- Try: Restart both dev servers

### Tool not being called
- Check: Tool name matches exactly (case-sensitive)
- Check: Tool description in systemPrompt is clear
- Try: Ask simpler questions to test

## 📝 Code Quality

- ✅ Strict TypeScript (`strict: true`)
- ✅ No `any` types
- ✅ Clear comments on functions
- ✅ Modular file structure
- ✅ Error handling throughout
- ✅ Async/await for concurrency

## 🚀 Next Steps / Ideas

1. **Persist messages**: Add SQLite for storage
2. **Real tools**: Implement actual web search or file operations
3. **Advanced tools**: Add code execution, image analysis, etc.
4. **Better UI**: Add syntax highlighting, streaming responses
5. **Multi-agent**: Let agents collaborate
6. **Tool validation**: Add stricter input validation

## 📄 License

MIT - Feel free to use and modify!

## 🤝 Contributing

Found a bug or want to improve? Feel free to extend this!

Key files to know:
- Agent logic: `backend/src/agent.ts`
- Tools: `backend/src/tools.ts`
- UI: `frontend/src/App.tsx` and components

---

**Happy learning! 🎓**

Questions? The code has comments throughout. Read the source!
