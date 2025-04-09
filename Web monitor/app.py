from flask import Flask, render_template
import plotly.express as px
import json
import pandas as pd
import plotly
from Final.likesCount import convert_likes

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data for the plot
    dataframe = pd.read_json(r"kzg.json")

    # Normalize the 'videos' field in the JSON
    dataframe = pd.json_normalize(dataframe['videos'])
    dataframe["likes"] = dataframe['likes'].apply(convert_likes)
    dataframe["views"] = dataframe['views'].str.replace(',', '').astype(int)
    print(dataframe.head())
    
    fig = px.scatter(dataframe, 
                 x='days ago', 
                 y='views', 
                #  text='video title',
                 size='likes',  # Points sized by this column
                 color='products',  # Different colors for categories
                 title='Views vs Days ago',
                 labels={'days ago': 'Days Since Upload', 'views': 'View Count'})
    # Create a Plotly figure
    fig.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=
        '<b>Title</b>: %{customdata[0]}<br>' +  # Access video title from customdata
        '<b>Views</b>: %{y:,}<br>' +
        '<b>Days Ago</b>: %{x}<br>' +
        '<b>Likes</b>: %{marker.size:,}<br>' +
        '<b>Products</b>: %{customdata[1]}<br>',
        customdata=dataframe[['video title', 'products']]  # Pass both title and products as customdata
    )    
    fig.update_layout(
    showlegend=True,
    hovermode='closest',
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.5,
    xaxis_title="Days Since Upload",
    yaxis_title="View Count",
    yaxis=dict(tickformat=",")
)


    # Convert the figure to JSON for rendering in the template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
