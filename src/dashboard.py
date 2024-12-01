import dash
from dash import dcc, html
import plotly.graph_objects as go

def create_dashboard(data, predictions=None, best_params=None, best_sharpe=None):
    """Create an interactive dashboard for visualization."""
    import dash
    from dash import dcc, html
    import plotly.graph_objects as go

    app = dash.Dash(__name__)

    # Price chart with predictions
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))
    if predictions is not None:
        fig_price.add_trace(go.Scatter(x=data.index[-len(predictions):], y=predictions.flatten(), name='Predicted Price'))

    # Cumulative Returns Plot
    fig_cum_returns = go.Figure()
    fig_cum_returns.add_trace(go.Scatter(x=data.index, y=data['Cumulative Returns'], name='Cumulative Returns'))
    fig_cum_returns.update_layout(title="Cumulative Returns", xaxis_title="Date", yaxis_title="Returns")

    # Drawdown Plot
    fig_drawdown = go.Figure()
    fig_drawdown.add_trace(go.Scatter(x=data.index, y=data['Drawdown'], name='Drawdown', line=dict(color='red')))
    fig_drawdown.update_layout(title="Portfolio Drawdown", xaxis_title="Date", yaxis_title="Drawdown")

    # Layout
    app.layout = html.Div([
        html.H1("Trading Strategy Dashboard"),
        dcc.Graph(figure=fig_price),
        html.Div([
            html.H3("Optimization Results"),
            html.P(f"Best Parameters: SMA Short = {best_params[0]}, SMA Long = {best_params[1]}" if best_params else "No optimization data."),
            html.P(f"Best Sharpe Ratio: {best_sharpe:.2f}" if best_sharpe else "No Sharpe ratio calculated.")
        ]),
        dcc.Graph(figure=fig_cum_returns),
        dcc.Graph(figure=fig_drawdown)
    ])

    app.run_server(debug=True)




