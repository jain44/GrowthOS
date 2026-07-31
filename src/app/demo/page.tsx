"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Brain,
  Zap,
  CheckCircle,
  AlertTriangle,
  TrendingUp,
  ChevronDown,
  ChevronUp,
  DollarSign,
  Megaphone,
  Truck,
  Monitor,
  BarChart3,
  Package,
  RefreshCw,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  HelpCircle,
} from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
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

const RANG_STUDIO_DEMO_RESULTS: AgentResult[] = [
  {
    agent: "Finance",
    priority: { level: "critical", score: 9 },
    problems: [
      "Gross profit margin is 39.1% — 16 points below Indian apparel benchmark of 55–65%",
      "High COGS and 62% COD dependency are eroding monthly net profit by ₹2.95L vs benchmark",
    ],
    insights: [
      "Monthly revenue: ₹18.4L | Monthly expenses: ₹11.2L | Net profit: ₹7.2L (39.1% margin)",
      "Unabsorbed return shipping losses from 22% RTO cut net profit margin by 3.2 percentage points",
    ],
    actions: [
      {
        title: "Renegotiate fabric supplier terms for top 3 ethnic wear SKUs",
        impact: "Recover 5% COGS margin → +₹92,000/month profit",
        effort: "medium",
        timeToResult: "30 days",
        tool: "Unicommerce COGS Analytics / Direct Supplier Review",
        howTo: "Audit top 3 fabric suppliers in Jaipur. Offer 30-day upfront bulk commitment in exchange for 5% cost reduction per meter. Benchmark unit costs using Unicommerce supplier reports.",
      },
    ],
  },
  {
    agent: "Operations",
    priority: { level: "critical", score: 9 },
    problems: [
      "62% COD rate with 22% RTO rate creates ₹2,49,984/mo cash flow at risk",
      "Wasted return shipping fees cost ₹23,900/month across 1,470 monthly orders",
    ],
    insights: [
      "RTO rate of 22% exceeds Indian apparel benchmark threshold of 15%",
      "Average forward + reverse freight cost per returned order is ₹240 via Shiprocket 3PL",
    ],
    actions: [
      {
        title: "Deploy automated NDR (Non-Delivery Report) WhatsApp workflow",
        impact: "Reduce RTO rate from 22% to 15% → save ₹8,700/month in freight",
        effort: "medium",
        timeToResult: "14 days",
        tool: "Shiprocket NDR Panel + Interakt WhatsApp API",
        howTo: "Enable automated WhatsApp NDR trigger within 2 hours of a failed delivery attempt. Offer address re-confirmation and landmark selection. Shiprocket benchmarks show 7pp RTO reduction with active NDR follow-up.",
      },
    ],
  },
  {
    agent: "Marketing",
    priority: { level: "high", score: 8 },
    problems: [
      "Customer Acquisition Cost (CAC) spiked 31% over 6 months from ₹290 → ₹380",
      "Meta Ads account for 60% of budget with diminishing 1.9x ROAS on prospecting campaigns",
    ],
    insights: [
      "Blended ROAS is 2.4x (above break-even 1.64x but below 2.8x target)",
      "Google Shopping and Intent Search remain underfunded at only 15% of monthly ad spend",
    ],
    actions: [
      {
        title: "Reallocate ₹25,000/mo Meta ad budget to Google Shopping & Performance Max",
        impact: "Lift blended ROAS from 2.4x to 2.85x → +₹18,000 net profit/month",
        effort: "low",
        timeToResult: "14 days",
        tool: "Google Merchant Center + Meta Ads Manager",
        howTo: "Filter top 10 bestselling ethnic co-ord sets. Connect Google Merchant Center feed with automated pricing updates. Shift ₹25K from underperforming Meta retargeting to Google PMax.",
      },
    ],
  },
  {
    agent: "Technology",
    priority: { level: "high", score: 7 },
    problems: [
      "Cart abandonment rate is 71% — standard multi-step checkout creating friction",
      "Prepaid conversion is low at 38% due to missing instant payment incentives",
    ],
    insights: [
      "Prepaid orders deliver 0% RTO rate and immediate cash settlement via Razorpay",
      "Mobile traffic constitutes 84% of store visits with a 2.8s page load speed bottleneck",
    ],
    actions: [
      {
        title: "Enable Razorpay Magic 1-Click Checkout with ₹50 prepaid incentive",
        impact: "Convert 12% COD to prepaid → save ₹8,900/mo in RTO losses",
        effort: "low",
        timeToResult: "3 days",
        tool: "Razorpay Magic Checkout (Shopify App)",
        howTo: "Install Razorpay Magic Checkout on Shopify store. Configure auto-fill address engine and display '₹50 Flat Discount on UPI/Cards' banner at checkout. Takes under 3 days to deploy.",
      },
    ],
  },
  {
    agent: "Unit Economics",
    priority: { level: "medium", score: 6 },
    problems: [
      "LTV:CAC ratio is 4.57x (healthy), but RTO freight adjustments compress real ratio to 4.02x",
      "Contribution margin per order is ₹761 against ₹1,250 AOV",
    ],
    insights: [
      "Repeat purchase multiplier is 1.39x based on 28% repeat customer rate",
      "CAC payback period is ultra-fast at 0.30 months",
    ],
    actions: [
      {
        title: "Introduce Festive Bundle Kits with minimum ₹1,800 threshold for Free Express Delivery",
        impact: "Increase AOV from ₹1,250 to ₹1,480 → +₹42,000/month gross profit",
        effort: "low",
        timeToResult: "7 days",
        tool: "Shopify Bundles / Bold Bundles",
        howTo: "Combine matching Dupatta + Kurta sets into pre-packaged bundles. Set free express shipping threshold at ₹1,800 to encourage multi-item cart additions.",
      },
    ],
  },
  {
    agent: "Inventory & Supply Chain",
    priority: { level: "medium", score: 5 },
    problems: [
      "Stockouts on top 2 fast-moving kurta sizes (M & L) lost an estimated 45 orders last month",
      "Supplier replenishment lead time in Jaipur averages 18 days",
    ],
    insights: [
      "Inventory turnover is 5.2x/year (benchmark: 6x–8x/year for Indian apparel)",
      "Safety stock levels are uncalibrated for peak festive weekend demand surges",
    ],
    actions: [
      {
        title: "Set up automated reorder point alerts in Unicommerce for sizes M & L",
        impact: "Prevent stockouts → protect ₹56,250/month in lost sales",
        effort: "low",
        timeToResult: "5 days",
        tool: "Unicommerce / Zoho Inventory WMS",
        howTo: "Configure automated reorder triggers when size M & L stock hits 14 days of average daily velocity. Send instant SMS/email alert to procurement lead in Jaipur.",
      },
    ],
  },
  {
    agent: "Retention & LTV",
    priority: { level: "medium", score: 5 },
    problems: [
      "Repeat rate stagnated at 28% for 3 consecutive months",
      "Post-purchase communication relies on basic SMS without interactive WhatsApp follow-up",
    ],
    insights: [
      "WhatsApp flows in India achieve 88% open rate vs 14% for email marketing",
      "Second-time buyers have a 52% higher prepaid likelihood than first-time buyers",
    ],
    actions: [
      {
        title: "Launch 3-step WhatsApp Post-Purchase Retention & VIP Review sequence",
        impact: "Increase repeat purchase rate from 28% to 33% → +₹45,000/month recurring revenue",
        effort: "medium",
        timeToResult: "21 days",
        tool: "Interakt / AiSensy WhatsApp API",
        howTo: "Set up automated 3-part sequence: Day 3 delivery check + care instructions; Day 15 review prompt with 10% repeat discount code; Day 45 new catalog preview.",
      },
    ],
  },
];

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

function AgentCard({ agent }: { agent: AgentResult }) {
  const [open, setOpen] = useState(false);
  const Icon = agentIcons[agent.agent] ?? Brain;

  return (
    <div className="border border-[rgba(255,255,255,0.07)] rounded-[6px] bg-[#141517] overflow-hidden transition-colors">
      <button
        className="w-full px-4 py-3 flex items-center gap-3 text-left hover:bg-[rgba(255,255,255,0.02)] transition-colors"
        onClick={() => setOpen(!open)}
      >
        <div className="w-6 h-6 rounded-[4px] bg-[#1C1D1F] border border-[rgba(255,255,255,0.08)] flex items-center justify-center flex-shrink-0">
          <Icon className="w-3.5 h-3.5 text-[#5E6AD2]" />
        </div>
        <div className="flex-1 min-w-0 flex items-center gap-3">
          <span className="text-[13px] font-medium text-[#F1F1F1]">{agent.agent} Agent</span>
          <Badge priority={agent.priority.level} />
          <p className="text-[12px] text-[#8A8A8A] truncate hidden sm:block">
            {agent.problems[0] ?? "Analysis complete"}
          </p>
        </div>
        <div className="flex items-center gap-4 flex-shrink-0">
          <span className="text-[11px] text-[#8A8A8A] hidden md:block">Score {agent.priority.score}/10</span>
          {open ? <ChevronUp className="w-3.5 h-3.5 text-[#8A8A8A]" /> : <ChevronDown className="w-3.5 h-3.5 text-[#8A8A8A]" />}
        </div>
      </button>

      {open && (
        <div className="px-4 py-3 border-t border-[rgba(255,255,255,0.05)] bg-[#101113] space-y-3">
          {agent.problems.length > 0 && (
            <div>
              <h4 className="text-[10px] font-medium text-[#EB5757] uppercase tracking-wider mb-1.5 flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" /> Friction Points
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
                <CheckCircle className="w-3.5 h-3.5" /> Prescribed Strategic Actions
              </h4>
              <div className="space-y-2">
                {agent.actions.map((a, i) => (
                  <ActionCard key={i} action={a} idx={i} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function DemoPage() {
  const [agents] = useState<AgentResult[]>(RANG_STUDIO_DEMO_RESULTS);

  return (
    <div className="min-h-screen bg-[#090A0F] text-zinc-100 flex flex-col font-sans overflow-x-hidden relative">
      <Navbar />

      {/* Demo Banner */}
      <div className="bg-gradient-to-r from-indigo-900/80 via-purple-900/80 to-zinc-900 border-b border-indigo-500/30 px-6 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between gap-4 flex-wrap text-xs">
          <div className="flex items-center gap-2 text-zinc-200">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span>
              <strong>PITCH DEMO MODE:</strong> Exploring live diagnosis for <strong>Rang Studio</strong> (Ethnic Wear D2C · ₹18.4L/mo · 62% COD · 22% RTO).
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/register">
              <Button variant="primary" size="sm" className="h-8 text-xs gap-1.5">
                Analyze Your Store Free
                <ArrowRight className="w-3 h-3" />
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <main className="flex-1 max-w-5xl mx-auto px-6 py-10 w-full space-y-6">
        {/* Store Header Strip */}
        <div className="p-6 rounded-2xl bg-zinc-900/60 border border-white/10 flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-white tracking-tight">Rang Studio</h1>
              <Badge variant="primary">Apparel & Ethnic Wear</Badge>
              <Badge variant="secondary" className="border-emerald-500/30 text-emerald-400">
                ₹18.4L Revenue/mo
              </Badge>
            </div>
            <p className="text-xs text-zinc-400 mt-1">
              Shopify India · Jaipur Manufacturing · Shiprocket 3PL · 62% COD · 22% RTO
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/register">
              <Button variant="gradient" className="gap-2 text-xs">
                <Brain className="w-4 h-4" />
                Connect Your Store
              </Button>
            </Link>
          </div>
        </div>

        {/* Diagnostic Brief & Health ring */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Health Score */}
          <Card className="flex flex-col items-center justify-center p-6 text-center bg-zinc-900/80 border-white/10">
            <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-3">
              Store Health Index
            </p>
            <div className="relative w-32 h-32 flex items-center justify-center">
              <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
                <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10" />
                <circle
                  cx="60" cy="60" r="50" fill="none"
                  stroke="#FFA726" strokeWidth="10" strokeLinecap="round"
                  strokeDasharray="194 314"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-extrabold text-white">62</span>
                <span className="text-xs text-zinc-400">/100</span>
              </div>
            </div>
            <p className="text-xs font-semibold text-amber-400 mt-3">Moderate Risk · Margin Bleed</p>
          </Card>

          {/* CEO Intelligence */}
          <Card className="md:col-span-2 p-6 bg-zinc-900/80 border-white/10 space-y-3">
            <h3 className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
              <Brain className="w-4 h-4" /> CEO Intelligence — Cross-Agent Synthesis
            </h3>
            <p className="text-xs font-semibold text-white leading-relaxed">
              🎯 <strong>Root Cause:</strong> 62% COD dependency combined with a 22% RTO rate is eroding ₹23,900/mo in freight losses while masking Facebook Ad inefficiency.
            </p>
            <div className="space-y-2 pt-2 border-t border-white/10 text-xs text-zinc-300">
              <div className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">1.</span>
                <span>
                  <strong>Finance + Operations:</strong> High COD (62%) and low gross margins (39.1%) create an urgent profit deficit of ₹2.95L/mo vs Indian ethnic wear benchmarks (55-65%).
                </span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">2.</span>
                <span>
                  <strong>Technology + Marketing:</strong> Razorpay 1-Click Magic Checkout with a ₹50 prepaid incentive can convert ~12% of COD orders to prepaid, saving ₹8,900/mo in RTO.
                </span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">3.</span>
                <span>
                  <strong>Retention + Unit Economics:</strong> Shifting customer repeat touchpoints from email to automated WhatsApp flows can elevate repeat revenue from 28% to 33%.
                </span>
              </div>
            </div>
          </Card>
        </div>

        {/* 7 Agent Cards */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold text-zinc-400 uppercase tracking-wider">
              7 Specialized Agent Diagnoses — Ranked by Priority
            </h2>
            <span className="text-xs text-zinc-500">Click any row to expand strategic action plan</span>
          </div>

          <div className="space-y-2">
            {agents.map((agent) => (
              <AgentCard key={agent.agent} agent={agent} />
            ))}
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="p-8 rounded-2xl bg-gradient-to-b from-indigo-950/40 to-zinc-950 border border-white/10 text-center space-y-4">
          <h3 className="text-xl font-extrabold text-white">Ready to run GrowthOS on your own store?</h3>
          <p className="text-xs text-zinc-400 max-w-md mx-auto">
            Connect Shopify India, WooCommerce, Shiprocket, or Razorpay in under 60 seconds.
          </p>
          <div className="pt-2">
            <Link href="/register">
              <Button variant="gradient" size="lg" className="gap-2 text-xs px-8 h-11">
                Start Free Trial Now
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </main>

      <footer className="px-6 py-8 border-t border-white/5 text-center text-xs text-zinc-500 relative z-10">
        © {new Date().getFullYear()} GrowthOS Inc. Pitch Demo Mode. All rights reserved.
      </footer>
    </div>
  );
}
