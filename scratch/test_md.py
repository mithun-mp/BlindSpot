import markdown_it
import textwrap

md = markdown_it.MarkdownIt()

pos = 1
tok = "The"
occ_tag = ""
badge_html = ""
pct = 3.0
bar_color = "#38bdf8"
delta_html = ""
score_str = " 0.0%"
row_bg = "background:transparent;"

raw_html = f"""<div style="display:flex; justify-content:space-between; align-items:center; font-family:monospace; font-size:0.8rem; margin:3px 0; padding:2px 4px; border-radius:4px; {row_bg}"><span style="color:#64748b; font-size:0.75rem; width:28px;">#{pos}</span><span style="color:#f1f5f9; width:130px; overflow:hidden; text-overflow:ellipsis; font-weight:600;">{tok}{occ_tag}{badge_html}</span><div style="flex-grow:1; margin:0 8px; background:#1e293b; border-radius:3px; height:8px;"><div style="width:{pct:.1f}%; background:{bar_color}; height:8px; border-radius:3px;"></div></div>{delta_html}<span style="color:{bar_color}; font-weight:bold; width:60px; text-align:right;">{score_str}</span></div>"""

tokens = md.parse(raw_html)
for t in tokens:
    print(t.type, t.tag, repr(t.content)[:80])
