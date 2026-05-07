"""DHS Content Strategy — polished 3-page deck.

Changes from prior version:
- Polished typography, refined colour palette, tighter spacing system
- Accurate reporting: only metrics NovaBuildBot can actually pull from GSC + GA4
- Workflow simplified to single POC (Dr. Hardik) with publish-then-feedback model
- Honest about what tooling would need to be added for conversion / backlink tracking
"""
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

# Refined palette
INK        = colors.HexColor("#0F1B2D")   # body / titles
INK_SOFT   = colors.HexColor("#3F4856")
BRAND      = colors.HexColor("#0B5D8A")   # primary
BRAND_DARK = colors.HexColor("#073F60")
BRAND_TINT = colors.HexColor("#EAF2F7")
ACCENT_OK  = colors.HexColor("#2B8A3E")   # confident green
ACCENT_WARN= colors.HexColor("#9C6B14")   # measured amber
ACCENT_RISK= colors.HexColor("#A2342B")   # honest red
RULE       = colors.HexColor("#D8DEE5")
SUBTLE     = colors.HexColor("#F6F8FA")
ROW_ALT    = colors.HexColor("#F9FBFC")
MUTED      = colors.HexColor("#6B7280")

styles = getSampleStyleSheet()

H_DISPLAY = ParagraphStyle("HDisplay", parent=styles["Heading1"], fontName="Helvetica-Bold",
                           fontSize=26, leading=30, textColor=BRAND, spaceAfter=4, alignment=TA_LEFT)
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=15, leading=18, textColor=BRAND_DARK, spaceAfter=4, spaceBefore=4)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=11, leading=14, textColor=INK,
                    spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=9.5, leading=14, textColor=INK, spaceAfter=4, alignment=TA_LEFT)
BODY_SOFT = ParagraphStyle("BodySoft", parent=BODY, textColor=INK_SOFT)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.5, leading=12, textColor=MUTED)
TINY  = ParagraphStyle("Tiny", parent=BODY, fontSize=7.5, leading=10, textColor=MUTED)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=12, bulletIndent=2, spaceAfter=2)
KICKER = ParagraphStyle("Kicker", parent=BODY, fontName="Helvetica-Bold",
                        fontSize=8, leading=10, textColor=BRAND,
                        alignment=TA_LEFT)


def hr(color=RULE, height=0.5, w=170):
    class HR(Flowable):
        def wrap(self, *_): return w * mm, 4
        def draw(self):
            self.canv.setStrokeColor(color); self.canv.setLineWidth(height)
            self.canv.line(0, 1, w * mm, 1)
    return HR()


# ---- header / footer chrome (every page) ----
def draw_chrome(c, doc):
    c.saveState()

    # Thin brand band at very top of every page
    c.setFillColor(BRAND); c.rect(0, A4[1] - 4 * mm, A4[0], 4 * mm, stroke=0, fill=1)

    # Top header text (left + right)
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, A4[1] - 9 * mm,
                 "DHS Multispecialty Hospital — Content Strategy")
    c.drawRightString(A4[0] - 15 * mm, A4[1] - 9 * mm,
                      "NovaBuildBot · SEO Bot")

    # Bottom footer
    c.setStrokeColor(RULE); c.setLineWidth(0.4)
    c.line(15 * mm, 12 * mm, A4[0] - 15 * mm, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, 8 * mm,
                 "Prepared by NovaBuildBot's SEO Bot · Nova AI Technologies LLP")
    c.drawRightString(A4[0] - 15 * mm, 8 * mm, f"Page {doc.page} of 3")
    c.restoreState()


story = []

# =============================================================================
# PAGE 1  ·  Cover, attribution, executive summary, strategy at a glance
# =============================================================================

# Generous top whitespace under the chrome header
story.append(Spacer(1, 8 * mm))

# Kicker (small label) + display title
story.append(Paragraph("FOR DHS MULTISPECIALTY HOSPITAL", KICKER))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph("Content Strategy", H_DISPLAY))
story.append(Paragraph(
    f"A 6-month plan for SEO, AI Overviews, and local Ahmedabad reach &nbsp;·&nbsp; "
    f"prepared {date.today().strftime('%d %B %Y')}",
    BODY_SOFT))

story.append(Spacer(1, 6 * mm))

# Attribution panel — refined design
attribution = Table([[
    Paragraph(
        "<b>Prepared by NovaBuildBot's SEO Bot</b><br/>"
        "<font size='8.5' color='#6B7280'>An AI agent from Nova AI Technologies LLP</font>",
        ParagraphStyle("ah", parent=BODY, fontSize=12, leading=15,
                       textColor=BRAND, fontName="Helvetica-Bold"))
],[
    Paragraph(
        "NovaBuildBot ships SEO and content work end-to-end &mdash; research, drafting, "
        "schema, publishing, and distribution. <b>DHS does not need to hire writers, "
        "SEO consultants, or marketing leads.</b> Our standing commitment is one thing: "
        "Dr. Hardik Shah, as Medical Director, signs off on the strategy and reviews each "
        "post after publish. We adjust based on his feedback. Everything else &mdash; "
        "research, drafting, optimisation, publishing, distribution, monthly reporting "
        "&mdash; is on us.",
        BODY)
]], colWidths=[170 * mm])
attribution.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), BRAND_TINT),
    ("LINEBELOW", (0, 0), (-1, 0), 0.4, RULE),
    ("BOX", (0, 0), (-1, -1), 0.6, BRAND),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (0, 0), 10),
    ("BOTTOMPADDING", (0, 0), (0, 0), 8),
    ("TOPPADDING", (0, 1), (0, 1), 8),
    ("BOTTOMPADDING", (0, 1), (0, 1), 12),
]))
story.append(attribution)

story.append(Spacer(1, 6 * mm))

# Executive summary
story.append(Paragraph("Executive summary", H1))
story.append(hr(RULE, 0.6, 170))
story.append(Spacer(1, 1 * mm))
story.append(Paragraph(
    "DHS has a strong technical SEO foundation and a high-value differentiator "
    "&mdash; VELYS robotic knee replacement. The next growth lever is "
    "<b>consistent, doctor-validated editorial content</b> that captures patient "
    "questions early in the search journey. AI Overviews and ChatGPT now answer "
    "many medical questions before any link is clicked; ranking inside the AI "
    "summary depends on having clean, question-shaped, doctor-reviewed content "
    "indexed against your domain.",
    BODY))

# Strategy at a glance — refined kv table
story.append(Paragraph("Strategy at a glance", H2))
strategy = Table([
    [Paragraph("<b>Pillar &amp; cluster</b>", BODY),
     Paragraph("Service pages are pillars (VELYS landing, Joint Replacement, etc.). Blog posts are clusters that answer specific patient questions and link back to the pillar &mdash; signalling topical authority to Google and AI engines.", BODY)],
    [Paragraph("<b>Three editorial rules</b>", BODY),
     Paragraph("(1) Question-shaped title that matches the patient's actual query. (2) Doctor by-line on every post (YMYL E-E-A-T standard). (3) Each post links to one pillar and mentions Ahmedabad + a specific neighbourhood (Vastrapur, Gurukul, Drive-In, Satellite, Bodakdev, Memnagar, Thaltej, Sabarmati, Naranpura).", BODY)],
    [Paragraph("<b>Funnel balance</b>", BODY),
     Paragraph("DHS already has bottom-of-funnel pages (book appointment, doctor profiles, VELYS landing). The next 24 posts focus on top- and middle-of-funnel queries that feed those pages from earlier in the patient's research.", BODY)],
], colWidths=[36 * mm, 134 * mm])
strategy.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SUBTLE),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 11),
    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(strategy)

story.append(PageBreak())

# =============================================================================
# PAGE 2  ·  Workflow + 24-post calendar
# =============================================================================

story.append(Spacer(1, 5 * mm))
story.append(Paragraph("How this works", H_DISPLAY))
story.append(Paragraph(
    "Single point of contact &mdash; Dr. Hardik Shah, Medical Director.",
    BODY_SOFT))
story.append(Spacer(1, 3 * mm))

# Workflow steps as a clean 4-step grid
workflow = Table([[
    Paragraph("<b>1. NovaBuildBot drafts</b><br/>"
              "<font size='8.5' color='#3F4856'>Research, draft, schema, optimise &mdash; in DHS doctors' voice</font>", BODY),
    Paragraph("<b>2. We publish</b><br/>"
              "<font size='8.5' color='#3F4856'>Live to /blog/ on the agreed weekly cadence</font>", BODY),
    Paragraph("<b>3. Dr. Hardik reviews</b><br/>"
              "<font size='8.5' color='#3F4856'>At his convenience &mdash; sends feedback by email or WhatsApp</font>", BODY),
    Paragraph("<b>4. We adjust</b><br/>"
              "<font size='8.5' color='#3F4856'>Edit the post and apply the feedback to future drafts</font>", BODY),
]], colWidths=[42.5 * mm, 42.5 * mm, 42.5 * mm, 42.5 * mm])
workflow.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), BRAND_TINT),
    ("BOX", (0, 0), (-1, -1), 0.4, BRAND),
    ("LINEAFTER", (0, 0), (-2, -1), 0.3, BRAND),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(workflow)
story.append(Spacer(1, 3 * mm))
story.append(Paragraph(
    "<b>Total Dr. Hardik time:</b> approximately 1 hour per month at weekly cadence "
    "&mdash; reviewing posts after publish and sending notes back. No pre-publish "
    "approvals to slow shipping; no review pool to coordinate.",
    SMALL))

story.append(Spacer(1, 3 * mm))

# Calendar
story.append(Paragraph("6-month editorial calendar", H1))
story.append(hr(RULE, 0.6, 170))
story.append(Paragraph(
    "<b>One post per week, 24 posts in 6 months.</b> "
    "<b>Cornerstone</b> = long-form pillar guide (1,200&ndash;1,800 words). "
    "<b>Mid-weight</b> = focused 600&ndash;900 word comparison or explainer. "
    "Same E-E-A-T standard for both.",
    SMALL))
story.append(Spacer(1, 2 * mm))

calendar = [
    ["Wk", "Post (working title)", "Tier", "Funnel", "Pillar"],
    ["1 ✓", "VELYS Robotic Knee Replacement now in Ahmedabad (launched)", "Cornerstone", "Booking", "VELYS"],
    ["2",  "Knee Pain in Older Adults — When to Consider Replacement", "Cornerstone", "Top",     "Joint Replacement"],
    ["3",  "Robotic vs Traditional Knee Replacement — Quick Comparison", "Mid-weight", "Middle",  "VELYS"],
    ["4",  "What to Expect on the Day of Your Knee Replacement",         "Cornerstone", "Middle",  "Joint Replacement"],
    ["5",  "5 Questions to Ask Your Knee Surgeon",                       "Mid-weight", "Middle",  "Joint Replacement"],
    ["6",  "Knee Replacement Recovery — Week-by-Week Timeline",          "Cornerstone", "Middle",  "VELYS"],
    ["7",  "ACL Tears in Athletes — Symptoms, Surgery, Return to Sport", "Cornerstone", "Top",     "Sports Medicine"],
    ["8",  "Why Indians Are Switching to Robotic Surgery — Patient FAQ", "Mid-weight", "Middle",  "VELYS"],
    ["9",  "Trauma &amp; Accident Care — When to Come to DHS Emergency", "Cornerstone", "Top",     "Trauma + ICU"],
    ["10", "Cost &amp; Insurance for Robotic Knee Surgery in India",     "Mid-weight", "Middle",  "VELYS"],
    ["11", "Heart Attack Warning Signs You Shouldn't Ignore",            "Cornerstone", "Top",     "Cardiology"],
    ["12", "Hip Replacement vs Knee Replacement — Which Comes First?",   "Mid-weight", "Middle",  "Joint Replacement"],
    ["13", "Spine Surgery — When Is Conservative Care No Longer Enough?","Cornerstone", "Top",     "Spine Surgery"],
    ["14", "Diabetes &amp; Joint Pain — The Hidden Connection",          "Mid-weight", "Top",     "Internal Medicine"],
    ["15", "Cancer Surgery in Ahmedabad — Choosing a Surgical Oncologist","Cornerstone","Middle", "Cancer Care"],
    ["16", "Reading Your Knee MRI Report — Plain-English Patient Guide", "Mid-weight", "Top",     "Radiology"],
    ["17", "Hernia Repair — Laparoscopic vs Open Surgery Compared",      "Cornerstone", "Middle",  "General Surgery"],
    ["18", "Stroke Care in Ahmedabad — The Golden Window",               "Mid-weight", "Top",     "Neurosurgery"],
    ["19", "Kidney Stones — Symptoms, Treatment &amp; Prevention",       "Cornerstone", "Top",     "Urology"],
    ["20", "Pre-op Anaesthesia — What Patients Worry About",             "Mid-weight", "Middle",  "ICU"],
    ["21", "Gallbladder Stones — Surgery vs Watch-and-Wait",             "Cornerstone", "Middle",  "Gastroenterology"],
    ["22", "Why Sleep Matters After Major Surgery",                      "Mid-weight", "Top",     "Internal Medicine"],
    ["23", "Choosing Between OPD and Hospital Admission",                "Mid-weight", "Top",     "Internal Medicine"],
    ["24", "A Year of Robotic Knee Replacement at DHS — Patient Stories","Cornerstone", "Booking", "VELYS"],
]

data = []
for i, row in enumerate(calendar):
    if i == 0:
        data.append([Paragraph(f"<font color='white'><b>{c}</b></font>",
                               ParagraphStyle("hd", parent=BODY, fontSize=8.5)) for c in row])
    else:
        funnel_color = {"Top": colors.HexColor("#1B4F8A"),
                        "Middle": ACCENT_WARN,
                        "Booking": ACCENT_OK}.get(row[3], INK)
        tier_color = ACCENT_OK if row[2] == "Cornerstone" else ACCENT_WARN
        cells = [
            Paragraph(row[0], ParagraphStyle("c0", parent=BODY, fontName="Helvetica-Bold", fontSize=8, textColor=BRAND_DARK)),
            Paragraph(row[1], ParagraphStyle("c1", parent=BODY, fontSize=8, leading=10)),
            Paragraph(row[2], ParagraphStyle("c2", parent=BODY, fontSize=7.5, fontName="Helvetica-Bold", textColor=tier_color, leading=10)),
            Paragraph(f"<b>{row[3]}</b>", ParagraphStyle("c3", parent=BODY, fontSize=8, textColor=funnel_color)),
            Paragraph(row[4], ParagraphStyle("c4", parent=BODY, fontSize=8.5, leading=10)),
        ]
        data.append(cells)

t = Table(data, colWidths=[10 * mm, 84 * mm, 22 * mm, 16 * mm, 38 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND),
    ("LINEBELOW", (0, 0), (-1, 0), 0.4, BRAND_DARK),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("LINEBELOW", (0, 1), (-1, -2), 0.2, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
]))
story.append(t)

story.append(PageBreak())

# =============================================================================
# PAGE 3  ·  Targets, what we'll report, what we won't pretend to track, decision
# =============================================================================

story.append(Spacer(1, 8 * mm))
story.append(Paragraph("Targets &amp; what we report", H_DISPLAY))
story.append(Paragraph(
    "Honest framing: targets, not promises. Reporting based only on tools "
    "DHS already has (Google Search Console + GA4).",
    BODY_SOFT))
story.append(Spacer(1, 4 * mm))

# Confidence tiers — refined visual
tier = Table([
    [Paragraph("<b>HIGH CONFIDENCE</b>", ParagraphStyle("th", parent=BODY, textColor=ACCENT_OK, fontName="Helvetica-Bold", fontSize=8.5)),
     Paragraph(
         "Branded queries (<i>'DHS Hospital'</i>) up meaningfully &middot; "
         "all 24 new posts indexed within 1&ndash;2 weeks &middot; "
         "top-10 ranking on long-tail queries (e.g. <i>'VELYS robotic knee replacement Ahmedabad'</i>, "
         "<i>'knee pain old age Gurukul'</i>) &middot; "
         "stronger snippet appearance for existing brand and ortho queries", BODY)],
    [Paragraph("<b>STRETCH</b>", ParagraphStyle("ts", parent=BODY, textColor=ACCENT_WARN, fontName="Helvetica-Bold", fontSize=8.5)),
     Paragraph(
         "Material lift in total organic sessions over a 12-month horizon &middot; "
         "non-branded informational traffic growing fastest of any segment &middot; "
         "top-3 ranking on a handful of priority queries by month 9", BODY)],
    [Paragraph("<b>VARIABLE</b>", ParagraphStyle("tv", parent=BODY, textColor=ACCENT_RISK, fontName="Helvetica-Bold", fontSize=8.5)),
     Paragraph(
         "Capturing AI Overview citations is genuinely volatile &mdash; "
         "Google's AI Overview model is updated frequently and quotes shift "
         "even between identical-content runs &middot; "
         "specific timing varies; could land month 5 or month 14", BODY)],
], colWidths=[28 * mm, 142 * mm])
tier.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SUBTLE),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(tier)
story.append(Spacer(1, 5 * mm))

# What we WILL report — and what we WON'T pretend to
report_table = Table([
    [Paragraph("<b>Monthly report covers</b>",
               ParagraphStyle("rh", parent=BODY, textColor=ACCENT_OK, fontName="Helvetica-Bold", fontSize=10)),
     Paragraph("<b>Not in scope without extra setup</b>",
               ParagraphStyle("rh2", parent=BODY, textColor=ACCENT_RISK, fontName="Helvetica-Bold", fontSize=10))],
    [Paragraph(
        "&bull; Impressions, clicks, CTR per priority query "
        "<i>(Google Search Console)</i><br/>"
        "&bull; Average position movements on tracked queries<br/>"
        "&bull; Branded vs non-branded query split<br/>"
        "&bull; Organic sessions, top landing pages, engagement "
        "<i>(GA4 — already installed)</i><br/>"
        "&bull; New pages indexed and any crawl errors<br/>"
        "&bull; AI Overview captures we spot manually<br/>"
        "&bull; Recommendations &amp; the next month's plan",
        BODY),
     Paragraph(
        "&bull; <b>Appointment-form conversion attribution</b> &mdash; requires "
        "GA4 conversion events on the appointment form, phone-click, and "
        "WhatsApp-click. We can wire this up in ~30 minutes if DHS wants it; "
        "until then, we report traffic, not bookings.<br/><br/>"
        "&bull; <b>Detailed backlink monitoring</b> &mdash; needs a paid tool "
        "(Ahrefs / Semrush, ~₹8&ndash;25k/month). GSC's link report is rudimentary. "
        "We can flag obvious mentions when we see them, but we will not claim "
        "comprehensive backlink data without the tooling.",
        BODY)],
], colWidths=[85 * mm, 85 * mm])
report_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EBF7EE")),
    ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FBEDEC")),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(report_table)

story.append(Spacer(1, 5 * mm))

# Risks
story.append(Paragraph("What could derail this", H2))
story.append(Paragraph(
    "<b>Backlink gap</b> &mdash; content alone rarely beats well-linked "
    "competitors. The cross-link from Dr. Hardik's site helps; broader PR "
    "and healthcare-directory listings are out of scope for this engagement "
    "but worth planning separately.&nbsp; "
    "<b>Algorithm volatility</b> &mdash; Google's medical-content updates can "
    "move rankings overnight; the strategy hedges by spreading across many "
    "long-tail queries rather than betting everything on one head term.&nbsp; "
    "<b>Local pack</b> &mdash; the Maps 3-pack eats most clicks for "
    "<i>'hospital near me'</i> queries and is a separate Google Business "
    "Profile workstream.",
    BODY))

story.append(Spacer(1, 4 * mm))

# Decision needed — single approval
decision = Table([[
    Paragraph(
        "<b>Single decision needed before we ship Post #2</b><br/><br/>"
        "Dr. Hardik Shah signs off on this strategy. That is the only approval "
        "required upfront. From there, we ship one post per week on the calendar "
        "above, Dr. Hardik reviews each post after publish at his convenience, "
        "and we apply his feedback to the post and to the queue.",
        ParagraphStyle("dn", parent=BODY, fontSize=10, leading=14, textColor=INK))
]], colWidths=[170 * mm])
decision.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), BRAND_TINT),
    ("BOX", (0, 0), (-1, -1), 0.6, BRAND),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(decision)

story.append(Spacer(1, 3 * mm))
story.append(Paragraph(
    f"Document version {date.today().strftime('%Y-%m-%d')} &middot; "
    "NovaBuildBot &middot; Nova AI Technologies LLP",
    TINY))


doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=14 * mm, bottomMargin=16 * mm,
    title="DHS Hospital — Content Strategy",
    author="NovaBuildBot SEO Bot — Nova AI Technologies LLP",
    subject="DHS Multispecialty Hospital content strategy and 6-month editorial calendar",
    creator="NovaBuildBot — Nova AI Technologies LLP",
)
doc.build(story, onFirstPage=draw_chrome, onLaterPages=draw_chrome)
print("Wrote", OUT)
