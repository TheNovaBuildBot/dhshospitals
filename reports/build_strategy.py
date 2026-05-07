"""Generate the DHS Hospital Content Strategy PDF (shareable for review)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable, ListFlowable, ListItem
)
from datetime import date

OUT = "reports/DHS-Content-Strategy.pdf"

PRIMARY = colors.HexColor("#0B5D8A")
PRIMARY_DARK = colors.HexColor("#084468")
ACCENT = colors.HexColor("#28A745")
GOLD = colors.HexColor("#9E7530")
LIGHT_BG = colors.HexColor("#F4F8FB")
LIGHT_BORDER = colors.HexColor("#E0E6EC")
TEXT = colors.HexColor("#1A1A2E")
MUTED = colors.HexColor("#666666")
ROW_ALT = colors.HexColor("#F8FAFC")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=22, leading=28, textColor=PRIMARY, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=14, leading=18, textColor=PRIMARY_DARK,
                    spaceBefore=14, spaceAfter=6)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=11, leading=14, textColor=PRIMARY_DARK,
                    spaceBefore=6, spaceAfter=4)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=10.5, leading=15, textColor=TEXT, spaceAfter=6,
                      alignment=TA_JUSTIFY)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=14, bulletIndent=2,
                        spaceAfter=4)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=9, leading=12, textColor=MUTED)
LABEL = ParagraphStyle("Label", parent=BODY, fontName="Helvetica-Bold",
                       fontSize=9, textColor=colors.white, alignment=TA_CENTER, leading=11)
COVER_TITLE = ParagraphStyle("CoverTitle", parent=H1, fontSize=30, leading=36,
                             alignment=TA_CENTER, textColor=PRIMARY)
COVER_SUB = ParagraphStyle("CoverSub", parent=BODY, fontSize=14, leading=20,
                           alignment=TA_CENTER, textColor=MUTED)


def hr(color=LIGHT_BORDER, height=0.6):
    class HR(Flowable):
        def wrap(self, *_): return 170 * mm, 6
        def draw(self):
            self.canv.setStrokeColor(color); self.canv.setLineWidth(height)
            self.canv.line(0, 2, 170 * mm, 2)
    return HR()


def callout(title, body, color=PRIMARY):
    bg = colors.HexColor("#EBF4FA")
    t = Table([
        [Paragraph(f"<b>{title}</b>", ParagraphStyle("c1", parent=BODY, textColor=color,
                                                     fontName="Helvetica-Bold", fontSize=11))],
        [Paragraph(body, BODY)],
    ], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.5, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def kv_table(rows, col1=44 * mm):
    data = [[Paragraph(f"<b>{k}</b>", BODY), Paragraph(v, BODY)] for k, v in rows]
    t = Table(data, colWidths=[col1, 170 * mm - col1])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ]))
    return t


# ---- header / footer ----
def draw_chrome(c, doc):
    c.saveState()
    c.setFillColor(PRIMARY); c.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, stroke=0, fill=1)
    c.setFillColor(MUTED); c.setFont("Helvetica", 8)
    c.drawString(20 * mm, 12 * mm, "DHS Multispecialty Hospital — Content Strategy")
    c.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    c.setStrokeColor(LIGHT_BORDER); c.setLineWidth(0.4)
    c.line(20 * mm, 16 * mm, A4[0] - 20 * mm, 16 * mm)
    c.restoreState()


# ---- content ----
story = []

# COVER
story.append(Spacer(1, 40 * mm))
story.append(Paragraph("Content Strategy", COVER_TITLE))
story.append(Spacer(1, 8 * mm))
story.append(Paragraph("DHS Multispecialty Hospital — www.dhshospitals.com", COVER_SUB))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph("A 6-month plan for SEO, AI Overviews, and local Ahmedabad reach",
                       ParagraphStyle("subt", parent=COVER_SUB, fontSize=12, textColor=PRIMARY)))
story.append(Spacer(1, 26 * mm))

cover_box = [[
    Paragraph(f"<b>Prepared for</b><br/>DHS Multispecialty Hospital", BODY),
    Paragraph(f"<b>Report date</b><br/>{date.today().strftime('%B %d, %Y')}", BODY),
    Paragraph("<b>Status</b><br/>For review &amp; approval", BODY),
]]
ct = Table(cover_box, colWidths=[55 * mm, 55 * mm, 55 * mm])
ct.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(ct)
story.append(PageBreak())

# 1. EXECUTIVE SUMMARY
story.append(Paragraph("1. Executive Summary", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "DHS Multispecialty Hospital has a strong technical SEO foundation and a "
    "high-value differentiator (VELYS robotic knee replacement). The next "
    "growth lever is <b>consistent, doctor-authored editorial content</b> that "
    "captures patient questions before they decide where to seek care.",
    BODY))
story.append(Paragraph(
    "This document proposes a <b>pillar-and-cluster</b> content model, three "
    "non-negotiable editorial rules, a 6-month editorial calendar, and a "
    "recommended first follow-up post. It is intended for review with the DHS "
    "leadership team before publication begins.",
    BODY))

story.append(Spacer(1, 6))
story.append(Paragraph("Why now", H3))
story.append(Paragraph(
    "Two industry shifts make this the right moment:",
    BODY))
story.append(Paragraph(
    "<b>1.</b> Google's AI Overviews and ChatGPT/Perplexity now answer many "
    "patient questions before any link is clicked. Ranking in the AI summary "
    "depends on having clean, question-shaped, doctor-authored content "
    "indexed against your hospital domain.",
    BULLET))
story.append(Paragraph(
    "<b>2.</b> Local search competition in Ahmedabad orthopedics is rising. "
    "The hospitals that publish first capture the long-tail informational "
    "queries (e.g. \"knee pain old age\", \"is robotic surgery safer\") "
    "that feed the booking funnel.",
    BULLET))
story.append(PageBreak())

# 2. CURRENT STATE
story.append(Paragraph("2. Where We Are Today", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Spacer(1, 4))

story.append(Paragraph("Already shipped (May 2026)", H3))
story.append(Paragraph("Service pillar pages — strong, well-linked, schema-rich:", BODY))
story.append(Paragraph("• <b>/velys-robotic-knee-replacement-ahmedabad/</b> — exact-match landing for the highest-intent VELYS query, with comparison table, recovery cards, both surgeon profiles, and 9 FAQs", BULLET))
story.append(Paragraph("• <b>/departments/robotic-surgery/</b> — robotic joint replacement hub with 10 question-shaped FAQs", BULLET))
story.append(Paragraph("• <b>/departments/joint-replacement/</b>, <b>/departments/orthopedics/</b>, all 21 clinical department pages", BULLET))
story.append(Paragraph("• <b>/doctors/doctor-hardik/</b>, <b>/doctors/doctor-swagat/</b> — Physician schema, expertise listed", BULLET))
story.append(Spacer(1, 4))
story.append(Paragraph("Blog posts — one launch announcement live:", BODY))
story.append(Paragraph("• <b>/blog/robotic-knee-replacement-ahmedabad/</b> — VELYS launch (May 2026)", BULLET))

story.append(Paragraph("The gap", H3))
story.append(Paragraph(
    "The site's content funnel is currently <b>bottom-heavy</b>. We have "
    "transactional pages (book appointment, doctor profiles, the launch "
    "announcement) but very little <b>top-of-funnel</b> content — articles "
    "that capture patients while they are still researching symptoms and "
    "haven't decided where to seek care.",
    BODY))
story.append(Paragraph(
    "Top-of-funnel content is what AI Overviews quote, what featured "
    "snippets pull from, and what eventually drives a measurable share of "
    "appointment bookings 60–90 days after publication.",
    BODY))
story.append(PageBreak())

# 3. STRATEGY
story.append(Paragraph("3. Strategy — Pillar &amp; Cluster", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "Each major service is a <b>pillar page</b>. Around it, we publish "
    "<b>cluster posts</b> that answer specific patient questions and link "
    "back to the pillar. This signals topical authority to Google and gives "
    "AI engines a connected knowledge graph to draw from.",
    BODY))

story.append(Paragraph("How a cluster looks", H3))
story.append(Paragraph(
    "Pillar — <b>VELYS Robotic Knee Replacement</b><br/>"
    "&nbsp;&nbsp;↳ Cluster post — Knee pain in older adults: when to consider replacement<br/>"
    "&nbsp;&nbsp;↳ Cluster post — Robotic vs traditional knee replacement<br/>"
    "&nbsp;&nbsp;↳ Cluster post — What to expect the day of your knee replacement<br/>"
    "&nbsp;&nbsp;↳ Cluster post — Knee replacement recovery: a week-by-week timeline<br/>"
    "&nbsp;&nbsp;↳ Cluster post — Cost &amp; insurance for robotic knee surgery in India",
    BODY))

story.append(Paragraph("Three editorial rules — non-negotiable", H2))
story.append(callout(
    "1. Question-shaped title",
    "Every post title is phrased as the patient's actual query. "
    "<i>\"How long does knee replacement recovery take?\"</i> beats "
    "<i>\"Knee Replacement Recovery\"</i> on AI Overviews and featured "
    "snippets, and reads more naturally when shared on WhatsApp. "
    "Use the same phrasing as the H1 — they should match."
))
story.append(Spacer(1, 6))
story.append(callout(
    "2. Doctor by-line + medical reviewer",
    "Healthcare content is YMYL (Your Money or Your Life) — Google's "
    "highest E-E-A-T bar. Every post must be authored by a credentialed "
    "DHS specialist and reviewed by a second physician. The author block "
    "is rendered with credentials (FRCS, MS, DNB, etc.) and links to the "
    "doctor's profile page so search engines can verify identity."
))
story.append(Spacer(1, 6))
story.append(callout(
    "3. One pillar, one location",
    "Each post links to at least one service pillar (VELYS, Joint "
    "Replacement, Cardiology, etc.) and mentions \"Ahmedabad\" plus a "
    "specific neighbourhood (Vastrapur, Gurukul, Drive-In, Satellite, "
    "Bodakdev, Memnagar, Thaltej, Sabarmati, Naranpura). Locality lives "
    "in body copy, breadcrumbs, and structured data — never in the "
    "title alone."
))
story.append(PageBreak())

# 4. SEARCH INTENT LADDER
story.append(Paragraph("4. Search Intent Ladder", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "Patients move through three search stages before booking. We need "
    "content at each stage:",
    BODY))

ladder = [
    ["Stage", "What the patient asks", "Page type", "Where DHS stands"],
    ["Top of funnel\n(information)",
     "\"Why does my knee hurt?\"\n\"What is a slipped disc?\"\n\"Heart attack warning signs\"",
     "Symptom &amp; condition\nguides written by\nspecialists",
     "Almost no coverage —\nbiggest opportunity"],
    ["Middle of funnel\n(comparison)",
     "\"Robotic vs traditional\nknee replacement\"\n\"Cost of bypass surgery\"",
     "Comparison guides,\ndecision aids,\nrecovery timelines",
     "Partial — VELYS landing\ncovers one comparison"],
    ["Bottom of funnel\n(transactional)",
     "\"Best knee surgeon\nAhmedabad\"\n\"Robotic surgery near me\"",
     "Pillar landing pages,\ndoctor profiles,\nbooking flow",
     "Strong — VELYS landing,\ndoctor pages, schema"],
]
data = []
for i, row in enumerate(ladder):
    if i == 0:
        data.append([Paragraph(f"<font color='white'><b>{c}</b></font>", BODY) for c in row])
    else:
        styles_per_col = [
            ParagraphStyle("s1", parent=BODY, fontName="Helvetica-Bold", textColor=PRIMARY_DARK),
            BODY, BODY,
            ParagraphStyle("s4", parent=BODY, textColor=GOLD if "opportunity" in row[3] else (ACCENT if "Strong" in row[3] else TEXT)),
        ]
        data.append([Paragraph(c.replace('\n', '<br/>'), styles_per_col[j]) for j, c in enumerate(row)])

t = Table(data, colWidths=[26 * mm, 56 * mm, 44 * mm, 44 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
]))
story.append(t)
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Implication:</b> The next 4–5 posts should focus on top-of-funnel and "
    "middle-of-funnel content. This balances the funnel and feeds qualified "
    "traffic into the existing transactional pages.",
    BODY))
story.append(PageBreak())

# 5. EDITORIAL CALENDAR
story.append(Paragraph("5. 6-Month Editorial Calendar", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "One post every 2–3 weeks. Each entry includes the funnel stage, the "
    "service pillar it supports, and the local Ahmedabad keyword angle.",
    BODY))
story.append(Spacer(1, 6))

calendar = [
    ["Month", "Post (working title)", "Funnel", "Pillar", "Author"],
    ["May 2026 ✅", "VELYS Robotic Knee Replacement now in Ahmedabad (launch)", "BoF", "VELYS", "Dr. Hardik Shah"],
    ["Jun 2026", "Knee Pain in Older Adults — When to Consider Replacement", "ToF", "Joint Replacement", "Dr. Hardik Shah"],
    ["Jun 2026", "Robotic vs Traditional Knee Replacement — What's Actually Different?", "MoF", "VELYS", "Dr. Hardik Shah"],
    ["Jul 2026", "What to Expect on the Day of Your Knee Replacement", "MoF", "Joint Replacement", "Dr. Swagat Shah"],
    ["Jul 2026", "Knee Replacement Recovery — A Week-by-Week Timeline", "MoF", "VELYS", "Dr. Swagat Shah"],
    ["Aug 2026", "ACL Tears in Athletes — Symptoms, Surgery &amp; Return to Sport", "ToF", "Sports Medicine", "Dr. Swagat Shah"],
    ["Aug 2026", "Trauma &amp; Accident Care — When to Come to DHS Emergency", "ToF", "Trauma + ICU", "Dr. Hardik Shah"],
    ["Sep 2026", "Cost &amp; Insurance for Robotic Knee Surgery in India", "MoF", "VELYS", "Hospital + Dr. Hardik"],
    ["Sep 2026", "Heart Attack Warning Signs You Shouldn't Ignore", "ToF", "Cardiology", "Dr. Sunil"],
    ["Oct 2026", "Spine Surgery — When Is Conservative Care No Longer Enough?", "ToF/MoF", "Spine Surgery", "Dr. Hardik Shah"],
    ["Oct 2026", "Cancer Surgery in Ahmedabad — Choosing a Surgical Oncologist", "MoF", "Cancer Care", "Dr. Dileep"],
    ["Nov 2026", "Hernia Repair — Laparoscopic vs Open Surgery Compared", "MoF", "General Surgery", "Dr. Chirag / Dr. Devshi"],
]
data = []
for i, row in enumerate(calendar):
    if i == 0:
        data.append([Paragraph(f"<font color='white'><b>{c}</b></font>", BODY) for c in row])
    else:
        funnel_color = {"ToF": colors.HexColor("#1976D2"),
                        "MoF": colors.HexColor("#9E7530"),
                        "BoF": ACCENT,
                        "ToF/MoF": colors.HexColor("#1976D2")}.get(row[2], TEXT)
        cells = [
            Paragraph(row[0], ParagraphStyle("c0", parent=BODY, fontName="Helvetica-Bold", fontSize=9.5)),
            Paragraph(row[1], BODY),
            Paragraph(f"<b>{row[2]}</b>", ParagraphStyle("c2", parent=BODY, textColor=funnel_color, fontSize=9.5)),
            Paragraph(row[3], ParagraphStyle("c3", parent=BODY, fontSize=9.5)),
            Paragraph(row[4], ParagraphStyle("c4", parent=BODY, fontSize=9.5, textColor=MUTED)),
        ]
        data.append(cells)

t = Table(data, colWidths=[20 * mm, 70 * mm, 16 * mm, 28 * mm, 36 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
]))
story.append(t)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Cadence:</b> 2 posts per month avg. Adjust to specialist availability — "
    "we strongly prefer doctor-authored content over a steady drumbeat of "
    "generic posts.",
    SMALL))
story.append(PageBreak())

# 6. NEXT POST DETAIL
story.append(Paragraph("6. Recommended Next Post (Post #2)", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "<b>Working title:</b> Knee Pain in Older Adults — When Should You Consider Knee Replacement?",
    ParagraphStyle("nx", parent=BODY, fontName="Helvetica-Bold", textColor=PRIMARY_DARK, fontSize=12)))
story.append(Spacer(1, 6))

story.append(kv_table([
    ("URL", "/blog/knee-pain-when-to-consider-knee-replacement-ahmedabad/"),
    ("Funnel", "Top of funnel (information)"),
    ("Target queries",
     "\"knee pain old age\", \"knee pain treatment Ahmedabad\", "
     "\"when do I need knee replacement\", \"is my knee pain serious\""),
    ("Pillar link", "/departments/joint-replacement/  →  /velys-robotic-knee-replacement-ahmedabad/"),
    ("Author", "Dr. Hardik M Shah (MS Orthopedic, FRCS Germany)"),
    ("Reviewer", "Dr. Swagat M Shah (FIAAS UK)"),
    ("Estimated length", "1,200–1,500 words"),
    ("Hero image", "Original photo of an outpatient knee assessment (recommended)"),
]))

story.append(Paragraph("Why this post specifically", H3))
story.append(Paragraph(
    "<b>1. Highest search volume.</b> &quot;Knee pain&quot;, &quot;knee pain "
    "in old age&quot;, and &quot;knee pain treatment&quot; are massive queries "
    "in India. Approaching the topic from a symptom-first angle captures "
    "patients <i>before</i> they have decided on surgery — much earlier in the "
    "decision journey than &quot;knee replacement&quot; alone.",
    BODY))
story.append(Paragraph(
    "<b>2. Funnels naturally to your existing pillars.</b> The post will "
    "conclude by pointing readers who have decided to consider surgery toward "
    "the Joint Replacement and VELYS landing pages.",
    BODY))
story.append(Paragraph(
    "<b>3. E-E-A-T friendly.</b> Symptoms and red-flag content is exactly "
    "what Google rewards when written by a credentialed surgeon — the "
    "&quot;experience&quot; and &quot;expertise&quot; signals are obvious.",
    BODY))
story.append(Paragraph(
    "<b>4. AI Overview bait.</b> Patients ask AI assistants &quot;is my knee "
    "pain serious?&quot; daily. Question-shaped subheadings (&quot;When is "
    "knee pain just ageing?&quot;, &quot;Red flags that mean you should see "
    "a specialist&quot;) are the exact paragraph shapes AI engines quote.",
    BODY))
story.append(Paragraph(
    "<b>5. Local SEO win.</b> &quot;Knee pain Ahmedabad&quot; has clear "
    "commercial intent and no dominant ranking page yet — a clean ranking "
    "opportunity in 60–90 days.",
    BODY))

story.append(Paragraph("Proposed outline", H3))
story.append(Paragraph(
    "1. Why knees ache as we age (the basic biomechanics)<br/>"
    "2. When is knee pain just ageing — and when is it something more?<br/>"
    "3. Red flags that mean you should see a specialist<br/>"
    "4. Conservative options doctors try first (medication, physio, injections)<br/>"
    "5. When is knee replacement the right answer?<br/>"
    "6. What changes with robotic-assisted knee replacement<br/>"
    "7. How DHS Multispecialty Hospital approaches knee care in Ahmedabad<br/>"
    "8. FAQs (5–6 question-shaped, AI-quotable)<br/>"
    "9. CTA — book a consultation",
    BODY))
story.append(PageBreak())

# 7. KPIS
story.append(Paragraph("7. Measurement &amp; KPIs", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "Content marketing pays off in 60–120 days, not 60–120 hours. We need "
    "the right metrics so leadership can judge progress without false signals.",
    BODY))

story.append(Paragraph("What we will measure (monthly)", H3))
story.append(Paragraph("• <b>Organic impressions</b> for target keyword clusters (Google Search Console)", BULLET))
story.append(Paragraph("• <b>Average position</b> for the 5–10 priority queries per pillar", BULLET))
story.append(Paragraph("• <b>Organic clicks</b> to each blog post and to its linked pillar page", BULLET))
story.append(Paragraph("• <b>Appointment-form conversions</b> attributed to blog landings (GA4 event)", BULLET))
story.append(Paragraph("• <b>AI Overview / featured-snippet wins</b> for tracked queries (manual quarterly check)", BULLET))
story.append(Paragraph("• <b>Backlinks earned</b> per post (Ahrefs / free SEO tools)", BULLET))

story.append(Paragraph("What we will not over-index on", H3))
story.append(Paragraph("• <b>Page views in week 1.</b> Most patient-research content takes 6–12 weeks to rank, then climbs steadily.", BULLET))
story.append(Paragraph("• <b>Bounce rate.</b> Informational content has higher bounce by design — readers got their answer.", BULLET))
story.append(Paragraph("• <b>Social shares.</b> Hospital content is rarely shared; that's not the channel.", BULLET))

story.append(Paragraph("Realistic targets (12-month horizon)", H3))
story.append(kv_table([
    ("Total organic sessions", "+150% over baseline"),
    ("Branded queries (e.g. \"DHS Hospital\")", "+50%"),
    ("Non-branded informational queries", "+300% (largest growth)"),
    ("Blog → appointment conversion rate", "1.5%–3% (industry benchmark for hospitals)"),
    ("AI Overviews citing DHS for ortho queries", "≥3 captured per quarter"),
    ("Top-3 ranking on at least 5 priority queries", "by month 9"),
]))
story.append(PageBreak())

# 8. ROLES & APPROVAL
story.append(Paragraph("8. Roles, Approval &amp; Channels", H1))
story.append(hr(PRIMARY, 1.2))

story.append(Paragraph("Roles (proposed)", H3))
story.append(kv_table([
    ("Author", "DHS specialist relevant to the topic (Dr. Hardik, Dr. Swagat, etc.)"),
    ("Medical reviewer", "A second DHS physician — verifies facts &amp; safety"),
    ("Editorial lead", "Hospital marketing / digital lead — owns the calendar &amp; SEO targets"),
    ("Publisher", "Web/dev (currently via Eleventy + GitHub) — handles publishing &amp; schema"),
    ("Final approval", "Medical Director (Dr. Hardik Shah) — sign-off before publish"),
]))

story.append(Paragraph("Process per post", H3))
story.append(Paragraph(
    "1. Editorial lead briefs the assigned doctor (target query, outline, length)<br/>"
    "2. Doctor delivers a draft (rough, voice-noted, or written — whatever is easiest)<br/>"
    "3. Editorial lead polishes for SEO + readability + house style<br/>"
    "4. Second physician reviews medically<br/>"
    "5. Medical Director gives final sign-off<br/>"
    "6. Publisher pushes to /blog/, requests indexing in Search Console, links from any related pillar pages<br/>"
    "7. Editorial lead schedules an Instagram + WhatsApp push within 48 hours of publish",
    BODY))

story.append(Paragraph("Distribution beyond search", H3))
story.append(Paragraph(
    "Publishing the post is half the job. Each post should also be:",
    BODY))
story.append(Paragraph("• <b>Promoted on Instagram</b> — short-form summary post, swipe carousel of key takeaways", BULLET))
story.append(Paragraph("• <b>Sent on WhatsApp</b> — to the hospital's existing patient list with a one-line teaser", BULLET))
story.append(Paragraph("• <b>Cross-linked from Dr. Hardik's external site</b> (drhardikshahortho.com) — bidirectional backlink boosts both domains", BULLET))
story.append(Paragraph("• <b>Submitted to Google Search Console</b> — &quot;Request indexing&quot; on day of publish for fastest pickup", BULLET))
story.append(Paragraph("• <b>Featured in the next month's email newsletter</b> if/when one launches", BULLET))

story.append(Spacer(1, 18))
story.append(hr(PRIMARY, 1))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Decision needed before we ship Post #2.</b> Please confirm:",
    BODY))
story.append(Paragraph("• Approval of the pillar-and-cluster strategy and the 6-month calendar", BULLET))
story.append(Paragraph("• Author + reviewer assignment for Post #2 (currently proposed: Dr. Hardik authors, Dr. Swagat reviews)", BULLET))
story.append(Paragraph("• Editorial cadence — 2 posts/month is the proposal; comfortable, sustainable", BULLET))
story.append(Paragraph("• Final approval workflow — single Medical Director sign-off vs. broader committee", BULLET))

story.append(Spacer(1, 14))
story.append(Paragraph(
    f"<i>This document was prepared {date.today().strftime('%B %d, %Y')} by Nova BuildBot for DHS Multispecialty Hospital. For questions or revisions, reach out via the same channel.</i>",
    SMALL))


doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=18 * mm, bottomMargin=20 * mm,
    title="DHS Hospital — Content Strategy",
    author="Nova BuildBot",
)
doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=draw_chrome)
print("Wrote", OUT)
