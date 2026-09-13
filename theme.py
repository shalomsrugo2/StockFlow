"""Visual layer for the Stockline portal.

Everything cosmetic lives here: palette tokens, font loading and the CSS that
re-skins Streamlit's default chrome into a minimal light portal with a dark
navigation rail.
"""

import streamlit as st

# --- tokens -----------------------------------------------------------------

INK = "#0B0D12"
INK_SOFT = "#454C59"
MUTED = "#868E9C"
LINE = "#E8EAEE"
CANVAS = "#F7F8F9"
PAPER = "#FFFFFF"

ACCENT = "#4F46E5"
ACCENT_SOFT = "#EEEDFD"
GOOD = "#0F7B55"
GOOD_SOFT = "#E7F4EE"
WARN = "#B4690E"
WARN_SOFT = "#FDF3E4"
BAD = "#B42318"
BAD_SOFT = "#FDEEEC"

RAIL = "#0C0E14"

DISPLAY = "'Space Grotesk', system-ui, sans-serif"
SANS = "'Instrument Sans', system-ui, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, monospace"

TONES = {
    "good": (GOOD, GOOD_SOFT),
    "warn": (WARN, WARN_SOFT),
    "bad": (BAD, BAD_SOFT),
    "accent": (ACCENT, ACCENT_SOFT),
    "neutral": (INK_SOFT, "#F1F2F4"),
}

_FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Space+Grotesk:wght@400;500;600;700"
    "&family=Instrument+Sans:wght@400;500;600;700"
    "&family=JetBrains+Mono:wght@400;500;600"
    "&display=swap"
)

_CSS = """
:root {
  --ink: %(ink)s; --ink-soft: %(ink_soft)s; --muted: %(muted)s;
  --line: %(line)s; --canvas: %(canvas)s; --paper: %(paper)s;
  --accent: %(accent)s; --rail: %(rail)s;
  --sans: %(sans)s; --display: %(display)s; --mono: %(mono)s;
}

html, body, [class*="st-"], .stApp, button, input, textarea, select {
  font-family: var(--sans);
  -webkit-font-smoothing: antialiased;
}
.stApp { background: var(--canvas); color: var(--ink); }

/* strip Streamlit chrome down to nothing */
header[data-testid="stHeader"] { background: transparent; height: 0; }
#MainMenu, footer, [data-testid="stStatusWidget"] { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stMainBlockContainer"] {
  padding: 28px 34px 72px; max-width: 1440px;
}
[data-testid="stVerticalBlock"] { gap: 14px; }

/* ---- dark navigation rail ---- */
section[data-testid="stSidebar"] { background: var(--rail); border-right: 0; width: 246px !important; }
section[data-testid="stSidebar"] > div { background: var(--rail); padding-top: 0; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-top: 4px; }
section[data-testid="stSidebar"] * { color: #E6E8EE; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.08); margin: 10px 0; }

[data-testid="stSidebarNav"] { padding: 2px 8px 4px; }
[data-testid="stSidebarNav"] ul { gap: 1px; }
[data-testid="stSidebarNav"] a {
  border-radius: 9px; padding: 7px 10px; margin: 0;
  transition: background .14s ease, color .14s ease;
}
[data-testid="stSidebarNav"] a span, [data-testid="stSidebarNav"] a p {
  font-family: var(--sans); font-size: 13px; font-weight: 500;
  color: #99A1B0; letter-spacing: -.005em;
}
[data-testid="stSidebarNav"] a:hover { background: rgba(255,255,255,.055); }
[data-testid="stSidebarNav"] a:hover span, [data-testid="stSidebarNav"] a:hover p { color: #FFF; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(255,255,255,.1); }
[data-testid="stSidebarNav"] a[aria-current="page"] span,
[data-testid="stSidebarNav"] a[aria-current="page"] p { color: #FFF; font-weight: 600; }
[data-testid="stSidebarNav"] svg { fill: #99A1B0; }
[data-testid="stSidebarNavSeparator"] { display: none; }

/* ---- typography ---- */
h1, h2, h3, h4 { font-family: var(--display); letter-spacing: -.03em; color: var(--ink); }
h1 { font-size: 27px !important; font-weight: 600 !important; margin: 0 !important; }
h2 { font-size: 17px !important; font-weight: 600 !important; }
h3 { font-size: 15px !important; font-weight: 600 !important; }
p, li, label, span { color: var(--ink-soft); }

/* ---- surfaces ---- */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { background: transparent; }
div[data-testid="stVerticalBlock"] > div > [data-testid="stVerticalBlockBorderWrapper"][style*="border"],
[data-testid="stExpander"] {
  background: var(--paper); border: 1px solid var(--line) !important;
  border-radius: 14px; box-shadow: 0 1px 2px rgba(11,13,18,.03);
}
[data-testid="stExpander"] summary { font-weight: 500; font-size: 13px; }

/* ---- controls ---- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  border-radius: 10px; border: 1px solid var(--line); background: var(--paper);
  color: var(--ink); font-size: 13px; font-weight: 500; padding: 6px 14px;
  box-shadow: none; transition: background .14s ease, border-color .14s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover { background: #F3F4F7; border-color: #DCDFE6; color: var(--ink); }
.stButton > button[kind="primary"], .stFormSubmitButton > button {
  background: var(--ink); border-color: var(--ink); color: #FFF;
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button:hover { background: #23262F; color: #FFF; }

[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] {
  border-radius: 10px !important; border-color: var(--line) !important;
  background: var(--paper) !important; font-size: 13px;
}
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {
  border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(79,70,229,.13);
}
[data-testid="stWidgetLabel"] p { font-size: 11px; font-weight: 500; color: var(--muted);
  text-transform: uppercase; letter-spacing: .09em; font-family: var(--mono); }

[data-baseweb="segmented-control"], [data-testid="stButtonGroup"] { gap: 2px; }
[data-testid="stButtonGroup"] button { font-size: 12.5px !important; border-radius: 8px !important; }

/* ---- tables ---- */
[data-testid="stDataFrame"] { border-radius: 12px; border: 1px solid var(--line); overflow: hidden; }
[data-testid="stDataFrame"] [role="columnheader"] {
  font-family: var(--mono) !important; font-size: 10.5px !important;
  letter-spacing: .07em; text-transform: uppercase; color: var(--muted) !important;
}
[data-testid="stDataFrame"] [role="gridcell"] { font-size: 12.5px; font-variant-numeric: tabular-nums; }

/* ---- charts / misc ---- */
[data-testid="stVegaLiteChart"] { font-family: var(--sans); }
[data-testid="stToast"] { border-radius: 12px; font-size: 13px; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #D6D9E0; border-radius: 8px; border: 3px solid transparent; background-clip: content-box; }
section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: rgba(255,255,255,.16); background-clip: content-box; }
a { color: var(--accent); text-decoration: none; }
a:hover { color: #3F37C9; text-decoration: underline; }
""" % {
    "ink": INK, "ink_soft": INK_SOFT, "muted": MUTED, "line": LINE,
    "canvas": CANVAS, "paper": PAPER, "accent": ACCENT, "rail": RAIL,
    "sans": SANS, "display": DISPLAY, "mono": MONO,
}


def apply_theme() -> None:
    """Load fonts + inject the portal stylesheet. Call once per rerun."""
    st.html(
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link rel="stylesheet" href="{_FONTS}">'
        f"<style>{_CSS}</style>"
    )


def style_chart(chart):
    """Apply the shared Altair look: no frame, mono tick labels, hairline axes."""
    return (
        chart.configure_view(stroke=None)
        .configure_axis(
            labelFont="JetBrains Mono",
            labelFontSize=10,
            labelColor=MUTED,
            titleFont="Instrument Sans",
            titleFontSize=10,
            titleColor=MUTED,
            domainColor=LINE,
            tickColor=LINE,
            gridColor="#F2F3F6",
            labelPadding=6,
        )
        .configure_legend(
            labelFont="Instrument Sans",
            labelColor=INK_SOFT,
            labelFontSize=11,
            titleColor=MUTED,
            titleFontSize=10,
            symbolType="square",
        )
    )
