#%% 

import pandas as pd
import altair as alt
# %%

wine = pd.read_csv("~/Downloads/wines_SPA.csv")

#%%
wine.describe


#%%
alt.Chart(wine).mark_bar().encode(
    x="region",
    y=
    )

#%%
(
alt
.Chart(wine.groupby('region').size().reset_index(name='count'))
.encode(x='region', y='count').mark_bar()
)

# there are 76 regions - too many values 

#%%

# this produces an error
# using the transformation

alt.Chart(wine).mark_bar().encode(
    x='region', y='count()'
    )


#%%
lego_stats = pd.read_parquet(
        "https://github.com/anly503/datasets/raw/main/year_stats_tbl.parquet"
)

#%%
lego_stats.head()


