# Resale Tracker

**Resale Tracker** is an AI-powered trading card resale dashboard built by:

- Sharnpreet Sidhu
- Ariful Shayun
- Raj Chowdhury
- Justin Huang

The app helps a reseller enter a card listing, compare it against recent comparable sales, estimate a recency-weighted market value, classify the listing as **Good Deal / Fair Price / Overpriced**, and show a **Buy / Watch / Avoid** recommendation.

## Final project features

- Polished Streamlit web app with a modern dark 3D/glass UI
- Main visible search/scanner panel, so the inputs are not hidden if the sidebar is collapsed
- Defaults to **Connor Bedard — Upper Deck Young Guns RC — Grade 9** on first load
- Dynamic card preview that changes based on the selected player/card
- Animated card preview with optional real card images in `assets/card_images/`
- Dataset with **9,720 comparable-sale rows** across **27 real card identities** and **13 selected players**
- Recency-weighted market value calculation
- Potential profit, market gap, deal score, and AI flip signal
- Decision Tree vs Random Forest model comparison
- Confusion matrix and model evaluation dashboard
- Marketplace comparison and downloadable filtered comps
- Modular source code in `src/`

## How to run

```bash
pip install -r requirements.txt
python train_eval.py
streamlit run app.py
```

## Project structure

```text
app.py
generate_dataset.py
train_eval.py
requirements.txt
README.md
CARD_IMAGE_SHOT_LIST.md

data/
  resale_data.csv
  card_value_baselines.csv

assets/
  brand/resale_tracker_logo.svg
  card_images/

src/
  config.py
  data_loader.py
  pricing.py
  modeling.py
  charts.py
  ui.py
```

## Important data note

The included dataset uses **real trading card identities** and realistic price-guide-style baseline values, then generates comparable-sale variation around those baselines so the AI pipeline can be tested with thousands of rows.

Do not describe every row as a verified live sale. For a production version, replace or extend `data/resale_data.csv` with verified sold-listing data from approved marketplace sources or APIs.

## Adding card images

Put raw front images in:

```text
assets/card_images/
```

Use filenames from `CARD_IMAGE_SHOT_LIST.md`.

Examples:

```text
assets/card_images/connor-bedard-upper-deck-young-guns-rc.png
assets/card_images/lebron-james-topps-chrome-rookie.png
assets/card_images/victor-wembanyama-panini-prizm-rookie.png
```

JPG works too. The same raw card image is used for all grades unless you add a grade-specific image like:

```text
connor-bedard-upper-deck-young-guns-rc-g10.png
```
