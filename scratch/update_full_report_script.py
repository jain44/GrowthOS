import os
import sys

# Append Section 7 and 8 into generate_fsd1_project_report.py
report_script_path = os.path.join(os.path.dirname(__file__), "generate_fsd1_project_report.py")

with open(report_script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Check if section 7 is already in the script
if "7. ANNEXURE (COMPLETE SOURCE CODE)" not in content:
    # Replace the save block to add section 7 and 8 before saving
    old_end = """    # Save outputs
    docx_sub_path = "submissions/GrowthOS_FSD1_Project_Report.docx"
    doc.save(docx_sub_path)
    print(f"Saved: {docx_sub_path}")
    
    docx_root_path = "GrowthOS_FSD1_Project_Report.docx"
    doc.save(docx_root_path)
    print(f"Saved: {docx_root_path}")"""

    new_end = """    doc.add_page_break()

    # =========================================================================
    # 7. ANNEXURE (COMPLETE SOURCE CODE & ARCHITECTURAL IMPLEMENTATION)
    # =========================================================================
    add_heading_16(doc, "7. Annexure (Complete Source Code & Architecture)")
    add_content_12(doc, "This annexure presents the core production source code modules powering the GrowthOS platform, covering relational entity schemas, NextAuth v5 JWT security, the resilient database hybrid fallback client, the 7-agent parallel diagnostic pipeline, Monte Carlo strategy simulation, CEO briefing generation, and live dashboard components.", bold_prefix="Implementation Overview: ")

    def read_code_snippet(rel_path):
        full_path = os.path.join(project_root, rel_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f_in:
                return f_in.read()
        return f"// File not found: {rel_path}"

    add_content_heading_14(doc, "7.1 Database Architecture & Schema Definition (prisma/schema.prisma)")
    add_content_12(doc, "Models User profiles, D2C store logistics (COD rate, RTO percentage), historical financial snapshots, diagnosis runs, what-if simulations, executive reports, and RAG knowledge chunks.", bold_prefix="Relational Schema: ")
    add_code_block(doc, read_code_snippet("prisma/schema.prisma"))

    add_content_heading_14(doc, "7.2 Authentication Provider & Session Security (src/auth.ts)")
    add_content_12(doc, "NextAuth.js v5 JWT configuration with credential validation, instant demo bypass (demo@growthos.ai), and same-origin redirect protection.", bold_prefix="Security Layer: ")
    add_code_block(doc, read_code_snippet("src/auth.ts"))

    add_content_heading_14(doc, "7.3 Resilient Database Hybrid Client & Fallback Store (src/lib/db.ts)")
    add_content_12(doc, "High-availability Prisma wrapper with automatic zero-latency fallback to the complete 'Rang Studio' D2C dataset during network disconnections.", bold_prefix="Resilience Client: ")
    add_code_block(doc, read_code_snippet("src/lib/db.ts"))

    add_content_heading_14(doc, "7.4 Multi-Agent AI Diagnostic & Synthesis Engine (src/lib/ai/analyze.ts)")
    add_content_12(doc, "Coordinates the 7 autonomous growth agents over Groq Llama-3.3-70B LPUs via Promise.allSettled() and synthesizes prioritized action playbooks.", bold_prefix="Multi-Agent Engine: ")
    add_code_block(doc, read_code_snippet("src/lib/ai/analyze.ts"))

    add_content_heading_14(doc, "7.5 Strategy Simulator & Financial Impact Forecaster (src/lib/ai/simulate.ts)")
    add_content_12(doc, "Predictive counterfactual modeling engine projecting short-term margin effects and 12-month annualized cash flow impacts.", bold_prefix="Simulation Engine: ")
    add_code_block(doc, read_code_snippet("src/lib/ai/simulate.ts"))

    add_content_heading_14(doc, "7.6 Executive CEO Briefing Generator (src/lib/ai/report.ts)")
    add_content_12(doc, "Autonomous synthesis engine compiling board-ready executive summaries, hazard warnings, and 30-day tactical roadmaps.", bold_prefix="Report Engine: ")
    add_code_block(doc, read_code_snippet("src/lib/ai/report.ts"))

    add_content_heading_14(doc, "7.7 Retrieval-Augmented Generation RAG Engine (src/lib/ai/rag.ts)")
    add_content_12(doc, "Domain benchmark retriever grounding LLM recommendations in verified Indian e-commerce logistics and unit economics data.", bold_prefix="RAG Engine: ")
    add_code_block(doc, read_code_snippet("src/lib/ai/rag.ts"))

    doc.add_page_break()

    # =========================================================================
    # 8. PRESENTATION SLIDES & EVALUATION ALIGNMENT
    # =========================================================================
    add_heading_16(doc, "8. Presentation Slide Deck & Evaluation Alignment")
    add_content_12(doc, "The capstone project is supported by an official 11-slide presentation deck titled 'GrowthOS_Presentation.pptx' and accompanying verbatim speaker notes, aligned directly with university FSD-1 evaluation rubrics.", bold_prefix="Presentation Summary: ")

    ppt_tbl = doc.add_table(rows=12, cols=3)
    ppt_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    ppt_hdrs = ["Slide #", "Slide Title", "Key Content & Technical Demonstration"]
    for c_i, h_t in enumerate(ppt_hdrs):
        cell = ppt_tbl.cell(0, c_i)
        set_cell_background(cell, "1B365D")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(h_t)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    s_data = [
        ("Slide 1", "Title Slide: GrowthOS", "Autonomous Multi-Agent Growth Operating System for Indian E-Commerce Brands."),
        ("Slide 2", "The Indian D2C Crisis", "High COD dependency (60-70%), crushing RTO freight loss (20-30%), and rising Meta CAC."),
        ("Slide 3", "Introducing GrowthOS", "Real-time AI board of directors diagnosing, simulating, and optimizing unit economics autonomously."),
        ("Slide 4", "Multi-Agent System Architecture", "Parallel execution of 7 specialized domain agents via Groq Cloud Llama-3.3-70B & RAG domain grounding."),
        ("Slide 5", "The 7 Autonomous Growth Agents", "Finance, Operations, Marketing, Technology, Unit Economics, Inventory/Supply Chain, and Retention/LTV."),
        ("Slide 6", "Full-Stack Technology Stack", "Next.js 16 (Turbopack), TypeScript 5, Tailwind CSS, PostgreSQL, Prisma ORM, NextAuth.js v5 JWT."),
        ("Slide 7", "Case Study: Rang Studio", "₹18.4L MRR ethnic wear brand; 62% COD, 22% RTO. Health score 62/100 analyzed across 6 months of historical data."),
        ("Slide 8", "What-If Strategy Simulator", "Counterfactual scenario testing: +₹1.4L/mo profit recovery by shifting 25% COD to prepaid with WhatsApp NDR."),
        ("Slide 9", "Autonomous CEO Briefing & PDF", "One-click institutional board reports with prioritized operational playbooks, software click paths, and copy templates."),
        ("Slide 10", "Business Impact & Metrics", "15% COD fee shifted 15% orders to prepaid; 6% RTO reduction; ₹1.8L monthly cash flow unlocked."),
        ("Slide 11", "Future Roadmap & Conclusion", "Automated Shopify/Shiprocket API webhooks, fine-tuned Indian commerce SLMs, and multi-tenant enterprise orchestration.")
    ]

    for r_i, (s_num, s_title, s_desc) in enumerate(s_data, start=1):
        c0 = ppt_tbl.cell(r_i, 0)
        c1 = ppt_tbl.cell(r_i, 1)
        c2 = ppt_tbl.cell(r_i, 2)
        c0.width = Inches(1.0)
        c1.width = Inches(2.2)
        c2.width = Inches(3.3)
        bg = "F9FAFB" if r_i % 2 == 1 else "FFFFFF"
        set_cell_background(c0, bg)
        set_cell_background(c1, bg)
        set_cell_background(c2, bg)
        for c, t, is_b in [(c0, s_num, True), (c1, s_title, True), (c2, s_desc, False)]:
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(t)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = is_b
            r.font.color.rgb = RGBColor(30, 30, 30)

    # Save outputs
    docx_sub_path = "submissions/GrowthOS_FSD1_Project_Report.docx"
    doc.save(docx_sub_path)
    print(f"Saved: {docx_sub_path}")
    
    docx_root_path = "GrowthOS_FSD1_Project_Report.docx"
    doc.save(docx_root_path)
    print(f"Saved: {docx_root_path}")"""

    content = content.replace(old_end, new_end)
    with open(report_script_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated generate_fsd1_project_report.py successfully!")
