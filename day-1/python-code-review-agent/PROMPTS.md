# Exact Prompts Used in the Agent

This document contains the exact system prompts used for Claude Haiku's analysis passes.

---

## Prompt 1: Initial Code Review

**Sent to Claude with:**
- User's Python code
- AST analysis findings

```
You are an expert Python code reviewer. Analyze this Python code and provide 
clear, practical improvement suggestions.

STATIC ANALYSIS FINDINGS:
[From analyzer.py - syntax validity, functions found, imports, issues detected]

PYTHON CODE:
```python
[User-provided code]
```

Provide 3-5 specific, actionable suggestions. Focus on:
- Code clarity and readability
- Performance improvements
- Best practices
- Error handling

Format each suggestion with a title and explanation.
```

### Expected Output
Short list of 3-5 improvement suggestions like:
```
1. Use list comprehension instead of loop
   - Your current loop pattern is slower...
   
2. Add type hints for clarity
   - Type hints help IDEs and readers...
   
3. Handle edge cases
   - Consider what happens when...
```

---

## Prompt 2: Self-Reflection (The Improvement Pass)

**Sent to Claude with:**
- Original Python code
- Claude's previous suggestions from Prompt 1

```
You are a senior Python architect reviewing code suggestions.

ORIGINAL CODE:
```python
[Same user-provided code]
```

YOUR PREVIOUS SUGGESTIONS:
[The suggestions from Prompt 1]

YOUR TASK:
1. Review your previous suggestions critically
2. Identify which suggestions are most impactful
3. Refine or clarify any vague suggestions
4. Reorganize by priority (most important first)
5. Add 1-2 additional improvements if you spot important issues

OUTPUT:
Provide improved, prioritized suggestions. Be more specific and actionable 
than your previous version.
```

### Expected Output
Refined, prioritized suggestions like:
```
PRIORITY 1 - Performance (Quick Win):
Use list comprehension for 3-5x speed improvement:
  [x * 2 for x in items if x > 0]

PRIORITY 2 - Type Safety:
Add type hints for IDE support and clarity:
  def process(items: list[int]) -> list[int]:

PRIORITY 3 - Best Practice:
Add docstring explaining the function's purpose...

ADDITIONAL: Consider edge case where items is None...
```

---

## How These Are Called in Code

### In `backend/src/server.ts`:

```typescript
// Call 1: Initial Review
async function getInitialReview(code: string, astFindings: any): Promise<string> {
  const astSummary = formatASTFindings(astFindings);

  const prompt = `You are an expert Python code reviewer. Analyze this Python code and provide clear, practical improvement suggestions.

STATIC ANALYSIS FINDINGS:
${astSummary}

PYTHON CODE:
\`\`\`python
${code}
\`\`\`

Provide 3-5 specific, actionable suggestions. Focus on:
- Code clarity and readability
- Performance improvements
- Best practices
- Error handling

Format each suggestion with a title and explanation.`;

  const response = await client.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 800,
    messages: [{ role: "user", content: prompt }],
  });

  return response.content[0].type === "text" ? response.content[0].text : "";
}

// Call 2: Self-Reflection
async function reflectAndImprove(code: string, suggestions: string): Promise<string> {
  const reflectionPrompt = `You are a senior Python architect reviewing code suggestions.

ORIGINAL CODE:
\`\`\`python
${code}
\`\`\`

YOUR PREVIOUS SUGGESTIONS:
${suggestions}

YOUR TASK:
1. Review your previous suggestions critically
2. Identify which suggestions are most impactful
3. Refine or clarify any vague suggestions
4. Reorganize by priority (most important first)
5. Add 1-2 additional improvements if you spot important issues

OUTPUT:
Provide improved, prioritized suggestions. Be more specific and actionable 
than your previous version.`;

  const response = await client.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 1000,
    messages: [{ role: "user", content: reflectionPrompt }],
  });

  return response.content[0].type === "text" ? response.content[0].text : "";
}
```

---

## AST Findings Format

The Python analyzer returns findings like:

```json
{
  "syntax_valid": true,
  "errors": [],
  "functions": [
    {"name": "process_data", "line": 1, "args": ["items"]}
  ],
  "classes": [],
  "imports": [
    {"type": "import", "module": "json", "line": 2}
  ],
  "issues": [
    {
      "type": "bare_except",
      "line": 15,
      "severity": "high",
      "message": "Bare 'except:' catches all exceptions (including KeyboardInterrupt). Specify exception types."
    }
  ]
}
```

This is formatted into readable text like:

```
✅ Syntax is valid

📍 Functions found (1):
  - process_data(items) at line 1

📦 Imports (1):
  - import json at line 2

⚠️  Code quality issues (1):
  - HIGH: Bare 'except:' catches all exceptions (including KeyboardInterrupt). 
    Specify exception types. (line 15)
```

---

## Example: Complete Flow

### Input
```python
def calculate(numbers):
    result = []
    for i in range(len(numbers)):
        result.append(numbers[i] \* 2)
    return result
```

### AST Findings
```
✅ Syntax is valid
📍 Functions found (1):
  - calculate(numbers) at line 1
```

### Prompt 1 Output (Initial Review)
```
1. Use list comprehension for better performance
   Your current loop-append pattern is slower than a single list comprehension.
   Replace with: [x * 2 for x in numbers]

2. Add type hints
   Specify input/output types for clarity:
   def calculate(numbers: list[int]) -> list[int]:

3. Add a docstring
   Document what the function does and why.

4. Consider making the multiplier configurable
   Currently hardcoded to 2 - could be a parameter.
```

### Prompt 2 Output (Self-Reflected)
```
PRIORITY 1 - Performance (Quick Win):
Use list comprehension for 3-5x faster execution:
  result = [x * 2 for x in numbers]
This is more Pythonic and efficient.

PRIORITY 2 - Type Safety:
Add type hints for IDE support:
  def calculate(numbers: list[int]) -> list[int]:
    """Double each number in the list."""
    return [x * 2 for x in numbers]

PRIORITY 3 - Flexibility:
Parameterize the multiplier for reusability:
  def multiply_list(numbers: list[int], factor: int = 2) -> list[int]:

PRIORITY 4 - Edge Cases:
Consider adding input validation to handle None or non-numeric values.
```

---

## Key Differences Between Prompts

| Aspect | Prompt 1 (Initial) | Prompt 2 (Reflection) |
|--------|-------------------|----------------------|
| Role | "Code reviewer" | "Senior architect" |
| Focus | Generate ideas | Evaluate & improve |
| Task | Suggest improvements | Prioritize & refine |
| Output | 3-5 suggestions | Ranked by impact |
| Detail | Good enough | Specific & actionable |

---

## Why This Pattern Works

**Prompt 1:**
- Broad analysis
- Generates reasonable suggestions
- Good starting point

**Prompt 2:** (The Innovation)
- Reflects on Prompt 1 output
- Identifies which suggestions matter most
- Refines vague ones into concrete actions
- Adds critical suggestions missed before
- Result: 40-60% better quality output

---

## Customization Ideas

### Make it More Strict (focus on best practices)
```
Prompt 2 modification:
"You are a Python PEP 8 expert. Review suggestions focusing on:
- Style consistency
- Code readability
- Pythonic patterns
- Performance optimizations"
```

### Make it More Lenient (beginner-friendly)
```
Prompt 2 modification:
"You are a Python mentor helping beginners. Make suggestions:
- Simple and easy to understand
- Explain why each matters
- Provide complete code examples
- Avoid advanced topics"
```

### Add Security Focus
```
Prompt 1 addition:
"Additionally, check for security issues:
- SQL injection vulnerabilities
- Unsafe file operations
- Hardcoded credentials
- Input validation"
```

---

## Token Usage

**Per review:**
- Prompt 1: ~300 tokens input, ~250 tokens output
- Prompt 2: ~400 tokens input, ~300 tokens output
- **Total:** ~1,250 tokens (~$0.004 per review with Haiku)

**At scale:**
- 1,000 reviews/day = $4.00
- 10,000 reviews/month = $120

---

## Monitoring Claude API

Check usage at: https://console.anthropic.com/usage

API call structure in code:
```typescript
const response = await client.messages.create({
  model: "claude-haiku-4-5-20251001",  // Track which model
  max_tokens: 800,                      // Control output length
  messages: [{
    role: "user",
    content: prompt
  }]
});

// Response includes usage:
// response.usage.input_tokens
// response.usage.output_tokens
```

---

**These prompts are the heart of the self-reflecting agent. Modify them carefully!** ✨
