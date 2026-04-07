# Example Queries & Expected Output

Use this to test the ReAct agent and understand how it works.

## Category 1: Simple Calculations

### Query 1: Basic Math
```
User: What is 15 + 23?
```

**Expected Agent Behavior:**
- ✅ Recognizes a calculation task
- ✅ Calls calculator tool with "15 + 23"
- ✅ Receives "Result: 38"
- ✅ Responds: "The result of 15 + 23 is 38."

**Reasoning Panel:**
```
Step 1:
💭 Thought: The user is asking for a simple arithmetic calculation. I should use the calculator tool.

🎯 Action: calculator
Input: { "expression": "15 + 23" }

👁️ Observation: Result: 38
```

---

### Query 2: Complex Expression
```
User: Calculate (100 + 50) * 2
```

**Expected Behavior:**
- ✅ Recognizes complex expression
- ✅ Uses calculator with "(100 + 50) * 2"
- ✅ Returns "Result: 300"

---

### Query 3: Multiple Operations
```
User: First calculate 10 * 5, then add 25 to the result
```

**Expected Behavior:**
- ✅ First iteration: calculate "10 * 5" → "Result: 50"
- ✅ Second iteration: calculate "50 + 25" → "Result: 75"
- ✅ Final response: "Step 1: 10 × 5 = 50. Step 2: 50 + 25 = 75."

**Tools Panel:**
```
Tool Call #1:
🛠️ calculator
Input: { "expression": "10 * 5" }
Output: Result: 50

Tool Call #2:
🛠️ calculator
Input: { "expression": "50 + 25" }
Output: Result: 75
```

---

## Category 2: Information Queries

### Query 4: Weather Information
```
User: What is the weather today?
```

**Expected Behavior:**
- ✅ Recognizes information request
- ✅ Calls web_search tool
- ✅ Gets mock result: "It is currently sunny with temperature of 72°F"
- ✅ Responds with weather info

---

### Query 5: General Knowledge
```
User: What is the capital of France?
```

**Expected Behavior:**
- ✅ Calls web_search with "capital of France"
- ✅ Gets result: "Paris is the capital of France"
- ✅ Returns: "Paris is the capital of France."

---

### Query 6: Searching for Multiple Facts
```
User: Tell me about the population and capital of France
```

**Expected Behavior:**
- ✅ First web_search: "capital of France" → "Paris is the capital..."
- ✅ Second web_search: "population of France" → "...information..."
- ✅ Combines results in final response

---

## Category 3: File Operations

### Query 7: Read a File
```
User: Can you read the readme.txt file for me?
```

**Expected Behavior:**
- ✅ Calls file_reader with "readme.txt"
- ✅ Gets: "This is a sample README file.\nIt contains documentation."
- ✅ Returns file contents

---

### Query 8: Check Multiple Files
```
User: What format is the data.csv file in?
```

**Expected Behavior:**
- ✅ Calls file_reader with "data.csv"
- ✅ Gets CSV content
- ✅ Analyzes and responds: "The data.csv file is in CSV (comma-separated values) format with columns: name, age, city"

---

## Category 4: Hybrid Queries (Multiple Tools)

### Query 9: Calculate and Search
```
User: Calculate 50 + 30 and also tell me about AI
```

**Expected Behavior:**
- ✅ Tool 1: calculator("50 + 30") → "Result: 80"
- ✅ Tool 2: web_search("AI") → "AI and machine learning are rapidly advancing..."
- ✅ Combines both in response

**Multi-Step Logs:**
```
Tools Panel:
Tool Call #1: 🧮 calculator
  Input: { "expression": "50 + 30" }
  Output: Result: 80

Tool Call #2: 🔍 web_search
  Input: { "query": "AI" }
  Output: AI and machine learning...
```

---

### Query 10: Complex Task
```
User: What is 200 / 4, and then search for information about the weather?
```

**Expected Reasoning Chain:**
```
1. Calculate 200 / 4
2. Receive result: 50
3. Search weather information
4. Combine into response
```

---

## Category 5: Edge Cases & Error Handling

### Query 11: Invalid Calculation
```
User: Calculate "apple + orange"
```

**Expected Behavior:**
- ✅ Tries calculator with "apple + orange"
- ✅ Gets error: "Invalid expression - SyntaxError"
- ✅ Agent sees error as observation
- ✅ Responds: "I cannot calculate with text. 'apple' and 'orange' are words, not numbers."

---

### Query 12: File Not Found
```
User: Read the secrets.txt file
```

**Expected Behavior:**
- ✅ Calls file_reader with "secrets.txt"
- ✅ Gets: "Error: File 'secrets.txt' not found"
- ✅ Agent sees error
- ✅ Responds: "I couldn't find secrets.txt. Available files are: readme.txt, config.json, data.csv"

---

### Query 13: Ambiguous Query
```
User: Help me with something
```

**Expected Behavior:**
- ✅ Agent thinks about what help is needed
- ✅ Asks for clarification (no tool called)
- ✅ Responds: "I'd like to help, but could you be more specific? Tell me:\n- What calculation do you need?\n- What information are you looking for?\n- Which file would you like to read?"

---

## Category 6: Reasoning Chains

### Query 14: Multi-Step Reasoning
```
User: If I invest $1000 at 10% interest, how much will I have after 1 year?
```

**Expected Behavior:**
- ✅ Thought: "Need to calculate compound interest"
- ✅ Action: calculator with formula/calculation
- ✅ Observation: Result
- ✅ Response: Explanation with answer

---

### Query 15: Verification Task
```
User: Is 144 exactly 12 * 12?
```

**Expected Behavior:**
- ✅ Action: calculator("12 * 12")
- ✅ Observation: "Result: 144"
- ✅ Response: "Yes, 144 is exactly 12 × 12. Verified! ✓"

---

## Understanding the Panels

### When You See Tool Not Called

Some queries don't need tools:

```
User: "Hello! How are you?"
```

**Expected:**
- No tools called
- Agent responds directly
- Reasoning Panel: Only a Thought, no Action
- Tools Panel: Empty

```
Chat: "Hello! I'm working well, thank you for asking. What can I help you with?"
Reasoning:
  Step 1:
  💭 Thought: This is a simple greeting. No tools needed.
  (No Action or Observation)
```

---

### When You See Multiple Iterations

Some complex queries require multiple steps:

```
User: "Calculate the area of a circle with radius 5"
```

**Expected:**
- Iteration 1: Agent thinks about formula
- Iteration 2: calculator(3.14159 * 5 * 5)
- Iteration 3: Final response

Each iteration shows in Reasoning Panel as separate steps.

---

## Testing Checklist

Use this to verify everything works:

- [ ] **Calculator works**: Try "2+2", should get 4
- [ ] **Web search works**: Try "weather", should get mock weather
- [ ] **File reader works**: Try "read readme.txt", should show contents
- [ ] **Reasoning visible**: Click a message, see steps in middle panel
- [ ] **Tools visible**: Check right panel shows tool executions
- [ ] **Error handling**: Try invalid query, see graceful error
- [ ] **Multi-step**: Try complex query, see multiple iterations
- [ ] **Direct response**: Try simple greeting, see no tools called

---

## Debugging Tips

### Check Reasoning Panel
If agent didn't call a tool you expected:
- Look at "Thought" - agent may have decided tool wasn't needed
- Read Thought carefully to understand agent's logic

### Check Tools Panel
If response seems incomplete:
- Verify all tool calls succeeded
- Check tool outputs for errors
- Observe is a tool's observation empty?

### Check Browser Console (F12)
Network errors appear here:
- "Failed to fetch" = backend not running
- CORS errors = check backend CORS setup
- 500 errors = backend crash, check backend terminal

### Check Backend Terminal
Server logs show:
- API errors
- Tool execution details
- Gemini API errors

---

## Common Issues vs Solutions

| Issue | Example | Solution |
|-------|---------|----------|
| Tool not called | Calculate 2+2, no calculator called | Your prompt may not be clear. Rephrase: "What is 2+2?" |
| Wrong tool | Web search for math | Agent chose wrong tool. Rephrasing can help |
| Error in response | Tool says "Error: Invalid" | Check tool input format. Ensure it's valid for the tool |
| No response | Stuck loading | Backend may have crashed. Check backend terminal |
| Slow response | >10 seconds | API latency. Check internet connection |

---

## Advanced Testing

### Test Token Limits
Long query to see how agent handles large context:
```
User: [Send a very long question with multiple parts...]
```
→ See if agent handles it or asks to simplify

### Test Tool Combinations
Query using multiple tools:
```
User: Calculate 100+50 and search for weather and read readme.txt
```
→ Verify agent calls multiple tools in sequence

### Test Error Recovery
Query designed to fail first then succeed:
```
User: First try to read a file called "nonexistent.txt", then read "readme.txt"
```
→ See agent recover from error and retry

---

## Sample Conversation

Here's a full chat session you can replicate:

```
User: Hello!
Agent: [Direct response, no tools]

User: What is 42 * 2?
Agent: [Uses calculator, returns 84]

User: Now divide that by 7
Agent: [Uses calculator with "84 / 7", returns 12]

User: Great! What's the weather?
Agent: [Uses web_search, returns mock weather]

User: Can you read readme.txt?
Agent: [Uses file_reader, returns file contents]

User: That's helpful!
Agent: [Direct response, happy to help]
```

Each message will populate the Reasoning and Tools panels as the agent works.

---

**Happy Testing! Watch the agent think step-by-step! 🧠**
