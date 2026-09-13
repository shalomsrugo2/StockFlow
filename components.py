"""Small HTML building blocks so every screen looks the same.

Streamlit has no primitive for a KPI strip or a status pill, so these render
tight inline-styled markup through ``st.html``.
"""

from __future__ import annotations

import streamlit as st

from theme import ACCENT, DISPLAY, INK, INK_SOFT, LINE, MONO, MUTED, PAPER, SANS, TONES


def page_head(crumb: str, title: str, subtitle: str) -> None:
    st.html(
        f"""
        <div style="margin:0 0 18px">
          <div style="font:400 10.5px/1 {MONO};letter-spacing:.1em;text-transform:uppercase;
                      color:{MUTED};margin-bottom:9px">{crumb}</div>
          <h1 style="margin:0;font:600 27px/1.1 {DISPLAY};letter-spacing:-.035em;color:{INK}">{title}</h1>
          <p style="margin:7px 0 0;font:400 13.5px/1.5 {SANS};color:{INK_SOFT};max-width:68ch">{subtitle}</p>
        </div>
        """
    )


def kpi_row(items: list[dict]) -> None:
    """items: [{label, value, delta, tone}] — tone drives the delta colour."""
    cells = []
    for i, it in enumerate(items):
        fg, _ = TONES.get(it.get("tone", "neutral"), TONES["neutral"])
        border = "" if i == 0 else f"border-left:1px solid {LINE};"
        cells.append(
            f"""<div style="{border}padding:16px 20px 18px;min-width:0">
              <div style="font:500 10.5px/1 {MONO};letter-spacing:.1em;text-transform:uppercase;
                          color:{MUTED};white-space:nowrap">{it['label']}</div>
              <div style="margin-top:12px;font:600 28px/1 {DISPLAY};letter-spacing:-.035em;
                          color:{INK};font-variant-numeric:tabular-nums">{it['value']}</div>
              <div style="margin-top:8px;font:500 11.5px/1 {SANS};color:{fg}">{it.get('delta','')}</div>
            </div>"""
        )
    st.html(
        f"""<div style="display:grid;grid-template-columns:repeat({len(items)},minmax(0,1fr));
                        background:{PAPER};border:1px solid {LINE};border-radius:14px;
                        box-shadow:0 1px 2px rgba(11,13,18,.03);overflow:hidden">
              {''.join(cells)}
            </div>"""
    )


def badge(text: str, tone: str = "neutral") -> str:
    fg, bg = TONES.get(tone, TONES["neutral"])
    return (
        f'<span style="display:inline-block;padding:3px 8px;border-radius:6px;background:{bg};'
        f'color:{fg};font:600 10.5px/1.35 {MONO};letter-spacing:.04em">{text}</span>'
    )


def panel_head(title: str, meta: str = "", action: str = "") -> None:
    right = (
        f'<span style="font:500 11.5px {SANS};color:{ACCENT}">{action}</span>'
        if action
        else f'<span style="font:400 10.5px {MONO};color:{MUTED}">{meta}</span>'
    )
    st.html(
        f"""<div style="display:flex;align-items:baseline;justify-content:space-between;gap:12px;
                        margin:-2px 0 10px">
              <h2 style="margin:0;font:600 15px/1.2 {DISPLAY};letter-spacing:-.02em;color:{INK}">{title}</h2>
              {right}
            </div>"""
    )


def rows(items: list[dict]) -> None:
    """Compact list rows: [{title, meta, value, value_tone, tail}]."""
    out = []
    for i, it in enumerate(items):
        fg, _ = TONES.get(it.get("value_tone", "neutral"), TONES["neutral"])
        sep = f"border-top:1px solid #F1F2F5;" if i else ""
        out.append(
            f"""<div style="{sep}display:flex;align-items:center;gap:14px;padding:11px 2px">
              <div style="flex:1;min-width:0">
                <div style="font:500 13px/1.35 {SANS};color:{INK};white-space:nowrap;
                            overflow:hidden;text-overflow:ellipsis">{it['title']}</div>
                <div style="font:400 10.5px/1.4 {MONO};color:{MUTED};margin-top:3px">{it.get('meta','')}</div>
              </div>
              <div style="text-align:right;white-space:nowrap">
                <div style="font:600 13px/1.2 {MONO};color:{fg};font-variant-numeric:tabular-nums">{it.get('value','')}</div>
                <div style="font:400 10.5px/1.4 {SANS};color:{MUTED};margin-top:3px">{it.get('tail','')}</div>
              </div>
            </div>"""
        )
    st.html(f'<div style="margin-top:-4px">{"".join(out)}</div>')


def meter(label: str, value: float, cap: float, tone: str = "accent", note: str = "") -> str:
    fg, bg = TONES.get(tone, TONES["accent"])
    pct = 0 if cap <= 0 else min(100, round(value / cap * 100))
    return f"""<div style="margin:0 0 12px">
      <div style="display:flex;justify-content:space-between;gap:10px;margin-bottom:6px">
        <span style="font:500 12.5px {SANS};color:{INK}">{label}</span>
        <span style="font:500 11px {MONO};color:{MUTED}">{note or f'{pct}%'}</span>
      </div>
      <div style="height:6px;border-radius:99px;background:{bg};overflow:hidden">
        <div style="width:{pct}%;height:100%;border-radius:99px;background:{fg}"></div>
      </div>
    </div>"""


def html_block(inner: str) -> None:
    st.html(inner)
