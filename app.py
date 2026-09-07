import pathlib

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="VIP DAU 보고",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA = pathlib.Path(__file__).parent / "data"
KFONT = "'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; }
.hdr { font-size: 26px; font-weight: 700; color:#1a2236; margin-bottom: 2px; }
.section-title { font-size:18px; font-weight:700; color:#1a2236; margin:24px 0 10px;
  padding-bottom:6px; border-bottom:2px solid #e7ebf2; scroll-margin-top:20px; }
.metric-card { background:#f8f9fa; border-radius:10px; padding:12px 16px; border-left:4px solid #2C5F8A; }
.metric-label { font-size:13px; color:#666; margin-bottom:4px; }
.metric-value { font-size:24px; font-weight:700; color:#1a2236; }
.metric-sub { font-size:12px; color:#888; margin-top:2px; }
.note { font-size:13px; color:#555; background:#f6f7f9; border-radius:8px; padding:10px 14px; }
.fac-q { font-size:12px; color:#888; }
.fac-c { font-size:14px; color:#1a2236; }
.badge { font-size:12px; font-weight:700; border-radius:6px; padding:3px 10px; white-space:nowrap; }
a.navlink { display:block; padding:7px 12px; margin:3px 0; border-radius:8px;
  background:#eef3f9; color:#2C5F8A; text-decoration:none; font-size:14px;
  font-weight:600; border:1px solid #dde7f2; }
a.navlink:hover { background:#e0ebf7; color:#1d4666; }
table.stbl { border-collapse:collapse; width:100%; background:#fff; }
table.stbl th { background:#eef1f6; color:#55606f; font-size:12px; font-weight:700; padding:8px 10px;
  border:1px solid #e3e9f2; text-align:left; }
table.stbl td { border:1px solid #e3e9f2; padding:8px 10px; font-size:13px; color:#1a2236; vertical-align:middle; }
table.stbl td.fn { font-weight:700; white-space:nowrap; }
table.stbl td.fc { color:#444; }
table.tree { border-collapse:collapse; width:100%; background:#fff; }
table.tree th { background:#eef1f6; color:#55606f; font-size:12px; font-weight:700; padding:8px;
  border:1px solid #e3e9f2; text-align:center; }
table.tree td { border:1px solid #e3e9f2; padding:8px 10px; font-size:13px; color:#1a2236; vertical-align:middle; }
table.tree td.root { background:#eef4ff; color:#2C5F8A; font-weight:700; text-align:center; }
table.tree td.axis { background:#f6f7f9; font-weight:600; text-align:center; }
table.tree td.axiskey { background:#efeafb; font-weight:600; text-align:center; }
table.tree td.driver.bad { border-left:3px solid #C44E52; }
table.tree td.driver.warn { border-left:3px solid #DD9A16; }
table.tree td.act.on { background:#eef4ff; color:#2C5F8A; font-weight:600; }
.sub { font-size:11px; color:#888; font-weight:400; }
.ctitle { font-size:14px; font-weight:700; color:#1a2236; margin:0 0 4px; }
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

VERDICT = {"제외": "#9aa0a6", "유효": "#C44E52", "부분 유효": "#DD9A16",
           "범위 제외": "#6c8ebf", "보류": "#7f8c8d"}


def metric(col, label, value, sub, color):
    col.markdown(
        f'<div class="metric-card" style="border-left-color:{color}">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def title(text, anchor):
    st.markdown(f'<div class="section-title" id="{anchor}">{text}</div>', unsafe_allow_html=True)


# ── 사이드바 ①: 설정 (원본 올리기) ──────────────────────────
with st.sidebar:
    st.header("⚙️ 설정")
    with st.expander("📤 원본 올리기 (월 갱신)", expanded=False):
        st.caption("갱신할 CSV를 **파일명 그대로** 올리면 git push 없이 즉시 반영됩니다. "
                   "(kpi · channel · frequency · transition · nodes · factors · daytype .csv)")
        _ups = st.file_uploader("CSV 올리기", type="csv", accept_multiple_files=True,
                                label_visibility="collapsed", key="up")
    uploaded = {u.name: u for u in (_ups or [])}
    if uploaded:
        st.success("업로드 반영: " + ", ".join(uploaded.keys()))


def load(name, fill=False):
    src = uploaded[name] if name in uploaded else (DATA / name)
    df = pd.read_csv(src)
    return df.fillna("") if fill else df


nodes = load("nodes.csv", fill=True)
factors = load("factors.csv", fill=True)
kpi = load("kpi.csv")
channel = load("channel.csv")
freq = load("frequency.csv")
trans = load("transition.csv")
daytype = load("daytype.csv")

# ── 사이드바 ②: 메뉴 ────────────────────────────────────────
with st.sidebar:
    st.markdown("#### 📂 메뉴")
    st.markdown(
        '<a href="#now" class="navlink">1 · 현황</a>'
        '<a href="#factors" class="navlink">2 · 요인 점검</a>'
        '<a href="#map" class="navlink">3 · 동인맵 · 실행</a>',
        unsafe_allow_html=True,
    )


def base_layout(fig, h=260, ttl=None):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=(36 if ttl else 22), b=34),
                      font=dict(family=KFONT), plot_bgcolor="white",
                      legend=dict(orientation="h", y=-0.2, x=0, font=dict(size=11)),
                      yaxis=dict(ticksuffix="%", gridcolor="#eee", zeroline=False))
    if ttl:
        fig.update_layout(title=dict(text=ttl, x=0.5, xanchor="center", y=0.97, yanchor="top",
                                     font=dict(family=KFONT, size=13, color="#1a2236")))
    return fig


def fig_kpi():
    d = kpi
    xlab = [str(m)[2:] for m in d["month"]]
    f = go.Figure()
    f.add_trace(go.Scatter(x=xlab, y=d["mau_yoy"], name="MAU 전년비",
                           mode="lines+markers", line=dict(color="#55A868", width=3)))
    f.add_trace(go.Scatter(x=xlab, y=d["dau_yoy"], name="DAU 전년비",
                           mode="lines+markers", line=dict(color="#C44E52", width=3)))
    f.add_hline(y=0, line_dash="dot", line_color="#bbb")
    f.update_xaxes(type="category")
    return base_layout(f, ttl="MAU vs DAU 전년비 추이")


def fig_daytype():
    f = go.Figure(go.Bar(x=daytype["type"], y=daytype["yoy"], marker_color="#2C5F8A",
                         text=[f"{v:+.1f}%" for v in daytype["yoy"]], textposition="outside"))
    f.add_hline(y=0, line_color="#bbb")
    f.update_layout(showlegend=False)
    return base_layout(f, ttl="일자유형별 DAU 전년비")


def fig_channel():
    colc = ["#C44E52" if v < 0 else "#B0B0B0" for v in channel["yoy"]]
    f = go.Figure(go.Bar(x=channel["channel"], y=channel["yoy"], marker_color=colc,
                         text=[f"{v:+.0f}%" for v in channel["yoy"]], textposition="outside"))
    f.add_hline(y=0, line_color="#bbb")
    f.update_layout(showlegend=False)
    return base_layout(f, ttl="채널별 DAU 전년비")


def fig_freq():
    f = go.Figure()
    f.add_trace(go.Bar(name="2025", x=freq["group"], y=freq["y2025"], marker_color="#B0C4DE"))
    f.add_trace(go.Bar(name="2026", x=freq["group"], y=freq["y2026"], marker_color="#2C5F8A"))
    f.update_layout(barmode="group")
    return base_layout(f, ttl="빈도 구성비 (2025 → 2026)")


def html_transition():
    cols = ["고빈도", "중빈도", "저빈도"]
    mt = ['<table class="mtx"><tr><th></th>'] + [f"<th>26 {c}</th>" for c in cols] + ["</tr>"]
    for i, r in trans.iterrows():
        mt.append(f'<tr><th>{r["from"]}</th>')
        for j, c in enumerate(cols):
            cls = "d" if j == i else ("dn" if j > i else "up")
            mt.append(f'<td class="{cls}">{r[c]:.1f}%</td>')
        mt.append("</tr>")
    mt.append("</table>")
    return "".join(mt)


def render_tree(df):
    total = len(df)
    sizes = df.groupby("axis", sort=False).size().to_dict()
    seen, body, first = set(), [], True
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
        cells.append(f'<td class="act on">{na}</td>' if na
                     else '<td class="act" style="color:#bbb">—</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    head = ("<tr><th>성과지표</th><th>Level-Ⅰ · 1차 동인</th><th>Level-Ⅱ · 2차 동인</th>"
            "<th>Level-Ⅲ · 실행 레버</th><th>새로운 실행 방안</th></tr>")
    return '<table class="tree">' + head + "".join(body) + "</table>"


def render_evidence(f):
    ev = f["evidence"]
    key = f"ev_{f['num']}"
    if ev == "kpi":
        st.plotly_chart(fig_kpi(), use_container_width=True, key=key)
    elif ev == "daytype":
        st.plotly_chart(fig_daytype(), use_container_width=True, key=key)
    elif ev == "channel":
        st.plotly_chart(fig_channel(), use_container_width=True, key=key)
    elif ev == "freq_transition":
        a, b = st.columns(2)
        with a:
            st.plotly_chart(fig_freq(), use_container_width=True, key=key + "_f")
        with b:
            st.markdown('<span class="sub">전이행렬 (행 합계 100%)</span>', unsafe_allow_html=True)
            st.markdown(html_transition(), unsafe_allow_html=True)
    elif ev == "compare":
        unit = f["cmp_unit"] if isinstance(f["cmp_unit"], str) else ""
        v25, v26 = float(f["cmp_2025"]), float(f["cmp_2026"])
        delta = v26 - v25
        dsuf = "%p" if unit == "%" else unit
        dcolor = "#9aa0a6" if abs(delta) < 1 else ("#C44E52" if delta < 0 else "#55A868")
        st.markdown(
            '<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;'
            'background:#f8f9fa;border-radius:10px;padding:12px 16px">'
            f'<span style="font-size:13px;color:#666">{f["cmp_label"]}</span>'
            f'<span style="font-size:20px;font-weight:700;color:#1a2236">'
            f'{v25:g}{unit} <span style="color:#bbb">→</span> {v26:g}{unit}</span>'
            f'<span class="badge" style="background:{dcolor}22;color:{dcolor}">'
            f'전년비 {delta:+.1f}{dsuf}</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption("정량 근거 없음 — CRM 통제 밖으로 분석 범위에서 제외.")


st.markdown('<div class="hdr">VIP DAU 보고</div>', unsafe_allow_html=True)
st.caption("현황 → 요인 점검 → 동인맵·실행  |  수치는 전년비·구성비, 절대수 비노출")

# ── 1. 현황 ─────────────────────────────────────────────────
title("1. 현황", "now")
last = kpi.iloc[-1]
c1, c2, c3 = st.columns(3)
metric(c1, f"DAU 전년비 ({last['month']})", f"{last['dau_yoy']:+.1f}%", "방문 빈도 역신장", "#C44E52")
metric(c2, f"MAU 전년비 ({last['month']})", f"{last['mau_yoy']:+.1f}%", "모수는 유지·증가", "#55A868")
metric(c3, "MAU − DAU 갭", f"{last['mau_yoy'] - last['dau_yoy']:+.1f}%p", "모수 아닌 '빈도' 문제", "#2C5F8A")
g1, g2, g3 = st.columns(3)
with g1:
    st.plotly_chart(fig_kpi(), use_container_width=True, key="now_kpi")
with g2:
    st.plotly_chart(fig_channel(), use_container_width=True, key="now_ch")
with g3:
    st.plotly_chart(fig_freq(), use_container_width=True, key="now_fq")
st.markdown('<div class="note">광고 <b>flat</b> · 하락 전액 '
            '<b style="color:#C44E52">직접·푸시</b> → 재방문 축에서 발생.</div>',
            unsafe_allow_html=True)

# ── 2. 요인 점검 ────────────────────────────────────────────
title("2. 요인 점검", "factors")
counts = factors["verdict"].value_counts()
cols = st.columns(4)
for col, label in zip(cols, ["제외", "유효", "부분 유효", "범위 제외"]):
    metric(col, label, f"{int(counts.get(label, 0))}건", "", VERDICT[label])
st.caption("후보 요인 전체 판정을 한눈에 확인하고, 아래에서 하나를 골라 근거 데이터를 확인.")

srows = []
for r in factors.itertuples():
    color = VERDICT.get(r.verdict, "#7f8c8d")
    srows.append(
        f'<tr><td class="fn">{r.num}. {r.factor}</td>'
        f'<td><span class="badge" style="background:{color}22;color:{color}">{r.verdict}</span></td>'
        f'<td class="fc">{r.conclusion}</td></tr>'
    )
st.markdown('<table class="stbl"><tr><th>요인</th><th>판정</th><th>결론</th></tr>'
            + "".join(srows) + "</table>", unsafe_allow_html=True)

st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
labels = [f"{r.num}. {r.factor}" for r in factors.itertuples()]
sel = st.selectbox("요인 골라서 근거 데이터 보기", labels)
f = factors.iloc[labels.index(sel)]
color = VERDICT.get(f["verdict"], "#7f8c8d")
with st.container(border=True):
    st.markdown(
        f'<span class="badge" style="background:{color}22;color:{color}">{f["verdict"]}</span> '
        f'<span class="fac-q" style="margin-left:6px">{f["question"]}</span>'
        f'<div class="fac-c" style="margin-top:6px">{f["conclusion"]}</div>',
        unsafe_allow_html=True,
    )
    render_evidence(f)

# ── 3. 동인맵 · 실행 ────────────────────────────────────────
title("3. 동인맵 · 실행", "map")
st.markdown('<span class="sub">VIP DAU = 방문 모수 × 인당 방문빈도 · '
            'CRM 통제 가능(teal) / CRM 밖(gray)</span>', unsafe_allow_html=True)
st.markdown(render_tree(nodes), unsafe_allow_html=True)

st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
st.markdown('<span class="sub">실행 계획</span>', unsafe_allow_html=True)
exec_rows = [
    ("단일 레버", "재방문 트리거 — D-1 발송 → 행동 발생 즉시 발송 전환 (근거: W컨셉 등 벤치마크, 자사 A/B 검증)"),
    ("트랙 A / B", "A = 실시간 행동 트리거(본 레버) · B = 미보유 재설치(즉시 착수)"),
    ("목표", "반등 아닌 '역신장 폭 축소' — 보수 −8% / 기본 −5% / 상한 −2.5%"),
    ("측정", "발송군 vs 홀드아웃(대조군) 재방문율 차이로 순효과 검증 (4주)"),
]
erows = "".join(f'<tr><td class="fn">{k}</td><td class="fc">{v}</td></tr>' for k, v in exec_rows)
st.markdown('<table class="stbl"><tr><th>구분</th><th>내용</th></tr>' + erows + "</table>",
            unsafe_allow_html=True)

st.markdown("---")
st.caption("데이터: `data/*.csv` (사이드바 설정에서 CSV 업로드로 교체 가능) · "
           "수치는 전년비·구성비(절대수 비노출) · DAU 정의는 한 기준으로 통일 후 사용 권장.")
