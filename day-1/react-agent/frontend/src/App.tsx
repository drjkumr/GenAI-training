/**
 * Main App component - orchestrates the GUI layout and manages state
 */

import React, { useState, useCallback } from "react";
import { ChatWindow, Message } from "./components/ChatWindow";
import { ReasoningPanel } from "./components/ReasoningPanel";
import { ToolsPanel } from "./components/ToolsPanel";

const API_URL = "http://localhost:3001";

interface SelectedMessageData {
  steps: Array<{
    thought?: string;
    action?: { tool: string; input: Record<string, unknown> };
    observation?: string;
  }>;
  toolCalls: Array<{ tool: string; input: Record<string, unknown>; result: string }>;
}

export const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedMessageId, setSelectedMessageId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Get selected message data
  const selectedMessage = messages.find((m) => m.id === selectedMessageId);
  const selectedData: SelectedMessageData = selectedMessage?.agentData || {
    steps: [],
    toolCalls: [],
  };

  /**
   * Handle sending a message to the agent
   */
  const handleSendMessage = useCallback(async () => {
    if (!inputValue.trim()) return;

    setError(null);
    setIsLoading(true);

    const userMessage: Message = {
      id: `msg-${Date.now()}-user`,
      role: "user",
      content: inputValue,
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Failed to get response from agent");
      }

      const agentResponse = await response.json();

      const assistantMessage: Message = {
        id: agentResponse.id,
        role: "assistant",
        content: agentResponse.content,
        timestamp: Date.now(),
        agentData: agentResponse.agentData,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setSelectedMessageId(assistantMessage.id);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Unknown error";
      setError(errorMsg);
      console.error("Error:", err);
    } finally {
      setIsLoading(false);
    }
  }, [inputValue]);

  /**
   * Handle pressing Enter to send message
   */
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  /**
   * Clear chat history
   */
  const handleResetChat = useCallback(async () => {
    try {
      await fetch(`${API_URL}/api/reset`, { method: "POST" });
      setMessages([]);
      setSelectedMessageId(null);
      setError(null);
    } catch (err) {
      setError("Failed to reset chat");
    }
  }, []);

  return (
    <div style={styles.root}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.title}>🤖 ReAct Agent Demo</h1>
        <p style={styles.subtitle}>
          Reasoning + Acting with Gemini API
        </p>
      </div>

      {/* Error banner */}
      {error && (
        <div style={styles.errorBanner}>
          <div style={styles.errorContent}>
            <span>❌ {error}</span>
            <button
              style={styles.closeButton}
              onClick={() => setError(null)}
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Main layout - 3 column */}
      <div style={styles.main}>
        {/* Left: Chat window */}
        <div style={styles.leftPane}>
          <ChatWindow
            messages={messages}
            selectedMessageId={selectedMessageId}
            onSelectMessage={setSelectedMessageId}
          />
        </div>

        {/* Middle: Reasoning panel */}
        <div style={styles.centerPane}>
          <ReasoningPanel
            steps={selectedData.steps}
            isLoading={isLoading}
          />
        </div>

        {/* Right: Tools panel */}
        <div style={styles.rightPane}>
          <ToolsPanel
            toolCalls={selectedData.toolCalls}
            isLoading={isLoading}
          />
        </div>
      </div>

      {/* Footer - Input and controls */}
      <div style={styles.footer}>
        <div style={styles.inputContainer}>
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything... (Shift+Enter for new line)"
            style={styles.input}
            disabled={isLoading}
          />
          <div style={styles.buttonGroup}>
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              style={{
                ...styles.button,
                ...(isLoading || !inputValue.trim()
                  ? styles.buttonDisabled
                  : {}),
              }}
            >
              {isLoading ? "⏳ Thinking..." : "📤 Send"}
            </button>
            <button
              onClick={handleResetChat}
              disabled={isLoading}
              style={{
                ...styles.button,
                ...styles.buttonSecondary,
                ...(isLoading ? styles.buttonDisabled : {}),
              }}
            >
              🔄 Reset
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  root: {
    display: "flex" as const,
    flexDirection: "column" as const,
    height: "100vh",
    backgroundColor: "#fff",
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  header: {
    backgroundColor: "#1976d2",
    color: "white",
    padding: "16px 20px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  title: {
    margin: "0 0 4px 0",
    fontSize: "24px",
    fontWeight: "bold" as const,
  },
  subtitle: {
    margin: "0",
    fontSize: "13px",
    opacity: 0.9,
  },
  errorBanner: {
    backgroundColor: "#ffebee",
    borderBottom: "1px solid #ffcdd2",
    padding: "8px 16px",
  },
  errorContent: {
    display: "flex" as const,
    justifyContent: "space-between" as const,
    alignItems: "center" as const,
    fontSize: "13px",
    color: "#c62828",
  },
  closeButton: {
    background: "none",
    border: "none",
    color: "#c62828",
    cursor: "pointer" as const,
    fontSize: "16px",
  },
  main: {
    display: "flex" as const,
    flex: 1,
    minHeight: 0,
    gap: "0",
  },
  leftPane: {
    flex: "1 1 30%",
    minWidth: "250px",
    borderRight: "1px solid #ddd",
  },
  centerPane: {
    flex: "1 1 35%",
    minWidth: "280px",
    borderRight: "1px solid #ddd",
  },
  rightPane: {
    flex: "1 1 35%",
    minWidth: "280px",
  },
  footer: {
    borderTop: "1px solid #ddd",
    backgroundColor: "#f5f5f5",
    padding: "12px 16px",
  },
  inputContainer: {
    display: "flex" as const,
    gap: "8px",
    alignItems: "flex-end" as const,
  },
  input: {
    flex: 1,
    padding: "8px 12px",
    fontSize: "13px",
    border: "1px solid #ddd",
    borderRadius: "6px",
    fontFamily: "inherit",
    resize: "none" as const,
    maxHeight: "100px",
    minHeight: "40px",
  },
  buttonGroup: {
    display: "flex" as const,
    gap: "6px",
  },
  button: {
    padding: "8px 16px",
    fontSize: "13px",
    fontWeight: "500" as const,
    border: "none",
    borderRadius: "6px",
    cursor: "pointer" as const,
    transition: "all 0.2s",
    backgroundColor: "#1976d2",
    color: "white",
  },
  buttonSecondary: {
    backgroundColor: "#666",
  },
  buttonDisabled: {
    opacity: 0.5,
    cursor: "not-allowed" as const,
  },
};
