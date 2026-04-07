# Setup Instructions

## Part 1: Backend Setup

### Step 1: Navigate to backend directory
```bash
cd backend
```

### Step 2: Install dependencies
```bash
npm install
```

This installs:
- `@google-ai/generativeai` - Gemini API client
- `express` - Web server
- `cors` - Enable frontend to call backend
- `dotenv` - Load environment variables
- `typescript` - Type safety
- `tsx` - Run TypeScript directly

### Step 3: Create .env file
```bash
cp .env.example .env
```

### Step 4: Configure Gemini API Key

Get your FREE API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Edit `backend/.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
PORT=3001
NODE_ENV=development
```

### Step 5: Start the backend server
```bash
npm run dev
```

You should see:
```
🚀 ReAct Agent Server running on http://localhost:3001
📡 API endpoints:
   POST   /api/chat        - Send message to agent
   GET    /api/history     - Get conversation history
   POST   /api/reset       - Clear history
   GET    /api/health      - Health check
```

The server is ready! Leave it running.

---

## Part 2: Frontend Setup (New Terminal)

### Step 1: Navigate to frontend directory
```bash
cd frontend
```

### Step 2: Install dependencies
```bash
npm install
```

This installs:
- `react` & `react-dom` - UI framework
- `vite` - Fast frontend build tool
- `typescript` - Type safety for React

### Step 3: Start the frontend dev server
```bash
npm run dev
```

You should see:
```
  VITE v4.5.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Vite should open the app in your browser automatically at http://localhost:5173

---

## Part 3: Using the App

### The Interface

You'll see 3 panels:

**Left (Chat)**: 
- Shows message history
- Click any assistant message to see its reasoning

**Center (Reasoning)**:
- Shows the Thought → Action → Observation chain
- Watch the agent think step-by-step

**Right (Tools)**:
- Shows all tools the agent executed
- Displays tool inputs and outputs

### Try These Examples

1. **Calculator**: "What is 50 + 25?"
   - Expects: Agent uses calculator tool

2. **Web Search**: "What's the capital of Japan?"
   - Expects: Agent uses web_search tool

3. **Multiple Steps**: "Calculate 100 / 5 and then multiply by 3"
   - Expects: Agent uses calculator twice in sequence

4. **File Operations**: "Read the readme.txt file"
   - Expects: Agent uses file_reader tool

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "GEMINI_API_KEY not configured" | Add valid key to `backend/.env` and restart backend |
| Backend won't start | Check if port 3001 is available: `lsof -i :3001` |
| Frontend can't reach backend | Make sure backend is running: http://localhost:3001/api/health |
| No response from agent | Check browser console (F12) for network errors |
| Slow responses | Normal - API calls take 2-5 seconds |

---

## Commands Quick Reference

**Backend**:
```bash
npm run dev           # Start server with auto-reload
npm run build         # Compile to dist/
npm run start         # Run compiled code
npm run type-check    # Check for TypeScript errors
```

**Frontend**:
```bash
npm run dev           # Start dev server
npm run build         # Build for production
npm run preview       # Preview production build
```

---

## What's Happening Behind the Scenes?

1. **You send a message** → Frontend calls `POST /api/chat`

2. **Backend receives it** → Passes to `runAgent()` function

3. **Agent thinks** → 
   - Calls Gemini with system prompt + question
   - Parses response for Thought/Action/Input

4. **Agent acts** →
   - If action detected: executes matching tool
   - Tool returns result

5. **Agent observes** →
   - Adds tool result to conversation
   - Loops back for next iteration (max 5)

6. **Agent responds** →
   - When no more actions: returns final response

7. **Frontend shows it** →
   - Chat message appears
   - Reasoning and tools panels populate

---

## Next Steps

Once it's working:

1. **Read the code**: Start with `backend/src/agent.ts` - that's the ReAct loop
2. **Add a tool**: Follow instructions in [`backend/src/tools.ts`](../backend/src/tools.ts)
3. **Modify the prompt**: Edit [`backend/src/prompts.ts`](../backend/src/prompts.ts)
4. **Try different models**: Change `gemini-pro` to `gemini-1.5-flash` in agent.ts
5. **Build something**: Use this as a foundation for your own agent

---

**You're ready to explore how ReAct agents work! 🚀**
