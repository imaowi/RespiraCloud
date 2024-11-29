import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Read the CSV file
df = pd.read_csv('C:\\Users\\erika\\Downloads\\Dog Breads Around The World.csv')

# Group by 'Breed Type' and calculate the average 'Friendly Rating'
avg_friendliness_by_type = df.groupby('Type')['Friendly Rating (1-10)'].mean().reset_index()

# Create the Dash app
app = Dash(__name__)

# For deployment 
server = app.server

# Set up the layout
app.layout = html.Div([
    html.H1("Dog Breed Friendliness Dashboard"),
    dcc.Dropdown(
        id='breed-type-dropdown',
        options=[{'label': breed_type, 'value': breed_type} for breed_type in df['Type'].unique()],
        placeholder="Select a Breed Type",
        multi=True
    ),
    dcc.Graph(id='friendliness-chart')
])

# Add callback for interactivity
@app.callback(
    Output('friendliness-chart', 'figure'),
    [Input('breed-type-dropdown', 'value')]
)
def update_chart(selected_types):
    # Filter the data based on selected types
    filtered_df = avg_friendliness_by_type[avg_friendliness_by_type['Type'].isin(selected_types)] if selected_types else avg_friendliness_by_type

    # Create the bar chart
    fig = px.bar(
        filtered_df,
        x='Type',
        y='Friendly Rating (1-10)',
        title='Average Friendliness Rating by Breed Type',
        labels={'Friendly Rating (1-10)': 'Avg Friendliness Rating', 'Type': 'Breed Type'},
        color='Friendly Rating (1-10)',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(font=dict(size=14), hovermode="x unified")
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
