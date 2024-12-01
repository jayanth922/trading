def create_enhanced_dashboard(data, metrics=None, suggestions=None, best_params=None):
    """Create an enhanced dashboard with multiple sections."""
    import dash
    from dash import dcc, html
    import plotly.graph_objects as go

    # Price Chart with Buy/Sell Signals
    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='blue')))
    price_fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='50-Day SMA', line=dict(color='orange')))
    price_fig.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], name='200-Day SMA', line=dict(color='green')))
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    price_fig.add_trace(go.Scatter(
        x=buy_signals.index, y=buy_signals['Close'], mode='markers', name='Buy Signal',
        marker=dict(color='green', size=10, symbol='triangle-up')
    ))
    price_fig.add_trace(go.Scatter(
        x=sell_signals.index, y=sell_signals['Close'], mode='markers', name='Sell Signal',
        marker=dict(color='red', size=10, symbol='triangle-down')
    ))
    price_fig.update_layout(
        title="Price Chart with Buy/Sell Signals",
        xaxis_title="Date",
        yaxis_title="Price"
    )

    # Cumulative Portfolio Growth
    portfolio_fig = go.Figure()
    portfolio_fig.add_trace(go.Scatter(
        x=data.index, y=data['Cumulative Returns'], name='Cumulative Returns', line=dict(color='purple')
    ))
    portfolio_fig.update_layout(
        title="Portfolio Growth",
        xaxis_title="Date",
        yaxis_title="Cumulative Returns"
    )

    # Drawdown Plot
    drawdown_fig = go.Figure()
    drawdown_fig.add_trace(go.Scatter(
        x=data.index, y=data['Drawdown'], name='Drawdown', line=dict(color='red')
    ))
    drawdown_fig.update_layout(
        title="Portfolio Drawdown",
        xaxis_title="Date",
        yaxis_title="Drawdown"
    )

    # Dashboard Layout
    app = dash.Dash(__name__)
    app.layout = html.Div([
        # Header
        html.H1("Enhanced Trading Strategy Dashboard", style={'text-align': 'center'}),

        # Market Summary Section
        html.Div([
            html.H3("Market Summary"),
            html.P(suggestions if suggestions else "No suggestions available.", style={'font-size': '16px', 'color': 'blue'})
        ], style={'margin-bottom': '30px'}),

        # Best Strategy Parameters Section
        html.Div([
            html.H3("Best Strategy Parameters"),
            html.P(f"Best SMA Short Window: {best_params[0]}" if best_params else "No parameter optimization available."),
            html.P(f"Best SMA Long Window: {best_params[1]}" if best_params else "")
        ], style={'margin-bottom': '30px'}),

        # Price Chart Section
        html.Div([
            html.H2("Price Chart"),
            dcc.Graph(figure=price_fig)
        ], style={'margin-bottom': '30px'}),

        # Portfolio Growth and Drawdown Section
        html.Div([
            html.H2("Portfolio Performance"),
            dcc.Graph(figure=portfolio_fig),
            dcc.Graph(figure=drawdown_fig)
        ], style={'margin-bottom': '30px'}),

        # Key Metrics Section
        html.Div([
            html.H2("Performance Metrics"),
            html.P(f"Sharpe Ratio: {metrics['sharpe']}" if metrics else "No metrics available."),
            html.P(f"Max Drawdown: {metrics['drawdown']}" if metrics else ""),
            html.P(f"Win Rate: {metrics['win_rate']}%" if metrics else "")
        ], style={'margin-bottom': '30px'})
    ])

    # Run the app
    app.run_server(debug=True)
