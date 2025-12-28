"""
NREL SLOPE Dashboard - Vercel Deployment Version
This version uses pre-scraped static data for deployment
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
import os
from pathlib import Path

# Initialize Dash app
app = dash.Dash(
    __name__,
    title="NREL SLOPE County Dashboard",
    suppress_callback_exceptions=True
)
server = app.server  # For Vercel deployment

# Load data function
def load_dashboard_data():
    """Load data from static file or use sample data"""

    # Try to load from multiple possible locations
    possible_paths = [
        Path(__file__).parent.parent / "data" / "processed" / "dashboard_data.json",
        Path(__file__).parent / "data" / "dashboard_data.json",
        Path("data/processed/dashboard_data.json"),
        Path("dashboard_data.json")
    ]

    for data_path in possible_paths:
        if data_path.exists():
            try:
                with open(data_path, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
                print(f"✓ Loaded data from: {data_path}")
                return df
            except Exception as e:
                print(f"Error loading {data_path}: {e}")
                continue

    # If no data file found, use sample data
    print("⚠️ No data file found, using sample data")
    return create_sample_data()

def create_sample_data():
    """Create sample data for demonstration"""
    import numpy as np

    num_counties = 100
    state_fips = [f"{i:02d}" for i in range(1, 51)]

    data = {
        'geoid': [f"G{np.random.choice(state_fips)}{i:05d}" for i in range(num_counties)],
        'state_fips': np.random.choice(state_fips, num_counties),
        'county_fips': [f"{i:05d}" for i in range(num_counties)],
        'scrape_status': np.random.choice(['success', 'error'], num_counties, p=[0.9, 0.1]),
        'page_title': [f"County {i}" for i in range(num_counties)],
    }

    return pd.DataFrame(data)

# Load data
df = load_dashboard_data()

# Dashboard Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("NREL SLOPE County Energy Dashboard",
               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
        html.P("Interactive visualization of county-level energy data from NREL SLOPE platform",
              style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': 30}),
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px'}),

    # Stats Cards
    html.Div([
        html.Div([
            html.Div([
                html.H3(str(len(df)), style={'margin': 0, 'color': '#3498db'}),
                html.P("Total Counties", style={'margin': 0, 'color': '#7f8c8d'}),
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                     'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        ], style={'flex': 1, 'margin': '10px'}),

        html.Div([
            html.Div([
                html.H3(str(len(df[df['scrape_status'] == 'success'])),
                       style={'margin': 0, 'color': '#2ecc71'}),
                html.P("Successful Scrapes", style={'margin': 0, 'color': '#7f8c8d'}),
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                     'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        ], style={'flex': 1, 'margin': '10px'}),

        html.Div([
            html.Div([
                html.H3(str(df['state_fips'].nunique()),
                       style={'margin': 0, 'color': '#e74c3c'}),
                html.P("States Covered", style={'margin': 0, 'color': '#7f8c8d'}),
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                     'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        ], style={'flex': 1, 'margin': '10px'}),

    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Filter by State FIPS:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='state-filter',
                options=[{'label': 'All States', 'value': 'all'}] +
                        [{'label': f"State {s}", 'value': s}
                         for s in sorted(df['state_fips'].unique())],
                value='all',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label("Filter by Status:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='status-filter',
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'Success', 'value': 'success'},
                    {'label': 'Error', 'value': 'error'}
                ],
                value='all',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
    ], style={'padding': '20px', 'backgroundColor': 'white', 'margin': '20px',
             'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    # Visualizations
    html.Div([
        # Distribution Chart
        html.Div([
            dcc.Graph(id='distribution-chart'),
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),

        # Status Chart
        html.Div([
            dcc.Graph(id='status-chart'),
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),

    # Data Table
    html.Div([
        html.H3("County Data Sample", style={'color': '#2c3e50'}),
        html.Div(id='data-table'),
    ], style={'padding': '20px', 'backgroundColor': 'white', 'margin': '20px',
             'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    # Footer
    html.Div([
        html.P("Data Source: NREL SLOPE Platform",
              style={'textAlign': 'center', 'color': '#95a5a6', 'margin': 0}),
        html.P("https://maps.nrel.gov/slope/",
              style={'textAlign': 'center', 'color': '#95a5a6', 'margin': 0}),
    ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'marginTop': '40px'}),

], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f5f6fa'})

# Callbacks
@app.callback(
    [Output('distribution-chart', 'figure'),
     Output('status-chart', 'figure'),
     Output('data-table', 'children')],
    [Input('state-filter', 'value'),
     Input('status-filter', 'value')]
)
def update_dashboard(state_value, status_value):
    # Filter data
    filtered_df = df.copy()

    if state_value != 'all':
        filtered_df = filtered_df[filtered_df['state_fips'] == state_value]

    if status_value != 'all':
        filtered_df = filtered_df[filtered_df['scrape_status'] == status_value]

    # Distribution chart
    state_counts = filtered_df['state_fips'].value_counts().reset_index()
    state_counts.columns = ['state_fips', 'count']

    dist_fig = px.bar(
        state_counts,
        x='state_fips',
        y='count',
        title='Counties by State FIPS',
        labels={'state_fips': 'State FIPS', 'count': 'Number of Counties'}
    )
    dist_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif")
    )

    # Status chart
    status_counts = filtered_df['scrape_status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']

    status_fig = px.pie(
        status_counts,
        values='count',
        names='status',
        title='Scraping Status Distribution',
        color='status',
        color_discrete_map={'success': '#2ecc71', 'error': '#e74c3c'}
    )
    status_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif")
    )

    # Data table
    table_data = filtered_df[['geoid', 'state_fips', 'county_fips',
                              'scrape_status', 'page_title']].head(20)

    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col, style={'padding': '10px', 'backgroundColor': '#3498db',
                                         'color': 'white', 'textAlign': 'left'})
                    for col in table_data.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(table_data.iloc[i][col],
                       style={'padding': '10px', 'borderBottom': '1px solid #ddd'})
                for col in table_data.columns
            ]) for i in range(len(table_data))
        ])
    ], style={'width': '100%', 'borderCollapse': 'collapse'})

    return dist_fig, status_fig, table

# For local testing
if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')
