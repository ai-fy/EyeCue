import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS
from vega_datasets import data

ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
st.title("Plotting Fun")

# Generating Data
source = pd.DataFrame({
    'Trial A': np.random.normal(0, 0.8, 1000),
    'Trial B': np.random.normal(-2, 1, 1000),
    'Trial C': np.random.normal(3, 2, 1000)
})

c = alt.Chart(source).transform_fold(
    ['Trial A', 'Trial B', 'Trial C'], as_=['Experiment', 'Measurement']).mark_bar(
        opacity=0.3, binSpacing=0).encode(
            alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
            alt.Y('count()', stack=None), alt.Color('Experiment:N'))
print(source)
st.altair_chart(c)

source = data.movies.url

pts = alt.selection(type="single", encodings=['x'])

rect = alt.Chart(data.movies.url).mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    alt.Color(
        'count()', scale=alt.Scale(scheme='greenblue'), legend=alt.Legend(title='Total Records')))

circ = rect.mark_point().encode(
    alt.ColorValue('grey'),
    alt.Size('count()', legend=alt.Legend(title='Records in Selection'))).transform_filter(pts)

bar = alt.Chart(source).mark_bar().encode(
    x='Major_Genre:N',
    y='count()',
    color=alt.condition(pts, alt.ColorValue("steelblue"), alt.ColorValue("grey"))).properties(
        width=550, height=200).add_selection(pts)

st.altair_chart(
    alt.vconcat(rect + circ, bar).resolve_legend(color="independent", size="independent"))

source = data.cars()

st.altair_chart(
    alt.Chart(source).mark_circle().encode(
        alt.X(alt.repeat("column"), type='quantitative'),
        alt.Y(alt.repeat("row"), type='quantitative'),
        color='Origin:N').properties(width=150, height=150).repeat(
            row=['Horsepower', 'Acceleration', 'Miles_per_Gallon'],
            column=['Miles_per_Gallon', 'Acceleration', 'Horsepower']).interactive())

source = data.cars()

# Configure the options common to all layers
brush = alt.selection(type='interval')
base = alt.Chart(source).add_selection(brush)

# Configure the points
points = base.mark_point().encode(
    x=alt.X('Miles_per_Gallon', title=''),
    y=alt.Y('Horsepower', title=''),
    color=alt.condition(brush, 'Origin', alt.value('grey')))

# Configure the ticks
tick_axis = alt.Axis(labels=False, domain=False, ticks=False)

x_ticks = base.mark_tick().encode(
    alt.X('Miles_per_Gallon', axis=tick_axis),
    alt.Y('Origin', title='', axis=tick_axis),
    color=alt.condition(brush, 'Origin', alt.value('lightgrey')))

y_ticks = base.mark_tick().encode(
    alt.X('Origin', title='', axis=tick_axis),
    alt.Y('Horsepower', axis=tick_axis),
    color=alt.condition(brush, 'Origin', alt.value('lightgrey')))

# Build the chart
st.altair_chart(y_ticks | (points & x_ticks))

source = data.stocks()

st.altair_chart(
    alt.Chart(source).transform_filter('datum.symbol==="GOOG"').mark_area(
        line={
            'color': 'darkgreen'
        },
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='darkgreen', offset=1)
            ],
            x1=1,
            x2=1,
            y1=1,
            y2=0)).encode(alt.X('date:T'), alt.Y('price:Q')))

source = data.unemployment_across_industries.url

base = alt.Chart(source).mark_area(
    color='goldenrod', opacity=0.3).encode(
        x='yearmonth(date):T',
        y='sum(count):Q',
    )

brush = alt.selection_interval(encodings=['x'], empty='all')
background = base.add_selection(brush)
selected = base.transform_filter(brush).mark_area(color='goldenrod')

st.altair_chart(background + selected)

airports = data.airports.url
states = alt.topo_feature(data.us_10m.url, feature='states')

# US states background
background = alt.Chart(states).mark_geoshape(
    fill='lightgray', stroke='white').properties(
        width=500, height=300).project('albersUsa')

# airport positions on background
points = alt.Chart(airports).transform_aggregate(
    latitude='mean(latitude)', longitude='mean(longitude)', count='count()',
    groupby=['state']).mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.Size('count:Q', title='Number of Airports'),
        color=alt.value('steelblue'),
        tooltip=['state:N', 'count:Q']).properties(title='Number of airports in US')

st.altair_chart(background + points)
