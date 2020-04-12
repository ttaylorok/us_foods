import plotly.graph_objects as go
animals=['giraffes', 'orangutans', 'monkeys']

fig = go.Figure(data=[
    go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23], orientation='h'),
    go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29], orientation='h')
])
# Change the bar mode
fig.update_layout(barmode='stack', orientation=0)
fig.show()

fig.write_html("plotly_test.html")