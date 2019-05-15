import dash
from dash.dependencies import Event, Output, Input
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Social Media Recommendation System',
                        className='nine columns'),
                
                html.H6(children='''
                        Suggesting People or Interests to follow based on correlation.
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        html.Div(
            [
                html.Div(
                    
                        id = 'none',
                        children = [],
                        style = {'display': 'none'}
                ),

            ], className="row"
        ),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='top-followees-graph'
                )], className= 'six columns'
                ),


            html.Div([
                dcc.Graph(
                    id='top-interests-graph'
                )], className= 'six columns'
                ),

            html.Div([
                dcc.Graph(
                    id='hist-distribution-followers'
                )], className= 'fifteen columns'
                ),

            html.Div([
                dcc.Graph(
                    id='hist-distribution-interests'
                )], className= 'fifteen columns'
                ),

        ], className="rows")
    ], className='ten columns offset-by-one')
)



follows = pd.read_csv('follows.csv', names = ['Follower ID', 'Followee ID'], header = 0)
temp_f = []

for i in range(len(follows)):
	temp_f.append(1)

follows['Temp'] = temp_f
rating_count_f = follows.groupby(by = ['Followee ID'])['Temp'].count().reset_index()
rating_count_f = rating_count_f.sort_values('Temp', ascending = False).reset_index(drop = True)
rating_count_f = rating_count_f.rename(index=str, columns={"Temp": "Number of Followers"})


interests = pd.read_csv('interests.csv', names = ['User ID', 'Interest'], header = 0)
temp_i = []

for i in range(len(interests)):
    temp_i.append(1)        

interests['Temp'] = temp_i
rating_count_i = interests.groupby(by = ['Interest'])['Temp'].count().reset_index()
rating_count_i = rating_count_i.sort_values('Temp', ascending = False).reset_index(drop = True)
rating_count_i = rating_count_i.rename(index=str, columns={"Temp": "Number of Followers"})

@app.callback(
    Output('top-followees-graph', 'figure'),
    [Input('none', 'children')])
def update_followees(none):
	temp_X = list(map(str, rating_count_f['Followee ID'].tolist()[:10]))
	X = ["ID " + s for s in temp_X]
	Y = rating_count_f['Number of Followers'].tolist()[:10]
	data = []
	data.append({'x': X, 'y': Y, 'type': 'bar'})

	figure = {
		'data': data,
		'layout': {
		'title': 'Top 10 Most Followed People',
		'xaxis' : dict(
			title='Followee ID',
			titlefont=dict(
			family='Courier New, monospace',
			size=15,
			color='#7f7f7f'
	)),
		'yaxis' : dict(
		title='Number of Followers',
		titlefont=dict(
		family='Helvetica, monospace',
		size=15,
		color='#7f7f7f'
	))
	}
	}
	return figure


@app.callback(
    Output('top-interests-graph', 'figure'),
    [Input('none', 'children')])
def update_interests(selector):
	X = rating_count_i['Interest'].tolist()[:10]
	Y = rating_count_i['Number of Followers'].tolist()[:10]
	data = []
	data.append({'x': X, 'y': Y, 'type': 'bar'})

	figure = {
		'data': data,
		'layout': {
		'title': 'Top 10 Most Followed Interests',
		'xaxis' : dict(
		    title='Interest',
		    titlefont=dict(
		    family='Courier New, monospace',
		    size=15,
		    color='#7f7f7f'
		)),
		'yaxis' : dict(
		    title='Number of Followers',
		    titlefont=dict(
		    family='Helvetica, monospace',
		    size=15,
		    color='#7f7f7f'
		))
	}
	}
	return figure


@app.callback(
    Output('hist-distribution-followers', 'figure'),
    [Input('none', 'children')])
def update_interests(selector):
	X = rating_count_f['Number of Followers'].tolist()

	data = []
	data.append({'x': X, 'type': 'histogram'})

	figure = {
		'data': data,
		'layout': {
		'title': 'Distribution of Followers',
		'xaxis' : dict(
		    title='Number of Followers',
		    titlefont=dict(
		    family='Courier New, monospace',
		    size=15,
		    color='#7f7f7f'
		)),
		'yaxis' : dict(
		    title='Number of People',
		    titlefont=dict(
		    family='Helvetica, monospace',
		    size=15,
		    color='#7f7f7f'
		))
	}
	}
	return figure

@app.callback(
    Output('hist-distribution-interests', 'figure'),
    [Input('none', 'children')])
def update_interests(selector):
	X = rating_count_i['Number of Followers'].tolist()

	data = []
	data.append({'x': X, 'type': 'histogram'})

	figure = {
		'data': data,
		'layout': {
		'title': 'Distribution of Interests',
		'xaxis' : dict(
		    title='Number of Followers',
		    titlefont=dict(
		    family='Courier New, monospace',
		    size=15,
		    color='#7f7f7f'
		)),
		'yaxis' : dict(
		    title='Number of Interests',
		    titlefont=dict(
		    family='Helvetica, monospace',
		    size=15,
		    color='#7f7f7f'
		))
	}
	}
	return figure

if __name__ == '__main__':
	app.run_server(debug=True)