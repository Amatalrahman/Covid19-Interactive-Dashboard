import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# --- 1. Load Data ---
df = pd.read_csv('C:\\Users\\lames\\Desktop\\depi_firstproject\\dash_board\\archive\\full_grouped.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_latest = pd.read_csv('C:\\Users\\lames\\Desktop\\depi_firstproject\\dash_board\\archive\\country_wise_latest.csv')
df['Log_Confirmed'] = np.log10(df['Confirmed'] + 1)

# Function to format numbers (e.g., 1.2M, 50K)
def format_num(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(int(num))

app = dash.Dash(__name__)

# --- 2. Styles ---
DARK_BG = "#121212" # Black background
CARD_BG = "#1e1e1e" # Darker gray for cards
TEXT_COLOR = "#FFFFFF" # White text
RED_PALETTE = ["#ff4d4d", "#ff0000", "#b30000", "#800000"] # Shades of Red

app.layout = html.Div(style={'backgroundColor': DARK_BG, 'minHeight': '100vh', 'color': TEXT_COLOR, 'padding': '20px'}, children=[
    
    # Header
    html.H1("COVID-19 GLOBAL REAL-TIME TRACKER", style={'textAlign': 'center', 'letterSpacing': '2px', 'fontWeight': 'bold'}),

    # Dropdown Section
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': 'Global View', 'value': 'Global'}] + [{'label': c, 'value': c} for c in df['Country/Region'].unique()],
            value='Global',
            clearable=False,
            style={'backgroundColor': '#333', 'color': '#000'}
        )
    ], style={'width': '40%', 'margin': '20px auto'}),

    # --- Indicators Row ---
    html.Div(id='indicator-cards', style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),

    # --- Main Visuals Row ---
    html.Div([
        html.Div([dcc.Graph(id='main-map')], style={'width': '65%', 'display': 'inline-block'}),
        html.Div([
            dcc.RadioItems(
                id='metric-selector',
                options=[{'label': ' Confirmed', 'value': 'Confirmed'}, {'label': ' Deaths', 'value': 'Deaths'}],
                value='Confirmed', inline=True, style={'marginBottom': '10px'}
            ),
            dcc.Graph(id='top-10-bar')
        ], style={'width': '33%', 'display': 'inline-block', 'float': 'right'})
    ], style={'display': 'flex', 'gap': '10px'}),

    # Date Picker
    html.Div([
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=df['Date'].min(), max_date_allowed=df['Date'].max(),
            start_date=df['Date'].min(), end_date=df['Date'].max(),
        )
    ], style={'textAlign': 'center', 'margin': '30px'}),

    # --- Bottom Row ---
    html.Div([
        dcc.Graph(id='line-plot', style={'width': '33%'}),
        dcc.Graph(id='pie-plot', style={'width': '33%'}),
        dcc.Graph(id='scatter-plot', style={'width': '33%'})
    ], style={'display': 'flex'})
])

# --- 3. Callbacks ---
@app.callback(
    [Output('indicator-cards', 'children'),
     Output('main-map', 'figure'),
     Output('top-10-bar', 'figure'),
     Output('line-plot', 'figure'),
     Output('pie-plot', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('country-dropdown', 'value'), Input('metric-selector', 'value'),
     Input('date-picker', 'start_date'), Input('date-picker', 'end_date')]
)
def update_dashboard(selected_country, metric, start_date, end_date):
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    f_df = df.loc[mask]

    # Indicator Logic
    if selected_country == 'Global':
        latest = f_df.groupby('Date').sum().reset_index().iloc[-1]
    else:
        latest = f_df[f_df['Country/Region'] == selected_country].iloc[-1]

    # Formatting Card Box
    def make_card(label, val, color):
        return html.Div([
            html.Div(label, style={'border': f'1px solid {color}', 'padding': '5px', 'borderRadius': '5px', 'fontSize': '14px', 'marginBottom': '10px'}),
            html.H2(format_num(val), style={'fontSize': '45px', 'margin': '0', 'fontWeight': 'bold'})
        ], style={'backgroundColor': CARD_BG, 'padding': '20px', 'borderRadius': '10px', 'width': '22%', 'textAlign': 'center', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.5)'})

    cards = [
        make_card("TOTAL CONFIRMED", latest['Confirmed'], "#ff4d4d"),
        make_card("TOTAL DEATHS", latest['Deaths'], "#b30000"),
        make_card("RECOVERED", latest['Recovered'], "#27ae60"),
        make_card("ACTIVE CASES", latest['Active'], "#f39c12")
    ]

    # Common Figure Styling function
    def apply_dark_theme(fig):
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color=TEXT_COLOR, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
        )
        return fig

    # 1. Map
    map_fig = px.choropleth(f_df, locations="Country/Region", locationmode='country names', color="Log_Confirmed",
                            animation_frame=f_df["Date"].dt.strftime('%Y-%m-%d'),
                            color_continuous_scale="Reds", template="plotly_dark", height=500)
    apply_dark_theme(map_fig)

    # 2. Bar Plot
    top10 = df_latest.sort_values(by=metric, ascending=False).head(10)
    bar_fig = px.bar(top10, x=metric, y='Country/Region', orientation='h', color=metric, color_continuous_scale="Reds")
    apply_dark_theme(bar_fig)

    # 3. Line Plot
    line_data = f_df.groupby('Date').sum().reset_index() if selected_country == 'Global' else f_df[f_df['Country/Region'] == selected_country]
    line_fig = px.line(line_data, x='Date', y=['Confirmed', 'Deaths','Recovered'], color_discrete_sequence=['blue', 'red','LightSlateGray'])
    apply_dark_theme(line_fig)

    # 4. Pie Plot
    pie_fig = px.pie(names=['Active', 'Recovered', 'Deaths'], values=[latest['Active'], latest['Recovered'], latest['Deaths']],
                     color_discrete_sequence=RED_PALETTE, hole=0.4)
    apply_dark_theme(pie_fig)

    # 5. Scatter Plot
    scatter_fig = px.scatter(df_latest, x="Deaths / 100 Cases", y="Recovered / 100 Cases", size="Confirmed",
                             color_discrete_sequence=[RED_PALETTE[1]], template="plotly_dark")
    apply_dark_theme(scatter_fig)

    return cards, map_fig, bar_fig, line_fig, pie_fig, scatter_fig

if __name__ == '__main__':
    app.run(debug=True)