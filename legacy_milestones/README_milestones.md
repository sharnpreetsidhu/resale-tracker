# Resale Tracker Milestone 1

This is the basic Milestone 1 version of the AI-powered resale market tracker.

## What it does

- Loads sample trading card sale data from `resale_data.csv`
- Lets the user enter a card/player/grade and asking price
- Calculates estimated market value using the average of recent sale prices
- Classifies the listing as Good Deal, Fair Price, or Overpriced
- Gives a simple recommendation: Buy, Hold / Consider, or Avoid

## How to run in VS Code

1. Open this folder in VS Code.
2. Make sure Python is installed.
3. Open the terminal in VS Code.
4. Install pandas if needed:

```bash
pip install pandas
```

5. Run:

```bash
python milestone1_tracker.py
```

## Example input

Player name: Connor Bedard  
Card name: Young Guns  
Grade: 9  
Asking price: 190  

## Example output

Estimated Market Value: $225.00  
Asking Price: $190.00  
Difference From Market: 15.56%  
Deal Rating: Good Deal  
Recommendation: Buy  


AI Resale Market Tracker - Milestone 2

Files:
- resale_data.csv: expanded resale dataset
- milestone1_tracker.py: baseline price estimator from Milestone 1
- milestone2_model.py: Decision Tree deal classification model
- milestone2_graph.py: recent sale price trend graph
- milestone2_app.py: Streamlit website interface

How to run:
1. Install dependencies:
   pip install pandas matplotlib scikit-learn streamlit

2. Run ML model:
   python milestone2_model.py

3. Run website:
   streamlit run milestone2_app.py