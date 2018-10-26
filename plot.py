import plotly
import plotly.graph_objs as go

# x-axis - index for the scenario
# y-axis - total cost
def plot_result(payment_range_a, payment_range_b, total_costs):
    x = list(range(1, len((total_costs))))
    y = [ int(total_cost) for total_cost in total_costs ]

    hovertext = []
    for i in range(0, len(total_costs) -1):
        hovertext.append('payment_a: ${:,}<br>payment_b: ${:,}'
                            .format(payment_range_a[i], payment_range_b[i]))

    data = [go.Bar(
            x=x,
            y=y,
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
            ),
            hovertext=hovertext,
            opacity=0.6
        )]

    layout = go.Layout(
        showlegend=False,
        xaxis={
            'title': 'Scenarios'
        },
        yaxis={
            'title': 'Total Cost',
            'tickformat': '$,.0'
        }
    )

    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, auto_open=True)
    
