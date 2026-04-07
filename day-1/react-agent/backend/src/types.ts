/**
 * Type definitions for the ReAct agent system
 */

export interface Tool {
  name: string;
  description: string;
  inputSchema: {
    type: string;
    properties: Record<string, unknown>;
    required: string[];
  };
  execute: (input: Record<string, unknown>) => Promise<string>;
}

export interface ReActStep {
  thought?: string;
  action?: {
    tool: string;
    input: Record<string, unknown>;
  };
  observation?: string;
}

export interface AgentResponse {
  success: boolean;
  steps: ReActStep[];
  finalResponse: string;
  toolCalls: {
    tool: string;
    input: Record<string, unknown>;
    result: string;
  }[];
  error?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  agentData?: {
    steps: ReActStep[];
    toolCalls: {
      tool: string;
      input: Record<string, unknown>;
      result: string;
    }[];
  };
}
