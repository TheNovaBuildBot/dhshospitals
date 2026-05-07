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
story.append(Spacer(1, 8 * mm))
story.append(Paragraph(
    "Prepared by <b>NovaBuildBot's SEO Bot</b> &middot; an AI agent from <b>Nova AI Technologies LLP</b>",
    ParagraphStyle("byline", parent=COVER_SUB, fontSize=10, textColor=MUTED)))
story.append(Spacer(1, 18 * mm))

cover_box = [[
    Paragraph(f"<b>Prepared for</b><br/>DHS Multispecialty Hospital", BODY),
    Paragraph(f"<b>Prepared by</b><br/>NovaBuildBot — SEO Bot agent<br/><font size='8' color='#666666'>a product of Nova AI Technologies LLP</font>", BODY),
    Paragraph(f"<b>Report date</b><br/>{date.today().strftime('%B %d, %Y')}<br/><font size='8' color='#666666'>For review &amp; approval</font>", BODY),
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
story.append(Spacer(1, 14 * mm))

# About this document — moved to cover so attribution is the first thing seen
about_panel = Table([[
    Paragraph(
        f"<b>About this document.</b> &nbsp;Prepared by <b>NovaBuildBot's SEO Bot</b>, "
        f"an AI agent from <b>Nova AI Technologies LLP</b>. NovaBuildBot ships SEO and "
        f"content work end-to-end &mdash; research, drafting, schema, publishing, and "
        f"distribution &mdash; so partner organisations like DHS do not need to hire writers, "
        f"SEO consultants, or marketing leads. The only thing we ask of DHS is a "
        f"<b>10&ndash;15 minute medical-accuracy review</b> from one specialist before each "
        f"post goes live. The buck stops at medical accuracy &mdash; everything else is on us.",
        ParagraphStyle("aboutpanel", parent=BODY, fontSize=10, leading=15, textColor=TEXT))
]], colWidths=[170 * mm])
about_panel.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EBF4FA")),
    ("BOX", (0, 0), (-1, -1), 0.6, PRIMARY),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 12),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
]))
story.append(about_panel)

story.append(PageBreak())

# 1. EXECUTIVE SUMMARY
story.append(Paragraph("1. Executive Summary", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "DHS Multispecialty Hospital has a strong technical SEO foundation and a "
    "high-value differentiator (VELYS robotic knee replacement). The next "
    "growth lever is <b>consistent, doctor-validated editorial content</b> "
    "that captures patient questions before they decide where to seek care.",
    BODY))
story.append(Paragraph(
    "<b>NovaBuildBot is built for exactly this.</b> DHS does not need to "
    "hire a content writer, an SEO consultant, or a digital marketing lead. "
    "Our SEO Bot agent drafts, edits, optimises, publishes, and promotes every "
    "post end-to-end. The only thing we ask of DHS is a <b>10–15 minute "
    "medical-accuracy review</b> from one specialist on the relevant topic, "
    "before each post goes live. The buck stops at medical accuracy — "
    "everything else is on us.",
    BODY))
story.append(Paragraph(
    "This document proposes a <b>pillar-and-cluster</b> content model, three "
    "non-negotiable editorial rules, a 6-month weekly editorial calendar, and "
    "a recommended first follow-up post. It is intended for review with the "
    "DHS leadership team before publication begins.",
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
story.append(Paragraph("5. 6-Month Editorial Calendar — Weekly", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "<b>Cadence: one post per week, 24 posts in 6 months.</b> NovaBuildBot "
    "drafts each post end-to-end; the assigned DHS specialist reviews for "
    "medical accuracy in roughly 10–15 minutes before publish.",
    BODY))
story.append(Spacer(1, 6))
story.append(callout(
    "Two-tier post mix",
    "<b>Cornerstone (every other week, 12 posts)</b> — long-form 1,200–1,800 "
    "word patient guides that anchor a service pillar.<br/><br/>"
    "<b>Mid-weight (every other week, 12 posts)</b> — focused 600–900 word "
    "posts: comparison guides, plain-English explainers, condition primers, "
    "patient FAQs. Same E-E-A-T standard, faster to read, faster to review.",
    PRIMARY
))

calendar = [
    ["Week", "Post (working title)", "Tier", "Funnel", "Pillar", "Reviewer"],
    ["W1 ✅",     "VELYS Robotic Knee Replacement now in Ahmedabad (launch)", "Cornerstone", "BoF", "VELYS", "Dr. Hardik"],
    ["W2",        "Knee Pain in Older Adults — When to Consider Replacement", "Cornerstone", "ToF", "Joint Replacement", "Dr. Hardik"],
    ["W3",        "Robotic vs Traditional Knee Replacement — Quick Comparison", "Mid-weight", "MoF", "VELYS", "Dr. Hardik"],
    ["W4",        "What to Expect on the Day of Your Knee Replacement", "Cornerstone", "MoF", "Joint Replacement", "Dr. Swagat"],
    ["W5",        "5 Questions to Ask Your Knee Surgeon", "Mid-weight", "MoF", "Joint Replacement", "Dr. Hardik"],
    ["W6",        "Knee Replacement Recovery — A Week-by-Week Timeline", "Cornerstone", "MoF", "VELYS", "Dr. Swagat"],
    ["W7",        "ACL Tears in Athletes — Symptoms, Surgery &amp; Return to Sport", "Cornerstone", "ToF", "Sports Medicine", "Dr. Swagat"],
    ["W8",        "Why Indians Are Switching to Robotic Surgery — Patient FAQ", "Mid-weight", "MoF", "VELYS", "Dr. Hardik"],
    ["W9",        "Trauma &amp; Accident Care — When to Come to DHS Emergency", "Cornerstone", "ToF", "Trauma + ICU", "Dr. Hardik"],
    ["W10",       "Cost &amp; Insurance for Robotic Knee Surgery in India", "Mid-weight", "MoF", "VELYS", "Dr. Hardik"],
    ["W11",       "Heart Attack Warning Signs You Shouldn't Ignore", "Cornerstone", "ToF", "Cardiology", "Dr. Sunil"],
    ["W12",       "Hip Replacement vs Knee Replacement — Which Comes First?", "Mid-weight", "MoF", "Joint Replacement", "Dr. Hardik"],
    ["W13",       "Spine Surgery — When Is Conservative Care No Longer Enough?", "Cornerstone", "ToF/MoF", "Spine Surgery", "Dr. Hardik"],
    ["W14",       "Diabetes &amp; Joint Pain — The Hidden Connection", "Mid-weight", "ToF", "Internal Medicine", "Dr. Archit"],
    ["W15",       "Cancer Surgery in Ahmedabad — Choosing a Surgical Oncologist", "Cornerstone", "MoF", "Cancer Care", "Dr. Dileep"],
    ["W16",       "Reading Your Knee MRI Report — A Patient's Plain-English Guide", "Mid-weight", "ToF", "Radiology", "Dr. Yesha"],
    ["W17",       "Hernia Repair — Laparoscopic vs Open Surgery Compared", "Cornerstone", "MoF", "General Surgery", "Dr. Chirag"],
    ["W18",       "Stroke Care in Ahmedabad — The Golden Window", "Mid-weight", "ToF", "Neurosurgery", "Dr. Kushal"],
    ["W19",       "Kidney Stones — Symptoms, Treatment &amp; Prevention", "Cornerstone", "ToF", "Urology", "Dr. Darshil"],
    ["W20",       "Pre-op Anaesthesia — What Patients Worry About (And Shouldn't)", "Mid-weight", "MoF", "ICU", "Dr. Mansi"],
    ["W21",       "Gallbladder Stones — Surgery vs Watch-and-Wait", "Cornerstone", "MoF", "Gastroenterology", "Dr. Ruchir"],
    ["W22",       "Why Sleep Matters After Major Surgery", "Mid-weight", "ToF", "Internal Medicine", "Dr. Archit"],
    ["W23",       "Choosing Between OPD and Hospital Admission — A Quick Guide", "Mid-weight", "ToF", "Internal Medicine", "Dr. Archit"],
    ["W24",       "Patient Stories — A Year of Robotic Knee Replacement at DHS", "Cornerstone", "BoF", "VELYS", "Dr. Hardik"],
]
data = []
for i, row in enumerate(calendar):
    if i == 0:
        data.append([Paragraph(f"<font color='white'><b>{c}</b></font>", BODY) for c in row])
    else:
        funnel_color = {"ToF": colors.HexColor("#1976D2"),
                        "MoF": colors.HexColor("#9E7530"),
                        "BoF": ACCENT,
                        "ToF/MoF": colors.HexColor("#1976D2")}.get(row[3], TEXT)
        tier_color = ACCENT if row[2].startswith("Cornerstone") else colors.HexColor("#9E7530")
        cells = [
            Paragraph(row[0], ParagraphStyle("c0", parent=BODY, fontName="Helvetica-Bold", fontSize=9)),
            Paragraph(row[1], ParagraphStyle("c1", parent=BODY, fontSize=9, leading=12)),
            Paragraph(row[2], ParagraphStyle("c2t", parent=BODY, textColor=tier_color, fontSize=8.5, fontName="Helvetica-Bold")),
            Paragraph(f"<b>{row[3]}</b>", ParagraphStyle("c2", parent=BODY, textColor=funnel_color, fontSize=9)),
            Paragraph(row[4], ParagraphStyle("c3", parent=BODY, fontSize=9)),
            Paragraph(row[5], ParagraphStyle("c4", parent=BODY, fontSize=9, textColor=MUTED)),
        ]
        data.append(cells)

t = Table(data, colWidths=[14 * mm, 56 * mm, 22 * mm, 14 * mm, 28 * mm, 22 * mm], repeatRows=1)
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
    "<b>Reviewer column</b> = the DHS specialist NovaBuildBot will share the "
    "draft with for a ~10-minute medical accuracy check. Adjust the assignment "
    "freely; we will follow the doctor pool DHS provides.",
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
    ("Tier", "Cornerstone"),
    ("Funnel", "Top of funnel (information)"),
    ("Target queries",
     "\"knee pain old age\", \"knee pain treatment Ahmedabad\", "
     "\"when do I need knee replacement\", \"is my knee pain serious\""),
    ("Pillar link", "/departments/joint-replacement/  →  /velys-robotic-knee-replacement-ahmedabad/"),
    ("Drafted by", "<b>NovaBuildBot SEO Bot</b> — full draft in Dr. Hardik's voice, with schema, locality, citations"),
    ("Medical reviewer", "Dr. Hardik M Shah (MS Orthopedic, FRCS Germany) — ~15 min accuracy review"),
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
story.append(Paragraph("8. How This Works — DHS Reviews, NovaBuildBot Ships", H1))
story.append(hr(PRIMARY, 1.2))
story.append(Paragraph(
    "<b>DHS does not need to hire writers, SEO specialists, content "
    "strategists, or a digital marketing lead.</b> NovaBuildBot's SEO Bot "
    "agent does that work end-to-end. The only thing we ask of DHS is "
    "<b>medical accuracy review</b> — typically 10–15 minutes per post, "
    "from any one specialist on the relevant topic.",
    BODY))

story.append(Spacer(1, 4))
story.append(Paragraph("Who does what", H3))
story.append(kv_table([
    ("Topic research &amp; SEO", "<b>NovaBuildBot</b> — keyword analysis, search-intent mapping, competitor gap analysis"),
    ("Drafting", "<b>NovaBuildBot</b> — full draft in DHS doctors' voice, with locality, schema, citations"),
    ("Editorial polish", "<b>NovaBuildBot</b> — SEO, readability, AI-Overview formatting, house style"),
    ("Medical accuracy review", "<b>One DHS specialist</b> (~10–15 min) — verifies clinical facts &amp; safety. The buck stops here."),
    ("Final sign-off", "<b>Medical Director</b> (Dr. Hardik Shah) — short approval before publish"),
    ("Publishing", "<b>NovaBuildBot</b> — to /blog/, schema, sitemap, search console, internal links"),
    ("Distribution", "<b>NovaBuildBot</b> — Instagram + WhatsApp + cross-link to drhardikshahortho.com"),
    ("Performance reporting", "<b>NovaBuildBot</b> — monthly KPI report to DHS leadership"),
]))

story.append(Paragraph("Per-post process — total DHS time: ~15 min", H3))
story.append(Paragraph(
    "<b>1.</b> NovaBuildBot picks the next post from the agreed calendar, drafts it end-to-end<br/>"
    "<b>2.</b> Draft is shared with the assigned DHS specialist (the topic owner)<br/>"
    "<b>3.</b> Specialist reviews for medical accuracy — flags anything to correct (~10–15 min)<br/>"
    "<b>4.</b> Medical Director signs off (single tap/email)<br/>"
    "<b>5.</b> NovaBuildBot publishes, indexes, cross-links, schedules Instagram + WhatsApp",
    BODY))
story.append(Spacer(1, 6))
story.append(callout(
    "What this means in practice",
    "At the proposed cadence (1 post / week), DHS doctor review time totals "
    "roughly <b>1 hour per month</b>, distributed across whichever specialists "
    "are most appropriate per topic. There is no marketing team to hire, no "
    "SEO consultant to onboard, no editorial workflow tools to set up. "
    "NovaBuildBot brings all of that to the table as part of the engagement.",
    PRIMARY
))

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
story.append(Paragraph("• Approval of the pillar-and-cluster strategy and the weekly 6-month calendar (24 posts)", BULLET))
story.append(Paragraph("• A small <b>review pool</b> of 3–5 DHS specialists who can each take a 10–15 minute medical-accuracy review when their topic comes up", BULLET))
study_default = "single Medical Director sign-off (Dr. Hardik Shah) is the simplest workflow"
story.append(Paragraph(f"• Final sign-off path — {study_default} unless a broader committee is preferred", BULLET))
story.append(Paragraph("• Confirmation that NovaBuildBot may publish to /blog/, request indexing, and run Instagram + WhatsApp distribution on DHS's behalf", BULLET))

story.append(Spacer(1, 14))
story.append(Paragraph(
    f"<i>Document version: {date.today().strftime('%Y-%m-%d')}. "
    f"NovaBuildBot &middot; Nova AI Technologies LLP.</i>",
    SMALL))


doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=18 * mm, bottomMargin=20 * mm,
    title="DHS Hospital — Content Strategy",
    author="NovaBuildBot SEO Bot — Nova AI Technologies LLP",
    subject="DHS Multispecialty Hospital content strategy and 6-month editorial calendar",
    creator="NovaBuildBot — Nova AI Technologies LLP",
)
doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=draw_chrome)
print("Wrote", OUT)
