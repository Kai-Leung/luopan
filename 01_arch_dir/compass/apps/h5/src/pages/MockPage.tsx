import React, { useState } from "react";

type MockStep = "mock_input" | "mock_candidate" | "mock_s2" | "mock_confirm" | "mock_l2" | "mock_l3";

const MOCK_STEPS: { key: MockStep; label: string }[] = [
  { key: "mock_input", label: "Mock L0 输入演示" },
  { key: "mock_candidate", label: "Mock L1 候选演示" },
  { key: "mock_s2", label: "Mock S2 治理演示" },
  { key: "mock_confirm", label: "Mock MC 确认演示" },
  { key: "mock_l2", label: "Mock L2 入链演示" },
  { key: "mock_l3", label: "Mock L3 视图演示" },
];

export default function MockPage() {
  const [currentStep, setCurrentStep] = useState<MockStep>("mock_input");
  const [text, setText] = useState("Mock 演示输入：防水验收完成");
  const [log, setLog] = useState<string[]>([]);

  const addLog = (msg: string) => setLog((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);

  async function runStep() {
    addLog(`Mock 演示步骤，不调用正式接口，不形成正式事实：${MOCK_STEPS.find((s) => s.key === currentStep)?.label}`);
    setCurrentStep(currentStep);
  }

  return (
    <div style={{ padding: "16px", fontFamily: "sans-serif", maxWidth: 600, margin: "0 auto" }}>
      <h2>Mock 沙盒演示</h2>
      <p style={{ color: "#666", fontSize: 13, lineHeight: 1.6, margin: "8px 0 16px" }}>
        仅用于前端演示，不调用正式 L0-L3 接口，不生成治理结果，不进入人工确认，不形成正式事实。
      </p>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
        {MOCK_STEPS.map((step, i) => (
          <button
            key={step.key}
            onClick={() => setCurrentStep(step.key)}
            style={{
              padding: "6px 12px",
              border: "1px solid #ccc",
              borderRadius: 6,
              background: currentStep === step.key ? "#007aff" : "#fff",
              color: currentStep === step.key ? "#fff" : "#333",
              cursor: "pointer",
              fontSize: 13,
            }}
          >
            {i + 1}. {step.label}
          </button>
        ))}
      </div>
      <div style={{ marginBottom: 12 }}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={3}
          style={{ width: "100%", boxSizing: "border-box", padding: 8, borderRadius: 6, border: "1px solid #ccc" }}
        />
      </div>
      <button
        onClick={runStep}
        style={{ padding: "8px 20px", background: "#007aff", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer" }}
      >
        执行 Mock 演示步骤
      </button>
      <div style={{ marginTop: 16, background: "#f5f5f5", borderRadius: 6, padding: 12, minHeight: 100 }}>
        <pre style={{ margin: 0, fontSize: 12, whiteSpace: "pre-wrap" }}>{log.join("\n") || "等待 Mock 演示操作..."}</pre>
      </div>
    </div>
  );
}
