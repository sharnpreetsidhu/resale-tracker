# Real data guide

This project includes real card identities and realistic price-guide-style baseline values, then generates many comparable-sale rows around those baselines for a reproducible AI prototype.

For a production-quality dataset, replace or extend `data/resale_data.csv` with verified sold-listing data.

## Recommended manual collection fields

Keep these columns:

```text
sale_id,player,year,card_name,sport,grade,rarity,autograph,rookie_card,condition,sale_price,site,sale_date,baseline_psa9_value,value_note
```

## Good verified comp sources to use manually

- eBay sold listings
- 130point sold listing search
- Card Ladder / price-guide exports if available
- PWCC / Goldin public auction results
- Your own manually verified marketplace comps

## Important

Only label data as verified if your group actually verified the sold listing. Otherwise describe it as structured sample/prototype data.
