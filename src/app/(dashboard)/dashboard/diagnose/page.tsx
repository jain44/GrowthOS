"use client";

import { useState } from "react";
import {
  Brain,
  CheckCircle,
  AlertTriangle,
  TrendingUp,
  ChevronDown,
  ChevronUp,
  Zap,
  DollarSign,
  Megaphone,
  Truck,
  Monitor,
  BarChart3,
  Package,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Spinner, LoadingDots } from "@/components/ui/spinner";
import { type AgentResult, type ActionItem } from "@/agents/shared";

const agentIcons: Record<string, React.ElementType> = {
  Finance: DollarSign,
  Marketing: Megaphone,
  Operations: Truck,
  Technology: Monitor,
  "Unit Economics": BarChart3,
  "Inventory & Supply Chain": Package,
  "Retention & LTV": RefreshCw,
};

const agentOrder = [
  "Finance",
  "Marketing",
  "Operations",
  "Technology",
  "Unit Economics",
  "Inventory & Supply Chain",
  "Retention & LTV",
];

interface SynthesisResult {
  crossAgentInsights: string[];
  rootCause: string;
  conflictResolution?: string;
}

interface DiagnosisResult {
  healthScore: number;
  summary: {
    topRisk: string;
    biggestOpportunity: string;
    primaryAction: string;
  };
  agents: AgentResult[];
  synthesis?: SynthesisResult;
}

function ActionCard({ action, idx }: { action: ActionItem; idx: number }) {
  const [showHow, setShowHow] = useState(false);
  const [copied, setCopied] = useState(false);
  const effortColor = { low: "#4CAF50", medium: "#FFA726", high: "#EB5757" }[action.effort] ?? "#8A8A8A";

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-[6px] border border-[rgba(255,255,255,0.08)] bg-[#141517] overflow-hidden">
      <div className="px-3.5 py-3 flex items-start gap-2.5">
        <span className="text-[#4CAF50] font-semibold text-[12px] flex-shrink-0 mt-0.5">{idx + 1}.</span>
        <div className="flex-1 min-w-0">
          <p className="text-[13px] font-semibold text-[#F1F1F1] leading-snug">{action.title}</p>
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <span className="text-[10px] px-2 py-0.5 rounded bg-[rgba(76,175,80,0.12)] text-[#81C784] font-medium border border-[rgba(76,175,80,0.2)]">
              {action.impact}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded border border-[rgba(255,255,255,0.08)]" style={{ color: effortColor }}>
              Effort: {action.effort}
            </span>
            <span className="text-[10px] text-[#8A8A8A]">⏱ {action.timeToResult}</span>
            {action.tool && <span className="text-[10px] text-[#8E96EA]">🔧 {action.tool}</span>}
          </div>

          {(action.howTo || action.copyTemplate || action.clickPath) && (
            <button
              onClick={() => setShowHow(!showHow)}
              className="mt-2 text-[11px] text-[#5E6AD2] hover:text-[#8E96EA] font-medium transition-colors flex items-center gap-1 underline underline-offset-2"
            >
              {showHow ? "Hide Operational Playbook ▲" : "📋 View Operational Playbook & Copy Templates →"}
            </button>
          )}

          {showHow && (
            <div className="mt-3 space-y-2.5 text-[11px] text-[#8A8A8A] border-l-2 border-[#5E6AD2] pl-3 py-1 bg-[#0F1012] rounded-r p-2.5">
              {action.clickPath && (
                <div>
                  <span className="text-[10px] font-bold text-[#8E96EA] uppercase tracking-wider block mb-0.5">
                    ⚙️ Software Click Path
                  </span>
                  <p className="text-[#F1F1F1] font-mono text-[10px] bg-[#1A1B1E] p-1.5 rounded border border-white/5">
                    {action.clickPath}
                  </p>
                </div>
              )}

              {action.copyTemplate && (
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-bold text-[#81C784] uppercase tracking-wider">
                      💬 {action.copyTemplate.label}
                    </span>
                    <button
                      onClick={() => handleCopy(action.copyTemplate!.text)}
                      className="text-[10px] px-2 py-0.5 rounded bg-[rgba(94,106,210,0.2)] text-[#8E96EA] hover:bg-[rgba(94,106,210,0.3)] transition-colors font-medium"
                    >
                      {copied ? "✓ Copied!" : "📋 Copy Template"}
                    </button>
                  </div>
                  <pre className="text-[10px] text-[#E1E1E1] bg-[#18191C] p-2 rounded border border-white/5 font-sans whitespace-pre-wrap leading-relaxed">
                    {action.copyTemplate.text}
                  </pre>
                </div>
              )}

              {action.sopSteps && action.sopSteps.length > 0 ? (
                <div>
                  <span className="text-[10px] font-bold text-[#FFA726] uppercase tracking-wider block mb-1">
                    📝 Step-by-Step SOP Checklist
                  </span>
                  <ul className="space-y-1">
                    {action.sopSteps.map((step, sIdx) => (
                      <li key={sIdx} className="flex items-start gap-1.5 text-[11px] text-[#D1D1D1]">
                        <span className="text-[#5E6AD2] font-bold">{sIdx + 1}.</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                action.howTo && (
                  <div>
                    <span className="text-[10px] font-bold text-[#FFA726] uppercase tracking-wider block mb-0.5">
                      📝 Implementation Guide
                    </span>
                    <p className="text-[#D1D1D1] leading-relaxed">{action.howTo}</p>
                  </div>
                )
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function AgentRow({ agent }: { agent: AgentResult }) {
  const [open, setOpen] = useState(false);
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);
  const Icon = agentIcons[agent.agent] ?? Brain;

  const handleFeedback = async (rating: "up" | "down") => {
    setFeedback(rating);
    fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ agentName: agent.agent, rating: rating === "up" ? 5 : 1 }),
    }).catch(() => {});
  };

  return (
    <div className="border border-[rgba(255,255,255,0.07)] rounded-[6px] bg-[#141517] overflow-hidden transition-colors">
      <button
        className="w-full px-4 py-3 flex items-center gap-3 text-left hover:bg-[rgba(255,255,255,0.02)] transition-colors"
        onClick={() => setOpen(!open)}
        id={`agent-card-${agent.agent.toLowerCase().replace(/[^a-z]/g, "-")}`}
      >
        <div className="w-6 h-6 rounded-[4px] bg-[#1C1D1F] border border-[rgba(255,255,255,0.08)] flex items-center justify-center flex-shrink-0">
          <Icon className="w-3.5 h-3.5 text-[#5E6AD2]" />
        </div>
        <div className="flex-1 min-w-0 flex items-center gap-3">
          <span className="text-[13px] font-medium text-[#F1F1F1]">{agent.agent}</span>
          <Badge priority={agent.priority.level} />
          <p className="text-[12px] text-[#8A8A8A] truncate hidden sm:block">
            {agent.problems[0] ?? "Analysis complete"}
          </p>
        </div>
        <div className="flex items-center gap-4 flex-shrink-0">
          <div className="text-right hidden md:block">
            <span className="text-[11px] text-[#4E4E4E]">Priority {agent.priority.score}/10</span>
          </div>
          {open ? (
            <ChevronUp className="w-3.5 h-3.5 text-[#8A8A8A]" />
          ) : (
            <ChevronDown className="w-3.5 h-3.5 text-[#8A8A8A]" />
          )}
        </div>
      </button>

      {open && (
        <div className="px-4 py-3 border-t border-[rgba(255,255,255,0.05)] bg-[#101113] space-y-3">
          {agent.problems.length > 0 && (
            <div>
              <h4 className="text-[10px] font-medium text-[#EB5757] uppercase tracking-wider mb-1.5 flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" /> Identified Friction Points
              </h4>
              <ul className="space-y-1">
                {agent.problems.map((p, i) => (
                  <li key={i} className="flex items-start gap-2 text-[12px] text-[#8A8A8A]">
                    <span className="w-1 h-1 rounded-full bg-[#EB5757] flex-shrink-0 mt-1.5" />
                    {p}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {agent.insights.length > 0 && (
            <div>
              <h4 className="text-[10px] font-medium text-[#4DA6FF] uppercase tracking-wider mb-1.5 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> Core Findings & Benchmarks
              </h4>
              <ul className="space-y-1">
                {agent.insights.map((ins, i) => (
                  <li key={i} className="flex items-start gap-2 text-[12px] text-[#8A8A8A]">
                    <span className="w-1 h-1 rounded-full bg-[#4DA6FF] flex-shrink-0 mt-1.5" />
                    {ins}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {agent.actions.length > 0 && (
            <div>
              <h4 className="text-[10px] font-medium text-[#4CAF50] uppercase tracking-wider mb-2 flex items-center gap-1">
                <CheckCircle className="w-3 h-3" /> Prescribed Strategic Actions
              </h4>
              <div className="space-y-2">
                {agent.actions.map((a, i) => (
                  <ActionCard key={i} action={a} idx={i} />
                ))}
              </div>
            </div>
          )}

          {/* Feedback */}
          <div className="pt-2 border-t border-[rgba(255,255,255,0.04)] flex items-center gap-2">
            <span className="text-[10px] text-[#4E4E4E]">Was this useful?</span>
            <button
              onClick={() => handleFeedback("up")}
              className={`text-[14px] transition-opacity ${feedback === "up" ? "opacity-100" : "opacity-40 hover:opacity-80"}`}
            >👍</button>
            <button
              onClick={() => handleFeedback("down")}
              className={`text-[14px] transition-opacity ${feedback === "down" ? "opacity-100" : "opacity-40 hover:opacity-80"}`}
            >👎</button>
            {feedback && <span className="text-[10px] text-[#4CAF50] ml-1">Thanks!</span>}
          </div>
        </div>
      )}
    </div>
  );
}

export default function DiagnosePage() {
  const [running, setRunning] = useState(false);
  const [runningAgent, setRunningAgent] = useState<string | null>(null);
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [error, setError] = useState("");

  const runDiagnosis = async () => {
    setError("");
    setRunning(true);
    setResult(null);

    const bizRes = await fetch("/api/business");
    const bizData = await bizRes.json();
    const business = bizData.businesses?.[0];

    if (!business) {
      setError("No business profile found. Please complete onboarding first.");
      setRunning(false);
      return;
    }

    const animateAgents = async () => {
      for (const agentName of agentOrder) {
        setRunningAgent(agentName);
        await new Promise((r) => setTimeout(r, 350));
      }
    };

    const [analysisResponse] = await Promise.all([
      fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ businessId: business.id }),
      }),
      animateAgents(),
    ]);

    setRunningAgent(null);
    setRunning(false);

    if (!analysisResponse.ok) {
      const err = await analysisResponse.json();
      setError(err.error ?? "Analysis failed. Please try again.");
      return;
    }

    const data = await analysisResponse.json();
    setResult(data);
  };

  const sortedAgents = result?.agents
    ? [...result.agents].sort((a, b) => b.priority.score - a.priority.score)
    : [];

  return (
    <div className="max-w-4xl space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.06)]">
        <div>
          <h1 className="text-[16px] font-semibold text-[#F1F1F1] tracking-tight">7-Agent AI Diagnosis</h1>
          <p className="text-[12px] text-[#8A8A8A]">
            Parallel specialized agents inspecting store metrics in real-time.
          </p>
        </div>
        {result && (
          <Button onClick={runDiagnosis} size="sm" variant="secondary" className="gap-1.5">
            <Zap className="w-3.5 h-3.5" />
            Re-run Analysis
          </Button>
        )}
      </div>

      {/* Trigger CTA */}
      {!running && !result && (
        <Card className="p-8 text-center border-dashed border-[rgba(255,255,255,0.1)]">
          <div className="w-10 h-10 rounded-[6px] bg-[rgba(94,106,210,0.12)] border border-[rgba(94,106,210,0.2)] flex items-center justify-center mx-auto mb-4">
            <Brain className="w-5 h-5 text-[#5E6AD2]" />
          </div>
          <h2 className="text-[14px] font-semibold text-[#F1F1F1] mb-1">Execute Parallel Diagnostic</h2>
          <p className="text-[12px] text-[#8A8A8A] max-w-sm mx-auto mb-5">
            All 7 AI agents (Finance, Marketing, Operations, Tech, Unit Economics, Inventory, Retention) will evaluate your operational metrics concurrently.
          </p>
          <Button onClick={runDiagnosis} size="md" className="gap-2" id="run-diagnosis-btn">
            <Zap className="w-3.5 h-3.5" />
            Start 7-Agent Diagnosis
          </Button>
        </Card>
      )}

      {/* Running State Progress */}
      {running && (
        <Card className="p-5">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-[rgba(255,255,255,0.05)]">
            <div className="flex items-center gap-2">
              <Spinner size="sm" />
              <span className="text-[13px] font-medium text-[#F1F1F1]">Executing Diagnostic Matrix</span>
            </div>
            <span className="text-[11px] text-[#8A8A8A]">Parallel Groq Llama 3.3 Engine</span>
          </div>

          <div className="space-y-1.5">
            {agentOrder.map((agentName) => {
              const agentIndex = agentOrder.indexOf(agentName);
              const runningIndex = runningAgent ? agentOrder.indexOf(runningAgent) : -1;
              const isDone = runningIndex > agentIndex;
              const isActive = runningAgent === agentName;
              const Icon = agentIcons[agentName] ?? Brain;

              return (
                <div
                  key={agentName}
                  className={`flex items-center gap-3 px-3 py-2 rounded-[4px] transition-colors ${
                    isActive
                      ? "bg-[rgba(94,106,210,0.1)] border border-[rgba(94,106,210,0.2)]"
                      : isDone
                      ? "bg-[rgba(76,175,80,0.04)] border border-[rgba(76,175,80,0.1)]"
                      : "bg-[#141517] border border-transparent"
                  }`}
                >
                  <div className="w-5 h-5 rounded-[4px] bg-[#1C1D1F] flex items-center justify-center flex-shrink-0">
                    {isDone ? (
                      <CheckCircle className="w-3.5 h-3.5 text-[#4CAF50]" />
                    ) : isActive ? (
                      <Spinner size="sm" />
                    ) : (
                      <Icon className="w-3 h-3 text-[#4E4E4E]" />
                    )}
                  </div>
                  <span
                    className={`text-[12px] font-medium ${
                      isActive
                        ? "text-[#8E96EA]"
                        : isDone
                        ? "text-[#81C784]"
                        : "text-[#8A8A8A]"
                    }`}
                  >
                    {agentName} Agent
                  </span>
                  {isActive && <LoadingDots className="ml-auto" />}
                  {isDone && (
                    <span className="ml-auto text-[11px] text-[#4CAF50]">Complete</span>
                  )}
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Results View */}
      {result && (
        <div className="space-y-4 animate-slide-up">
          {/* Summary Strip */}
          <div className="p-4 rounded-[6px] border border-[rgba(255,255,255,0.08)] bg-[#141517] flex items-center justify-between gap-4 flex-wrap">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-[4px] bg-[#5E6AD2]/15 border border-[#5E6AD2]/30 flex items-center justify-center text-[15px] font-bold text-white">
                {result.healthScore}
              </div>
              <div>
                <p className="text-[10px] text-[#4E4E4E] uppercase tracking-wider">Health Index</p>
                <p className="text-[13px] font-medium text-[#F1F1F1]">Analysis Complete</p>
              </div>
            </div>
            <div className="hidden sm:block max-w-xs">
              <p className="text-[10px] text-[#EB5757] uppercase tracking-wider">Primary Risk</p>
              <p className="text-[12px] text-[#8A8A8A] truncate">{result.summary.topRisk}</p>
            </div>
            <div className="hidden md:block max-w-xs">
              <p className="text-[10px] text-[#4CAF50] uppercase tracking-wider">Primary Upside</p>
              <p className="text-[12px] text-[#8A8A8A] truncate">{result.summary.biggestOpportunity}</p>
            </div>
          </div>

          {/* Synthesis Panel */}
          {result.synthesis && result.synthesis.crossAgentInsights.length > 0 && (
            <div className="p-4 rounded-[6px] border border-[rgba(94,106,210,0.2)] bg-[rgba(94,106,210,0.05)]">
              <h3 className="text-[11px] font-medium text-[#5E6AD2] uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Brain className="w-3.5 h-3.5" /> CEO Intelligence — Cross-Agent Synthesis
              </h3>
              {result.synthesis.rootCause && (
                <p className="text-[12px] text-[#F1F1F1] font-medium mb-2">
                  🎯 Root Cause: {result.synthesis.rootCause}
                </p>
              )}
              <ul className="space-y-1.5">
                {result.synthesis.crossAgentInsights.map((insight, i) => (
                  <li key={i} className="flex items-start gap-2 text-[12px] text-[#8A8A8A]">
                    <span className="text-[#5E6AD2] font-medium flex-shrink-0">{i + 1}.</span>
                    {insight}
                  </li>
                ))}
              </ul>
              {result.synthesis.conflictResolution && (
                <p className="mt-2 text-[11px] text-[#FFA726] border-l-2 border-[rgba(255,167,38,0.3)] pl-2">
                  ⚡ Conflict resolved: {result.synthesis.conflictResolution}
                </p>
              )}
            </div>
          )}

          {/* Agent Rows */}
          <div className="space-y-2">
            <h2 className="text-[11px] font-medium text-[#4E4E4E] uppercase tracking-wider">
              Agent Diagnosis Rows — Ranked by Priority Score
            </h2>
            {sortedAgents.map((agent) => (
              <AgentRow key={agent.agent} agent={agent} />
            ))}
          </div>
        </div>
      )}

      {/* Error Output */}
      {error && (
        <div className="px-3 py-2 rounded-[4px] bg-[rgba(235,87,87,0.1)] border border-[rgba(235,87,87,0.2)] text-[12px] text-[#EB5757] flex items-start gap-2">
          <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0 mt-0.5" />
          {error}
        </div>
      )}
    </div>
  );
}
