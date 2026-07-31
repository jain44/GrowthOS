import Link from "next/link";
import Image from "next/image";
import {
  Brain,
  Zap,
  CheckCircle,
  ArrowRight,
  DollarSign,
  Megaphone,
  Truck,
  Monitor,
  BarChart3,
  Package,
  RefreshCw,
  Sparkles,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Button } from "@/components/ui/button";

const AGENTS = [
  { name: "Finance Agent", role: "Profit Margins, Expense Ratios & Cash Flow", icon: DollarSign, color: "from-emerald-500 to-teal-500", glow: "border-emerald-500/30" },
  { name: "Marketing Agent", role: "Blended CAC, ROAS & Ad Channel Optimization", icon: Megaphone, color: "from-blue-500 to-indigo-500", glow: "border-blue-500/30" },
  { name: "Operations Agent", role: "Fulfillment SLA & Logistics Bottlenecks", icon: Truck, color: "from-amber-500 to-orange-500", glow: "border-amber-500/30" },
  { name: "Technology Agent", role: "Cart Abandonment & Checkout Conversion Rate", icon: Monitor, color: "from-purple-500 to-pink-500", glow: "border-purple-500/30" },
  { name: "Unit Economics Agent", role: "Contribution Margins & LTV:CAC Ratio", icon: BarChart3, color: "from-indigo-500 to-cyan-500", glow: "border-indigo-500/30" },
  { name: "Inventory Agent", role: "Stockout Risk & Turnover Velocity", icon: Package, color: "from-rose-500 to-red-500", glow: "border-rose-500/30" },
  { name: "Retention Agent", role: "Repeat Customer Rate & LTV Growth", icon: RefreshCw, color: "from-violet-500 to-purple-500", glow: "border-violet-500/30" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#090A0F] text-zinc-100 flex flex-col font-sans overflow-x-hidden relative">
      {/* Glow Effects */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-gradient-to-tr from-indigo-600/20 via-purple-600/20 to-pink-600/10 rounded-full blur-[120px] pointer-events-none" />

      <Navbar />

      {/* Hero Section */}
      <section className="px-6 pt-20 pb-16 text-center max-w-5xl mx-auto flex-1 flex flex-col justify-center items-center relative z-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-xs font-semibold text-indigo-300 mb-8 shadow-lg shadow-indigo-500/10 animate-fade-in">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          7 Parallel AI Agents · Built for D2C Brands
        </div>

        <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight text-white max-w-4xl leading-[1.1] mb-6">
          Institutional-grade growth intelligence for <span className="gradient-text">E-Commerce Founders</span>
        </h1>

        <p className="text-lg text-zinc-400 max-w-2xl mb-10 leading-relaxed font-normal">
          GrowthOS ingests your unit metrics and orchestrates 7 specialized AI agents in parallel to diagnose risks, simulate strategic moves, and produce CEO-level briefs in under 4 seconds.
        </p>

        <div className="flex items-center gap-4 mb-16">
          <Link href="/register">
            <Button variant="gradient" size="lg" className="gap-2 text-base px-7 h-12">
              Launch GrowthOS Free
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="secondary" size="lg" className="text-base px-6 h-12">
              Sign In to Workspace
            </Button>
          </Link>
        </div>

        {/* Hero Mockup Graphic */}
        <div className="w-full max-w-5xl rounded-2xl border border-white/10 bg-zinc-900/60 p-3 backdrop-blur-2xl shadow-2xl shadow-indigo-500/10 relative group">
          <div className="flex items-center gap-2 px-4 py-2 border-b border-white/5 mb-3">
            <div className="w-3 h-3 rounded-full bg-rose-500/80" />
            <div className="w-3 h-3 rounded-full bg-amber-500/80" />
            <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
            <span className="text-xs text-zinc-500 ml-2 font-mono">growthos.app/dashboard</span>
          </div>
          <div className="relative rounded-xl overflow-hidden aspect-[16/9] border border-white/5">
            <Image
              src="/hero_mockup.jpg"
              alt="GrowthOS Dashboard Mockup"
              fill
              sizes="(max-width: 1200px) 100vw, 1200px"
              className="object-cover group-hover:scale-[1.01] transition-transform duration-500"
              priority
            />
          </div>
        </div>
      </section>

      {/* 7 AI Agents Grid */}
      <section className="px-6 py-24 border-t border-white/[0.08] bg-zinc-950/60 relative z-10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-xs font-semibold text-purple-300 mb-3">
              <Brain className="w-3.5 h-3.5" /> Parallel Groq Llama-3.3 Engine
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
              7 Specialized AI Agents Working in Parallel
            </h2>
            <p className="text-zinc-400 mt-2 max-w-xl mx-auto text-sm">
              Instead of generic LLM advice, GrowthOS deploys domain-specific agent personas designed around e-commerce unit economics.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {AGENTS.map((agent) => (
              <div
                key={agent.name}
                className={`p-6 rounded-2xl border bg-zinc-900/40 backdrop-blur-md hover:bg-zinc-900/80 transition-all duration-300 ${agent.glow} group hover:-translate-y-1`}
              >
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${agent.color} flex items-center justify-center mb-4 shadow-lg`}>
                  <agent.icon className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-1 group-hover:text-indigo-300 transition-colors">
                  {agent.name}
                </h3>
                <p className="text-xs text-zinc-400 leading-relaxed">{agent.role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Indian D2C Localisation Section */}
      <section className="px-6 py-20 border-t border-white/[0.08] bg-zinc-950/80 relative z-10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-semibold text-emerald-300 mb-3">
              🇮🇳 Tailored for Indian Founders & D2C Operators
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Built for <span className="gradient-text">India-Specific Metrics</span> & Ecosystems
            </h2>
            <p className="text-zinc-400 mt-2 max-w-xl mx-auto text-sm">
              Generic US tools ignore COD and RTO. GrowthOS tracks Cash on Delivery, Return to Origin, and Prepaid conversion as core growth drivers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-white/10 space-y-2">
              <div className="text-2xl font-bold text-emerald-400">₹ Lakhs Notation</div>
              <h4 className="text-sm font-semibold text-white">Native INR Financials</h4>
              <p className="text-xs text-zinc-400 leading-relaxed">
                All metrics, CAC, LTV, and action impacts formatted in ₹ and Indian lakhs (e.g. ₹18.4L/mo) with exact margin calculations.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-white/10 space-y-2">
              <div className="text-2xl font-bold text-amber-400">COD & RTO Engine</div>
              <h4 className="text-sm font-semibold text-white">Fulfillment & Return Risk</h4>
              <p className="text-xs text-zinc-400 leading-relaxed">
                Pre-calculates cash-in-transit risk, NDR shipping loss (₹240/order), and prepaid conversion upside for COD orders.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-white/10 space-y-2">
              <div className="text-2xl font-bold text-indigo-400">Indian Tech Integrations</div>
              <h4 className="text-sm font-semibold text-white">Razorpay, Shiprocket & Meesho</h4>
              <p className="text-xs text-zinc-400 leading-relaxed">
                Action cards prescribe specific Indian D2C tools like Razorpay Magic Checkout, Shiprocket NDR, Unicommerce & Gokwik.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-white/10 space-y-2">
              <div className="text-2xl font-bold text-purple-400">WhatsApp Retention</div>
              <h4 className="text-sm font-semibold text-white">WhatsApp-First Playbooks</h4>
              <p className="text-xs text-zinc-400 leading-relaxed">
                Replaces low-performing email sequences with high-conversion WhatsApp post-purchase flows (Interakt, AiSensy, Wati).
              </p>
            </div>
          </div>

          <div className="mt-12 text-center">
            <Link href="/demo">
              <Button variant="secondary" size="lg" className="gap-2 text-sm px-7 border-indigo-500/30 text-indigo-300 hover:bg-indigo-500/10">
                <Sparkles className="w-4 h-4 text-indigo-400" />
                Try Interactive Demo with Rang Studio (Ethnic Wear D2C) →
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Key Value Pillars */}
      <section className="px-6 py-24 max-w-6xl mx-auto border-t border-white/[0.08] relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-8 rounded-2xl bg-zinc-900/50 border border-white/10 hover:border-indigo-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center mb-5">
              <Zap className="w-6 h-6 text-indigo-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Sub-4s Parallel Diagnosis</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Run all 7 agents simultaneously via high-concurrency Groq inference. Identify your store&apos;s chief risk score in seconds.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-zinc-900/50 border border-white/10 hover:border-purple-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center mb-5">
              <TrendingUp className="w-6 h-6 text-purple-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Strategy Scenario Simulator</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Test strategic moves like 3PL migration, free shipping thresholds, or subscription offers before committing capital.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-zinc-900/50 border border-white/10 hover:border-emerald-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mb-5">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">CEO Brief & PDF Export</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Synthesize findings into executive briefing documents complete with a 30-day tactical roadmap ready for board presentation.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 bg-gradient-to-b from-indigo-950/40 to-zinc-950 border-t border-white/10 text-center relative z-10">
        <div className="max-w-3xl mx-auto space-y-6">
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            Ready to give your store institutional intelligence?
          </h2>
          <p className="text-zinc-400 text-base max-w-xl mx-auto">
            Get your store health score and 7-agent diagnostic report in under 60 seconds.
          </p>
          <div className="pt-2">
            <Link href="/register">
              <Button variant="gradient" size="lg" className="gap-2 text-base px-8 h-12">
                Launch Your Diagnosis Now
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-8 border-t border-white/5 text-center text-xs text-zinc-500 relative z-10">
        © {new Date().getFullYear()} GrowthOS Inc. All rights reserved.
      </footer>
    </div>
  );
}
