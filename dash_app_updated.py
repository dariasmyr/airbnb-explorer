import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from modules.database_repository import Database
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css?family=Roboto+Slab&display=swap",
]

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, "
                       "initial-scale=1.0, "
                       "maximum-scale=1.2, "
                       "minimum-scale=0.5,",
        }
    ],
)

# Initialize the database connection
database = Database("sqlite+pysqlite:///:/../data/database.sqlite3")
database.connect()

# Define the color scheme and shared visual properties
colors = {
    "background": "#ffffff",
    "text": "#444444",
    "accent": "#008080",
    "neighbourhood_group": {
        "Manhattan": "blue",
        "Brooklyn": "green",
        "Queens": "red",
        "Staten Island": "purple",
        "Bronx": "orange",
    },
}

style = {
    "page": {
        "backgroundColor": colors["background"],
        "boxShadow": "0px 0px 20px 0px rgba(0,0,0,0.05)",
        "border-radius": "20px",
        "fontFamily": "Roboto Slab, sans-serif",
    },
    "title": {
        "font": {
            "size": 20,
            "color": colors["text"],
            "family": "Roboto Slab, sans-serif",
        },
        "x": 0.5,
        "y": 0.9,
    },
    "axis_title": {
        "font": {
            "size": 18,
            "color": colors["text"],
            "family": "Roboto Slab, sans-serif",
        },
    },
    "text": {
        "color": colors["text"],
        "font": {"size": 24, "family": "Roboto Slab, sans-serif"},
    },
    "h1": {
        "textAlign": "left",
        "color": colors["text"],
        "font": {"size": 48, "weight": "bold", "family": "Roboto Slab, sans-serif"},
        "padding": "40px 0px 10px 20px",
    },
    "h2": {
        "textAlign": "left",
        "color": colors["text"],
        "font": {"size": 36, "weight": "bold", "family": "Roboto Slab, sans-serif"},
        "padding": "15px 0px 15px 20px",
    },
    "h3": {
        "textAlign": "left",
        "color": colors["text"],
        "font": {"size": 24, "weight": "bold", "family": "Roboto Slab, sans-serif"},
        "padding": "0px 0px 10px 20px",
    },
    "p": {"textAlign": "left", "padding": "0px 0px 10px 20px"},
    "graph": {"padding": "0px 20px 20px 20px", "width": "100%", "height": "400px"},
    "dropdown": {"padding": "0px 20px 20px 20px"},
}

df = database.get_dataframe()

mean_price_per_neighbourhood = (
    df.groupby("neighbourhood_group")["price"].mean().sort_values(ascending=False)
)

mean_price_per_neighbourhood_fig = px.bar(
    mean_price_per_neighbourhood,
    x=mean_price_per_neighbourhood.values,
    y=mean_price_per_neighbourhood.index,
    orientation="h",
    color_discrete_sequence=[colors["accent"]],
)

mean_price_per_neighbourhood_fig.update_layout(
    title={"text": "Average price", **style["title"]},
    xaxis_title={"text": "Price", **style["axis_title"]},
    yaxis_title={"text": "Neighbourhood group", **style["axis_title"]},
    yaxis_range=[
        mean_price_per_neighbourhood.index[-1],
        mean_price_per_neighbourhood.index[0],
    ],
    margin=dict(t=100),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
)

numeric_cols = [
    "price",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "availability_365",
]

correlation_with_price = df[numeric_cols].corr()["price"].sort_values(ascending=False)

correlation_with_price_fig = px.bar(
    correlation_with_price,
    x=correlation_with_price.values,
    y=correlation_with_price.index,
    orientation="h",
    color_discrete_sequence=[colors["accent"]],
)

correlation_with_price_fig.update_layout(
    title={"text": "Correlation with price", **style["title"]},
    xaxis_title={"text": "Correlation", **style["axis_title"]},
    yaxis_title={"text": "Feature", **style["axis_title"]},
    yaxis_range=[correlation_with_price.index[-1], correlation_with_price.index[0]],
    margin=dict(t=100),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
)

parallel_coordinates_fig = px.parallel_coordinates(
    df,
    dimensions=numeric_cols,
    color='price',
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=2,
)

parallel_coordinates_fig.update_layout(
    title={"text": "Parallel coordinates", **style["title"]},
    margin=dict(t=100),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
)

percentage_of_available_listings_from_each_neighbourhood_group = (
    df.groupby("neighbourhood_group")["minimum_nights"]
    .apply(lambda x: (x >= 10).sum() / len(x) * 100)
    .sort_values(ascending=False)
)

percentage_of_available_listings_from_each_neighbourhood_group_fig = px.bar(
    percentage_of_available_listings_from_each_neighbourhood_group,
    x=percentage_of_available_listings_from_each_neighbourhood_group.values,
    y=percentage_of_available_listings_from_each_neighbourhood_group.index,
    orientation="h",
    color_discrete_sequence=[colors["accent"]],
)

percentage_of_available_listings_from_each_neighbourhood_group_fig.update_layout(
    title={"text": "Available listings", **style["title"]},
    xaxis_title={"text": "Percentage", **style["axis_title"]},
    yaxis_title={"text": "Neighbourhood group", **style["axis_title"]},
    yaxis_range=[
        percentage_of_available_listings_from_each_neighbourhood_group.index[-1],
        percentage_of_available_listings_from_each_neighbourhood_group.index[0],
    ],
    margin=dict(t=100),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
)

hosts_with_multiple_listings = df.groupby("host_name")["host_id"].count()

top_hosts = hosts_with_multiple_listings.nlargest(10)

top_hosts_fig = px.bar(
    top_hosts,
    x=top_hosts.values,
    y=top_hosts.index,
    orientation="h",
    color_discrete_sequence=[colors["accent"]],
)

top_hosts_fig.update_layout(
    title={"text": "Top hosts", **style["title"]},
    xaxis_title={"text": "Number of listings", **style["axis_title"]},
    yaxis_title={"text": "Host name", **style["axis_title"]},
    yaxis_range=[top_hosts.index[-1], top_hosts.index[0]],
    margin=dict(t=100),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
)

mean_price_per_neighbourhood_group = (
    df.groupby(["neighbourhood_group", "last_review", "room_type"])["price"]
    .mean()
    .reset_index()
)
mean_price_per_neighbourhood_group["last_review"] = pd.to_datetime(
    mean_price_per_neighbourhood_group["last_review"]
)
mean_price_per_neighbourhood_group = mean_price_per_neighbourhood_group.set_index(
    "last_review"
)

# resample the data to group by month and calculate the mean price
mean_price_per_neighbourhood_group = (
    mean_price_per_neighbourhood_group.groupby(["neighbourhood_group", "room_type"])
    .resample("Y")
    .mean(numeric_only=True)
    .reset_index()
)


@app.callback(
    Output("mean_price_per_neighbourhood_group_fig", "figure"),
    Input("room_type_dropdown", "value"),
)
def update_mean_price_per_neighbourhood_group(room_type):
    filtered_df = mean_price_per_neighbourhood_group[
        mean_price_per_neighbourhood_group["room_type"] == room_type
        ]
    fig = px.line(
        filtered_df,
        x="last_review",
        y="price",
        color="neighbourhood_group",
        color_discrete_map=colors["neighbourhood_group"],
    )
    fig.update_layout(
        title={"text": "Price dynamics", **style["title"]},
        xaxis_title={"text": "Last review", **style["axis_title"]},
        yaxis_title={"text": "Price", **style["axis_title"]},
        margin=dict(t=100),
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        showlegend=False,
    )
    return fig


# Define the average data for each neighborhood group
average_data = (
    df.groupby(["neighbourhood_group", "neighbourhood"])
    .mean(numeric_only=True)
    .reset_index()
)

# Filter the data to only include NYC neighborhoods and the average data
nyc_data = average_data[
    average_data["neighbourhood_group"].isin(
        ["Manhattan", "Brooklyn", "Queens", "Staten Island", "Bronx"]
    )
].copy()


@app.callback(
    Output("nyc_map", "figure"), Input("nyc_map_neighbourhood_group_dropdown", "value")
)
def update_nyc_map(neighbourhood_group):
    filtered_df = nyc_data[nyc_data["neighbourhood_group"] == neighbourhood_group]
    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        size="price",
        color="neighbourhood_group",
        hover_name="neighbourhood",
        color_discrete_map=colors["neighbourhood_group"],
        size_max=15,
        center={"lat": 40.7128, "lon": -74.0060},
        opacity=0.7,
        zoom=10,
    )
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        showlegend=False,
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig


top_most_reviewed_listings = (
    df.groupby(["neighbourhood_group", "name", "price"])["number_of_reviews"]
    .sum()
    .sort_values(ascending=False)
    .groupby("neighbourhood_group")
    .head(3)
    .reset_index()
)


@app.callback(
    Output("top_most_reviewed_listings_fig", "figure"),
    Input("most_reviewed_listings_neighbourhood_group_dropdown", "value"),
)
def update_top_most_reviewed_listings(neighbourhood_group):
    filtered_df = top_most_reviewed_listings[
        top_most_reviewed_listings["neighbourhood_group"] == neighbourhood_group
        ]
    fig = px.scatter(
        filtered_df,
        x="number_of_reviews",
        y="price",
        size="number_of_reviews",
        color="neighbourhood_group",
        hover_name="name",
        color_discrete_map=colors["neighbourhood_group"],
        size_max=60,
    )
    fig.update_layout(
        title={"text": "Top 3 most reviewed listings", **style["title"]},
        xaxis_title={"text": "Number of reviews", **style["axis_title"]},
        yaxis_title={"text": "Price", **style["axis_title"]},
        margin=dict(t=100),
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        showlegend=False,
    )
    return fig


app.layout = dbc.Container(
    style=style["page"],
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            children="Welcome to the Airbnb Explorer!",
                            style=style["h1"],
                        ),
                        html.P(
                            children="The Airbnb Explorer project aims to provide users with insights into Airbnb "
                                     "listings in New "
                                     "York City. "
                                     "By analyzing data on Airbnb listings, this project helps users find the perfect rental "
                                     "for "
                                     "their needs.",
                            style=style["p"],
                        ),
                    ],
                    width={"size": 12},
                ),
            ],
            justify="left",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(children="Map", style=style["h2"]),
                        html.H3(
                            children="Airbnb listings in New York City",
                            style=style["h3"],
                        ),
                        html.P(
                            children="The map below shows the location of all Airbnb listings in New York City. "
                                     "The size of the marker indicates the price of the listing. "
                                     "The colour of the marker indicates the neighbourhood group the listing is in. "
                                     "Hovering over the marker shows more information about the listing.",
                            style=style["p"],
                        ),
                        dcc.Dropdown(
                            id="nyc_map_neighbourhood_group_dropdown",
                            options=[
                                {
                                    "label": neighbourhood_group,
                                    "value": neighbourhood_group,
                                }
                                for neighbourhood_group in df[
                                    "neighbourhood_group"
                                ].unique()
                            ],
                            value=df["neighbourhood_group"].unique()[0],
                            style=style["dropdown"],
                            clearable=False,
                        ),
                        dcc.Graph(id="nyc_map", style=style["graph"]),
                    ],
                    width={"size": 12},
                )
            ],
            justify="left",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(children="Price", style=style["h2"]),
                    ],
                    width={"size": 12},
                )
            ],
            justify="left",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(
                            children="Mean price per neighbourhood group",
                            style=style["h3"],
                        ),
                        html.P(
                            children="The average price of Airbnb listings in each neighbourhood group is shown in "
                                     "the graph "
                                     "below. "
                                     "The most expensive neighbourhood group is Manhattan, followed by Brooklyn and Queens. "
                                     "The cheapest neighbourhood group is Bronx.",
                            style=style["p"],
                        ),
                        dcc.Graph(
                            id="mean_price_per_neighbourhood",
                            figure=mean_price_per_neighbourhood_fig,
                            style=style["graph"],
                        ),
                    ],
                    xs=10,
                    sm=8,
                    md=5,
                    lg=6,
                    xl=5,
                ),
                dbc.Col(
                    [
                        html.H3(children="Correlation with price", style=style["h3"]),
                        html.P(
                            children="The correlation between the price of an Airbnb listing and other features is "
                                     "shown in the "
                                     "graph below. "
                                     "The most important features for determining the price of an Airbnb listing are "
                                     "the number "
                                     "of reviews, the availability of the listing, and the number of reviews per "
                                     "month. "
                                     "The least important feature is the minimum number of nights.",
                            style=style["p"],
                        ),
                        dcc.Graph(
                            id="correlation_with_price",
                            figure=correlation_with_price_fig,
                            style=style["graph"],
                        ),
                    ],
                    xs=10,
                    sm=8,
                    md=5,
                    lg=6,
                    xl=5,
                ),
            ],
            justify="left",
        ),
        dbc.Row(
            [
                dbc.Col(
[
                        html.H3(children="Parallel correlation", style=style["h3"]),
                        html.P(
                            children="The correlation between the price of a listing and the other features is "
                                     "shown in the "
                                     "graph below. "
                                     "The features are grouped into 3 categories: "
                                     "location, property and host. "
                                     "The correlation between the price and the features in each category is shown in "
                                     "parallel. ",
                            style=style["p"],
                        ),
                        dcc.Graph(
                            id="parallel_coordinates_fig",
                            figure=parallel_coordinates_fig,
                            style=style["graph"],
                        ),
                    ],
                ),
            ], justify="left",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(children="Price dynamics", style=style["h3"]),
                        html.P(
                            children="The price dynamics of listings in each neighbourhood group per year are shown in "
                                     "the graph below.",
                            style=style["p"],
                        ),
                        dcc.Dropdown(
                            id="room_type_dropdown",
                            options=[
                                {"label": room_type, "value": room_type}
                                for room_type in df["room_type"].unique()
                            ],
                            value=df["room_type"].unique()[0],
                            style=style["dropdown"],
                            clearable=False,
                        ),
                        dcc.Graph(
                            id="mean_price_per_neighbourhood_group_fig",
                            style=style["graph"],
                        ),
                    ]
                ),
            ],
            justify="left",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(children="Availability", style=style["h2"]),
                        html.H3(
                            children="Percentage of available listings",
                            style=style["h3"],
                        ),
                        html.P(
                            children="The percentage of available listings from each neighbourhood group is shown in the graph "
                                     "below. "
                                     "The neighbourhood group with the highest percentage of available listings is Staten "
                                     "Island, followed by Bronx and Queens.",
                            style=style["p"],
                        ),
                        dcc.Graph(
                            id="percentage_of_available_listings_from_each_neighbourhood_group",
                            figure=percentage_of_available_listings_from_each_neighbourhood_group_fig,
                            style=style["graph"],
                        ),
                    ],
                    xs=10,
                    sm=8,
                    md=5,
                    lg=6,
                    xl=5,
                ),
                dbc.Col(
                    [
                        html.H2(children="Hosts", style=style["h2"]),
                        html.H3(
                            children="Top hosts with most listings", style=style["h3"]
                        ),
                        html.P(
                            children="The top 10 hosts with most listings are shown in the graph below. "
                                     "The host with the most listings are followed by David and Michael having 355 and 309 "
                                     "listings respectively. Anna finishes the list having 159 listings.",
                            style=style["p"],
                        ),
                        dcc.Graph(
                            id="top_hosts", figure=top_hosts_fig, style=style["graph"]
                        ),
                    ],
                    xs=10,
                    sm=8,
                    md=5,
                    lg=6,
                    xl=5,
                ),
            ],
            justify="left",
            align="top",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(children="Listings", style=style["h2"]),
                        html.H3(
                            children="Top 10 most reviewed listings in each neighbourhood group",
                            style=style["h3"],
                        ),
                        html.P(
                            children="The top 10 most reviewed listings in each neighbourhood group are shown in the graph below. "
                                     "The most reviewed listings are all located in Manhattan.",
                            style=style["p"],
                        ),
                        dcc.Dropdown(
                            id="most_reviewed_listings_neighbourhood_group_dropdown",
                            options=[
                                {
                                    "label": neighbourhood_group,
                                    "value": neighbourhood_group,
                                }
                                for neighbourhood_group in df[
                                    "neighbourhood_group"
                                ].unique()
                            ],
                            value=df["neighbourhood_group"].unique()[0],
                            style=style["dropdown"],
                            clearable=False,
                        ),
                        dcc.Graph(
                            id="top_most_reviewed_listings_fig", style=style["graph"]
                        ),
                    ]
                )
            ],
            justify="left",
        ),
    ],
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
