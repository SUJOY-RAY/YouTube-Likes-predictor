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
    dataframe = pd.read_json(r"D:\YouTube-Likes-predictor\Web monitor\kzg.json")

    # Normalize the 'videos' field in the JSON
    dataframe = pd.json_normalize(dataframe['videos'])
    dataframe["likes"] = dataframe['likes'].apply(convert_likes)
    dataframe["views"] = dataframe['views'].str.replace(',', '').astype(int)
    pd.set_option('display.max_columns', None)
    print(dataframe.head())
    
    """Views vs Days ago"""
    fig1 = px.scatter(dataframe, 
                 x='days ago', 
                 y='views', 
                #  text='video title',
                 size='likes',  # Points sized by this column
                 color='products',  # Different colors for categories
                 title='Views vs Days ago',
                 labels={'days ago': 'Days Since Upload', 'views': 'View Count'})
    # Create a Plotly figure
    fig1.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=
        '<b>Title</b>: %{customdata[0]}<br>' +  # Access video title from customdata
        '<b>Views</b>: %{y:,}<br>' +
        '<b>Days Ago</b>: %{x}<br>' +
        '<b>Likes</b>: %{marker.size:,}<br>' +
        '<b>Products</b>: %{customdata[1]}<br>',
        customdata=dataframe[['video title', 'products']]  # Pass both title and products as customdata
    )    
    fig1.update_layout(
    showlegend=True,
    hovermode='closest',
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.5,
    xaxis_title="Days Since Upload",
    yaxis_title="View Count",
    yaxis=dict(tickformat=",")
    )
    print(fig1)

    """Likes vs Days ago"""
    fig2 = px.scatter(dataframe, 
                 x='days ago', 
                 y='views', 
                #  text='video title',
                 size='likes',  # Points sized by this column
                 color='products',  # Different colors for categories
                 title='Views vs Days ago',
                 labels={'days ago': 'Days Since Upload', 'views': 'Likes Count'})
    # Create a Plotly figure
    fig2.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=
        '<b>Title</b>: %{customdata[0]}<br>' +  # Access video title from customdata
        '<b>Views</b>: %{y:,}<br>' +
        '<b>Days Ago</b>: %{x}<br>' +
        '<b>Likes</b>: %{marker.size:,}<br>' +
        '<b>Products</b>: %{customdata[1]}<br>',
        customdata=dataframe[['video title', 'products']]  # Pass both title and products as customdata
    )    
    fig2.update_layout(
    showlegend=True,
    hovermode='closest',
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.5,
    xaxis_title="Days Since Upload",
    yaxis_title="Likes Count",
    yaxis=dict(tickformat=",")
    )
    print(fig1)

    """Views vs likes"""
    fig3 = px.scatter(dataframe,
                    x='views',
                    y='likes',
                    color='products',
                    size='days ago',  # Could also size by recency
                    title='Likes vs Views',
                    labels={'views': 'View Count', 'likes': 'Likes Count'})

    fig3.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=
        '<b>Title</b>: %{customdata[0]}<br>' +
        '<b>Views</b>: %{x:,}<br>' +
        '<b>Likes</b>: %{y:,}<br>' +
        '<b>Days Ago</b>: %{marker.size:,}<br>' +
        '<b>Products</b>: %{customdata[1]}<br>',
        customdata=dataframe[['video title', 'products']]
    )

    """Likes per View vs Days Ago"""

    dataframe['likes_per_view'] = dataframe['likes'] / dataframe['views']

    fig4 = px.scatter(dataframe,
                    x='days ago',
                    y='likes_per_view',
                    color='products',
                    size='views',
                    title='Likes per View vs Days Ago',
                    labels={'days ago': 'Days Since Upload', 'likes_per_view': 'Likes/View Ratio'})

    fig4.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=
        '<b>Title</b>: %{customdata[0]}<br>' +
        '<b>Likes/View</b>: %{y:.4f}<br>' +
        '<b>Days Ago</b>: %{x}<br>' +
        '<b>Products</b>: %{customdata[1]}<br>',
        customdata=dataframe[['video title', 'products']]
    )

    """Views per Day (Growth Rate) vs Days Ago"""
    dataframe['views_per_day'] = dataframe['views'] / dataframe['days ago']

    fig5 = px.scatter(dataframe,
                    x='days ago',
                    y='views_per_day',
                    color='products',
                    size='likes',
                    title='Views per Day vs Days Ago',
                    labels={'days ago': 'Days Since Upload', 'views_per_day': 'Views per Day'})

    fig5.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=
        '<b>Title</b>: %{customdata[0]}<br>' +
        '<b>Views per Day</b>: %{y:,.0f}<br>' +
        '<b>Days Ago</b>: %{x}<br>' +
        '<b>Likes</b>: %{marker.size:,}<br>' +
        '<b>Products</b>: %{customdata[1]}<br>',
        customdata=dataframe[['video title', 'products']]
    )


    # Convert the figure to JSON for rendering in the template
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

        
    return render_template('index.html',
                        graphJSON1=graphJSON1,
                        graphJSON2=graphJSON2,
                        graphJSON3=graphJSON3,
                        graphJSON4=graphJSON4,
                        graphJSON5=graphJSON5)

@app.route('/get_charts')
def get_charts():
    dataframe = pd.read_json(r"D:\YouTube-Likes-predictor\Web monitor\kzg.json")
    dataframe = pd.json_normalize(dataframe['videos'])
    dataframe["likes"] = dataframe['likes'].apply(convert_likes)
    dataframe["views"] = dataframe['views'].str.replace(',', '').astype(int)

    dataframe['likes_per_view'] = dataframe['likes'] / dataframe['views']
    dataframe['views_per_day'] = dataframe['views'] / dataframe['days ago']

    # Chart 1: Views vs Days Ago
    fig1 = px.scatter(dataframe, x='days ago', y='views', size='likes', color='products',
                      title='Views vs Days Ago',
                      labels={'days ago': 'Days Since Upload', 'views': 'View Count'})
    fig1.update_traces(customdata=dataframe[['video title', 'products']],
                       marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    # Chart 2: Likes vs Days Ago
    fig2 = px.scatter(dataframe, x='days ago', y='likes', size='views', color='products',
                      title='Likes vs Days Ago',
                      labels={'days ago': 'Days Since Upload', 'likes': 'Likes Count'})
    fig2.update_traces(customdata=dataframe[['video title', 'products']],
                       marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # Chart 3: Likes vs Views
    fig3 = px.scatter(dataframe, x='views', y='likes', size='days ago', color='products',
                      title='Likes vs Views',
                      labels={'views': 'View Count', 'likes': 'Likes Count'})
    fig3.update_traces(customdata=dataframe[['video title', 'products']],
                       marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # Chart 4: Likes/View vs Days Ago
    fig4 = px.scatter(dataframe, x='days ago', y='likes_per_view', size='views', color='products',
                      title='Likes per View vs Days Ago',
                      labels={'days ago': 'Days Since Upload', 'likes_per_view': 'Likes/View'})
    fig4.update_traces(customdata=dataframe[['video title', 'products']],
                       marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # Chart 5: Views/Day vs Days Ago
    fig5 = px.scatter(dataframe, x='days ago', y='views_per_day', size='likes', color='products',
                      title='Views per Day vs Days Ago',
                      labels={'days ago': 'Days Since Upload', 'views_per_day': 'Views/Day'})
    fig5.update_traces(customdata=dataframe[['video title', 'products']],
                       marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    return {
        'chart1': json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)),
        'chart2': json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)),
        'chart3': json.loads(json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)),
        'chart4': json.loads(json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)),
        'chart5': json.loads(json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)),
    }





if __name__ == '__main__':
    app.run(debug=True)
