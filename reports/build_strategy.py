"""DHS Content Strategy — strategy-focused 3-page deck for Dr. Hardik's review."""
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
INK        = colors.HexColor("#0F1B2D")
INK_SOFT   = colors.HexColor("#3F4856")
BRAND      = colors.HexColor("#0B5D8A")
BRAND_DARK = colors.HexColor("#073F60")
BRAND_TINT = colors.HexColor("#EAF2F7")
ACCENT_OK  = colors.HexColor("#2B8A3E")
ACCENT_WARN= colors.HexColor("#9C6B14")
ACCENT_RISK= colors.HexColor("#A2342B")
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
                    fontSize=11, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=9.5, leading=14, textColor=INK, spaceAfter=4, alignment=TA_LEFT)
BODY_SOFT = ParagraphStyle("BodySoft", parent=BODY, textColor=INK_SOFT)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.5, leading=12, textColor=MUTED)
TINY  = ParagraphStyle("Tiny", parent=BODY, fontSize=7.5, leading=10, textColor=MUTED)
KICKER = ParagraphStyle("Kicker", parent=BODY, fontName="Helvetica-Bold",
                        fontSize=8, leading=10, textColor=BRAND, alignment=TA_LEFT)


def hr(color=RULE, height=0.5, w=170):
    class HR(Flowable):
        def wrap(self, *_): return w * mm, 4
        def draw(self):
            self.canv.setStrokeColor(color); self.canv.setLineWidth(height)
            self.canv.line(0, 1, w * mm, 1)
    return HR()


def draw_chrome(c, doc):
    c.saveState()
    # Brand band at top
    c.setFillColor(BRAND); c.rect(0, A4[1] - 4 * mm, A4[0], 4 * mm, stroke=0, fill=1)
    # Header
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, A4[1] - 9 * mm,
                 "DHS Multispecialty Hospital — Content Strategy")
    c.drawRightString(A4[0] - 15 * mm, A4[1] - 9 * mm,
                      "NovaBuildBot · SEO Bot")
    # Footer
    c.setStrokeColor(RULE); c.setLineWidth(0.4)
    c.line(15 * mm, 12 * mm, A4[0] - 15 * mm, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, 8 * mm,
                 "Prepared by NovaBuildBot's SEO Bot · Nova AI Technologies LLP")
    c.drawRightString(A4[0] - 15 * mm, 8 * mm, f"Page {doc.page} of 3")
    c.restoreState()


story = []

# =============================================================================
# PAGE 1  ·  Cover, executive summary, why content marketing now
# =============================================================================

story.append(Spacer(1, 8 * mm))
story.append(Paragraph("FOR DHS MULTISPECIALTY HOSPITAL", KICKER))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph("Content Strategy", H_DISPLAY))
story.append(Paragraph(
    "A 6-month plan for SEO, AI Overviews, and local Ahmedabad reach",
    BODY_SOFT))

story.append(Spacer(1, 4 * mm))

# Visible byline — strategy report has an author
byline = Table([[
    Paragraph(
        "<b>Prepared by NovaBuildBot's SEO Bot</b> &nbsp;·&nbsp; "
        "<font color='#3F4856'>An AI agent from Nova AI Technologies LLP</font>"
        f" &nbsp;·&nbsp; <font color='#6B7280'>{date.today().strftime('%d %B %Y')}</font>",
        ParagraphStyle("byline", parent=BODY, fontSize=9.5, leading=12,
                       textColor=BRAND, fontName="Helvetica"))
]], colWidths=[170 * mm])
byline.setStyle(TableStyle([
    ("LINEABOVE", (0, 0), (-1, 0), 0.6, BRAND),
    ("LINEBELOW", (0, 0), (-1, 0), 0.6, BRAND),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(byline)

story.append(Spacer(1, 6 * mm))

# Executive summary
story.append(Paragraph("Executive summary", H1))
story.append(hr(RULE, 0.6, 170))
story.append(Spacer(1, 1 * mm))
story.append(Paragraph(
    "DHS Multispecialty Hospital has a strong technical SEO foundation and a "
    "high-value differentiator &mdash; VELYS robotic knee replacement in Ahmedabad. "
    "The next growth lever is <b>consistent, doctor-validated editorial content</b> "
    "that captures patient questions early in the search journey, well before the "
    "patient has decided where to seek care.",
    BODY))
story.append(Paragraph(
    "AI Overviews and ChatGPT now answer many medical questions before a single "
    "link is clicked. Ranking <i>inside</i> the AI summary, and earning the "
    "&quot;hospital near me&quot; click that follows, depends on having clean, "
    "question-shaped, doctor-validated content indexed against the DHS domain.",
    BODY))
story.append(Paragraph(
    "This document proposes a pillar-and-cluster model, three non-negotiable "
    "editorial rules, a 6-month weekly editorial calendar of 24 posts, and an "
    "honest set of targets &mdash; benchmarks, not promises &mdash; with the "
    "risks that could move them.",
    BODY))

story.append(Spacer(1, 6 * mm))

# Strategy at a glance
story.append(Paragraph("Strategy at a glance", H1))
story.append(hr(RULE, 0.6, 170))
story.append(Spacer(1, 1 * mm))

strategy = Table([
    [Paragraph("<b>Pillar &amp; cluster</b>", BODY),
     Paragraph(
         "Service pages are the pillars (VELYS landing, Joint Replacement, "
         "Cardiology, etc.). Blog posts are clusters that answer specific patient "
         "questions and link back to the relevant pillar. This signals topical "
         "authority to Google and creates the connected knowledge graph that AI "
         "engines draw from.",
         BODY)],
    [Paragraph("<b>Three editorial rules</b>", BODY),
     Paragraph(
         "<b>(1) Question-shaped title.</b> Every post title is phrased as the "
         "patient's actual query &mdash; <i>'How long does knee replacement "
         "recovery take?'</i> beats <i>'Knee Replacement Recovery'</i> for AI "
         "Overviews and featured snippets.<br/>"
         "<b>(2) Doctor by-line on every post.</b> Healthcare content is YMYL "
         "(Your Money or Your Life), Google's strictest E-E-A-T category. Every "
         "post is attributed to a credentialed DHS specialist.<br/>"
         "<b>(3) One pillar, one location.</b> Each post links to a service "
         "pillar and mentions Ahmedabad plus a specific neighbourhood &mdash; "
         "Vastrapur, Gurukul, Drive-In, Satellite, Bodakdev, Memnagar, Thaltej, "
         "Sabarmati, Naranpura.",
         BODY)],
    [Paragraph("<b>Funnel balance</b>", BODY),
     Paragraph(
         "DHS already has bottom-of-funnel pages &mdash; book appointment, doctor "
         "profiles, the VELYS landing. The next 24 posts focus on top- and "
         "middle-of-funnel queries (<i>'knee pain old age'</i>, <i>'robotic vs "
         "traditional knee replacement'</i>, <i>'knee replacement recovery "
         "timeline'</i>) that capture patients earlier and feed the existing "
         "booking pages.",
         BODY)],
], colWidths=[36 * mm, 134 * mm])
strategy.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SUBTLE),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 11),
    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(strategy)

story.append(PageBreak())

# =============================================================================
# PAGE 2  ·  6-month editorial calendar
# =============================================================================

story.append(Spacer(1, 6 * mm))
story.append(Paragraph("6-month editorial calendar", H_DISPLAY))
story.append(Paragraph(
    "One post per week, 24 posts, two tiers.",
    BODY_SOFT))
story.append(Spacer(1, 4 * mm))

# Tier explainer
tiers = Table([[
    Paragraph(
        "<b style='color:#2B8A3E'>Cornerstone</b> — long-form pillar guide, "
        "1,200&ndash;1,800 words. Anchors a service area and is built to rank "
        "and stay relevant for 12+ months.",
        BODY),
    Paragraph(
        "<b style='color:#9C6B14'>Mid-weight</b> — focused 600&ndash;900 word "
        "comparison, explainer, or condition primer. Same E-E-A-T standard, "
        "faster to read, captures specific queries.",
        BODY),
]], colWidths=[85 * mm, 85 * mm])
tiers.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EBF7EE")),
    ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FBF6E8")),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("LINEAFTER", (0, 0), (0, 0), 0.3, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(tiers)
story.append(Spacer(1, 4 * mm))

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
# PAGE 3  ·  Targets, risks, what we measure
# =============================================================================

story.append(Spacer(1, 6 * mm))
story.append(Paragraph("What to expect", H_DISPLAY))
story.append(Paragraph(
    "Targets, not promises. SEO outcomes depend on competitor activity, "
    "backlink earning, algorithm shifts, and the starting baseline.",
    BODY_SOFT))
story.append(Spacer(1, 4 * mm))

tier = Table([
    [Paragraph("<b>HIGH CONFIDENCE</b>",
               ParagraphStyle("th", parent=BODY, textColor=ACCENT_OK, fontName="Helvetica-Bold", fontSize=8.5)),
     Paragraph(
         "Branded queries (<i>'DHS Hospital'</i>) up meaningfully &middot; "
         "all 24 new posts indexed within 1&ndash;2 weeks &middot; "
         "top-10 ranking on long-tail queries (e.g. <i>'VELYS robotic knee replacement Ahmedabad'</i>, "
         "<i>'knee pain old age Gurukul'</i>) &middot; "
         "stronger snippet appearance for existing brand and orthopedic queries.",
         BODY)],
    [Paragraph("<b>STRETCH</b>",
               ParagraphStyle("ts", parent=BODY, textColor=ACCENT_WARN, fontName="Helvetica-Bold", fontSize=8.5)),
     Paragraph(
         "Material lift in total organic sessions over a 12-month horizon &middot; "
         "non-branded informational traffic growing fastest of any segment &middot; "
         "top-3 ranking on a handful of priority queries by month 9.",
         BODY)],
    [Paragraph("<b>VARIABLE</b>",
               ParagraphStyle("tv", parent=BODY, textColor=ACCENT_RISK, fontName="Helvetica-Bold", fontSize=8.5)),
     Paragraph(
         "Capturing AI Overview citations is genuinely volatile &mdash; Google's "
         "AI Overview model is updated frequently and quotes shift between runs. "
         "Specific timing varies; gains could land at month 5 or month 14.",
         BODY)],
], colWidths=[28 * mm, 142 * mm])
tier.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SUBTLE),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(tier)
story.append(Spacer(1, 5 * mm))

# Risks
story.append(Paragraph("What could derail this", H1))
story.append(hr(RULE, 0.6, 170))
story.append(Spacer(1, 1 * mm))
story.append(Paragraph(
    "<b>Backlink gap.</b> Content alone rarely beats well-linked competitors. "
    "The cross-link from Dr. Hardik Shah's site helps; broader PR mentions and "
    "healthcare-directory listings would compound the gains and are worth "
    "planning separately.",
    BODY))
story.append(Paragraph(
    "<b>Algorithm volatility.</b> Google's medical-content updates can move "
    "rankings overnight. The strategy hedges by spreading across many long-tail "
    "queries rather than betting everything on one head term.",
    BODY))
story.append(Paragraph(
    "<b>Local pack dominance.</b> The Maps 3-pack eats most clicks for "
    "<i>'hospital near me'</i> queries and is a separate Google Business Profile "
    "workstream &mdash; complementary to content, not replaced by it.",
    BODY))

story.append(Spacer(1, 4 * mm))

# Measurement — kept brief
story.append(Paragraph("How we will measure progress", H1))
story.append(hr(RULE, 0.6, 170))
story.append(Spacer(1, 1 * mm))
story.append(Paragraph(
    "Monthly reporting from Google Search Console and GA4 (already installed): "
    "impressions, clicks, click-through rate, average position, branded vs "
    "non-branded query split, organic sessions, top landing pages, engagement, "
    "indexed pages, and any AI Overview captures spotted manually. "
    "Each report ends with a recommendation for the next month.",
    BODY))

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
