import plotly.graph_objs as go
from plotly.offline import iplot

# Create a trace
trace = go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='lines',
    name='Line Chart'
)

# Create a layout
layout = go.Layout(
    title='My Line Chart'
)

# Create a figure
fig = go.Figure(data=[trace], layout=layout)

# Display the chart
iplot(fig)
