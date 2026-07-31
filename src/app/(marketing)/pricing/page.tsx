"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, Sparkles, Zap, Shield, HelpCircle, ArrowRight } from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Button } from "@/components/ui/button";

export default function PricingPage() {
  const [annual, setAnnual] = useState(true);

  const plans = [
    {
      name: "Starter",
      desc: "For early-stage Indian D2C stores finding product-market fit.",
      monthly: 999,
      annual: 799,
      popular: false,
      features: [
        "1 Connected Store",
        "5 AI Diagnoses per month",
        "7 Specialized Agents",
        "Indian D2C Benchmarks (₹)",
        "COD & RTO Risk Calculator",
        "Standard Email Support",
      ],
      cta: "Start 14-Day Free Trial",
      href: "/register?plan=starter",
    },
    {
      name: "Growth",
      desc: "For fast-scaling D2C brands optimizing unit economics & ROAS.",
      monthly: 2999,
      annual: 2399,
      popular: true,
      features: [
        "Unlimited AI Diagnoses",
        "Strategy Scenario Simulator",
        "CEO Executive PDF Exports",
        "Full RAG Empirical Knowledge Base",
        "Historical Snapshot Trend Deltas",
        "Shiprocket & Razorpay Integration",
        "Priority WhatsApp & Email Support",
      ],
      cta: "Start Growth Trial",
      href: "/register?plan=growth",
    },
    {
      name: "Agency / Multi-Store",
      desc: "For D2C agencies & holding groups managing multiple brands.",
      monthly: 7999,
      annual: 6399,
      popular: false,
      features: [
        "Up to 10 Connected Stores",
        "White-label PDF Reports with logo",
        "Cross-Store Benchmark Comparison",
        "Custom Prompt Fine-tuning Access",
        "Dedicated Account Specialist",
        "24/7 SLA Priority Support",
      ],
      cta: "Contact Agency Sales",
      href: "/register?plan=agency",
    },
  ];

  const faqs = [
    {
      q: "Is my store financial data secure?",
      a: "Yes. GrowthOS uses bank-grade AES-256 encryption. We never share your revenue or customer data with third parties or use private data to train open LLM models.",
    },
    {
      q: "How does GrowthOS calculate COD and RTO losses?",
      a: "Our metrics engine pre-computes freight loss, NDR recovery rate, and cash-in-transit risk specifically calibrated for Indian 3PLs (Shiprocket, Delhivery) and payment gateways (Razorpay, Cashfree).",
    },
    {
      q: "Can I export PDF reports for my co-founders or investors?",
      a: "Yes! Growth and Agency plan members can generate and download executive CEO briefing reports in one click.",
    },
    {
      q: "Can I cancel or switch plans at any time?",
      a: "Absolutely. No lock-in contracts. You can upgrade, downgrade, or cancel your subscription directly from your billing settings whenever you choose.",
    },
  ];

  return (
    <div className="min-h-screen bg-[#090A0F] text-zinc-100 flex flex-col font-sans overflow-x-hidden relative">
      {/* Background Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[450px] bg-gradient-to-tr from-indigo-600/15 via-purple-600/15 to-pink-600/10 rounded-full blur-[120px] pointer-events-none" />

      <Navbar />

      <main className="flex-1 max-w-6xl mx-auto px-6 pt-16 pb-24 relative z-10 w-full">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs font-semibold text-indigo-300 mb-4 shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            Transparent INR Pricing · Built for Indian Founders
          </div>
          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight mb-4">
            Invest in your store&apos;s <span className="gradient-text">Profitability</span>
          </h1>
          <p className="text-zinc-400 text-base max-w-xl mx-auto">
            Get 7 AI consultants for less than the cost of a single freelance audit. No hidden fees. Cancel anytime.
          </p>

          {/* Monthly / Annual Toggle */}
          <div className="flex items-center justify-center gap-3 mt-8">
            <span className={`text-xs font-semibold ${!annual ? "text-white" : "text-zinc-400"}`}>
              Monthly Billing
            </span>
            <button
              onClick={() => setAnnual(!annual)}
              className="w-14 h-8 rounded-full bg-zinc-800 border border-white/10 p-1 flex items-center transition-colors relative"
            >
              <div
                className={`w-6 h-6 rounded-full bg-indigo-500 transition-transform ${
                  annual ? "translate-x-6 bg-gradient-to-r from-indigo-500 to-purple-500" : "translate-x-0"
                }`}
              />
            </button>
            <div className="flex items-center gap-1.5">
              <span className={`text-xs font-semibold ${annual ? "text-white" : "text-zinc-400"}`}>
                Annual Billing
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Save 20%
              </span>
            </div>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {plans.map((plan) => {
            const price = annual ? plan.annual : plan.monthly;
            return (
              <div
                key={plan.name}
                className={`rounded-2xl p-7 flex flex-col justify-between relative transition-all duration-300 ${
                  plan.popular
                    ? "bg-zinc-900/90 border-2 border-indigo-500 shadow-2xl shadow-indigo-500/20 transform md:-translate-y-2"
                    : "bg-zinc-900/40 border border-white/10 hover:border-white/20"
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3.5 py-1 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-[11px] font-bold text-white uppercase tracking-wider shadow-md">
                    Most Popular
                  </div>
                )}

                <div>
                  <h3 className="text-xl font-bold text-white mb-2">{plan.name}</h3>
                  <p className="text-xs text-zinc-400 min-h-[36px] leading-relaxed mb-6">{plan.desc}</p>

                  <div className="flex items-baseline gap-1 mb-6">
                    <span className="text-4xl font-extrabold text-white">₹{price.toLocaleString("en-IN")}</span>
                    <span className="text-xs text-zinc-400">/month</span>
                    {annual && <span className="text-[10px] text-zinc-500 ml-1">billed annually</span>}
                  </div>

                  <div className="space-y-3 pt-6 border-t border-white/10 mb-8">
                    {plan.features.map((feat) => (
                      <div key={feat} className="flex items-start gap-2.5 text-xs text-zinc-300">
                        <Check className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                        <span>{feat}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <Link href={plan.href}>
                  <Button
                    variant={plan.popular ? "gradient" : "secondary"}
                    className="w-full h-11 text-xs font-semibold gap-2"
                  >
                    {plan.cta}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Button>
                </Link>
              </div>
            );
          })}
        </div>

        {/* Demo Mode Banner */}
        <div className="p-8 rounded-2xl bg-gradient-to-r from-indigo-950/60 via-purple-950/40 to-zinc-900 border border-indigo-500/30 flex flex-col md:flex-row items-center justify-between gap-6 mb-20">
          <div className="space-y-2 text-center md:text-left">
            <h3 className="text-lg font-bold text-white flex items-center justify-center md:justify-start gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Want to see GrowthOS in action first?
            </h3>
            <p className="text-xs text-zinc-400 max-w-xl">
              Explore our pitch-safe interactive demo loaded with <strong>Rang Studio</strong> (ethnic wear D2C brand doing ₹18.4L/mo with 62% COD). No sign up needed.
            </p>
          </div>
          <Link href="/demo">
            <Button variant="secondary" className="whitespace-nowrap gap-2 text-xs h-11 px-6">
              Launch Live Demo Mode →
            </Button>
          </Link>
        </div>

        {/* FAQs */}
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-white flex items-center justify-center gap-2">
              <HelpCircle className="w-5 h-5 text-indigo-400" />
              Frequently Asked Questions
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {faqs.map((faq) => (
              <div key={faq.q} className="p-6 rounded-xl bg-zinc-900/40 border border-white/10 space-y-2">
                <h4 className="text-sm font-semibold text-white">{faq.q}</h4>
                <p className="text-xs text-zinc-400 leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      <footer className="px-6 py-8 border-t border-white/5 text-center text-xs text-zinc-500 relative z-10">
        © {new Date().getFullYear()} GrowthOS Inc. All rights reserved. Built for Indian D2C Founders.
      </footer>
    </div>
  );
}
