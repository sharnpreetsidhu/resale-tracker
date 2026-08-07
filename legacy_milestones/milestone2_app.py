from pathlib import Path
from html import escape

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(
    page_title="AI Resale Market Tracker",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATHS = [Path("data/resale_data.csv"), Path("resale_data.csv")]

FEATURE_COLUMNS = [
    "grade",
    "asking_price",
    "simple_market_value",
    "weighted_market_value",
    "difference_percent",
    "sale_count",
    "volatility_percent",
]

SPORT_MAP = {
    "Connor Bedard": "Hockey",
    "Sidney Crosby": "Hockey",
    "Auston Matthews": "Hockey",
    "Wayne Gretzky": "Hockey",
    "Victor Wembanyama": "Basketball",
    "LeBron James": "Basketball",
    "Michael Jordan": "Basketball",
    "Kobe Bryant": "Basketball",
    "Shohei Ohtani": "Baseball",
    "Tom Brady": "Football",
    "Patrick Mahomes": "Football",
    "Lionel Messi": "Soccer",
    "Cristiano Ronaldo": "Soccer",
}

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
    --bg:#050711;
    --panel:rgba(15,23,42,.76);
    --panel-strong:rgba(15,23,42,.94);
    --border:rgba(148,163,184,.20);
    --text:#F8FAFC;
    --muted:#94A3B8;
    --green:#22C55E;
    --blue:#38BDF8;
    --purple:#A78BFA;
    --gold:#FBBF24;
    --red:#EF4444;
}

html, body, [class*="css"]{
    font-family:'Inter',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
}

.stApp{
    background:
        radial-gradient(circle at 12% 3%, rgba(56,189,248,.24), transparent 27%),
        radial-gradient(circle at 87% 4%, rgba(167,139,250,.20), transparent 25%),
        radial-gradient(circle at 55% 88%, rgba(34,197,94,.14), transparent 30%),
        linear-gradient(180deg,#070A13 0%,#050711 100%);
    color:var(--text);
}

.block-container{
    padding-top:1.2rem;
    max-width:1500px;
}

#MainMenu, footer, header{
    visibility:hidden;
}

[data-testid="stSidebar"]{
    background:rgba(5,7,17,.96);
    border-right:1px solid var(--border);
}

.stButton > button{
    border-radius:16px !important;
    border:1px solid rgba(34,197,94,.38) !important;
    background:linear-gradient(135deg,rgba(34,197,94,.24),rgba(56,189,248,.18)) !important;
    color:#F8FAFC !important;
    font-weight:900 !important;
    padding:.75rem 1rem !important;
    box-shadow:0 12px 30px rgba(34,197,94,.10) !important;
}

.stButton > button:hover{
    border-color:rgba(34,197,94,.82) !important;
    transform:translateY(-1px);
}

div[data-testid="stMetric"]{
    background:rgba(15,23,42,.72);
    border:1px solid rgba(148,163,184,.16);
    border-radius:20px;
    padding:18px 18px 15px;
    box-shadow:0 18px 45px rgba(0,0,0,.18);
}

div[data-testid="stMetricValue"]{
    font-weight:900;
    color:#fff;
}

div[data-testid="stMetricLabel"]{
    color:#CBD5E1;
    font-weight:800;
}

.stTabs [data-baseweb="tab-list"]{
    gap:10px;
    background:rgba(15,23,42,.42);
    border:1px solid rgba(148,163,184,.14);
    border-radius:18px;
    padding:7px;
}

.stTabs [data-baseweb="tab"]{
    border-radius:14px;
    color:#CBD5E1;
    font-weight:800;
    padding:10px 16px;
}

.stTabs [aria-selected="true"]{
    background:linear-gradient(135deg,rgba(56,189,248,.20),rgba(34,197,94,.14));
    color:white;
}

.hero{
    position:relative;
    overflow:hidden;
    border-radius:34px;
    padding:36px;
    border:1px solid rgba(148,163,184,.20);
    background:
        linear-gradient(135deg,rgba(15,23,42,.95),rgba(2,6,23,.72)),
        radial-gradient(circle at 20% 10%,rgba(56,189,248,.30),transparent 28%);
    box-shadow:0 30px 100px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.05);
}

.hero:before{
    content:"";
    position:absolute;
    inset:-2px;
    background:linear-gradient(110deg,transparent 0%,rgba(255,255,255,.05) 20%,transparent 42%);
    transform:translateX(-100%);
    animation:shine 6s ease-in-out infinite;
}

@keyframes shine{
    0%{transform:translateX(-100%)}
    42%,100%{transform:translateX(100%)}
}

.hero-grid{
    position:relative;
    z-index:2;
    display:grid;
    grid-template-columns:minmax(0,1.4fr) 360px;
    gap:34px;
    align-items:center;
}

.eyebrow{
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:8px 13px;
    border-radius:999px;
    color:#BBF7D0;
    background:rgba(34,197,94,.13);
    border:1px solid rgba(34,197,94,.28);
    font-size:12px;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.08em;
}

.hero-title{
    font-size:58px;
    line-height:.98;
    letter-spacing:-.06em;
    font-weight:950;
    color:white;
    margin:18px 0 14px;
}

.hero-title span{
    background:linear-gradient(90deg,#FFFFFF,#BAE6FD,#86EFAC);
    -webkit-background-clip:text;
    color:transparent;
}

.hero-copy{
    font-size:18px;
    line-height:1.6;
    color:#CBD5E1;
    max-width:780px;
    margin-bottom:16px;
}

.pill-row{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:18px;
}

.pill{
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:10px 13px;
    border-radius:999px;
    background:rgba(255,255,255,.065);
    border:1px solid rgba(255,255,255,.10);
    color:#E2E8F0;
    font-size:13px;
    font-weight:850;
}

.pipeline{
    display:flex;
    flex-wrap:wrap;
    gap:9px;
    margin-top:18px;
    align-items:center;
}

.pipe-node{
    padding:9px 12px;
    border-radius:14px;
    background:rgba(15,23,42,.70);
    border:1px solid rgba(148,163,184,.14);
    color:#E2E8F0;
    font-size:12px;
    font-weight:900;
}

.pipe-arrow{
    color:#64748B;
    font-weight:900;
}

.slab-wrap{
    display:flex;
    justify-content:center;
    perspective:900px;
}

.mock-card{
    width:300px;
    padding:14px;
    border-radius:28px;
    background:linear-gradient(145deg,#F8FAFC,#CBD5E1 55%,#94A3B8);
    box-shadow:0 35px 80px rgba(56,189,248,.20);
    animation:float 4.2s ease-in-out infinite;
    transform:rotate(2deg);
}

@keyframes float{
    0%,100%{transform:translateY(0) rotate(2deg)}
    50%{transform:translateY(-10px) rotate(0deg)}
}

.slab-label{
    display:flex;
    justify-content:space-between;
    color:#0F172A;
    background:#E2E8F0;
    border:2px solid #0F172A;
    border-radius:14px;
    padding:10px 11px;
    font-weight:950;
    font-size:13px;
}

.card-art{
    margin-top:12px;
    min-height:292px;
    border-radius:20px;
    border:2px solid #0F172A;
    padding:18px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    color:white;
    background:
        radial-gradient(circle at 30% 20%,rgba(34,197,94,.95),transparent 18%),
        radial-gradient(circle at 70% 55%,rgba(56,189,248,.88),transparent 22%),
        linear-gradient(135deg,#0F172A,#111827 56%,#020617);
}

.card-orbit{
    height:120px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,.10);
    display:grid;
    place-items:center;
    background:radial-gradient(circle,rgba(255,255,255,.13),transparent 56%);
    color:rgba(255,255,255,.88);
    font-size:46px;
    font-weight:950;
    letter-spacing:-.05em;
}

.card-name{
    font-size:27px;
    line-height:1;
    font-weight:950;
    letter-spacing:-.03em;
}

.card-sub{
    margin-top:7px;
    color:#CBD5E1;
    font-size:13px;
}

.stamp{
    display:inline-flex;
    margin-top:14px;
    width:fit-content;
    padding:9px 11px;
    border-radius:13px;
    background:rgba(34,197,94,.18);
    border:1px solid rgba(34,197,94,.45);
    color:#BBF7D0;
    font-weight:950;
    font-size:12px;
}

.kpi-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:14px;
    margin:18px 0;
}

.kpi-card{
    position:relative;
    overflow:hidden;
    border-radius:24px;
    padding:20px;
    background:rgba(15,23,42,.72);
    border:1px solid rgba(148,163,184,.16);
    box-shadow:0 20px 55px rgba(0,0,0,.22);
    transition:transform .18s ease,border-color .18s ease,background .18s ease;
}

.kpi-card:hover{
    transform:translateY(-3px);
    border-color:rgba(56,189,248,.42);
    background:rgba(15,23,42,.88);
}

.kpi-card:after{
    content:"";
    position:absolute;
    right:-34px;
    top:-34px;
    width:92px;
    height:92px;
    border-radius:50%;
    background:rgba(56,189,248,.12);
}

.kpi-label{
    color:#94A3B8;
    text-transform:uppercase;
    letter-spacing:.08em;
    font-size:12px;
    font-weight:950;
}

.kpi-value{
    font-size:32px;
    line-height:1.1;
    color:white;
    font-weight:950;
    margin-top:10px;
    letter-spacing:-.04em;
}

.kpi-sub{
    color:#CBD5E1;
    font-size:13px;
    margin-top:7px;
}

.signal-card{
    border-radius:28px;
    padding:24px;
    background:linear-gradient(135deg,rgba(15,23,42,.94),rgba(2,6,23,.82));
    border:1px solid rgba(148,163,184,.18);
    box-shadow:0 28px 90px rgba(0,0,0,.32);
    margin:20px 0;
}

.signal-grid{
    display:grid;
    grid-template-columns:190px 1fr;
    gap:24px;
    align-items:center;
}

.score-ring{
    width:154px;
    height:154px;
    border-radius:999px;
    display:grid;
    place-items:center;
    margin:auto;
}

.score-inner{
    width:116px;
    height:116px;
    border-radius:999px;
    display:grid;
    place-items:center;
    background:#08111F;
    border:1px solid rgba(255,255,255,.08);
    box-shadow:inset 0 0 28px rgba(0,0,0,.45);
}

.score-number{
    font-size:38px;
    font-weight:950;
    color:white;
}

.signal-title{
    font-size:48px;
    font-weight:950;
    letter-spacing:-.05em;
    color:white;
    margin-top:10px;
}

.signal-copy{
    font-size:17px;
    color:#CBD5E1;
    line-height:1.6;
    margin-top:8px;
}

.section-title{
    font-size:26px;
    font-weight:950;
    color:white;
    letter-spacing:-.035em;
    margin:14px 0 12px;
}

.reason-box,.watch-card{
    border-radius:20px;
    padding:16px 18px;
    background:rgba(15,23,42,.72);
    border:1px solid rgba(148,163,184,.14);
    margin-bottom:10px;
    box-shadow:0 14px 35px rgba(0,0,0,.14);
}

.reason-box{
    display:flex;
    gap:12px;
    align-items:flex-start;
}

.reason-icon{
    width:26px;
    height:26px;
    border-radius:999px;
    flex:0 0 26px;
    display:grid;
    place-items:center;
    background:rgba(34,197,94,.14);
    color:#86EFAC;
    font-weight:950;
}

.reason-text{
    color:#E2E8F0;
    font-weight:750;
    line-height:1.45;
}

.watch-top{
    display:flex;
    justify-content:space-between;
    gap:12px;
    align-items:flex-start;
}

.watch-title{
    font-weight:950;
    color:white;
}

.watch-gap{
    font-weight:950;
    color:#86EFAC;
    white-space:nowrap;
}

.muted{
    color:#94A3B8;
    font-size:13px;
    margin-top:5px;
}

.prob-card{
    border-radius:24px;
    padding:18px;
    background:rgba(15,23,42,.72);
    border:1px solid rgba(148,163,184,.14);
}

.prob-row{
    margin:14px 0;
}

.prob-top{
    display:flex;
    justify-content:space-between;
    color:#CBD5E1;
    font-size:13px;
    font-weight:950;
    margin-bottom:7px;
}

.bar-bg{
    height:12px;
    border-radius:999px;
    background:rgba(148,163,184,.17);
    overflow:hidden;
}

.bar-fill{
    height:100%;
    border-radius:999px;
    transition:width .7s ease;
}

.footer-note{
    color:#94A3B8;
    border-top:1px solid rgba(148,163,184,.14);
    margin-top:24px;
    padding-top:18px;
    font-size:13px;
}

@media(max-width:1000px){
    .hero-grid,.signal-grid{
        grid-template-columns:1fr;
    }

    .kpi-grid{
        grid-template-columns:repeat(2,minmax(0,1fr));
    }

    .hero-title{
        font-size:42px;
    }

    .mock-card{
        width:260px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


def h(value) -> str:
    return escape(str(value))


def initials(name: str) -> str:
    return "".join(part[0] for part in str(name).split()[:2]).upper()


def infer_rarity(card_name: str) -> str:
    name = str(card_name).lower()

    if "national" in name or "patch" in name:
        return "Ultra Rare"

    if "prizm" in name or "chrome" in name or "young guns" in name or "holo" in name:
        return "Rare"

    if "rated" in name or "select" in name:
        return "Uncommon"

    return "Common"


@st.cache_data
def load_data() -> pd.DataFrame:
    for path in DATA_PATHS:
        if path.exists():
            df = pd.read_csv(path)
            break
    else:
        st.error("Could not find resale_data.csv. Put it beside this Python file or inside a data/ folder.")
        st.stop()

    required = {"player", "year", "card_name", "grade", "sale_price", "site", "sale_date"}
    missing = required - set(df.columns)

    if missing:
        st.error(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
        st.stop()

    df = df.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["grade"] = pd.to_numeric(df["grade"], errors="coerce")
    df["sale_price"] = pd.to_numeric(df["sale_price"], errors="coerce")
    df = df.dropna(subset=["sale_date", "grade", "sale_price"])
    df["grade"] = df["grade"].astype(int)

    if "sport" not in df.columns:
        df["sport"] = df["player"].map(SPORT_MAP).fillna("Trading Cards")

    if "rarity" not in df.columns:
        df["rarity"] = df["card_name"].apply(infer_rarity)

    return df


def weighted_average_price(matches: pd.DataFrame) -> float:
    ordered = matches.sort_values("sale_date")
    weights = np.arange(1, len(ordered) + 1)
    return float(np.average(ordered["sale_price"], weights=weights))


def make_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for (player, card, grade), group in df.groupby(["player", "card_name", "grade"]):
        simple = float(group["sale_price"].mean())
        weighted = weighted_average_price(group)
        volatility = 0.0 if simple == 0 else float(group["sale_price"].std(ddof=0) / simple * 100)
        latest = group.sort_values("sale_date").iloc[-1]

        rows.append({
            "player": player,
            "card_name": card,
            "grade": int(grade),
            "simple_market_value": simple,
            "weighted_market_value": weighted,
            "sale_count": int(len(group)),
            "volatility_percent": volatility,
            "last_sale_price": float(latest["sale_price"]),
            "last_sale_date": latest["sale_date"],
        })

    return pd.DataFrame(rows)


def label_from_gap(gap: float) -> str:
    if gap >= 12:
        return "Good Deal"

    if gap <= -12:
        return "Overpriced"

    return "Fair Price"


def recommendation_from_label(label: str) -> str:
    return {
        "Good Deal": "Buy",
        "Fair Price": "Hold / Consider",
        "Overpriced": "Avoid"
    }[label]


def deal_score_from_gap(gap: float) -> int:
    return int(np.clip(50 + gap * 2.2, 1, 99))


def signal_name(label: str, score: int) -> str:
    if label == "Good Deal" and score >= 85:
        return "Strong Buy"

    if label == "Good Deal":
        return "Buy"

    if label == "Fair Price":
        return "Watch / Negotiate"

    return "Avoid"


@st.cache_resource
def train_models(df: pd.DataFrame):
    summary = make_summary(df)
    rows = []

    multipliers = [0.68, 0.78, 0.88, 0.97, 1.03, 1.12, 1.22, 1.35]

    for _, row in summary.iterrows():
        market = row["weighted_market_value"]

        for mult in multipliers:
            asking = float(market * mult)
            gap = float((market - asking) / market * 100)

            rows.append({
                "grade": row["grade"],
                "asking_price": asking,
                "simple_market_value": row["simple_market_value"],
                "weighted_market_value": row["weighted_market_value"],
                "difference_percent": gap,
                "sale_count": row["sale_count"],
                "volatility_percent": row["volatility_percent"],
                "deal_label": label_from_gap(gap),
            })

    train_df = pd.DataFrame(rows)

    X = train_df[FEATURE_COLUMNS]
    y = train_df["deal_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    candidates = {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=160, max_depth=7, random_state=42),
    }

    fitted = {}
    scores = {}

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        fitted[name] = model
        scores[name] = accuracy_score(y_test, model.predict(X_test))

    best_name = max(scores, key=scores.get)
    best_model = fitted[best_name]
    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, best_model.predict(X_test), labels=labels)

    return {
        "summary": summary,
        "best_model": best_model,
        "best_name": best_name,
        "scores": scores,
        "training_count": len(train_df),
        "labels": labels,
        "confusion_matrix": cm,
    }


def features_for_prediction(grade: int, asking_price: float, matches: pd.DataFrame) -> pd.DataFrame:
    simple = float(matches["sale_price"].mean())
    weighted = weighted_average_price(matches)
    volatility = 0.0 if simple == 0 else float(matches["sale_price"].std(ddof=0) / simple * 100)
    gap = float((weighted - asking_price) / weighted * 100)

    return pd.DataFrame([{
        "grade": grade,
        "asking_price": asking_price,
        "simple_market_value": simple,
        "weighted_market_value": weighted,
        "difference_percent": gap,
        "sale_count": len(matches),
        "volatility_percent": volatility,
    }])


def kpi_card(label: str, value: str, sub: str) -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{h(label)}</div>'
        f'<div class="kpi-value">{h(value)}</div>'
        f'<div class="kpi-sub">{h(sub)}</div>'
        f'</div>'
    )


def probability_bars(classes, probabilities) -> str:
    colors = {
        "Good Deal": "#22C55E",
        "Fair Price": "#FBBF24",
        "Overpriced": "#EF4444"
    }

    parts = ['<div class="prob-card">']

    for label, prob in sorted(zip(classes, probabilities), key=lambda item: item[1], reverse=True):
        percent = float(prob) * 100
        color = colors.get(label, "#38BDF8")

        parts.append(
            f'<div class="prob-row">'
            f'<div class="prob-top"><span>{h(label)}</span><span>{percent:.1f}%</span></div>'
            f'<div class="bar-bg">'
            f'<div class="bar-fill" style="width:{percent:.1f}%; background:linear-gradient(90deg,{color},#38BDF8);"></div>'
            f'</div>'
            f'</div>'
        )

    parts.append('</div>')
    return "".join(parts)


def trend_chart(matches: pd.DataFrame, simple: float, weighted: float, asking: float, title: str) -> go.Figure:
    ordered = matches.sort_values("sale_date")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ordered["sale_date"],
        y=ordered["sale_price"],
        mode="lines+markers",
        name="Recent comps",
        line=dict(width=4, color="#38BDF8"),
        marker=dict(size=11, color="#22C55E", line=dict(width=1, color="white")),
        hovertemplate="Date: %{x|%b %d, %Y}<br>Sale: $%{y:,.2f}<extra></extra>",
    ))

    fig.add_hline(
        y=weighted,
        line_dash="dash",
        line_color="#22C55E",
        annotation_text=f"Weighted ${weighted:,.2f}"
    )

    fig.add_hline(
        y=simple,
        line_dash="dot",
        line_color="#A78BFA",
        annotation_text=f"Avg ${simple:,.2f}"
    )

    fig.add_hline(
        y=asking,
        line_dash="dash",
        line_color="#FBBF24",
        annotation_text=f"Ask ${asking:,.2f}"
    )

    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=470,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.38)",
        font=dict(color="#E2E8F0"),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.05),
    )

    fig.update_xaxes(gridcolor="rgba(148,163,184,.12)", title="Sale date")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.12)", title="Sale price ($)")

    return fig


def site_chart(site_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        site_summary,
        x="site",
        y="sale_price",
        text=site_summary["sale_price"].map(lambda x: f"${x:,.0f}")
    )

    fig.update_traces(marker_color="#38BDF8", textposition="outside")

    fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.38)",
        showlegend=False,
    )

    fig.update_xaxes(title="Marketplace")
    fig.update_yaxes(title="Average sale price")

    return fig


def confusion_chart(cm: np.ndarray, labels) -> go.Figure:
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        colorscale="Greens",
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16, "color": "white"}
    ))

    fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.38)",
        xaxis_title="Predicted",
        yaxis_title="Actual"
    )

    return fig


def model_comparison_chart(scores: dict) -> go.Figure:
    score_df = pd.DataFrame({
        "Model": list(scores.keys()),
        "Accuracy": [v * 100 for v in scores.values()]
    })

    fig = px.bar(
        score_df,
        x="Model",
        y="Accuracy",
        text=score_df["Accuracy"].map(lambda x: f"{x:.1f}%")
    )

    fig.update_traces(marker_color=["#A78BFA", "#22C55E"], textposition="outside")

    fig.update_layout(
        template="plotly_dark",
        height=330,
        yaxis_range=[0, 105],
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.38)",
        showlegend=False
    )

    return fig


def explain(deal_label: str, gap: float, simple: float, weighted: float, site_summary: pd.DataFrame, volatility: float):
    best_site = site_summary.sort_values("sale_price", ascending=False).iloc[0]

    reasons = [
        f"The asking price is {abs(gap):.2f}% {'below' if gap >= 0 else 'above'} the recency-weighted market estimate.",
        f"Recent comparable sales average ${simple:,.2f}, while the recency-weighted estimate is ${weighted:,.2f}.",
        f"The strongest marketplace signal is {best_site['site']} with an average sale price of ${best_site['sale_price']:,.2f}.",
        f"Price volatility is {volatility:.2f}%, which helps estimate how stable the recent market is.",
    ]

    if deal_label == "Good Deal":
        reasons.insert(
            0,
            "This listing is below current comps, giving a reseller potential room for profit before fees and shipping."
        )
    elif deal_label == "Fair Price":
        reasons.insert(
            0,
            "This listing is close to market value, so it may be worth watching or negotiating lower."
        )
    else:
        reasons.insert(
            0,
            "This listing is above current comps, so the expected resale upside is weak."
        )

    return reasons


df = load_data()
model_pack = train_models(df)
summary_df = model_pack["summary"]

st.sidebar.markdown("## 💎 Deal Scanner")
st.sidebar.caption("Scan a card listing like a reseller checking comps.")

players = sorted(df["player"].unique())
selected_player = st.sidebar.selectbox("Player", players)

cards = sorted(df.loc[df["player"] == selected_player, "card_name"].unique())
selected_card = st.sidebar.selectbox("Card", cards)

grades = sorted(df.loc[
    (df["player"] == selected_player) &
    (df["card_name"] == selected_card),
    "grade"
].unique())

selected_grade = int(st.sidebar.selectbox("Grade", grades))

matches = df[
    (df["player"] == selected_player) &
    (df["card_name"] == selected_card) &
    (df["grade"] == selected_grade)
].copy().sort_values("sale_date")

default_value = weighted_average_price(matches)
default_ask = float(max(1, default_value * 0.85))

asking_price = float(st.sidebar.number_input(
    "Seller asking price ($)",
    min_value=1.0,
    value=round(default_ask, 2),
    step=5.0
))

st.sidebar.button("Run AI Deal Scan", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Prototype note: sample resale records are used for testing. "
    "A real launch would connect to verified sold-listing APIs."
)

simple_value = float(matches["sale_price"].mean())
weighted_value = weighted_average_price(matches)
volatility = 0.0 if simple_value == 0 else float(matches["sale_price"].std(ddof=0) / simple_value * 100)
gap = float((weighted_value - asking_price) / weighted_value * 100)

features = features_for_prediction(selected_grade, asking_price, matches)

model = model_pack["best_model"]
deal_label = str(model.predict(features)[0])
recommendation = recommendation_from_label(deal_label)
score = deal_score_from_gap(gap)
signal = signal_name(deal_label, score)
probabilities = model.predict_proba(features)[0]
classes = list(model.classes_)

site_summary = matches.groupby("site", as_index=False)["sale_price"].mean().sort_values("sale_price", ascending=False)

upside = weighted_value - asking_price
score_color = "#22C55E" if deal_label == "Good Deal" else "#FBBF24" if deal_label == "Fair Price" else "#EF4444"
year = int(matches.iloc[0]["year"])

st.markdown(
    f"""
<div class="hero">
<div class="hero-grid">
<div>
<div class="eyebrow">⚡ Reseller Intelligence Dashboard</div>
<div class="hero-title">Find <span>undervalued cards</span> before the market catches up.</div>
<div class="hero-copy">Scan trading card listings, compare them against recent sales, estimate flip value, and get an AI-powered buy/watch/avoid signal built for card flippers and collectors.</div>
<div class="pill-row">
<span class="pill">📊 {len(df):,} resale records</span>
<span class="pill">💰 Profit gap detection</span>
<span class="pill">🤖 {h(model_pack['best_name'])} classifier</span>
<span class="pill">📈 Live comp trend</span>
<span class="pill">🛒 Marketplace comparison</span>
</div>
<div class="pipeline">
<span class="pipe-node">Listing input</span>
<span class="pipe-arrow">→</span>
<span class="pipe-node">Recent comps</span>
<span class="pipe-arrow">→</span>
<span class="pipe-node">Weighted pricing</span>
<span class="pipe-arrow">→</span>
<span class="pipe-node">ML signal</span>
<span class="pipe-arrow">→</span>
<span class="pipe-node">Flip decision</span>
</div>
</div>
<div class="slab-wrap">
<div class="mock-card">
<div class="slab-label"><span>AI COMP</span><span>GRADE {selected_grade}</span></div>
<div class="card-art">
<div class="card-orbit">{h(initials(selected_player))}</div>
<div>
<div class="card-name">{h(selected_player)}</div>
<div class="card-sub">{h(selected_card)} • {year}</div>
<div class="stamp">{h(signal.upper())} • {score}/100</div>
</div>
</div>
</div>
</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("### Reseller Deal Dashboard")

st.markdown(
    '<div class="kpi-grid">'
    + kpi_card("Estimated flip value", f"${weighted_value:,.2f}", "Recency-weighted market estimate")
    + kpi_card("Seller asking price", f"${asking_price:,.2f}", "Current listing price")
    + kpi_card("Potential profit", f"${upside:,.2f}", "Before fees, shipping, and tax")
    + kpi_card("Market gap", f"{gap:.2f}%", "Positive gap = below market")
    + '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="signal-card" style="border-color:{score_color};">
<div class="signal-grid">
<div>
<div class="score-ring" style="background:conic-gradient({score_color} {score}%, rgba(148,163,184,.14) 0);">
<div class="score-inner"><div class="score-number">{score}</div></div>
</div>
<div style="text-align:center;color:#CBD5E1;font-weight:950;margin-top:8px;">Deal Score</div>
</div>
<div>
<div class="eyebrow" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:#E2E8F0;">AI Flip Signal</div>
<div class="signal-title">{h(signal)}</div>
<div class="signal-copy">Deal rating: <b style="color:white;">{h(deal_label)}</b> • Recommended action: <b style="color:white;">{h(recommendation)}</b></div>
<div class="signal-copy">The system checks the seller price against recent comps, marketplace averages, recency-weighted value, and a machine-learning classifier.</div>
</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💸 Deal Analysis",
    "📈 Market Trend",
    "🛒 Marketplace Data",
    "🤖 Model Lab",
    "📁 Dataset"
])

with tab1:
    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.markdown('<div class="section-title">Why this could be a profitable flip</div>', unsafe_allow_html=True)

        for reason in explain(deal_label, gap, simple_value, weighted_value, site_summary, volatility):
            st.markdown(
                f'<div class="reason-box">'
                f'<div class="reason-icon">✓</div>'
                f'<div class="reason-text">{h(reason)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="section-title">Top opportunities watchlist</div>', unsafe_allow_html=True)

        opp = summary_df.copy()
        opp["sample_ask"] = opp["last_sale_price"]
        opp["gap_percent"] = (opp["weighted_market_value"] - opp["sample_ask"]) / opp["weighted_market_value"] * 100

        for _, row in opp.sort_values("gap_percent", ascending=False).head(5).iterrows():
            st.markdown(
                f'<div class="watch-card">'
                f'<div class="watch-top">'
                f'<div class="watch-title">{h(row["player"])} — {h(row["card_name"])} Grade {int(row["grade"])}</div>'
                f'<div class="watch-gap">{row["gap_percent"]:.1f}% gap</div>'
                f'</div>'
                f'<div class="muted">Weighted value ${row["weighted_market_value"]:,.2f} • Latest sample listing ${row["sample_ask"]:,.2f}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown('<div class="section-title">Model confidence</div>', unsafe_allow_html=True)
        st.markdown(probability_bars(classes, probabilities), unsafe_allow_html=True)
        st.markdown("---")

        st.metric("Player", selected_player)
        st.metric("Card", selected_card)
        st.metric("Grade", selected_grade)

        st.caption("Confidence values come from the classifier prediction probabilities for the selected listing.")

with tab2:
    st.markdown('<div class="section-title">Interactive recent comp trend</div>', unsafe_allow_html=True)

    st.plotly_chart(
        trend_chart(
            matches,
            simple_value,
            weighted_value,
            asking_price,
            f"{selected_player} — {selected_card} Grade {selected_grade}"
        ),
        use_container_width=True
    )

    a, b, c, d = st.columns(4)

    a.metric("Simple average", f"${simple_value:,.2f}")
    b.metric("Weighted average", f"${weighted_value:,.2f}")
    c.metric("Lowest sale", f"${matches['sale_price'].min():,.2f}")
    d.metric("Highest sale", f"${matches['sale_price'].max():,.2f}")

with tab3:
    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown('<div class="section-title">Matching recent sales</div>', unsafe_allow_html=True)

        display = matches[["sale_date", "site", "sale_price"]].copy()
        display["sale_date"] = display["sale_date"].dt.strftime("%Y-%m-%d")
        display["sale_price"] = display["sale_price"].map(lambda x: f"${x:,.2f}")

        st.dataframe(display, use_container_width=True, hide_index=True)

        st.download_button(
            "Download selected comps",
            data=matches.to_csv(index=False).encode("utf-8"),
            file_name="selected_sales.csv",
            mime="text/csv",
            use_container_width=True
        )

    with right:
        st.markdown('<div class="section-title">Marketplace comparison</div>', unsafe_allow_html=True)

        st.plotly_chart(site_chart(site_summary), use_container_width=True)

        site_display = site_summary.copy()
        site_display["sale_price"] = site_display["sale_price"].map(lambda x: f"${x:,.2f}")

        st.dataframe(
            site_display.rename(columns={
                "site": "Marketplace",
                "sale_price": "Average sale price"
            }),
            use_container_width=True,
            hide_index=True
        )

with tab4:
    st.markdown('<div class="section-title">Model evaluation dashboard</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Best model", model_pack["best_name"])
    m2.metric("Training examples", f"{model_pack['training_count']:,}")
    m3.metric("Best accuracy", f"{max(model_pack['scores'].values()) * 100:.2f}%")
    m4.metric("Features", len(FEATURE_COLUMNS))

    left, right = st.columns(2, gap="large")

    with left:
        st.plotly_chart(model_comparison_chart(model_pack["scores"]), use_container_width=True)

    with right:
        st.plotly_chart(
            confusion_chart(model_pack["confusion_matrix"], model_pack["labels"]),
            use_container_width=True
        )

    st.caption(
        "High accuracy is expected because prototype labels are generated from pricing thresholds. "
        "This demonstrates the end-to-end ML pipeline: feature creation, model training, evaluation, and prediction."
    )

with tab5:
    st.markdown('<div class="section-title">Dataset explorer</div>', unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4)

    d1.metric("Rows", f"{len(df):,}")
    d2.metric("Players", df["player"].nunique())
    d3.metric("Card types", df["card_name"].nunique())
    d4.metric("Marketplaces", df["site"].nunique())

    preview = df.copy()
    preview["sale_date"] = preview["sale_date"].dt.strftime("%Y-%m-%d")

    st.dataframe(preview, use_container_width=True, hide_index=True)

    st.download_button(
        "Download full dataset",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="resale_data.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown(
    '<div class="footer-note">'
    'Built as a resale decision-support prototype. Current data is structured sample data for testing; '
    'a production version would connect to verified sold-listing sources or approved marketplace APIs.'
    '</div>',
    unsafe_allow_html=True,
)