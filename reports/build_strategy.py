"""DHS Content Strategy — tight 3-page deck."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable
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
                    fontSize=20, leading=24, textColor=PRIMARY, spaceAfter=4)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=12, leading=15, textColor=PRIMARY_DARK,
                    spaceBefore=8, spaceAfter=4)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=10, leading=13, textColor=PRIMARY_DARK,
                    spaceBefore=4, spaceAfter=2)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=9.5, leading=13, textColor=TEXT, spaceAfter=4,
                      alignment=TA_LEFT)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8, leading=11, textColor=MUTED)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=10, bulletIndent=0, spaceAfter=2)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.5, leading=10, textColor=MUTED)


def hr(color=LIGHT_BORDER, height=0.6, w=170):
    class HR(Flowable):
        def wrap(self, *_): return w * mm, 4
        def draw(self):
            self.canv.setStrokeColor(color); self.canv.setLineWidth(height)
            self.canv.line(0, 1, w * mm, 1)
    return HR()


# ---- chrome ----
def draw_chrome(c, doc):
    c.saveState()
    c.setFillColor(PRIMARY); c.rect(0, A4[1] - 6 * mm, A4[0], 6 * mm, stroke=0, fill=1)
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, 8 * mm,
                 f"DHS Multispecialty Hospital — Content Strategy · prepared by NovaBuildBot's SEO Bot · Nova AI Technologies LLP")
    c.drawRightString(A4[0] - 15 * mm, 8 * mm, f"Page {doc.page} of 3")
    c.restoreState()


story = []

# ============================================================
# PAGE 1 — Cover-style header + Attribution + Executive Summary
# ============================================================

# Title block
story.append(Spacer(1, 4 * mm))
story.append(Paragraph(
    "DHS Multispecialty Hospital",
    ParagraphStyle("brand", parent=BODY, fontSize=10, textColor=MUTED, leading=12,
                   fontName="Helvetica-Bold")))
story.append(Paragraph(
    "Content Strategy",
    ParagraphStyle("title", parent=H1, fontSize=26, leading=30, spaceAfter=4,
                   textColor=PRIMARY)))
story.append(Paragraph(
    "A 6-month plan for SEO, AI Overviews, and local Ahmedabad reach &nbsp;·&nbsp; "
    f"prepared {date.today().strftime('%B %d, %Y')}",
    ParagraphStyle("sub", parent=BODY, textColor=MUTED, fontSize=10, leading=13)))

story.append(Spacer(1, 5 * mm))

# Big visible attribution panel — on page 1
attribution = Table([[
    Paragraph(
        "<b>Prepared by NovaBuildBot's SEO Bot</b> "
        "<font color='#666666'>· an AI agent from Nova AI Technologies LLP</font>",
        ParagraphStyle("attribhead", parent=BODY, fontSize=12, leading=15,
                       textColor=PRIMARY, fontName="Helvetica-Bold"))
],[
    Paragraph(
        "NovaBuildBot ships SEO and content work end-to-end &mdash; research, drafting, "
        "schema, publishing, and distribution &mdash; so DHS does not need to hire writers, "
        "SEO consultants, or marketing leads. <b>The only thing we ask of DHS is a "
        "10&ndash;15 minute medical-accuracy review</b> from one specialist before each "
        "post goes live. The buck stops at medical accuracy &mdash; everything else is on us.",
        BODY)
]], colWidths=[170 * mm])
attribution.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EBF4FA")),
    ("BOX", (0, 0), (-1, -1), 0.8, PRIMARY),
    ("LINEABOVE", (0, 1), (-1, 1), 0.4, LIGHT_BORDER),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(attribution)
story.append(Spacer(1, 5 * mm))

# Executive summary
story.append(Paragraph("Executive summary", H1))
story.append(hr(PRIMARY, 1, 170))
story.append(Spacer(1, 2))
story.append(Paragraph(
    "DHS has a strong technical SEO foundation and a high-value differentiator "
    "(VELYS robotic knee replacement). The next growth lever is "
    "<b>consistent, doctor-validated editorial content</b> that captures patient "
    "questions before they decide where to seek care. AI Overviews and "
    "ChatGPT/Perplexity now answer many medical questions before a single link "
    "is clicked &mdash; ranking inside the AI summary depends on having clean, "
    "question-shaped, doctor-reviewed content indexed against your domain.",
    BODY))

# Strategy at a glance
story.append(Paragraph("Strategy at a glance", H2))

strategy = Table([
    [Paragraph("<b>Pillar-and-cluster</b>", BODY),
     Paragraph("Service pages are pillars (VELYS landing, Joint Replacement, etc.). Blog posts are clusters that answer specific patient questions and link back to the pillar — signalling topical authority.", BODY)],
    [Paragraph("<b>Three editorial rules</b>", BODY),
     Paragraph("(1) Question-shaped title that matches the patient's actual query. (2) Doctor by-line + medical reviewer for every post (YMYL E-E-A-T). (3) Each post links to one pillar and mentions Ahmedabad + a specific neighbourhood (Vastrapur, Gurukul, Drive-In, Satellite, Bodakdev, Memnagar, Thaltej, Sabarmati, Naranpura).", BODY)],
    [Paragraph("<b>Funnel balance</b>", BODY),
     Paragraph("DHS has bottom-of-funnel pages (book appointment, doctor profiles, VELYS landing) but very little top-of-funnel content. The next 24 posts focus on top- and middle-of-funnel queries that feed the existing booking pages.", BODY)],
], colWidths=[35 * mm, 135 * mm])
strategy.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BOX", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(strategy)
story.append(Spacer(1, 4 * mm))

# How it works — minimal on page 1
story.append(Paragraph("How it works", H2))
ops = Table([
    [Paragraph("<b>NovaBuildBot does</b>", ParagraphStyle("opsh", parent=BODY, textColor=PRIMARY, fontName="Helvetica-Bold", fontSize=10)),
     Paragraph("<b>DHS does</b>", ParagraphStyle("opsh2", parent=BODY, textColor=ACCENT, fontName="Helvetica-Bold", fontSize=10))],
    [Paragraph(
        "Topic research · keyword analysis · drafting in doctor's voice · "
        "SEO &amp; readability polish · schema · publishing to /blog/ · "
        "Search Console indexing · Instagram + WhatsApp distribution · "
        "monthly KPI report.", BODY),
     Paragraph(
        "<b>10&ndash;15 minute medical-accuracy review</b> per post by the "
        "topic-relevant specialist · final sign-off by Medical Director "
        "(single email/tap).<br/><br/>Total DHS doctor time at weekly "
        "cadence: <b>~1 hour per month</b>, distributed across the doctor pool.",
        BODY)],
], colWidths=[85 * mm, 85 * mm])
ops.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EBF4FA")),
    ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#EBF7EE")),
    ("BOX", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(ops)

story.append(PageBreak())

# ============================================================
# PAGE 2 — Editorial Calendar (24 posts, weekly)
# ============================================================
story.append(Paragraph("6-month editorial calendar — weekly", H1))
story.append(hr(PRIMARY, 1, 170))
story.append(Paragraph(
    "<b>Cadence: 1 post per week, 24 posts in 6 months.</b> "
    "<b>Cornerstone</b> = long-form pillar-anchoring guide (1,200&ndash;1,800 words). "
    "<b>Mid-weight</b> = focused 600&ndash;900 word comparison / explainer / FAQ. "
    "Reviewer column shows the proposed DHS specialist for the medical-accuracy check.",
    SMALL))
story.append(Spacer(1, 3))

calendar = [
    ["Wk", "Post (working title)", "Tier", "Funnel", "Pillar", "Reviewer"],
    ["1✅", "VELYS Robotic Knee Replacement now in Ahmedabad (launch)", "Cornerstone", "BoF", "VELYS", "Dr. Hardik"],
    ["2", "Knee Pain in Older Adults — When to Consider Replacement", "Cornerstone", "ToF", "Joint Replacement", "Dr. Hardik"],
    ["3", "Robotic vs Traditional Knee Replacement — Quick Comparison", "Mid-weight", "MoF", "VELYS", "Dr. Hardik"],
    ["4", "What to Expect on the Day of Your Knee Replacement", "Cornerstone", "MoF", "Joint Replacement", "Dr. Swagat"],
    ["5", "5 Questions to Ask Your Knee Surgeon", "Mid-weight", "MoF", "Joint Replacement", "Dr. Hardik"],
    ["6", "Knee Replacement Recovery — Week-by-Week Timeline", "Cornerstone", "MoF", "VELYS", "Dr. Swagat"],
    ["7", "ACL Tears in Athletes — Symptoms, Surgery, Return to Sport", "Cornerstone", "ToF", "Sports Medicine", "Dr. Swagat"],
    ["8", "Why Indians Are Switching to Robotic Surgery — Patient FAQ", "Mid-weight", "MoF", "VELYS", "Dr. Hardik"],
    ["9", "Trauma &amp; Accident Care — When to Come to DHS Emergency", "Cornerstone", "ToF", "Trauma + ICU", "Dr. Hardik"],
    ["10", "Cost &amp; Insurance for Robotic Knee Surgery in India", "Mid-weight", "MoF", "VELYS", "Dr. Hardik"],
    ["11", "Heart Attack Warning Signs You Shouldn't Ignore", "Cornerstone", "ToF", "Cardiology", "Dr. Sunil"],
    ["12", "Hip Replacement vs Knee Replacement — Which Comes First?", "Mid-weight", "MoF", "Joint Replacement", "Dr. Hardik"],
    ["13", "Spine Surgery — When Is Conservative Care No Longer Enough?", "Cornerstone", "ToF/MoF", "Spine Surgery", "Dr. Hardik"],
    ["14", "Diabetes &amp; Joint Pain — The Hidden Connection", "Mid-weight", "ToF", "Internal Medicine", "Dr. Archit"],
    ["15", "Cancer Surgery in Ahmedabad — Choosing a Surgical Oncologist", "Cornerstone", "MoF", "Cancer Care", "Dr. Dileep"],
    ["16", "Reading Your Knee MRI Report — Plain-English Patient Guide", "Mid-weight", "ToF", "Radiology", "Dr. Yesha"],
    ["17", "Hernia Repair — Laparoscopic vs Open Surgery Compared", "Cornerstone", "MoF", "General Surgery", "Dr. Chirag"],
    ["18", "Stroke Care in Ahmedabad — The Golden Window", "Mid-weight", "ToF", "Neurosurgery", "Dr. Kushal"],
    ["19", "Kidney Stones — Symptoms, Treatment &amp; Prevention", "Cornerstone", "ToF", "Urology", "Dr. Darshil"],
    ["20", "Pre-op Anaesthesia — What Patients Worry About (And Shouldn't)", "Mid-weight", "MoF", "ICU", "Dr. Mansi"],
    ["21", "Gallbladder Stones — Surgery vs Watch-and-Wait", "Cornerstone", "MoF", "Gastroenterology", "Dr. Ruchir"],
    ["22", "Why Sleep Matters After Major Surgery", "Mid-weight", "ToF", "Internal Medicine", "Dr. Archit"],
    ["23", "Choosing Between OPD and Hospital Admission — A Quick Guide", "Mid-weight", "ToF", "Internal Medicine", "Dr. Archit"],
    ["24", "Patient Stories — A Year of Robotic Knee Replacement at DHS", "Cornerstone", "BoF", "VELYS", "Dr. Hardik"],
]
data = []
for i, row in enumerate(calendar):
    if i == 0:
        data.append([Paragraph(f"<font color='white'><b>{c}</b></font>",
                               ParagraphStyle("hd", parent=BODY, fontSize=8.5)) for c in row])
    else:
        funnel_color = {"ToF": colors.HexColor("#1976D2"),
                        "MoF": GOLD, "BoF": ACCENT,
                        "ToF/MoF": colors.HexColor("#1976D2")}.get(row[3], TEXT)
        tier_color = ACCENT if row[2] == "Cornerstone" else GOLD
        cells = [
            Paragraph(row[0], ParagraphStyle("c0", parent=BODY, fontName="Helvetica-Bold", fontSize=8)),
            Paragraph(row[1], ParagraphStyle("c1", parent=BODY, fontSize=8, leading=10)),
            Paragraph(row[2], ParagraphStyle("c2", parent=BODY, fontSize=7.5, fontName="Helvetica-Bold", textColor=tier_color, leading=10)),
            Paragraph(f"<b>{row[3]}</b>", ParagraphStyle("c3", parent=BODY, fontSize=8, textColor=funnel_color)),
            Paragraph(row[4], ParagraphStyle("c4", parent=BODY, fontSize=8, leading=10)),
            Paragraph(row[5], ParagraphStyle("c5", parent=BODY, fontSize=8, textColor=MUTED)),
        ]
        data.append(cells)

t = Table(data, colWidths=[10 * mm, 70 * mm, 22 * mm, 14 * mm, 32 * mm, 22 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("BOX", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
]))
story.append(t)

story.append(PageBreak())

# ============================================================
# PAGE 3 — Targets, what could derail, decision needed
# ============================================================
story.append(Paragraph("Targets &amp; what to expect", H1))
story.append(hr(PRIMARY, 1, 170))
story.append(Paragraph(
    "Content marketing pays off in 60&ndash;120 days, not 60&ndash;120 hours. "
    "Targets below are <b>benchmarks, not promises</b> &mdash; SEO outcomes "
    "depend on competitor activity, backlink earning, algorithm shifts, and "
    "your starting baseline.",
    BODY))

# Confidence tiers
ct = Table([
    [Paragraph("<b>High confidence (75&ndash;90%)</b>", ParagraphStyle("hc", parent=BODY, textColor=ACCENT, fontName="Helvetica-Bold")),
     Paragraph(
         "&bull; Branded queries (<i>'DHS Hospital'</i>) +50% &nbsp; "
         "&bull; All 24 posts indexed within 1&ndash;2 weeks of publish &nbsp; "
         "&bull; Top-10 ranking on long-tail queries (e.g. <i>'VELYS robotic knee replacement Ahmedabad'</i>) &nbsp; "
         "&bull; Blog &rarr; appointment conversion 1.5&ndash;3% (industry benchmark)", BODY)],
    [Paragraph("<b>Stretch (40&ndash;60%)</b>", ParagraphStyle("st", parent=BODY, textColor=GOLD, fontName="Helvetica-Bold")),
     Paragraph(
         "&bull; +150% total organic sessions in 12 months &nbsp; "
         "&bull; +300% non-branded informational traffic &nbsp; "
         "&bull; Top-3 on 5 priority queries by month 9", BODY)],
    [Paragraph("<b>Variable (25&ndash;40%)</b>", ParagraphStyle("vr", parent=BODY, textColor=colors.HexColor("#C0392B"), fontName="Helvetica-Bold")),
     Paragraph(
         "&bull; AI Overviews citing DHS for orthopedic queries (model-dependent) &nbsp; "
         "&bull; Specific timeline (could land month 5 or month 14)", BODY)],
], colWidths=[34 * mm, 136 * mm])
ct.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BOX", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT_BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(ct)
story.append(Spacer(1, 4 * mm))

# What could derail
story.append(Paragraph("What could derail this", H2))
story.append(Paragraph(
    "<b>1. Backlink gap.</b> Content alone rarely beats well-linked competitors. "
    "Dr. Hardik's site cross-link helps; we should plan for PR mentions and "
    "healthcare-directory listings in parallel. &nbsp; "
    "<b>2. Algorithm volatility.</b> Google's medical-content updates (Aug 2024 "
    "etc.) can move rankings overnight. &nbsp; "
    "<b>3. Local-pack dominance.</b> Google Maps 3-pack eats most clicks for "
    "<i>'hospital near me'</i> queries; needs Google Business Profile work in "
    "parallel to content.",
    BODY))

# What we'll measure
story.append(Paragraph("What NovaBuildBot will report monthly", H2))
story.append(Paragraph(
    "Organic impressions and clicks per pillar &middot; average position on the "
    "10 priority queries &middot; appointment-form conversions attributed to "
    "blog landings &middot; AI Overview / featured-snippet wins &middot; "
    "backlinks earned &middot; recommendations for the next month.",
    BODY))

# Decision needed
story.append(Spacer(1, 3 * mm))
story.append(Paragraph("Decision needed before we ship Post #2", H2))
story.append(Paragraph("&bull; Approval of the strategy and the weekly 24-post calendar", BULLET))
story.append(Paragraph("&bull; A review pool of 3&ndash;5 specialists for medical-accuracy reviews (10&ndash;15 min each, on rotation)", BULLET))
story.append(Paragraph("&bull; Confirmation of single-tap final sign-off (Medical Director Dr. Hardik Shah, unless a committee is preferred)", BULLET))
story.append(Paragraph("&bull; Authorisation for NovaBuildBot to publish to /blog/, request indexing, and run Instagram + WhatsApp distribution on DHS's behalf", BULLET))
story.append(Paragraph("&bull; A 30-day baseline measurement window in GA4 + Search Console <i>before</i> we ship Post #2 — so the &quot;+150%&quot; claim has a real number behind it", BULLET))

story.append(Spacer(1, 4 * mm))
story.append(hr(PRIMARY, 0.6, 170))
story.append(Paragraph(
    f"Document version {date.today().strftime('%Y-%m-%d')} &middot; "
    "Prepared by NovaBuildBot's SEO Bot &middot; Nova AI Technologies LLP",
    TINY))


doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=14 * mm, bottomMargin=14 * mm,
    title="DHS Hospital — Content Strategy",
    author="NovaBuildBot SEO Bot — Nova AI Technologies LLP",
    subject="DHS Multispecialty Hospital content strategy and 6-month editorial calendar",
    creator="NovaBuildBot — Nova AI Technologies LLP",
)
doc.build(story, onFirstPage=draw_chrome, onLaterPages=draw_chrome)
print("Wrote", OUT)
