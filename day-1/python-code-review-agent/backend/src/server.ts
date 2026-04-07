import express, { Request, Response } from "express";
import cors from "cors";
import dotenv from "dotenv";
import { spawn } from "child_process";
import { Anthropic } from "@anthropic-ai/sdk";
import path from "path";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Initialize Anthropic client with API key from environment
const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

app.use(cors());
app.use(express.json());

// Serve frontend
app.use(express.static(path.join(__dirname, "../..")));

// Health check
app.get("/health", (req: Request, res: Response) => {
  res.json({ status: "ok" });
});

// Main review endpoint
app.post("/review", async (req: Request, res: Response) => {
  try {
    const { code } = req.body as { code: string };

    if (!code || code.trim().length === 0) {
      res.status(400).json({ error: "Code input is required" });
      return;
    }

    // Step 1: Run Python AST analyzer
    console.log("📝 Step 1: Analyzing code with AST...");
    const astFindings = await runPythonAnalyzer(code);
    console.log("✓ AST findings:", astFindings);

    // Step 2: Initial AI review pass
    console.log("🤖 Step 2: Initial Claude review...");
    const initialSuggestions = await getInitialReview(code, astFindings);
    console.log("✓ Initial suggestions generated");

    // Step 3: Self-reflection pass - AI improves its own suggestions
    console.log("🔄 Step 3: Self-reflection - Claude improving suggestions...");
    const improvedSuggestions = await reflectAndImprove(code, initialSuggestions);
    console.log("✓ Suggestions improved through reflection");

    res.json({
      astFindings,
      initialSuggestions,
      improvedSuggestions,
      finalOutput: improvedSuggestions,
    });
  } catch (error) {
    console.error("Review error:", error);
    res.status(500).json({ error: "Failed to review code" });
  }
});

/**
 * Run Python AST analyzer as subprocess and capture JSON output
 */
async function runPythonAnalyzer(code: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const python = spawn("python", ["analyzer.py", code], {
      cwd: __dirname,
    });

    let output = "";
    let errorOutput = "";

    python.stdout.on("data", (data) => {
      output += data.toString();
    });

    python.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    python.on("close", (code) => {
      if (code !== 0) {
        console.error("Python analyzer error:", errorOutput);
        return reject(new Error(`Python analyzer failed: ${errorOutput}`));
      }

      try {
        const findings = JSON.parse(output.trim());
        resolve(findings);
      } catch (e) {
        reject(new Error(`Failed to parse analyzer output: ${output}`));
      }
    });
  });
}

/**
 * First pass: Claude analyzes code and AST findings, generates suggestions
 */
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
    messages: [
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  return response.content[0].type === "text" ? response.content[0].text : "";
}

/**
 * Second pass: Claude reviews its own suggestions and improves them
 * This is the self-reflection loop
 */
async function reflectAndImprove(code: string, suggestions: string): Promise<string> {
  const reflectionPrompt = `You are a senior Python architect reviewing code suggestions.

ORIGINAL CODE:
\`\`\`python
${code}
\`\`\`

YOUR PREVIOUS SUGGESTIONS:
${suggestions}

TASK:
1. Review your previous suggestions critically
2. Identify the most impactful improvements
3. Refine any vague or unclear suggestions
4. Reorganize by priority (most important first)
5. Add 1-2 additional improvements if you spot important issues

OUTPUT:
Provide improved, prioritized suggestions. Be more specific and actionable than before.`;

  const response = await client.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: reflectionPrompt,
      },
    ],
  });

  return response.content[0].type === "text" ? response.content[0].text : "";
}

/**
 * Format AST findings into readable text for the prompt
 */
function formatASTFindings(findings: any): string {
  let summary = "";

  if (!findings.syntax_valid) {
    summary += "❌ SYNTAX ERROR:\n";
    findings.errors.forEach((err: any) => {
      summary += `  - Line ${err.line}: ${err.message}\n`;
    });
  } else {
    summary += "✅ Syntax is valid\n";
  }

  if (findings.functions.length > 0) {
    summary += `\n📍 Functions found (${findings.functions.length}):\n`;
    findings.functions.forEach((fn: any) => {
      summary += `  - ${fn.name}(${fn.args.join(", ")}) at line ${fn.lineno}\n`;
    });
  }

  if (findings.imports.length > 0) {
    summary += `\n📦 Imports (${findings.imports.length}):\n`;
    findings.imports.forEach((imp: any) => {
      summary += `  - ${imp.type} ${imp.module} at line ${imp.line}\n`;
    });
  }

  if (findings.issues.length > 0) {
    summary += `\n⚠️  Code quality issues (${findings.issues.length}):\n`;
    findings.issues.forEach((issue: any) => {
      summary += `  - ${issue.severity.toUpperCase()}: ${issue.message} (line ${issue.line})\n`;
    });
  }

  return summary;
}

app.listen(PORT, () => {
  console.log(`\n✅ Python Code Review Agent running on http://localhost:${PORT}`);
  console.log(`   POST /review - Submit Python code for review\n`);
});
