# GrowthOS

**The AI Growth Operating System for E-Commerce Brands**

> Institutional-grade intelligence for D2C founders — 7 AI agents, 1 unified diagnosis.

---

## Stack

| Layer | Tech |
|---|---|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript (strict) |
| Styling | Tailwind CSS 3.4 |
| Database | PostgreSQL via Supabase + Prisma |
| Auth | Auth.js v5 (Credentials + Google OAuth) |
| AI | Groq SDK — Llama 3.3-70B |
| Charts | Recharts |
| PDF Export | jsPDF + html2canvas |
| Icons | Lucide React |

---

## Quick Start

### 1. Clone & Install
```bash
npm install
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Required values:
- `NEXTAUTH_SECRET` — generate with `openssl rand -base64 32`
- `DATABASE_URL` — Supabase pooler URL (port 6543)
- `DIRECT_URL` — Supabase direct URL (port 5432)
- `GROQ_API_KEY` — get from [console.groq.com](https://console.groq.com)
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — from Google Cloud Console

### 3. Set Up Database
```bash
npm run db:generate   # generate Prisma client
npm run db:push       # push schema to Supabase
```

### 4. Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Pages

| Route | Description |
|---|---|
| `/` | Marketing landing page |
| `/register` | Sign up (email or Google) |
| `/login` | Sign in |
| `/onboarding` | 3-step store setup wizard |
| `/dashboard` | KPI overview + health score |
| `/dashboard/diagnose` | 7-agent AI diagnosis |
| `/dashboard/simulate` | Strategy simulator |
| `/dashboard/report` | CEO executive report + PDF |
| `/dashboard/history` | Snapshot timeline + charts |
| `/dashboard/settings` | Account + store settings |

---

## AI Agents

| # | Agent | Focus |
|---|---|---|
| 1 | Finance | Margins, expenses, pricing |
| 2 | Marketing | CAC, ROAS, channel efficiency |
| 3 | Operations | Fulfillment, ops bottlenecks |
| 4 | Technology | Cart abandonment, CRO, tech stack |
| 5 | Unit Economics | AOV, contribution margin, LTV:CAC |
| 6 | Inventory & Supply Chain | Turnover, stockouts, 3PL |
| 7 | Retention & LTV | Repeat rate, subscription models |

All 7 run in parallel via `Promise.all()` — completing in under 4 seconds.

---

## Project Structure

```
src/
├── agents/              # 7 AI agent implementations
├── app/
│   ├── (auth)/          # Login + Register pages
│   ├── (dashboard)/     # Protected dashboard pages
│   ├── (marketing)/     # Landing page
│   └── api/             # API routes
├── components/
│   ├── layout/          # Navbar, Sidebar
│   └── ui/              # Button, Card, Input, Badge, Spinner
├── lib/
│   ├── ai/              # Groq client, orchestrator, simulator, report
│   ├── db.ts            # Prisma singleton
│   └── utils.ts         # Utility functions
├── auth.ts              # Auth.js config
└── middleware.ts        # Route protection
```
