from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
    fig.add_hline(y=weighted, line_dash="dash", line_color="#22C55E", annotation_text=f"Weighted ${weighted:,.2f}")
    fig.add_hline(y=simple, line_dash="dot", line_color="#A78BFA", annotation_text=f"Avg ${simple:,.2f}")
    fig.add_hline(y=asking, line_dash="dash", line_color="#FBBF24", annotation_text=f"Ask ${asking:,.2f}")
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


def site_comparison_chart(site_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        site_summary,
        x="site",
        y="sale_price",
        text=site_summary["sale_price"].map(lambda x: f"${x:,.0f}"),
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


def confusion_matrix_chart(cm: np.ndarray, labels: list[str]) -> go.Figure:
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        colorscale="Greens",
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16, "color": "white"},
    ))
    fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.38)",
        xaxis_title="Predicted",
        yaxis_title="Actual",
    )
    return fig


def model_comparison_chart(scores: dict[str, float]) -> go.Figure:
    score_df = pd.DataFrame({"Model": list(scores.keys()), "Accuracy": [v * 100 for v in scores.values()]})
    fig = px.bar(score_df, x="Model", y="Accuracy", text=score_df["Accuracy"].map(lambda x: f"{x:.1f}%"))
    fig.update_traces(marker_color=["#A78BFA", "#22C55E"], textposition="outside")
    fig.update_layout(
        template="plotly_dark",
        height=330,
        yaxis_range=[0, 105],
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.38)",
        showlegend=False,
    )
    return fig
