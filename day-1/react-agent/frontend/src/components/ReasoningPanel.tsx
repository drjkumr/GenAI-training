/**
 * Reasoning panel - displays ReAct steps (Thought/Action/Observation)
 */

import React from "react";

interface ReActStep {
  thought?: string;
  action?: {
    tool: string;
    input: Record<string, unknown>;
  };
  observation?: string;
}

interface ReasoningPanelProps {
  steps: ReActStep[];
  isLoading: boolean;
}

export const ReasoningPanel: React.FC<ReasoningPanelProps> = ({
  steps,
  isLoading,
}) => {
  return (
    <div style={styles.container}>
      <div style={styles.title}>🧠 Reasoning Steps</div>
      <div style={styles.content}>
        {isLoading && (
          <div style={styles.loading}>
            <span>⏳ Agent is thinking...</span>
          </div>
        )}

        {steps.length === 0 && !isLoading && (
          <div style={styles.emptyState}>
            No reasoning steps yet. Send a message to see how the agent thinks.
          </div>
        )}

        {steps.map((step, idx) => (
          <div key={idx} style={styles.step}>
            <div style={styles.stepNumber}>Step {idx + 1}</div>

            {step.thought && (
              <div style={styles.stepPart}>
                <div style={styles.label}>💭 Thought:</div>
                <div style={styles.value}>{step.thought}</div>
              </div>
            )}

            {step.action && (
              <div style={styles.stepPart}>
                <div style={styles.label}>🎯 Action:</div>
                <div style={styles.value}>{step.action.tool}</div>
                <div style={styles.inputBox}>
                  <pre>
                    {JSON.stringify(step.action.input, null, 2)}
                  </pre>
                </div>
              </div>
            )}

            {step.observation && (
              <div style={styles.stepPart}>
                <div style={styles.label}>👁️ Observation:</div>
                <div style={styles.value}>{step.observation}</div>
              </div>
            )}
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
    borderRight: "1px solid #ddd",
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
  step: {
    marginBottom: "16px",
    padding: "10px",
    backgroundColor: "#fff",
    borderLeft: "3px solid #2196f3",
    borderRadius: "4px",
  },
  stepNumber: {
    fontWeight: "bold" as const,
    fontSize: "12px",
    color: "#1976d2",
    marginBottom: "8px",
  },
  stepPart: {
    marginBottom: "8px",
  },
  label: {
    fontWeight: "600" as const,
    fontSize: "12px",
    color: "#555",
    marginBottom: "4px",
  },
  value: {
    fontSize: "12px",
    color: "#333",
    backgroundColor: "#f5f5f5",
    padding: "6px",
    borderRadius: "4px",
    wordBreak: "break-word" as const,
  },
  inputBox: {
    fontSize: "11px",
    backgroundColor: "#f9f9f9",
    padding: "6px",
    borderRadius: "4px",
    border: "1px solid #e0e0e0",
    marginTop: "4px",
    overflowX: "auto" as const,
  },
  emptyState: {
    textAlign: "center" as const,
    color: "#999",
    marginTop: "40px",
    fontSize: "13px",
  },
  loading: {
    textAlign: "center" as const,
    color: "#2196f3",
    marginTop: "40px",
    fontSize: "14px",
    fontWeight: "600" as const,
  },
};
