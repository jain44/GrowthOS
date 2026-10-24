import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def read_file(rel_path):
    path = os.path.join(project_root, rel_path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return f"// File not found: {rel_path}"

md_content = f"""# GROWTHOS — FSD-1 PROJECT REPORT
## SECTION 7: ANNEXURE (COMPLETE SOURCE CODE & ARCHITECTURE IMPLEMENTATION)

| Metadata Attribute | Description |
|---|---|
| **Course & Project Track:** | Full Stack Development - 1 (FSD-1) Academic Capstone |
| **Project System Name:** | GrowthOS — Autonomous Multi-Agent Growth Operating System |
| **Industry Domain & Focus:** | Indian D2C E-Commerce Logistics, Unit Economics & Cashflow Optimization |
| **Repository URL:** | [https://github.com/jain44/GrowthOS.git](https://github.com/jain44/GrowthOS.git) (Branch: `main`) |

---

## 7.0 Architectural Overview & Module Organization

**Architecture Summary:** This annexure contains the complete production-grade source code for GrowthOS. The application is built using Next.js 16 (App Router & Turbopack), TypeScript 5, React 19, Tailwind CSS, PostgreSQL with Prisma ORM, NextAuth.js v5 (JWT authentication), and Groq Cloud Llama-3.3-70B-Versatile for autonomous multi-agent reasoning.

**Engineering Design:** The repository is engineered around a clean separation of concerns, dividing domain models, multi-agent AI heuristics, retrieval-augmented generation (RAG), authentication security, RESTful endpoints, and rich client-side dashboard visualizations into self-contained, typed modules.

### 7.0.1 Repository File Structure & Core Components

```text
GrowthOS/
├── prisma/
│   ├── schema.prisma                  # PostgreSQL database schema & relational entity models
│   └── seed.ts                        # Indian D2C 'Rang Studio' seed dataset & benchmarks
├── src/
│   ├── auth.ts                        # NextAuth.js v5 JWT auth provider & demo bypass
│   ├── agents/
│   │   └── shared.ts                  # Multi-agent contracts, schemas, and prioritization types
│   ├── lib/
│   │   ├── db.ts                      # Resilient Prisma database client & zero-latency fallback store
│   │   ├── utils.ts                   # Currency formatters (₹ Lakhs/Crores), health-score color helpers
│   │   └── ai/
│   │       ├── analyze.ts             # 7-Agent parallel diagnosis & executive synthesis engine
│   │       ├── simulate.ts            # Monte Carlo scenario simulator & financial forecasting
│   │       ├── report.ts              # Autonomous Executive CEO Briefing generator
│   │       └── rag.ts                 # Domain RAG knowledge retriever (Shiprocket, Razorpay benchmarks)
│   ├── app/
│   │   ├── (auth)/login/page.tsx      # Dark-mode enterprise login portal
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/page.tsx     # Executive Dashboard (KPI metrics, margin cards, health score)
│   │   │   ├── dashboard/diagnose/page.tsx # Live 7-Agent Diagnostic runner & interactive playbook
│   │   │   ├── dashboard/simulate/page.tsx # What-If Strategy Simulator interface
│   │   │   ├── dashboard/report/page.tsx   # Strategic Board Report view & PDF exporter
│   │   │   └── dashboard/settings/page.tsx # Store settings & Groq engine parameters
│   │   └── api/
│   │       ├── analyze/route.ts       # POST /api/analyze (Trigger 7-agent diagnosis)
│   │       ├── simulate/route.ts      # POST /api/simulate (Run what-if scenario)
│   │       ├── report/route.ts        # POST /api/report (Generate CEO briefing)
│   │       └── business/route.ts      # GET/POST /api/business (Store profile CRUD)
│   └── components/layout/
│       └── dashboard-sidebar.tsx      # Sidebar navigation & same-origin logout handler
├── package.json                       # Core dependencies & npm scripts
└── next.config.ts                     # Turbopack & Next.js production build configuration
```

---

## 7.1 Database Architecture & Schema Definition (`prisma/schema.prisma`)

**Schema Design:** The relational schema models the entire lifecycle of an Indian D2C enterprise. It includes native attributes for Indian payment logistics including `codRate` (Cash on Delivery percentage), `rtoRate` (Return to Origin percentage), and `prepaidPercentage`, alongside multi-agent diagnosis runs, scenario simulations, board reports, historical financial snapshots, and RAG knowledge chunks.

```prisma
{read_file("prisma/schema.prisma")}
```

---

## 7.2 Authentication & Session Security Engine (`src/auth.ts`)

**Security Implementation:** GrowthOS implements NextAuth.js v5 (beta) utilizing an encrypted JSON Web Token (JWT) session strategy. To ensure absolute reliability during academic evaluations and offline presentations, the authorization engine features instant demo credential verification for `demo@growthos.ai` and safe relative-origin redirect handling.

```typescript
{read_file("src/auth.ts")}
```

---

## 7.3 Resilient Database Client & Zero-Latency Hybrid Fallback Layer (`src/lib/db.ts`)

**High-Availability Wrapper:** To guard against cloud pooler timeouts, network disconnections, or database dormancy during live evaluations, `db.ts` provides a resilient hybrid execution wrapper. When the primary PostgreSQL instance is active, queries execute through Prisma. If an infrastructure interruption or connection timeout occurs, the client automatically and transparently falls back to an in-memory repository containing the complete 'Rang Studio' Indian D2C dataset with zero latency.

```typescript
{read_file("src/lib/db.ts")}
```

---

## 7.4 Multi-Agent AI Diagnostic Engine (`src/lib/ai/analyze.ts`)

**Multi-Agent Orchestration:** This module coordinates the 7 domain-specific AI agents. Each agent (Finance, Operations, Marketing, Technology, Unit Economics, Inventory, Retention) receives specialized system prompts, benchmark retrieval contexts via RAG, and store parameters. The agents execute concurrently via `Promise.allSettled()` over the Groq Llama-3.3-70B inference engine, culminating in an executive synthesis pass that outputs prioritized problems, insights, and copy-pasteable operational playbooks.

```typescript
{read_file("src/lib/ai/analyze.ts")}
```

---

## 7.5 Multi-Agent Interface Contracts & Data Transfer Objects (`src/agents/shared.ts`)

**Type Safety Contracts:** Provides strict TypeScript interfaces for agent context inputs, diagnosis outputs, action items, operational playbook click paths, and executive synthesis scores.

```typescript
{read_file("src/agents/shared.ts")}
```

---

## 7.6 Strategy Simulation & Counterfactual Financial Engine (`src/lib/ai/simulate.ts`)

**Predictive Simulation:** The Strategy Simulator enables founders to test counterfactual scenarios (e.g., 'What happens if we reduce COD fee and mandate WhatsApp verification?'). It projects short-term margin effects, 12-month annualized financial impacts, and risk-adjusted confidence scores.

```typescript
{read_file("src/lib/ai/simulate.ts")}
```

---

## 7.7 Executive CEO Report Generation Engine (`src/lib/ai/report.ts`)

**Autonomous Briefing Generator:** Synthesizes multi-agent diagnostic findings into an institutional board briefing. Generates executive summaries, identifies the single greatest operational hazard, highlights the highest-leverage growth unlock, and produces a phased 30-day tactical roadmap.

```typescript
{read_file("src/lib/ai/report.ts")}
```

---

## 7.8 Retrieval-Augmented Generation (RAG) Engine (`src/lib/ai/rag.ts`)

**Domain Grounding:** Retrieves verified Indian e-commerce industry benchmarks from curated logistics reports (Shiprocket 2024), checkout studies (Razorpay Magic Checkout), and fashion margin playbooks (Bain & Co) to ground all LLM recommendations in real market realities.

```typescript
{read_file("src/lib/ai/rag.ts")}
```

---

## 7.9 Backend REST API Endpoints & Server Action Handlers

### 7.9.1 Diagnosis API Handler (`src/app/api/analyze/route.ts`)

```typescript
{read_file("src/app/api/analyze/route.ts")}
```

### 7.9.2 Strategy Simulation API Handler (`src/app/api/simulate/route.ts`)

```typescript
{read_file("src/app/api/simulate/route.ts")}
```

### 7.9.3 Executive Report API Handler (`src/app/api/report/route.ts`)

```typescript
{read_file("src/app/api/report/route.ts")}
```

### 7.9.4 Store Business Profile & Snapshot API Handler (`src/app/api/business/route.ts`)

```typescript
{read_file("src/app/api/business/route.ts")}
```

---

## 7.10 Frontend Executive Interface & Real-Time Visualization

### 7.10.1 Executive Dashboard Page (`src/app/(dashboard)/dashboard/page.tsx`)

```tsx
{read_file("src/app/(dashboard)/dashboard/page.tsx")}
```

### 7.10.2 Live 7-Agent Diagnostic Runner (`src/app/(dashboard)/dashboard/diagnose/page.tsx`)

```tsx
{read_file("src/app/(dashboard)/dashboard/diagnose/page.tsx")}
```

### 7.10.3 Sidebar Navigation & Same-Origin Logout Handler (`src/components/layout/dashboard-sidebar.tsx`)

```tsx
{read_file("src/components/layout/dashboard-sidebar.tsx")}
```

---

## 8.0 Presentation Slide Deck & Demonstration Alignment

**Presentation Context:** The academic PowerPoint presentation accompanying this technical report is titled `GrowthOS_Presentation.pptx`. It comprises 11 structured slides aligned with university evaluation criteria, presenting the live demonstration narrative, multi-agent architecture diagrams, unit economics case study ('Rang Studio'), and full stack implementation highlights.

| Slide # | Slide Title | Technical & Architectural Content Demonstrated |
|---|---|---|
| **Slide 1** | Title Slide: GrowthOS | Autonomous Multi-Agent Growth Operating System for Indian E-Commerce Brands. |
| **Slide 2** | The Indian D2C Crisis | High COD dependency (60-70%), crushing RTO freight loss (20-30%), rising Meta CAC, and low contribution margins. |
| **Slide 3** | Introducing GrowthOS | Real-time AI board of directors diagnosing, simulating, and optimizing unit economics autonomously. |
| **Slide 4** | Multi-Agent System Architecture | Parallel execution of 7 specialized domain agents via Groq Cloud Llama-3.3-70B & RAG domain grounding. |
| **Slide 5** | The 7 Autonomous Growth Agents | Finance, Operations, Marketing, Technology, Unit Economics, Inventory/Supply Chain, and Retention/LTV. |
| **Slide 6** | Full-Stack Technology Stack | Next.js 16 (Turbopack), TypeScript 5, Tailwind CSS, PostgreSQL, Prisma ORM, NextAuth.js v5 JWT. |
| **Slide 7** | Case Study: Rang Studio | ₹18.4L MRR ethnic wear brand; 62% COD, 22% RTO. Health score 62/100 analyzed across 6 months of historical data. |
| **Slide 8** | What-If Strategy Simulator | Counterfactual scenario testing: +₹1.4L/mo profit recovery by shifting 25% COD to prepaid with WhatsApp NDR. |
| **Slide 9** | Autonomous CEO Briefing & PDF | One-click institutional board reports with prioritized operational playbooks, software click paths, and copy templates. |
| **Slide 10** | Business Impact & Metrics | 15% COD fee shifted 15% orders to prepaid; 6% RTO reduction; ₹1.8L monthly cash flow unlocked. |
| **Slide 11** | Future Roadmap & Conclusion | Automated Shopify/Shiprocket API webhooks, fine-tuned Indian commerce SLMs, and multi-tenant enterprise orchestration. |
"""

out_sub = os.path.join(project_root, "submissions", "FSD1_ANNEXURE_SOURCE_CODE.md")
out_root = os.path.join(project_root, "FSD1_ANNEXURE_SOURCE_CODE.md")

with open(out_sub, "w", encoding="utf-8") as f:
    f.write(md_content)

with open(out_root, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"SUCCESS: Generated Markdown Annexure Document:\n- {out_sub}\n- {out_root}")
