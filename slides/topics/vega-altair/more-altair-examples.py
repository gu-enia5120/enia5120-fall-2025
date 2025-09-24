# %%
import altair as alt
import pandas as pd
from vega_datasets import data

# alt.data_transformers.enable('json')

# https://stackoverflow.com/questions/59224026/how-to-add-a-slider-to-a-choropleth-in-altair
us_counties = alt.topo_feature(data.us_10m.url, "counties")
fdf = pd.read_csv(
    "https://raw.githubusercontent.com/sdasara95/Opioid-Crisis/master/sample_data.csv"
)
fdf["year"] = fdf["year"].astype(str)
fdf = fdf.pivot(index="fips", columns="year", values="Pill_per_pop").reset_index()
columns = [str(year) for year in range(2006, 2013)]

slider = alt.binding_range(min=2006, max=2012, step=1)
select_year = alt.selection_single(
    name="year", fields=["year"], bind=slider, init={"year": 2006}
)

alt.Chart(us_counties).mark_geoshape(stroke="black", strokeWidth=0.05).project(
    type="albersUsa"
).transform_lookup(
    lookup="id", from_=alt.LookupData(fdf, "fips", columns)
).transform_fold(
    columns, as_=["year", "Pill_per_pop"]
).transform_calculate(
    year="parseInt(datum.year)",
    Pill_per_pop="isValid(datum.Pill_per_pop) ? datum.Pill_per_pop : -1",
).encode(
    color=alt.condition(
        "datum.Pill_per_pop > 0",
        alt.Color("Pill_per_pop:Q", scale=alt.Scale(scheme="blues")),
        alt.value("#dbe9f6"),
    )
).add_selection(
    select_year
).properties(
    width=700, height=400
).transform_filter(
    select_year
)

# %%

# https://matthewkudija.com/blog/2018/06/22/altair-interactive/

cars = data.cars.url

# define selection
click = alt.selection_multi(encodings=["color"])

# scatter plots of points
scatter = (
    alt.Chart(cars)
    .mark_circle()
    .encode(
        x="Horsepower:Q",
        y="Miles_per_Gallon:Q",
        size=alt.Size("Cylinders:O", scale=alt.Scale(range=(20, 100))),
        color=alt.Color("Origin:N", legend=None),
        tooltip=[
            "Name:N",
            "Horsepower:Q",
            "Miles_per_Gallon:Q",
            "Cylinders:O",
            "Origin:N",
        ],
    )
    .transform_filter(click)
    .interactive()
)

# legend
legend = (
    alt.Chart(cars)
    .mark_rect()
    .encode(
        y=alt.Y("Origin:N", axis=alt.Axis(title="Select Origin")),
        color=alt.condition(click, "Origin:N", alt.value("lightgray"), legend=None),
        size=alt.value(250),
    )
    .properties(selection=click)
)

chart = scatter | legend
chart
# %%

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(
    type="single", nearest=True, on="mouseover", fields=["date"], empty="none"
)

# The basic line
line = (
    alt.Chart()
    .mark_line(interpolate="basis")
    .encode(
        alt.X("date:T", axis=alt.Axis(title="")),
        alt.Y("price:Q", axis=alt.Axis(title="", format="$f")),
        color="symbol:N",
    )
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = (
    alt.Chart()
    .mark_point()
    .encode(
        x="date:T",
        opacity=alt.value(0),
    )
    .add_selection(nearest)
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align="left", dx=5, dy=-5).encode(
    text=alt.condition(nearest, "price:Q", alt.value(" "))
)

# Draw a rule at the location of the selection
rules = (
    alt.Chart()
    .mark_rule(color="gray")
    .encode(
        x="date:T",
    )
    .transform_filter(nearest)
)

# Put the five layers into a chart and bind the data
stockChart = alt.layer(
    line,
    selectors,
    points,
    rules,
    text,
    data="https://raw.githubusercontent.com/altair-viz/vega_datasets/master/vega_datasets/_data/stocks.csv",
    width=600,
    height=300,
    title="Stock History",
)
stockChart

# %%
# http://vega.github.io/vega-tutorials/airports/

states = alt.topo_feature(data.us_10m.url, feature="states")
airports = data.airports.url

# US states background
background = (
    alt.Chart(states)
    .mark_geoshape(
        fill="lightgray",
        stroke="white",
    )
    .properties(width=800, height=500)
    .project("albersUsa")
)

# airport positions on background
points = (
    alt.Chart(airports)
    .mark_circle()
    .encode(
        longitude="longitude:Q",
        latitude="latitude:Q",
        size=alt.value(15),
        color=alt.value("#3377B3"),
        tooltip=["iata:N", "name:N", "city:N", "state:N", "latitude:Q", "longitude:Q"],
    )
)

chart = background + points
chart

# %%

# birdstrikes = data.birdstrikes.url
color = alt.Color("Wildlife__Species:N")

# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_multi(encodings=["color"])

# Top panel is scatter plot of temperature vs time
points = (
    alt.Chart()
    .mark_circle()
    .encode(
        alt.X("yearmonthdate(Flight_Date):T", axis=alt.Axis(title="Date")),
        alt.Y(
            "Speed_IAS_in_knots:Q",
            axis=alt.Axis(title="Indicated Airspeed (kts)"),
        ),
        color=alt.condition(brush, color, alt.value("lightgray")),
        tooltip=[
            "Airport__Name:N",
            "Aircraft__Make_Model:N",
            "Flight_Date:T",
            "When__Phase_of_flight:N",
            "Wildlife__Species:N",
            "Speed_IAS_in_knots:Q",
        ],
    )
    .properties(width=600, height=300)
    .add_selection(brush)
    .transform_filter(click)
)

# Bottom panel is a bar chart of species
bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        alt.Y("count()", scale=alt.Scale(type="log")),
        alt.X(
            "Wildlife__Species:N",
            sort=alt.SortField(field="sort_order", op="count", order="descending"),
        ),
        color=alt.condition(click, color, alt.value("lightgray")),
    )
    .transform_filter(brush)
    .properties(
        width=600,
    )
    .add_selection(click)
)

alt.vconcat(
    points, bars, data=data.birdstrikes.url, title="Aircraft Birdstrikes: 1990-2003"
)
# %%

# https://towardsdatascience.com/altair-statistical-visualization-library-for-python-part-3-c1e650a8411e

cols = [
    "Attrition_Flag",
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Credit_Limit",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
]
churn = pd.read_csv("BankChurners.csv", usecols=cols).sample(n=1000)
churn.head()

selection = alt.selection(type="interval")

plt1 = (
    alt.Chart(churn)
    .mark_circle(size=50)
    .encode(
        x="Credit_Limit",
        y="Total_Trans_Amt",
        color=alt.condition(selection, "Gender", alt.value("lightgray")),
    )
    .add_selection(selection)
)
plt2 = (
    alt.Chart(churn)
    .mark_bar()
    .encode(y="Gender", x="count(Gender):Q", color="Gender")
    .transform_filter(selection)
)

plt1 & plt2
# %%

selection = alt.selection(type="interval")
plt1 = (
    alt.Chart()
    .mark_circle(size=50)
    .encode(x="Credit_Limit", y="Total_Trans_Amt", color="Gender")
    .transform_filter(selection)
)
plt2 = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="Marital_Status",
        y="mean(Total_Trans_Amt):Q",
        color=alt.condition(selection, alt.value("lightblue"), alt.value("lightgray")),
    )
    .properties(height=300, width=200)
    .add_selection(selection)
)

alt.hconcat(plt1, plt2, data=churn)

# %%

selection = alt.selection_multi(fields=["Education_Level"], bind="legend")

(
    alt.Chart(churn)
    .mark_circle(size=50)
    .encode(
        x="Total_Trans_Ct",
        y="Total_Trans_Amt",
        color=alt.Color("Education_Level:N", scale=alt.Scale(scheme="category20b")),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    )
    .properties(height=400, width=500)
    .add_selection(selection)
)
# %%
# https://stackoverflow.com/questions/64486472/altair-how-do-i-get-the-values-from-a-dropdown-menu


df = pd.DataFrame(
    {
        "x": np.random.randn(100),
        "y": np.random.randn(100),
        "c1": np.random.randint(0, 3, 100),
        "c2": np.random.randint(0, 3, 100),
        "c3": np.random.randint(0, 3, 100),
    }
)

selector = alt.selection_single(
    name="Color by",
    fields=["column"],
    bind=alt.binding_select(options=["c1", "c2", "c3"]),
    init={"column": "c1"},
)

alt.Chart(df).transform_fold(
    ["c1", "c2", "c3"], as_=["column", "value"]
).transform_filter(selector).mark_point().encode(
    x="x:Q", y="y:Q", color="value:Q", column="column:N"
).add_selection(
    selector
)

# %%

import numpy as np

df = pd.DataFrame(
    {
        "x": np.random.randn(100),
        "y": np.random.randn(100),
        "c1": np.random.randint(0, 3, 100),
        "c2": np.random.randint(0, 3, 100),
        "c3": np.random.randint(0, 3, 100),
    }
)

selector = alt.selection_single(
    name="Color by",
    fields=["column"],
    bind=alt.binding_select(options=["c1", "c2", "c3"]),
    init={"column": "c1"},
)

alt.Chart(df).transform_fold(
    ["c1", "c2", "c3"], as_=["column", "value"]
).transform_filter(selector).mark_point().encode(
    x="x:Q", y="y:Q", color="value:Q", column="column:N"
).add_selection(
    selector
)
# %%
