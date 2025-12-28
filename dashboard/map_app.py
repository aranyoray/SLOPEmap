"""
Interactive Map Dashboard with Hover and Search
Shows county data on hover, zooms on search
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from pathlib import Path
import numpy as np

# Initialize app
app = dash.Dash(__name__, title="NREL SLOPE Interactive Map")
server = app.server

# Load data
def load_data():
    """Load county data"""
    data_path = Path(__file__).parent / "data" / "dashboard_data.json"

    if data_path.exists():
        with open(data_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        # Sample data
        df = create_sample_data()

    # Add coordinates (sample - you'll get real coords from scraping)
    if 'lat' not in df.columns:
        df['lat'] = np.random.uniform(25, 50, len(df))
    if 'lon' not in df.columns:
        df['lon'] = np.random.uniform(-125, -65, len(df))

    return df

def create_sample_data():
    """Create sample data with coordinates"""
    num_counties = 100

    # Sample US county coordinates
    lats = np.random.uniform(25, 50, num_counties)
    lons = np.random.uniform(-125, -65, num_counties)

    data = {
        'geoid': [f"G{i:07d}" for i in range(num_counties)],
        'county_name': [f"County {i}" for i in range(num_counties)],
        'state': np.random.choice(['AL', 'CA', 'TX', 'NY', 'FL'], num_counties),
        'population': np.random.randint(10000, 1000000, num_counties),
        'solar_potential_mw': np.random.randint(100, 5000, num_counties),
        'wind_potential_mw': np.random.randint(50, 3000, num_counties),
        'energy_burden_pct': np.random.uniform(2, 8, num_counties),
        'lat': lats,
        'lon': lons,
        'scrape_status': 'success'
    }

    return pd.DataFrame(data)

# Load data
df = load_data()

# Create map figure
def create_map(df_filtered, zoom_lat=None, zoom_lon=None, zoom_level=3):
    """Create interactive map"""

    # Create hover text
    df_filtered['hover_text'] = df_filtered.apply(lambda row: f"""
<b>{row.get('county_name', 'Unknown County')}</b><br>
State: {row.get('state', 'N/A')}<br>
GeoID: {row.get('geoid', 'N/A')}<br>
Population: {row.get('population', 'N/A'):,}<br>
Solar Potential: {row.get('solar_potential_mw', 0):.0f} MW<br>
Wind Potential: {row.get('wind_potential_mw', 0):.0f} MW<br>
Energy Burden: {row.get('energy_burden_pct', 0):.1f}%<br>
Status: {row.get('scrape_status', 'Unknown')}
    """.strip(), axis=1)

    fig = go.Figure()

    # Add county markers
    fig.add_trace(go.Scattergeo(
        lon=df_filtered['lon'],
        lat=df_filtered['lat'],
        text=df_filtered['hover_text'],
        mode='markers',
        marker=dict(
            size=8,
            color=df_filtered.get('solar_potential_mw', 0),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Solar Potential (MW)"),
            line=dict(width=0.5, color='white')
        ),
        hovertemplate='%{text}<extra></extra>',
        name='Counties'
    ))

    # Set map layout
    center_lat = zoom_lat if zoom_lat else df_filtered['lat'].mean()
    center_lon = zoom_lon if zoom_lon else df_filtered['lon'].mean()

    fig.update_layout(
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            center=dict(lat=center_lat, lon=center_lon),
            projection_scale=zoom_level
        ),
        title=dict(
            text='NREL SLOPE County Energy Data',
            x=0.5,
            xanchor='center'
        ),
        height=700,
        hovermode='closest'
    )

    return fig

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("NREL SLOPE Interactive County Map",
               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
        html.P("Hover over counties for details • Search to zoom",
              style={'textAlign': 'center', 'color': '#7f8c8d'}),
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px'}),

    # Search and filters
    html.Div([
        html.Div([
            html.Label("Search County:", style={'fontWeight': 'bold'}),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='Enter county name or GeoID...',
                style={'width': '100%', 'padding': '8px', 'marginTop': '5px'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label("Filter by State:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='state-filter',
                options=[{'label': 'All States', 'value': 'all'}] +
                        [{'label': state, 'value': state}
                         for state in sorted(df['state'].unique())],
                value='all',
                style={'width': '100%', 'marginTop': '5px'}
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Button('Search & Zoom', id='search-button', n_clicks=0,
                       style={'padding': '10px 20px', 'backgroundColor': '#3498db',
                             'color': 'white', 'border': 'none', 'borderRadius': '4px',
                             'cursor': 'pointer', 'marginTop': '25px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'margin': '10px'}),

    ], style={'padding': '20px', 'backgroundColor': 'white', 'margin': '20px',
             'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    # Map
    html.Div([
        dcc.Graph(id='county-map', figure=create_map(df))
    ], style={'margin': '20px'}),

    # Stats
    html.Div([
        html.Div([
            html.H3(id='stat-total', children=str(len(df))),
            html.P("Total Counties"),
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px',
                 'backgroundColor': '#3498db', 'color': 'white', 'margin': '10px',
                 'borderRadius': '8px'}),

        html.Div([
            html.H3(id='stat-solar', children=f"{df['solar_potential_mw'].sum():,.0f}"),
            html.P("Total Solar Potential (MW)"),
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px',
                 'backgroundColor': '#2ecc71', 'color': 'white', 'margin': '10px',
                 'borderRadius': '8px'}),

        html.Div([
            html.H3(id='stat-wind', children=f"{df['wind_potential_mw'].sum():,.0f}"),
            html.P("Total Wind Potential (MW)"),
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px',
                 'backgroundColor': '#e74c3c', 'color': 'white', 'margin': '10px',
                 'borderRadius': '8px'}),

    ], style={'display': 'flex', 'margin': '20px'}),

    # County detail panel
    html.Div(id='county-detail', style={'margin': '20px', 'padding': '20px',
             'backgroundColor': 'white', 'borderRadius': '8px',
             'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    # Footer
    html.Div([
        html.P("Data Source: NREL SLOPE Platform • https://maps.nrel.gov/slope/",
              style={'textAlign': 'center', 'color': '#95a5a6'}),
    ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'marginTop': '40px'}),

], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f5f6fa'})

# Callbacks
@app.callback(
    [Output('county-map', 'figure'),
     Output('stat-total', 'children'),
     Output('stat-solar', 'children'),
     Output('stat-wind', 'children'),
     Output('county-detail', 'children')],
    [Input('search-button', 'n_clicks'),
     Input('state-filter', 'value')],
    [State('search-input', 'value')]
)
def update_map(n_clicks, state_filter, search_query):
    """Update map based on filters and search"""

    # Filter by state
    df_filtered = df.copy()
    if state_filter != 'all':
        df_filtered = df_filtered[df_filtered['state'] == state_filter]

    # Search and zoom
    zoom_lat, zoom_lon, zoom_level = None, None, 3
    county_detail = html.P("Select a county to see details", style={'color': '#7f8c8d'})

    if search_query and n_clicks > 0:
        # Search in county name or geoid
        search_mask = (
            df_filtered['county_name'].str.contains(search_query, case=False, na=False) |
            df_filtered['geoid'].str.contains(search_query, case=False, na=False)
        )
        search_results = df_filtered[search_mask]

        if len(search_results) > 0:
            # Zoom to first result
            first_result = search_results.iloc[0]
            zoom_lat = first_result['lat']
            zoom_lon = first_result['lon']
            zoom_level = 10  # Closer zoom

            # Show county details
            county_detail = html.Div([
                html.H3(f"{first_result['county_name']}", style={'color': '#2c3e50'}),
                html.P(f"State: {first_result['state']}", style={'marginBottom': '5px'}),
                html.P(f"GeoID: {first_result['geoid']}", style={'marginBottom': '5px'}),
                html.P(f"Population: {first_result['population']:,}", style={'marginBottom': '5px'}),
                html.P(f"Solar Potential: {first_result['solar_potential_mw']:.0f} MW",
                      style={'marginBottom': '5px'}),
                html.P(f"Wind Potential: {first_result['wind_potential_mw']:.0f} MW",
                      style={'marginBottom': '5px'}),
                html.P(f"Energy Burden: {first_result['energy_burden_pct']:.1f}%",
                      style={'marginBottom': '5px'}),
            ])

    # Create map
    fig = create_map(df_filtered, zoom_lat, zoom_lon, zoom_level)

    # Update stats
    total_counties = len(df_filtered)
    total_solar = f"{df_filtered['solar_potential_mw'].sum():,.0f} MW"
    total_wind = f"{df_filtered['wind_potential_mw'].sum():,.0f} MW"

    return fig, total_counties, total_solar, total_wind, county_detail


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')
