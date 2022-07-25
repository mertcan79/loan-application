
import plotly.express as px

def create_plotly(data,stat,value):

    color_palette = ["#557B83","#39AEA9","#A2D5AB","#E5EFC1"]

    fig = px.bar(data,
                  x='Lender',
                  y=stat,
                  title=stat,
                  barmode='group',
                  color_discrete_sequence =color_palette[:1])
    fig.add_vline(x=value, line_width=4, line_dash="dash", line_color="red")
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

    return fig

def fig_layout(fig, ytitle, ytickfromat, xtitle,ticker, legendtitle, type_of_plot, yaxis_tickprefix=None):
    fig.update_layout(
        yaxis={
            "title": ytitle,
            "tickformat": ytickfromat,
        },
        yaxis_tickprefix = yaxis_tickprefix,
        paper_bgcolor="#FFFFFF",  # rgba(0,0,0,0)',
        plot_bgcolor="#FFFFFF",  # 'rgba(0,0,0,0)',
        # autosize=True,
        legend=dict(
            title=legendtitle,
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        title={
            'text': '{} - {} <br><sup>tenxassets.com</sup>'.format(type_of_plot,ticker),
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(
            size=12,
            color="black"),

        template="simple_white",
        xaxis=dict(
            title=xtitle,
            showticklabels=True),
        showlegend=True,
        font=dict(
            # family="Courier New, monospace",
            size=12,
            color="black"
        ),
    )
    return fig



