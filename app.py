from __future__ import annotations

import pandas as pd
import streamlit as st

from src.charts import confusion_matrix_chart, model_comparison_chart, site_comparison_chart, trend_chart
from src.config import APP_PLAYERS, DATA_FILE, DEFAULT_CARD, DEFAULT_GRADE, DEFAULT_PLAYER
from src.data_loader import load_resale_data
from src.modeling import train_and_compare_models
from src.pricing import (
    build_prediction_features,
    deal_score_from_gap,
    explain_recommendation,
    market_gap_percent,
    recommendation_from_label,
    signal_name,
    simple_average_price,
    summarize_market,
    volatility_percent,
    weighted_average_price,
)
from src.ui import (
    apply_global_styles,
    find_card_image,
    footer,
    probability_bars,
    reason_box,
    render_hero,
    render_kpis,
    render_signal_card,
    watch_card,
)


st.set_page_config(
    page_title="Resale Tracker",
    page_icon="💎",
    layout="wide",
)

apply_global_styles()


@st.cache_data
def get_data() -> pd.DataFrame:
    data = load_resale_data(DATA_FILE)
    # Final scope control: only the 13 chosen demo players appear in the app.
    data = data[data["player"].isin(APP_PLAYERS)].copy()
    return data


@st.cache_resource
def get_model_pack(data: pd.DataFrame) -> dict:
    return train_and_compare_models(data)


def ordered_players(data: pd.DataFrame) -> list[str]:
    players = [player for player in APP_PLAYERS if player in set(data["player"].unique())]
    extras = sorted(set(data["player"].unique()) - set(players))
    return players + extras


def filtered_for_search(data: pd.DataFrame, query: str) -> pd.DataFrame:
    query = query.strip()
    if not query:
        return data
    mask = (
        data["player"].str.contains(query, case=False, na=False)
        | data["card_name"].str.contains(query, case=False, na=False)
        | data["sport"].str.contains(query, case=False, na=False)
    )
    return data[mask].copy()


df = get_data()
model_pack = get_model_pack(df)
summary_df = summarize_market(df)



st.markdown(
    """
<div class="scan-shell">
  <div class="scan-badge">🔎 Search + scan panel</div>
  <div class="scan-title">Scan any card listing in seconds.</div>
  <div class="scan-copy">Search by player or card, choose grade, enter the seller's asking price, and Resale Tracker updates the card preview, comps, AI signal, and deal score instantly.</div>
</div>
""",
    unsafe_allow_html=True,
)

search_col, player_col, card_col, grade_col, price_col = st.columns([1.15, 1.05, 1.35, 0.55, 0.8], gap="medium")

with search_col:
    quick_search = st.text_input(
        "Quick search",
        value="",
        placeholder="Search Connor, Young Guns, Prizm...",
    )

filtered_df = filtered_for_search(df, quick_search)
if filtered_df.empty:
    st.warning("No matches found for that search. Showing the full 13-player dataset instead.")
    filtered_df = df

players = ordered_players(filtered_df)
player_index = players.index(DEFAULT_PLAYER) if DEFAULT_PLAYER in players else 0
with player_col:
    selected_player = st.selectbox("Player", players, index=player_index)

player_cards_df = filtered_df[filtered_df["player"] == selected_player]
if player_cards_df.empty:
    player_cards_df = df[df["player"] == selected_player]

cards = sorted(player_cards_df["card_name"].unique())
card_index = cards.index(DEFAULT_CARD) if selected_player == DEFAULT_PLAYER and DEFAULT_CARD in cards else 0
with card_col:
    selected_card = st.selectbox("Card", cards, index=card_index)

grades = sorted(df.loc[(df["player"] == selected_player) & (df["card_name"] == selected_card), "grade"].unique())
grade_index = grades.index(DEFAULT_GRADE) if DEFAULT_GRADE in grades else len(grades) - 1
with grade_col:
    selected_grade = int(st.selectbox("Grade", grades, index=grade_index))

matches = df[
    (df["player"] == selected_player)
    & (df["card_name"] == selected_card)
    & (df["grade"] == selected_grade)
].copy().sort_values("sale_date")

weighted_value = weighted_average_price(matches)
default_ask = float(max(1, weighted_value * 0.85))
price_key = f"asking_{selected_player}_{selected_card}_{selected_grade}"
with price_col:
    asking_price = float(
        st.number_input(
            "Seller ask ($)",
            min_value=1.0,
            value=round(default_ask, 2),
            step=5.0,
            key=price_key,
        )
    )

st.button("🚀 Run AI Deal Scan", use_container_width=True)

simple_value = simple_average_price(matches)
weighted_value = weighted_average_price(matches)
volatility = volatility_percent(matches)
gap = market_gap_percent(weighted_value, asking_price)
features = build_prediction_features(selected_grade, asking_price, matches)

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
card_image = find_card_image(selected_player, selected_card, selected_grade)

render_hero(
    records=len(df),
    best_model=model_pack["best_name"],
    player=selected_player,
    card=selected_card,
    year=year,
    grade=selected_grade,
    signal=signal,
    score=score,
    card_image=card_image,
)

render_kpis(weighted_value, asking_price, upside, gap)
render_signal_card(score_color, score, signal, deal_label, recommendation)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💸 Deal Analysis",
    "📈 Market Trend",
    "🛒 Marketplace Data",
    "🤖 Model Lab",
    "📁 Dataset",
])

with tab1:
    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.markdown('<div class="section-title">Why this could be a profitable flip</div>', unsafe_allow_html=True)
        for reason in explain_recommendation(deal_label, gap, simple_value, weighted_value, site_summary, volatility):
            reason_box(reason)

        st.markdown('<div class="section-title">Top opportunities watchlist</div>', unsafe_allow_html=True)
        opp = summary_df.copy()
        opp["sample_ask"] = opp["last_sale_price"]
        opp["gap_percent"] = (opp["weighted_market_value"] - opp["sample_ask"]) / opp["weighted_market_value"] * 100
        for _, row in opp.sort_values("gap_percent", ascending=False).head(5).iterrows():
            watch_card(
                player=row["player"],
                card_name=row["card_name"],
                grade=int(row["grade"]),
                gap_percent=float(row["gap_percent"]),
                weighted=float(row["weighted_market_value"]),
                latest=float(row["sample_ask"]),
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
        trend_chart(matches, simple_value, weighted_value, asking_price, f"{selected_player} — {selected_card} Grade {selected_grade}"),
        use_container_width=True,
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
        display = matches[["sale_date", "site", "sale_price", "rarity", "sport"]].copy()
        display["sale_date"] = display["sale_date"].dt.strftime("%Y-%m-%d")
        display["sale_price"] = display["sale_price"].map(lambda x: f"${x:,.2f}")
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.download_button(
            "Download selected comps",
            data=matches.to_csv(index=False).encode("utf-8"),
            file_name="selected_sales.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with right:
        st.markdown('<div class="section-title">Marketplace comparison</div>', unsafe_allow_html=True)
        st.plotly_chart(site_comparison_chart(site_summary), use_container_width=True)
        site_display = site_summary.copy()
        site_display["sale_price"] = site_display["sale_price"].map(lambda x: f"${x:,.2f}")
        st.dataframe(site_display.rename(columns={"site": "Marketplace", "sale_price": "Average sale price"}), use_container_width=True, hide_index=True)

with tab4:
    st.markdown('<div class="section-title">Model evaluation dashboard</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Best model", model_pack["best_name"])
    m2.metric("Training examples", f"{len(model_pack['training_df']):,}")
    m3.metric("Best accuracy", f"{max(model_pack['scores'].values()) * 100:.2f}%")
    m4.metric("Features", len(model_pack["feature_columns"]))

    left, right = st.columns(2, gap="large")
    with left:
        st.plotly_chart(model_comparison_chart(model_pack["scores"]), use_container_width=True)
    with right:
        st.plotly_chart(confusion_matrix_chart(model_pack["confusion_matrix"], model_pack["labels"]), use_container_width=True)
    st.caption("High accuracy is expected because prototype labels are generated from pricing thresholds. This demonstrates the end-to-end ML pipeline: feature creation, model training, evaluation, and prediction.")

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
    st.download_button("Download full dataset", data=df.to_csv(index=False).encode("utf-8"), file_name="resale_data.csv", mime="text/csv", use_container_width=True)

footer()
