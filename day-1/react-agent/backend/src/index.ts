/**
 * Express server for the ReAct agent
 * Provides REST API endpoints for the frontend to interact with the agent
 */

import express, { Request, Response } from "express";
import cors from "cors";
import dotenv from "dotenv";
import { runAgent } from "./agent";
import { ChatMessage } from "./types";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;
const API_KEY = process.env.GEMINI_API_KEY;

// Middleware
app.use(cors());
app.use(express.json());

// Simple in-memory message store (not persistent)
const messageStore: ChatMessage[] = [];

/**
 * POST /api/chat
 * Main endpoint to send a message to the agent
 *
 * Request body: { message: string }
 * Response: { id: string, role: "assistant", content: string, agentData: {...} }
 */
app.post("/api/chat", async (req: Request, res: Response) => {
  try {
    const { message } = req.body;

    if (!message || typeof message !== "string") {
      return res.status(400).json({ error: "Message is required" });
    }

    if (!API_KEY) {
      return res.status(500).json({
        error: "GEMINI_API_KEY not configured. Please set it in .env file",
      });
    }

    // Convert stored messages to history format for agent
    const conversationHistory = messageStore.map((msg) => ({
      role: msg.role,
      content: msg.content,
    }));

    // Run the agent
    const agentResponse = await runAgent(message, API_KEY, conversationHistory);

    if (!agentResponse.success) {
      return res.status(500).json({
        error: agentResponse.error || "Agent error occurred",
      });
    }

    // Store the user message
    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}-user`,
      role: "user",
      content: message,
      timestamp: Date.now(),
    };
    messageStore.push(userMsg);

    // Store the assistant response
    const assistantMsg: ChatMessage = {
      id: `msg-${Date.now()}-assistant`,
      role: "assistant",
      content: agentResponse.finalResponse,
      timestamp: Date.now(),
      agentData: {
        steps: agentResponse.steps,
        toolCalls: agentResponse.toolCalls,
      },
    };
    messageStore.push(assistantMsg);

    // Return the response
    res.json({
      id: assistantMsg.id,
      role: "assistant",
      content: assistantMsg.content,
      agentData: assistantMsg.agentData,
    });
  } catch (error) {
    console.error("Error in /api/chat:", error);
    res.status(500).json({
      error: `Server error: ${(error as Error).message}`,
    });
  }
});

/**
 * GET /api/history
 * Returns the full conversation history
 */
app.get("/api/history", (req: Request, res: Response) => {
  res.json({
    messages: messageStore,
  });
});

/**
 * POST /api/reset
 * Clears the conversation history
 */
app.post("/api/reset", (req: Request, res: Response) => {
  messageStore.length = 0;
  res.json({ success: true, message: "History cleared" });
});

/**
 * GET /api/health
 * Health check endpoint
 */
app.get("/api/health", (req: Request, res: Response) => {
  res.json({
    status: "ok",
    apiKeyConfigured: !!API_KEY,
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`🚀 ReAct Agent Server running on http://localhost:${PORT}`);
  console.log(`📡 API endpoints:`);
  console.log(`   POST   /api/chat        - Send message to agent`);
  console.log(`   GET    /api/history     - Get conversation history`);
  console.log(`   POST   /api/reset       - Clear history`);
  console.log(`   GET    /api/health      - Health check`);

  if (!API_KEY) {
    console.warn("⚠️  GEMINI_API_KEY not set. Set it in .env file to use the agent.");
  }
});
