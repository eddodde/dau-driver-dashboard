import pathlib

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="VIP DAU 성과 동인맵",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA = pathlib.Path(__file__).parent / "data"
KFONT = "'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"


@st.cache_data
def load(name, fill=False):
    df = pd.read_csv(DATA / name)
    if fill:
        df = df.fillna("")
    return df


nodes = load("nodes.csv", fill=True)
kpi = load("kpi.csv")
channel = load("channel.csv")
freq = load("frequency.csv")
trans = load("transition.csv")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; }
.hdr { font-size: 26px; font-weight: 700; color:#1a1a2e; margin-bottom: 2px; }
.section-title { font-size:18px; font-weight:700; color:#1a1a2e; margin:26px 0 12px;
  padding-bottom:6px; border-bottom:2px solid #e9ecef; scroll-margin-top:60px; }
.metric-card { background:#f8f9fa; border-radius:10px; padding:14px 18px; border-left:4px solid #4C72B0; }
.metric-label { font-size:13px; color:#666; margin-bottom:4px; }
.metric-value { font-size:26px; font-weight:700; color:#1a1a2e; }
.metric-sub { font-size:12px; color:#888; margin-top:2px; }
.note { font-size:13px; color:#555; background:#f6f7f9; border-radius:8px; padding:10px 14px; }
a.navlink { display:block; padding:8px 12px; margin:4px 0; border-radius:8px; background:#f2f5fa;
  color:#2E68B0; text-decoration:none; font-size:14px; font-weight:600; border:1px solid #e3e9f2; }
a.navlink:hover { background:#e3ecf8; }
table.tree { border-collapse:collapse; width:100%; background:#fff; }
table.tree th { background:#eef1f6; color:#55606f; font-size:12px; font-weight:700; padding:8px;
  border:1px solid #e3e9f2; text-align:center; }
table.tree td { border:1px solid #e3e9f2; padding:8px 10px; font-size:13px; color:#1a1a2e; vertical-align:middle; }
table.tree td.root { background:#eef4ff; color:#2E68B0; font-weight:700; text-align:center; }
table.tree td.axis { background:#f6f7f9; font-weight:600; text-align:center; }
table.tree td.axiskey { background:#efeafb; font-weight:600; text-align:center; }
table.tree td.driver.bad { border-left:3px solid #C44E52; }
table.tree td.driver.warn { border-left:3px solid #DD9A16; }
table.tree td.act.on { background:#eef4ff; color:#2E68B0; font-weight:600; }
.sub { font-size:11px; color:#888; font-weight:400; }
.chip { font-size:10px; font-weight:700; border-radius:4px; padding:1px 6px; margin-left:4px; white-space:nowrap; }
.chip.crm { background:#E1F5EE; color:#0F6E56; }
.chip.out { background:#F1EFE8; color:#5F5E5A; }
table.mtx { border-collapse:collapse; }
table.mtx th { font-size:12px; color:#55606f; padding:6px 12px; background:#eef1f6; border:1px solid #e3e9f2; }
table.mtx td { text-align:center; padding:9px 16px; font-size:14px; font-weight:600; border:2px solid #fff; }
table.mtx td.d { background:#5DCAA5; color:#04342C; }
table.mtx td.dn { background:#F0997B; color:#4A1B0C; }
table.mtx td.up { background:#EAF3DE; color:#173404; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="hdr">VIP DAU 성과 동인맵</div>', unsafe_allow_html=True)
st.caption("재방문 중심 · 왼쪽 지표 → 오른쪽 실행  |  모든 수치는 전년비·구성비, 절대수 비노출")

with st.sidebar:
    st.markdown("### 목차")
    st.markdown('<a class="navlink" href="#kpi">1. MAU vs DAU</a>', unsafe_allow_html=True)
    st.markdown('<a class="navlink" href="#map">2. 성과 동인맵</a>', unsafe_allow_html=True)
    st.markdown('<a class="navlink" href="#channel">3. 채널 분해</a>', unsafe_allow_html=True)
    st.markdown('<a class="navlink" href="#freq">4. 빈도 구조</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption(
        "**워싱**: 모든 숫자는 `data/*.csv`에서 로드됩니다. "
        "기준 통일·마스킹은 CSV만 수정하면 되고 코드는 건드리지 않습니다."
    )


def section(title, anchor):
    st.markdown(f'<div class="section-title" id="{anchor}">{title}</div>', unsafe_allow_html=True)


def metric(col, label, value, sub, color):
    col.markdown(
        f'<div class="metric-card" style="border-left-color:{color}">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


# ── 1. MAU vs DAU ────────────────────────────────────────────
section("1. MAU vs DAU 전년비", "kpi")
last = kpi.iloc[-1]
c1, c2, c3 = st.columns(3)
metric(c1, f"MAU 전년비 ({last['month']})", f"{last['mau_yoy']:+.1f}%", "모수는 유지·증가", "#55A868")
metric(c2, f"DAU 전년비 ({last['month']})", f"{last['dau_yoy']:+.1f}%", "방문 빈도 역신장", "#C44E52")
metric(c3, "MAU − DAU 갭", f"{last['mau_yoy'] - last['dau_yoy']:+.1f}%p", "모수 아닌 '빈도' 문제", "#4C72B0")

figk = go.Figure()
figk.add_trace(go.Scatter(x=kpi["month"], y=kpi["mau_yoy"], name="MAU 전년비",
                          mode="lines+markers", line=dict(color="#55A868", width=3)))
figk.add_trace(go.Scatter(x=kpi["month"], y=kpi["dau_yoy"], name="DAU 전년비",
                          mode="lines+markers", line=dict(color="#C44E52", width=3)))
figk.add_hline(y=0, line_dash="dot", line_color="#bbb")
figk.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10),
                   font=dict(family=KFONT), plot_bgcolor="white",
                   legend=dict(orientation="h", y=1.15, x=0),
                   yaxis=dict(ticksuffix="%", gridcolor="#eee", zeroline=False))
st.plotly_chart(figk, use_container_width=True)

# ── 2. 성과 동인맵 ───────────────────────────────────────────
section("2. 성과 동인맵", "map")
st.markdown('<span class="sub">VIP DAU = 방문 모수 × 인당 방문빈도 · '
            'CRM 통제 가능(teal) / CRM 밖(gray)</span>', unsafe_allow_html=True)


def render_tree(df):
    total = len(df)
    sizes = df.groupby("axis", sort=False).size().to_dict()
    seen = set()
    body = []
    first = True
    for _, r in df.iterrows():
        cells = []
        if first:
            cells.append(f'<td class="root" rowspan="{total}">VIP DAU ↑</td>')
            first = False
        if r["axis"] not in seen:
            seen.add(r["axis"])
            cls = "axiskey" if "②" in r["axis"] else "axis"
            cells.append(f'<td class="{cls}" rowspan="{sizes[r["axis"]]}">{r["axis"]}'
                         f'<br><span class="sub">{r["axis_note"]}</span></td>')
        dcls = f'driver {r["status"]}'.strip()
        cells.append(f'<td class="{dcls}">{r["driver"]}</td>')
        chip = ('<span class="chip crm">CRM</span>' if r["crm"] == "CRM"
                else '<span class="chip out">CRM 밖</span>')
        cells.append(f'<td>{r["lever"]} {chip}</td>')
        na = r["new_action"].strip() if isinstance(r["new_action"], str) else ""
        if na:
            cells.append(f'<td class="act on">{na}</td>')
        else:
            cells.append('<td class="act" style="color:#bbb">—</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    head = ("<tr><th>성과지표</th><th>Level-Ⅰ · 1차 동인</th><th>Level-Ⅱ · 2차 동인</th>"
            "<th>Level-Ⅲ · 실행 레버</th><th>새로운 실행 방안</th></tr>")
    return '<table class="tree">' + head + "".join(body) + "</table>"


st.markdown(render_tree(nodes), unsafe_allow_html=True)

# ── 3. 채널 분해 ─────────────────────────────────────────────
section("3. 채널 분해 — 어디서 새는가", "channel")
colc = ["#C44E52" if v < 0 else "#B0B0B0" for v in channel["yoy"]]
figc = go.Figure(go.Bar(x=channel["channel"], y=channel["yoy"], marker_color=colc,
                        text=[f"{v:+.0f}%" for v in channel["yoy"]], textposition="outside"))
figc.add_hline(y=0, line_color="#bbb")
figc.update_layout(height=280, margin=dict(l=10, r=10, t=20, b=10),
                   font=dict(family=KFONT), plot_bgcolor="white",
                   yaxis=dict(ticksuffix="%", gridcolor="#eee", zeroline=False))
st.plotly_chart(figc, use_container_width=True)
st.markdown('<div class="note">광고 <b>flat</b> · 하락 전액 <b style="color:#C44E52">직접·푸시</b>'
            '(재방문 채널) → 하락은 <b>인당 빈도(재방문) 축</b>에서 발생. 신규·노출·광고 아님.</div>',
            unsafe_allow_html=True)

# ── 4. 빈도 구조 ─────────────────────────────────────────────
section("4. 빈도 구조 — 고빈도의 저빈도화", "freq")
cf1, cf2 = st.columns(2)

with cf1:
    st.markdown('<span class="sub">빈도 구성비 (2025 → 2026)</span>', unsafe_allow_html=True)
    figf = go.Figure()
    figf.add_trace(go.Bar(name="2025", x=freq["group"], y=freq["y2025"], marker_color="#B0C4DE"))
    figf.add_trace(go.Bar(name="2026", x=freq["group"], y=freq["y2026"], marker_color="#4C72B0"))
    figf.update_layout(barmode="group", height=300, margin=dict(l=10, r=10, t=30, b=10),
                       font=dict(family=KFONT), plot_bgcolor="white",
                       legend=dict(orientation="h", y=1.15, x=0),
                       yaxis=dict(ticksuffix="%", gridcolor="#eee"))
    st.plotly_chart(figf, use_container_width=True)

with cf2:
    st.markdown('<span class="sub">방문빈도 전이행렬 (2025 → 2026, 행 합계 100%)</span>',
                unsafe_allow_html=True)
    cols = ["고빈도", "중빈도", "저빈도"]
    mt = ['<table class="mtx"><tr><th></th>'] + [f"<th>26 {c}</th>" for c in cols] + ["</tr>"]
    for i, r in trans.iterrows():
        mt.append(f'<tr><th>{r["from"]}</th>')
        for j, c in enumerate(cols):
            cls = "d" if j == i else ("dn" if j > i else "up")
            mt.append(f'<td class="{cls}">{r[c]:.1f}%</td>')
        mt.append("</tr>")
    mt.append("</table>")
    st.markdown("".join(mt), unsafe_allow_html=True)
    st.markdown('<span class="sub">teal=유지 · 주황=하향 이탈 · 초록=상향</span>',
                unsafe_allow_html=True)

st.markdown("---")
st.caption("데이터: `data/*.csv` · 수치는 전년비·구성비(절대수 비노출) · "
           "DAU 정의는 한 기준으로 통일 후 사용 권장.")
