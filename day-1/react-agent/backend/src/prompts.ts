/**
 * Prompt templates for the ReAct agent
 * These guide the LLM to think step-by-step and decide which tools to use
 */

import { Tool } from "./types";

/**
 * Generate the system prompt that teaches the agent the ReAct pattern
 * Format: Thought → Action → Observation → Response
 */
export function generateSystemPrompt(tools: Tool[]): string {
  const toolDescriptions = tools
    .map((tool) => {
      const params = Object.entries(tool.inputSchema.properties)
        .map(([key, value]) => {
          const val = value as Record<string, unknown>;
          return `  - ${key} (${val.type}): ${val.description}`;
        })
        .join("\n");
      return `- ${tool.name}: ${tool.description}\n  Parameters:\n${params}`;
    })
    .join("\n");

  return `You are a helpful AI assistant using the ReAct (Reasoning + Acting) pattern.

Your decision-making process MUST follow this structure:
1. **Thought**: Think about what the user is asking and what you need to do
2. **Action**: Choose a tool to help answer the question (or skip if not needed)
3. **Observation**: Receive the tool's result
4. **Response**: Provide the final answer to the user

Always be concise and clear. When you use a tool, format it EXACTLY like this:
Action: [tool_name]
Input: {"param1": "value1", "param2": "value2"}

Available tools:
${toolDescriptions}

Remember:
- You can use multiple tools in sequence if needed
- Always provide clear thinking before taking action
- End your response with a clear answer to the user's question
- If an action fails, try an alternative approach`;
}

/**
 * Format the conversation history for the LLM
 */
export function formatConversationHistory(
  messages: { role: string; content: string }[]
): string {
  return messages
    .map((msg) => {
      const role = msg.role === "user" ? "User" : "Assistant";
      return `${role}: ${msg.content}`;
    })
    .join("\n\n");
}

/**
 * Create the complete prompt for a conversation turn
 */
export function createPrompt(
  systemPrompt: string,
  conversationHistory: string,
  userMessage: string
): string {
  return `${systemPrompt}

---

${conversationHistory}

User: ${userMessage}`;
}
