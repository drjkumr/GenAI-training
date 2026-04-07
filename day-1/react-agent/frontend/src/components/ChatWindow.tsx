/**
 * Chat window component - displays conversation history
 */

import React from "react";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  agentData?: {
    steps: Array<{
      thought?: string;
      action?: { tool: string; input: Record<string, unknown> };
      observation?: string;
    }>;
    toolCalls: Array<{ tool: string; input: Record<string, unknown>; result: string }>;
  };
}

interface ChatWindowProps {
  messages: Message[];
  selectedMessageId: string | null;
  onSelectMessage: (id: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  selectedMessageId,
  onSelectMessage,
}) => {
  const endRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div style={styles.container}>
      <div style={styles.title}>💬 Chat</div>
      <div style={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div style={styles.emptyState}>No messages yet. Start chatting!</div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              style={{
                ...styles.message,
                ...(msg.role === "user"
                  ? styles.userMessage
                  : styles.assistantMessage),
                ...(selectedMessageId === msg.id
                  ? styles.messageSelected
                  : {}),
              }}
              onClick={() => onSelectMessage(msg.id)}
            >
              <div style={styles.role}>
                {msg.role === "user" ? "👤 You" : "🤖 Agent"}
              </div>
              <div style={styles.content}>{msg.content}</div>
              {msg.agentData && msg.agentData.toolCalls.length > 0 && (
                <div style={styles.toolBadge}>
                  🔧 {msg.agentData.toolCalls.length} tool call(s)
                </div>
              )}
              <div style={styles.timestamp}>
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        <div ref={endRef} />
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex" as const,
    flexDirection: "column" as const,
    height: "100%",
    backgroundColor: "#f5f5f5",
    borderRight: "1px solid #ddd",
  },
  title: {
    padding: "12px 16px",
    fontWeight: "bold" as const,
    fontSize: "14px",
    borderBottom: "1px solid #ddd",
    backgroundColor: "#fff",
  },
  messagesContainer: {
    flex: 1,
    overflowY: "auto" as const,
    padding: "12px",
    display: "flex",
    flexDirection: "column" as const,
    gap: "8px",
  },
  message: {
    padding: "10px",
    borderRadius: "6px",
    cursor: "pointer" as const,
    transition: "all 0.2s",
    border: "1px solid transparent",
  },
  userMessage: {
    backgroundColor: "#e3f2fd",
    marginLeft: "20px",
  },
  assistantMessage: {
    backgroundColor: "#fff",
    marginRight: "20px",
  },
  messageSelected: {
    borderColor: "#1976d2",
    backgroundColor: "#fff3e0",
  },
  role: {
    fontWeight: "600" as const,
    fontSize: "12px",
    marginBottom: "4px",
    color: "#666",
  },
  content: {
    fontSize: "13px",
    lineHeight: "1.4",
    marginBottom: "6px",
    color: "#333",
  },
  toolBadge: {
    display: "inline-block",
    fontSize: "10px",
    backgroundColor: "#4caf50",
    color: "white",
    padding: "2px 6px",
    borderRadius: "3px",
    marginBottom: "4px",
  },
  timestamp: {
    fontSize: "11px",
    color: "#999",
    marginTop: "4px",
  },
  emptyState: {
    textAlign: "center" as const,
    color: "#999",
    marginTop: "40px",
    fontSize: "14px",
  },
};
