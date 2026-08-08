from __future__ import annotations

import base64
import re
from html import escape
from pathlib import Path
from typing import Optional

import streamlit as st


def h(value) -> str:
    return escape(str(value))


def initials(name: str) -> str:
    return "".join(part[0] for part in str(name).split()[:2]).upper()


def slugify(text: str) -> str:
    text = str(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def image_to_data_uri(path: Path) -> Optional[str]:
    if not path.exists() or not path.is_file():
        return None

    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(suffix)

    if not mime:
        return None

    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def find_card_image(player: str, card: str, grade: int, base_dir: str = "assets/card_images") -> Optional[str]:
    folder = Path(base_dir)
    player_slug = slugify(player)
    card_slug = slugify(card)

    candidates = []
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        candidates.extend([
            folder / f"{player_slug}-{card_slug}-g{grade}{ext}",
            folder / f"{player_slug}-{card_slug}{ext}",
            folder / f"{player_slug}{ext}",
        ])

    for path in candidates:
        uri = image_to_data_uri(path)
        if uri:
            return uri

    return None



def apply_global_styles() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --bg:#040711;
  --panel:rgba(15,23,42,.76);
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
  color:var(--text);
  background:
    radial-gradient(circle at 8% -6%, rgba(56,189,248,.34), transparent 32%),
    radial-gradient(circle at 88% 2%, rgba(167,139,250,.30), transparent 28%),
    radial-gradient(circle at 76% 88%, rgba(34,197,94,.18), transparent 34%),
    linear-gradient(180deg,#07101f 0%,#040711 52%,#02040B 100%);
}

.stApp:before{
  content:"";
  position:fixed;
  inset:0;
  pointer-events:none;
  z-index:0;
  background-image:
    linear-gradient(rgba(148,163,184,.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148,163,184,.035) 1px, transparent 1px);
  background-size:46px 46px;
  mask-image:linear-gradient(to bottom, rgba(0,0,0,.55), transparent 72%);
}

.stApp:after{
  content:"";
  position:fixed;
  inset:-20%;
  pointer-events:none;
  z-index:0;
  background:
    radial-gradient(circle at 25% 15%, rgba(56,189,248,.20), transparent 24%),
    radial-gradient(circle at 80% 25%, rgba(167,139,250,.18), transparent 22%),
    radial-gradient(circle at 52% 90%, rgba(34,197,94,.13), transparent 28%);
  filter:blur(8px);
  animation:auroraFloat 14s ease-in-out infinite alternate;
}

@keyframes auroraFloat{
  from{transform:translate3d(-2%, -1%, 0) scale(1);}
  to{transform:translate3d(2%, 2%, 0) scale(1.04);}
}

.block-container{
  padding-top:1.15rem;
  max-width:1500px;
  position:relative;
  z-index:1;
}

#MainMenu, footer, header{
  visibility:hidden;
}

[data-testid="stSidebar"]{
  position:relative;
  z-index:1;
  background:linear-gradient(180deg,rgba(5,7,17,.98),rgba(8,13,28,.96)) !important;
  border-right:1px solid var(--border);
  backdrop-filter:blur(18px);
  box-shadow:18px 0 80px rgba(0,0,0,.32);
}

[data-testid="stSidebar"] *{
  font-weight:650;
}

.stButton>button{
  border-radius:16px!important;
  border:1px solid rgba(34,197,94,.45)!important;
  background:linear-gradient(135deg,rgba(34,197,94,.28),rgba(56,189,248,.18))!important;
  color:#F8FAFC!important;
  font-weight:900!important;
  padding:.76rem 1rem!important;
  box-shadow:0 14px 36px rgba(34,197,94,.14)!important;
  transition:all .18s ease!important;
}

.stButton>button:hover{
  border-color:rgba(34,197,94,.92)!important;
  transform:translateY(-1px);
  box-shadow:0 18px 42px rgba(56,189,248,.16)!important;
}

div[data-testid="stMetric"]{
  background:rgba(15,23,42,.74);
  border:1px solid rgba(148,163,184,.16);
  border-radius:20px;
  padding:18px 18px 15px;
  box-shadow:0 18px 45px rgba(0,0,0,.18);
}

div[data-testid="stMetricValue"]{
  font-weight:950;
  color:#fff;
}

div[data-testid="stMetricLabel"]{
  color:#CBD5E1;
  font-weight:850;
}

.stTabs [data-baseweb="tab-list"]{
  gap:10px;
  background:rgba(15,23,42,.46);
  border:1px solid rgba(148,163,184,.14);
  border-radius:18px;
  padding:7px;
  backdrop-filter:blur(18px);
}

.stTabs [data-baseweb="tab"]{
  border-radius:14px;
  color:#CBD5E1;
  font-weight:850;
  padding:10px 16px;
}

.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(56,189,248,.21),rgba(34,197,94,.16));
  color:white;
  box-shadow:0 8px 24px rgba(56,189,248,.10);
}

/* scanner input panel */
.scan-shell{
  margin:4px 0 18px;
  padding:20px 22px;
  border-radius:28px;
  background:
    linear-gradient(135deg,rgba(56,189,248,.15),rgba(34,197,94,.10)),
    rgba(15,23,42,.74);
  border:1px solid rgba(125,211,252,.24);
  box-shadow:0 24px 80px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.06);
  backdrop-filter:blur(20px);
}

.scan-badge{
  display:inline-flex;
  width:fit-content;
  padding:8px 12px;
  border-radius:999px;
  color:#BAE6FD;
  background:rgba(56,189,248,.12);
  border:1px solid rgba(56,189,248,.25);
  font-size:12px;
  font-weight:950;
  text-transform:uppercase;
  letter-spacing:.08em;
}

.scan-title{
  margin-top:10px;
  color:white;
  font-size:30px;
  line-height:1.05;
  font-weight:950;
  letter-spacing:-.045em;
}

.scan-copy{
  margin-top:7px;
  max-width:960px;
  color:#CBD5E1;
  line-height:1.55;
  font-weight:650;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-baseweb="select"] > div{
  background:rgba(15,23,42,.82)!important;
  border:1px solid rgba(148,163,184,.20)!important;
  border-radius:16px!important;
  color:#F8FAFC!important;
  min-height:46px!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 12px 28px rgba(0,0,0,.16)!important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-baseweb="select"] > div:hover{
  border-color:rgba(56,189,248,.52)!important;
  box-shadow:0 0 0 2px rgba(56,189,248,.12),0 16px 34px rgba(0,0,0,.18)!important;
}

label, [data-testid="stWidgetLabel"]{
  color:#E2E8F0!important;
  font-weight:900!important;
}

/* hero */
.hero{
  position:relative;
  overflow:hidden;
  border-radius:36px;
  padding:40px;
  border:1px solid rgba(148,163,184,.20);
  background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(2,6,23,.82));
  box-shadow:0 38px 120px rgba(0,0,0,.50), inset 0 1px 0 rgba(255,255,255,.06);
  transform-style:preserve-3d;
}

.hero:before{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(circle at 20% 15%,rgba(56,189,248,.24),transparent 28%),
    radial-gradient(circle at 72% 40%,rgba(34,197,94,.18),transparent 30%),
    linear-gradient(110deg,transparent 0%,rgba(255,255,255,.06) 22%,transparent 44%);
  transform:translateX(-100%);
  animation:heroShine 6.5s ease-in-out infinite;
}

.hero:after{
  content:"";
  position:absolute;
  right:4%;
  top:8%;
  width:270px;
  height:270px;
  border-radius:999px;
  background:radial-gradient(circle,rgba(56,189,248,.14),transparent 62%);
  filter:blur(3px);
  animation:orbPulse 5.5s ease-in-out infinite;
}

@keyframes heroShine{
  0%{transform:translateX(-100%)}
  44%,100%{transform:translateX(100%)}
}

@keyframes orbPulse{
  0%,100%{opacity:.55; transform:scale(.96);}
  50%{opacity:.9; transform:scale(1.08);}
}

.hero-grid{
  position:relative;
  z-index:2;
  display:grid;
  grid-template-columns:minmax(0,1.35fr) 390px;
  gap:38px;
  align-items:center;
}

.eyebrow{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding:8px 13px;
  border-radius:999px;
  color:#BAE6FD;
  background:rgba(56,189,248,.12);
  border:1px solid rgba(56,189,248,.25);
  font-size:12px;
  font-weight:950;
  text-transform:uppercase;
  letter-spacing:.08em;
}

.hero-title{
  font-size:60px;
  line-height:.98;
  letter-spacing:-.065em;
  font-weight:950;
  color:white;
  margin:18px 0 14px;
}

.hero-title span{
  background:linear-gradient(90deg,#FFFFFF,#BAE6FD,#86EFAC,#FDE68A);
  -webkit-background-clip:text;
  color:transparent;
}

.hero-copy{
  font-size:18px;
  line-height:1.62;
  color:#CBD5E1;
  max-width:800px;
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
  font-weight:900;
}

.pipeline{
  display:flex;
  flex-wrap:wrap;
  gap:9px;
  margin-top:20px;
  align-items:center;
}

.pipe-node{
  padding:9px 12px;
  border-radius:14px;
  background:rgba(15,23,42,.72);
  border:1px solid rgba(148,163,184,.14);
  color:#E2E8F0;
  font-size:12px;
  font-weight:900;
}

.pipe-arrow{
  color:#64748B;
  font-weight:950;
}

/* brand */
.brand-lockup{
  display:flex;
  align-items:center;
  gap:12px;
  margin-bottom:16px;
}

.logo-mark{
  width:42px;
  height:42px;
  border-radius:14px;
  display:grid;
  place-items:center;
  background:linear-gradient(135deg,rgba(56,189,248,.25),rgba(34,197,94,.20));
  border:1px solid rgba(125,211,252,.32);
  box-shadow:0 0 28px rgba(56,189,248,.18),inset 0 1px 0 rgba(255,255,255,.10);
  font-weight:950;
  color:#E0F2FE;
}

.brand-name{
  font-size:26px;
  font-weight:950;
  color:white;
  letter-spacing:-.04em;
  line-height:1;
}

.brand-sub{
  font-size:12px;
  text-transform:uppercase;
  letter-spacing:.11em;
  color:#94A3B8;
  font-weight:900;
  margin-top:4px;
}


/* card slab */

.mock-card:hover{
  transform:translateY(-10px) rotate(.5deg) scale(1.02);
  box-shadow:
    0 40px 95px rgba(0,0,0,.52),
    0 0 55px rgba(56,189,248,.18);
}

@keyframes floatCard{
  0%,100%{transform:translateY(0) rotate(2.5deg)}
  50%{transform:translateY(-12px) rotate(.5deg)}
}

.slab-wrap{
  display:flex;
  justify-content:center;
  align-items:center;
  min-height:420px;
}

.mock-card{
  position:relative;
  width:320px;
  padding:0;
  border-radius:0;
  background:transparent;
  border:none;
  box-shadow:none;
  animation:none;
  transform:none;
  overflow:visible;
}

.mock-card:before,
.mock-card:after{
  display:none;
}

.slab-label{
  position:absolute;
  top:8px;
  left:50%;
  transform:translateX(-50%);
  z-index:5;
  display:flex;
  justify-content:space-between;
  align-items:center;
  width:260px;
  padding:10px 14px;
  border-radius:14px;
  background:rgba(15,23,42,.72);
  border:1px solid rgba(148,163,184,.18);
  color:#E2E8F0;
  font-weight:900;
  font-size:12px;
  letter-spacing:.06em;
  text-transform:uppercase;
  backdrop-filter:blur(10px);
  box-shadow:0 12px 28px rgba(0,0,0,.25);
}

.card-art.has-card-image{
  position:relative;
  height:390px;
  border:none;
  border-radius:0;
  overflow:visible;
  padding:0;
  background:transparent;
  box-shadow:none;
}

.card-art.has-card-image:before,
.card-art.has-card-image:after{
  display:none;
}

.card-art.has-card-image .card-image{
  position:absolute;
  top:40px;
  left:50%;
  transform:translateX(-50%);
  width:250px;
  height:340px;
  object-fit:contain;
  object-position:center;
  background:transparent;
  border-radius:18px;
  padding:0;
  z-index:2;
  opacity:1;
  filter:drop-shadow(0 24px 45px rgba(0,0,0,.42));
  animation:cardFloatOnly 4.2s ease-in-out infinite;
}

.card-art.has-card-image .card-art-content{
  position:absolute;
  inset:0;
  z-index:3;
  min-height:auto;
  padding:0;
  display:block;
  pointer-events:none;
}

.card-art.has-card-image .card-name,
.card-art.has-card-image .card-sub,
.card-art.has-card-image .card-orbit{
  display:none;
}

.card-art.has-card-image .stamp{
  position:absolute;
  left:50%;
  bottom:6px;
  transform:translateX(-50%);
  margin-top:0;
  backdrop-filter:blur(10px);
  background:rgba(5,7,17,.78);
  border:1px solid rgba(34,197,94,.45);
  box-shadow:0 12px 28px rgba(0,0,0,.28);
  color:#BBF7D0;
  font-weight:900;
}

@keyframes cardFloatOnly{
  0%,100%{
    transform:translateX(-50%) translateY(0px) rotate(-1deg);
  }
  50%{
    transform:translateX(-50%) translateY(-12px) rotate(1deg);
  }
}

@keyframes cardFloat{
  0%,100%{transform:translateY(0) scale(1);}
  50%{transform:translateY(-5px) scale(1.015);}
}

@keyframes holoImageSweep{
  0%,100%{transform:translateX(-60%) rotate(8deg);opacity:.18;}
  50%{transform:translateX(60%) rotate(8deg);opacity:.48;}
}

.card-orbit{
  height:126px;
  border-radius:20px;
  border:1px solid rgba(255,255,255,.11);
  display:grid;
  place-items:center;
  background:radial-gradient(circle,rgba(255,255,255,.14),transparent 56%);
  color:rgba(255,255,255,.9);
  font-size:48px;
  font-weight:950;
  letter-spacing:-.05em;
  backdrop-filter:blur(2px);
}

.card-name{
  font-size:28px;
  line-height:1;
  font-weight:950;
  letter-spacing:-.035em;
  text-shadow:0 3px 20px rgba(0,0,0,.45);
}

.card-sub{
  margin-top:7px;
  color:#CBD5E1;
  font-size:13px;
  text-shadow:0 3px 14px rgba(0,0,0,.45);
}

.stamp{
  display:inline-flex;
  margin-top:14px;
  width:fit-content;
  padding:9px 11px;
  border-radius:13px;
  background:rgba(34,197,94,.20);
  border:1px solid rgba(34,197,94,.46);
  color:#BBF7D0;
  font-weight:950;
  font-size:12px;
  backdrop-filter:blur(8px);
}

/* dashboard cards */
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
  background:rgba(15,23,42,.74);
  border:1px solid rgba(148,163,184,.16);
  box-shadow:0 20px 55px rgba(0,0,0,.22);
  transition:transform .18s ease,border-color .18s ease,background .18s ease;
  backdrop-filter:blur(18px);
}

.kpi-card:hover{
  transform:translateY(-3px);
  border-color:rgba(56,189,248,.46);
  background:rgba(15,23,42,.90);
}

.kpi-card:after{
  content:"";
  position:absolute;
  right:-34px;
  top:-34px;
  width:92px;
  height:92px;
  border-radius:50%;
  background:rgba(56,189,248,.13);
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

/* signal */
.signal-card{
  border-radius:28px;
  padding:24px;
  background:linear-gradient(135deg,rgba(15,23,42,.95),rgba(2,6,23,.84));
  border:1px solid rgba(148,163,184,.18);
  box-shadow:0 28px 90px rgba(0,0,0,.32);
  margin:20px 0;
  backdrop-filter:blur(18px);
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
  filter:drop-shadow(0 0 24px rgba(34,197,94,.18));
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

/* analysis */
.reason-box,
.watch-card,
.prob-card{
  backdrop-filter:blur(18px);
}

.reason-box,
.watch-card{
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

/* footer */
.team-line-footer{
  margin-top:22px;
  padding:16px 18px;
  border-radius:22px;
  background:rgba(15,23,42,.70);
  border:1px solid rgba(148,163,184,.14);
  color:#CBD5E1;
  font-size:13px;
}

.team-line-footer b{
  color:#86EFAC;
}

@media(max-width:1000px){
  .hero-grid,
  .signal-grid{
    grid-template-columns:1fr;
  }

  .kpi-grid{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }

  .hero-title{
    font-size:42px;
  }

  .mock-card{
    width:270px;
  }
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_hero(
    records: int,
    best_model: str,
    player: str,
    card: str,
    year: int,
    grade: int,
    signal: str,
    score: int,
    card_image: Optional[str] = None,
) -> None:
    image_html = f'<img class="card-image" src="{card_image}" alt="{h(player)} {h(card)}">' if card_image else ""
    image_class = " has-card-image" if card_image else ""
    orbit_html = "" if card_image else f'<div class="card-orbit">{h(initials(player))}</div>'

    html = (
        f'<div class="hero"><div class="hero-grid"><div>'
        f'<div class="brand-lockup"><div class="logo-mark">◆</div><div>'
        f'<div class="brand-name">Resale Tracker</div>'
        f'<div class="brand-sub">Sports card comp scanner</div></div></div>'
        f'<div class="eyebrow">⚡ Live Card Value Scanner</div>'
        f'<div class="hero-title">Spot <span>underpriced cards</span> before other buyers do.</div>'
        f'<div class="hero-copy">Built for card flippers and collectors: compare a seller&apos;s asking price against recent comps, marketplace averages, recency-weighted value, and an AI buy/watch/avoid signal.</div>'
        f'<div class="pill-row">'
        f'<span class="pill">📊 {records:,} comp records</span>'
        f'<span class="pill">💰 Profit gap detection</span>'
        f'<span class="pill">🤖 {h(best_model)} classifier</span>'
        f'<span class="pill">📈 Live comp trend</span>'
        f'<span class="pill">🛒 Marketplace comparison</span>'
        f'</div>'
        f'<div class="pipeline">'
        f'<span class="pipe-node">Listing input</span><span class="pipe-arrow">→</span>'
        f'<span class="pipe-node">Recent comps</span><span class="pipe-arrow">→</span>'
        f'<span class="pipe-node">Weighted pricing</span><span class="pipe-arrow">→</span>'
        f'<span class="pipe-node">AI signal</span><span class="pipe-arrow">→</span>'
        f'<span class="pipe-node">Flip decision</span>'
        f'</div></div>'
        f'<div class="slab-wrap"><div class="mock-card">'
        f'<div class="card-art{image_class}">{image_html}'
        f'<div class="card-art-content">{orbit_html}<div>'
        f'<div class="card-name">{h(player)}</div>'
        f'<div class="card-sub">{h(card)} • {year}</div>'
        f'<div class="stamp">{h(signal.upper())} • {score}/100</div>'
        f'</div></div></div></div></div>'
        f'</div></div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str) -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{h(label)}</div>'
        f'<div class="kpi-value">{h(value)}</div>'
        f'<div class="kpi-sub">{h(sub)}</div>'
        f'</div>'
    )


def render_kpis(weighted: float, asking: float, upside: float, gap: float) -> None:
    st.markdown("### Resale Tracker Deal Dashboard")
    st.markdown(
        '<div class="kpi-grid">'
        + kpi_card("Estimated flip value", f"${weighted:,.2f}", "Recency-weighted market estimate")
        + kpi_card("Seller asking price", f"${asking:,.2f}", "Current listing price")
        + kpi_card("Potential profit", f"${upside:,.2f}", "Before fees, shipping, and tax")
        + kpi_card("Market gap", f"{gap:.2f}%", "Positive gap = below market")
        + "</div>",
        unsafe_allow_html=True,
    )


def render_signal_card(score_color: str, score: int, signal: str, deal_label: str, recommendation: str) -> None:
    html = (
        f'<div class="signal-card" style="border-color:{score_color};">'
        f'<div class="signal-grid"><div>'
        f'<div class="score-ring" style="background:conic-gradient({score_color} {score}%, rgba(148,163,184,.14) 0);">'
        f'<div class="score-inner"><div class="score-number">{score}</div></div></div>'
        f'<div style="text-align:center;color:#CBD5E1;font-weight:950;margin-top:8px;">Deal Score</div>'
        f'</div><div>'
        f'<div class="eyebrow" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:#E2E8F0;">AI Flip Signal</div>'
        f'<div class="signal-title">{h(signal)}</div>'
        f'<div class="signal-copy">Deal rating: <b style="color:white;">{h(deal_label)}</b> • Recommended action: <b style="color:white;">{h(recommendation)}</b></div>'
        f'<div class="signal-copy">The system checks seller price against recent comps, marketplace averages, recency-weighted value, and a machine-learning classifier.</div>'
        f'</div></div></div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def probability_bars(classes, probabilities) -> str:
    colors = {
        "Good Deal": "#22C55E",
        "Fair Price": "#FBBF24",
        "Overpriced": "#EF4444",
    }

    parts = ['<div class="prob-card">']

    for label, prob in sorted(zip(classes, probabilities), key=lambda item: item[1], reverse=True):
        percent = float(prob) * 100
        color = colors.get(label, "#38BDF8")

        parts.append(
            f'<div class="prob-row">'
            f'<div class="prob-top"><span>{h(label)}</span><span>{percent:.1f}%</span></div>'
            f'<div class="bar-bg">'
            f'<div class="bar-fill" style="width:{percent:.1f}%;background:linear-gradient(90deg,{color},#38BDF8);"></div>'
            f'</div>'
            f'</div>'
        )

    parts.append("</div>")
    return "".join(parts)


def reason_box(text: str) -> None:
    st.markdown(
        f'<div class="reason-box"><div class="reason-icon">✓</div><div class="reason-text">{h(text)}</div></div>',
        unsafe_allow_html=True,
    )


def watch_card(player: str, card_name: str, grade: int, gap_percent: float, weighted: float, latest: float) -> None:
    st.markdown(
        f'<div class="watch-card">'
        f'<div class="watch-top">'
        f'<div class="watch-title">{h(player)} — {h(card_name)} Grade {grade}</div>'
        f'<div class="watch-gap">{gap_percent:.1f}% gap</div>'
        f'</div>'
        f'<div class="muted">Weighted value ${weighted:,.2f} • Latest sample listing ${latest:,.2f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        '<div class="team-line-footer"><b>Resale Tracker</b> final project by '
        'Sharnpreet Sidhu · Ariful Shayun · Raj Chowdhury · Justin Huang.<br>'
        'Prototype note: the app uses real card identities with structured, price-guide-style sample comps. '
        'A production system would connect to verified sold-listing data sources or approved marketplace APIs.'
        '</div>',
        unsafe_allow_html=True,
    )