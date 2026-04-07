import express from 'express';
import cors from 'cors';
import Anthropic from '@anthropic-ai/sdk';
import * as dotenv from 'dotenv';

// Load environment variables from .env
dotenv.config();

const app = express();
const port = process.env.PORT || 3001;
const apiKey = process.env.ANTHROPIC_API_KEY;

// Initialize Anthropic client with exact model
const client = new Anthropic({
  apiKey: apiKey,
});

// Middleware
app.use(cors());
app.use(express.json());

// Type definition for request body
interface SolveRequest {
  problem: string;
}

// Main API route: POST /solve
app.post('/solve', async (req: express.Request, res: express.Response) => {
  try {
    // Extract the math problem from request
    const { problem } = req.body as SolveRequest;

    // Validate input
    if (!problem || typeof problem !== 'string' || problem.trim().length === 0) {
      res.status(400).json({ error: 'Problem field is required and must be a non-empty string' });
      return;
    }

    // System prompt designed for chain-of-thought reasoning
    const systemPrompt = `You are an expert math tutor. When solving math problems, ALWAYS:
1. Break down the problem into clear steps
2. Explain your reasoning for each step
3. Show all calculations
4. Provide the final answer clearly

Format your response as numbered steps followed by the final answer.`;

    // Call Claude Haiku 4.5 with the exact model name
    const message = await client.messages.create({
      model: 'claude-haiku-4-5-20251001', // EXACT MODEL NAME
      max_tokens: 1024,
      system: systemPrompt,
      messages: [
        {
          role: 'user',
          content: `Solve this math problem step-by-step: ${problem}`,
        },
      ],
    });

    // Extract text response from the model
    const solution =
      message.content[0].type === 'text'
        ? message.content[0].text
        : 'Unable to generate solution';

    // Return the problem and solution
    res.json({
      problem: problem,
      solution: solution,
      model: 'claude-haiku-4-5-20251001',
      usage: {
        input_tokens: message.usage.input_tokens,
        output_tokens: message.usage.output_tokens,
      },
    });
  } catch (error) {
    // Simple error handling
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    console.error('Error:', errorMessage);

    // Check for API key issues
    if (errorMessage.includes('401') || errorMessage.includes('Unauthorized')) {
      res.status(401).json({ error: 'Invalid API key. Check your ANTHROPIC_API_KEY.' });
    } else if (errorMessage.includes('error')) {
      res.status(500).json({ error: errorMessage });
    } else {
      res.status(500).json({ error: 'Failed to solve the problem. Please try again.' });
    }
  }
});

// Health check route
app.get('/health', (req: express.Request, res: express.Response) => {
  res.json({ status: 'ok', model: 'claude-haiku-4-5-20251001' });
});

// Start server
app.listen(port, () => {
  console.log(`✓ Math Solver Backend running on http://localhost:${port}`);
  console.log(`✓ Model: claude-haiku-4-5-20251001`);
  console.log(`✓ API Key configured: ${apiKey ? 'Yes' : 'No'}`);
  console.log(`\nEndpoints:`);
  console.log(`  POST http://localhost:${port}/solve`);
  console.log(`  GET  http://localhost:${port}/health`);
});
