import streamlit as st

import data
from components import page_head, panel_head
from theme import INK, MONO, MUTED, SANS, TONES

log = data.activity()

page_head(
    "Records / Activity log",
    "Activity log",
    "An append-only trail of every change: who, what, when and from which channel. "
    "Retained for 24 months.",
)

c1, c2 = st.columns([0.6, 0.4], vertical_alignment="bottom")
channels = c1.multiselect("Channel", sorted(log.channel.unique()), placeholder="All channels")
actor = c2.selectbox("Actor", ["Everyone", *sorted(log.actor.unique())])

view = log.copy()
if channels:
    view = view[view.channel.isin(channels)]
if actor != "Everyone":
    view = view[view.actor == actor]

with st.container(border=True):
    panel_head("Event stream", f"{len(view)} events · newest first")
    items = []
    for i, (_, r) in enumerate(view.head(24).iterrows()):
        fg, bg = TONES.get(r.tone, TONES["neutral"])
        sep = "border-top:1px solid #F1F2F5;" if i else ""
        items.append(
            f"""<div style="{sep}display:flex;gap:14px;padding:12px 2px">
              <span style="width:7px;height:7px;border-radius:50%;background:{fg};flex:none;margin-top:6px"></span>
              <span style="flex:1;min-width:0">
                <span style="display:block;font:500 13px/1.45 {SANS};color:{INK}">{r.detail}</span>
                <span style="display:block;font:400 10.5px/1.5 {MONO};color:{MUTED};margin-top:3px">
                  {data.ago(r.at)} · {r.channel.lower()} · {r.actor}
                </span>
              </span>
              <span style="flex:none;padding:3px 8px;border-radius:6px;background:{bg};color:{fg};
                           font:600 10px/1.35 {MONO};letter-spacing:.05em;height:fit-content">
                {r.channel.upper()}
              </span>
            </div>"""
        )
    st.html(f'<div style="margin-top:-4px">{"".join(items)}</div>')
    st.download_button(
        "Export log (CSV)",
        view.to_csv(index=False).encode(),
        file_name="activity-log.csv",
        mime="text/csv",
    )

st.html(
    f'<div style="margin-top:6px;font:400 11.5px {SANS};color:{MUTED}">'
    f'Showing 24 of {len(view)} events. Older entries are available through the audit export.</div>'
)
