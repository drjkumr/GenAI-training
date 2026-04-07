/**
 * Tools panel - displays tool execution history
 */

import React from "react";

interface ToolCall {
  tool: string;
  input: Record<string, unknown>;
  result: string;
}

interface ToolsPanelProps {
  toolCalls: ToolCall[];
  isLoading: boolean;
}

export const ToolsPanel: React.FC<ToolsPanelProps> = ({
  toolCalls,
  isLoading,
}) => {
  const toolIcons: Record<string, string> = {
    calculator: "🧮",
    web_search: "🔍",
    file_reader: "📄",
  };

  return (
    <div style={styles.container}>
      <div style={styles.title}>🔧 Tool Executions</div>
      <div style={styles.content}>
        {isLoading && (
          <div style={styles.loading}>
            <span>⏳ Processing...</span>
          </div>
        )}

        {toolCalls.length === 0 && !isLoading && (
          <div style={styles.emptyState}>
            No tool calls yet. The agent will use tools as needed.
          </div>
        )}

        {toolCalls.map((call, idx) => (
          <div key={idx} style={styles.toolCall}>
            <div style={styles.toolHeader}>
              <span style={styles.toolIcon}>
                {toolIcons[call.tool] || "🛠️"}
              </span>
              <span style={styles.toolName}>{call.tool}</span>
              <span style={styles.callNumber}>#{idx + 1}</span>
            </div>

            <div style={styles.section}>
              <div style={styles.sectionLabel}>Input:</div>
              <div style={styles.code}>
                <pre>{JSON.stringify(call.input, null, 2)}</pre>
              </div>
            </div>

            <div style={styles.section}>
              <div style={styles.sectionLabel}>Output:</div>
              <div style={styles.result}>{call.result}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex" as const,
    flexDirection: "column" as const,
    height: "100%",
    backgroundColor: "#fafafa",
    overflowY: "auto" as const,
  },
  title: {
    padding: "12px 16px",
    fontWeight: "bold" as const,
    fontSize: "14px",
    borderBottom: "1px solid #ddd",
    backgroundColor: "#fff",
    position: "sticky" as const,
    top: 0,
    zIndex: 10,
  },
  content: {
    flex: 1,
    padding: "12px",
    overflowY: "auto" as const,
  },
  toolCall: {
    marginBottom: "16px",
    padding: "10px",
    backgroundColor: "#fff",
    borderLeft: "3px solid #4caf50",
    borderRadius: "4px",
  },
  toolHeader: {
    display: "flex" as const,
    alignItems: "center" as const,
    gap: "8px",
    marginBottom: "8px",
    fontWeight: "bold" as const,
    fontSize: "13px",
  },
  toolIcon: {
    fontSize: "16px",
  },
  toolName: {
    color: "#1976d2",
    flex: 1,
  },
  callNumber: {
    fontSize: "11px",
    color: "#999",
    backgroundColor: "#f0f0f0",
    padding: "2px 6px",
    borderRadius: "3px",
  },
  section: {
    marginBottom: "8px",
  },
  sectionLabel: {
    fontWeight: "600" as const,
    fontSize: "11px",
    color: "#555",
    marginBottom: "4px",
    textTransform: "uppercase" as const,
  },
  code: {
    fontSize: "11px",
    backgroundColor: "#f5f5f5",
    padding: "6px",
    borderRadius: "4px",
    border: "1px solid #e0e0e0",
    overflowX: "auto" as const,
  },
  result: {
    fontSize: "11px",
    backgroundColor: "#f5f5f5",
    padding: "6px",
    borderRadius: "4px",
    wordBreak: "break-word" as const,
    color: "#333",
  },
  emptyState: {
    textAlign: "center" as const,
    color: "#999",
    marginTop: "40px",
    fontSize: "13px",
  },
  loading: {
    textAlign: "center" as const,
    color: "#4caf50",
    marginTop: "40px",
    fontSize: "14px",
    fontWeight: "600" as const,
  },
};
