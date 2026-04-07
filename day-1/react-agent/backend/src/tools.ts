/**
 * Tool definitions for the ReAct agent
 * Each tool has a name, description, input schema, and execute function
 */

import { Tool } from "./types";

// Calculator tool: performs mathematical operations
export const calculatorTool: Tool = {
  name: "calculator",
  description:
    "Performs mathematical calculations. Supports +, -, *, /, and basic functions.",
  inputSchema: {
    type: "object",
    properties: {
      expression: {
        type: "string",
        description: "A mathematical expression (e.g., '2 + 2', '10 * 5')",
      },
    },
    required: ["expression"],
  },
  execute: async (input: Record<string, unknown>): Promise<string> => {
    const expression = input.expression as string;
    try {
      // Simple validation: only allow numbers, operators, and parentheses
      if (!/^[0-9+\-*/(). ]*$/.test(expression)) {
        return "Error: Invalid characters in expression";
      }
      // eslint-disable-next-line no-eval
      const result = eval(expression);
      if (typeof result !== "number") {
        return "Error: Expression did not return a number";
      }
      return `Result: ${result}`;
    } catch (e) {
      return `Error: Invalid expression - ${(e as Error).message}`;
    }
  },
};

// Web search tool: simulates web search (mock implementation)
export const webSearchTool: Tool = {
  name: "web_search",
  description:
    "Searches the web for information. Returns mock results for demonstration.",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "The search query",
      },
    },
    required: ["query"],
  },
  execute: async (input: Record<string, unknown>): Promise<string> => {
    const query = input.query as string;
    // Mock search results based on query topics
    const mockResults: Record<string, string> = {
      weather: "It is currently sunny with temperature of 72°F (22°C)",
      capital: "Paris is the capital of France",
      population: "The world population is approximately 8 billion people",
      technology: "AI and machine learning are rapidly advancing technologies",
      history: "History is the study of past events and civilizations",
    };

    const key = Object.keys(mockResults).find((k) =>
      query.toLowerCase().includes(k)
    );
    if (key) {
      return mockResults[key];
    }
    return `Search results for "${query}": No specific results found in demo. Try 'weather', 'capital', 'population', 'technology', or 'history'.`;
  },
};

// File reader tool: reads file contents (mock implementation)
export const fileReaderTool: Tool = {
  name: "file_reader",
  description: "Reads the contents of a text file. Returns mock file data.",
  inputSchema: {
    type: "object",
    properties: {
      filename: {
        type: "string",
        description: "The name or path of the file to read",
      },
    },
    required: ["filename"],
  },
  execute: async (input: Record<string, unknown>): Promise<string> => {
    const filename = input.filename as string;
    // Mock file responses
    const mockFiles: Record<string, string> = {
      "readme.txt": "This is a sample README file.\nIt contains documentation.",
      "config.json": '{"app": "ReAct Agent", "version": "1.0.0"}',
      "data.csv": "name,age,city\nAlice,30,NYC\nBob,25,LA",
    };

    const content = mockFiles[filename.toLowerCase()];
    if (content) {
      return `File contents of ${filename}:\n${content}`;
    }
    return `Error: File "${filename}" not found. Available mock files: ${Object.keys(mockFiles).join(", ")}`;
  },
};

/**
 * Registry of all available tools
 * The agent can select from these tools when deciding what action to take
 */
export const tools: Tool[] = [calculatorTool, webSearchTool, fileReaderTool];

/**
 * Get a tool by name
 */
export function getTool(name: string): Tool | undefined {
  return tools.find((t) => t.name === name);
}
