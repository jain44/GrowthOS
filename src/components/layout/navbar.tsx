import Link from "next/link";
import { Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-[#090A0F]/80 backdrop-blur-xl border-b border-white/[0.08] px-6 py-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <Zap className="w-4 h-4 text-white" />
          </div>
          <span className="text-base font-bold text-white tracking-tight">GrowthOS</span>
        </Link>

        <div className="flex items-center gap-6">
          <Link href="/pricing" className="text-xs font-semibold text-zinc-400 hover:text-white transition-colors">
            Pricing
          </Link>
          <Link href="/demo" className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition-colors flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
            Live Demo
          </Link>
          <div className="flex items-center gap-2.5 ml-2">
            <Link href="/login">
              <Button variant="ghost" size="sm" className="text-zinc-300 hover:text-white text-xs">
                Sign In
              </Button>
            </Link>
            <Link href="/register">
              <Button variant="primary" size="sm" className="text-xs">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
