/**
 * Core ReAct agent implementation
 * Handles the Thought → Action → Observation → Response loop
 */

import { GoogleGenerativeAI } from "@google/generative-ai";
import { ReActStep, AgentResponse } from "./types";
import { getTool } from "./tools";
import { generateSystemPrompt, formatConversationHistory, createPrompt } from "./prompts";
import { tools } from "./tools";

interface Message {
  role: string;
  content: string;
}

/**
 * Parse the agent's response to extract Thought, Action, Input, and Observation
 */
function parseReActResponse(response: string): {
  thought?: string;
  action?: string;
  input?: Record<string, unknown>;
  raw: string;
} {
  const lines = response.split("\n");
  const result: {
    thought?: string;
    action?: string;
    input?: Record<string, unknown>;
    raw: string;
  } = { raw: response };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Extract Thought
    if (line.startsWith("Thought:") || line.startsWith("**Thought**:")) {
      result.thought = line.replace(/^\*?\*?Thought\*?\*?:/, "").trim();
    }

    // Extract Action and Input
    if (line.startsWith("Action:") || line.startsWith("**Action**:")) {
      result.action = line.replace(/^\*?\*?Action\*?\*?:/, "").trim();
      // Look for Input on next line(s)
      for (let j = i + 1; j < lines.length; j++) {
        const nextLine = lines[j].trim();
        if (nextLine.startsWith("Input:") || nextLine.startsWith("**Input**:")) {
          const inputStr = nextLine.replace(/^\*?\*?Input\*?\*?:/, "").trim();
          try {
            result.input = JSON.parse(inputStr);
            break;
          } catch {
            // If JSON parsing fails, continue
          }
        }
      }
    }
  }

  return result;
}

/**
 * Execute a single step of the ReAct loop
 */
async function executeReActStep(
  client: GoogleGenerativeAI,
  systemPrompt: string,
  conversationHistory: Message[],
  userMessage: string,
  maxIterations: number = 5
): Promise<AgentResponse> {
  const steps: ReActStep[] = [];
  const toolCalls: AgentResponse["toolCalls"] = [];
  const history: Message[] = [...conversationHistory];

  let currentResponse = "";
  let iteration = 0;

  // Main loop: keep running until we get a final response or hit max iterations
  while (iteration < maxIterations) {
    iteration++;

    // Build the prompt including conversation history and ReAct system prompt
    const conversationStr = formatConversationHistory(
      history.length > 0 ? history : [{ role: "user", content: "Start here." }]
    );
    const prompt = createPrompt(systemPrompt, conversationStr, userMessage);

    // Call Gemini API
    const model = client.getGenerativeModel({ model: "models/gemini-1.5-flash" });
    const result = await model.generateContent(prompt);
    const text = result.response.text();

    currentResponse = text;

    // Parse the response for Thought/Action/Input
    const parsed = parseReActResponse(text);

    const step: ReActStep = {};
    if (parsed.thought) {
      step.thought = parsed.thought;
    }

    // Check if an action was taken
    if (parsed.action && parsed.input) {
      step.action = {
        tool: parsed.action,
        input: parsed.input,
      };

      // Execute the tool
      const tool = getTool(parsed.action);
      if (tool) {
        try {
          const toolResult = await tool.execute(parsed.input);
          step.observation = toolResult;

          toolCalls.push({
            tool: parsed.action,
            input: parsed.input,
            result: toolResult,
          });

          // Add the interaction to history for next iteration
          history.push({ role: "assistant", content: text });
          history.push({ role: "user", content: `Tool result: ${toolResult}` });
        } catch (error) {
          const errorMsg = `Error executing tool: ${(error as Error).message}`;
          step.observation = errorMsg;
          toolCalls.push({
            tool: parsed.action,
            input: parsed.input,
            result: errorMsg,
          });
          history.push({ role: "assistant", content: text });
          history.push({ role: "user", content: errorMsg });
        }
      } else {
        const errorMsg = `Tool "${parsed.action}" not found`;
        step.observation = errorMsg;
        history.push({ role: "assistant", content: text });
        history.push({ role: "user", content: errorMsg });
      }
    } else {
      // No action in this response - this is our final response
      break;
    }

    steps.push(step);

    // Safety check: if we have observations from multiple tool calls, stop
    if (toolCalls.length >= 3) {
      break;
    }
  }

  return {
    success: true,
    steps,
    finalResponse: currentResponse,
    toolCalls,
  };
}

/**
 * Main agent function: processes user input and returns agent response
 */
export async function runAgent(
  userMessage: string,
  apiKey: string,
  conversationHistory: Message[] = []
): Promise<AgentResponse> {
  try {
    const client = new GoogleGenerativeAI(apiKey);
    const systemPrompt = generateSystemPrompt(tools);

    // Run the ReAct loop
    const response = await executeReActStep(
      client,
      systemPrompt,
      conversationHistory,
      userMessage
    );

    return response;
  } catch (error) {
    return {
      success: false,
      steps: [],
      finalResponse: "",
      toolCalls: [],
      error: `Agent error: ${(error as Error).message}`,
    };
  }
}
