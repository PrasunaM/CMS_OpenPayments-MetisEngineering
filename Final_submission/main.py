import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import payments

top_layout = html.Div([
    #links to other pages
    # html.Div([
    #     html.Nav(className = "nav nav-pills", children=[
    #         html.A('2020', className="nav-item nav-link btn", href='/apps/payments_2020',
    #                 style={"font-size": "2rem",
    #                         "box-shadow": "4px 4px 2px #e3e3e3",
    #                         "padding": "5px",
    #                         'marginTop':'-15px'}),
    #         html.H5(""),

    #         html.A('2019', className="nav-item nav-link btn", href='/apps/payments_2019',
    #                 style={"font-size": "2rem",
    #                         "box-shadow": "4px 4px 2px #e3e3e3",
    #                         "padding": "5px",
    #                         'marginTop':'-15px'}),


    #         ],style = {'marginTop':'-15px'}),
    # ], className='one-third column', id = 'links', style={'textAlign':'center'}),


    # last update date
    #todo

], id='header',className='row flex-display', style={'margin-bottom': '10px','marginTop':'-15px'})

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    top_layout,
    html.Div(id='page-content',children=[])
], id='mainContainer', style={'display': 'flex','flex-direction':'column'})


app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    top_layout,
    html.Div(id='page-content',children=[])
], id='mainContainer', style={'display': 'flex','flex-direction':'column'})

@app.callback(Output('page-content', 'children'),
            [Input('url','pathname')])
def display_page(pathname):
    return payments.layout
    # if pathname == '/apps/payments_2020':
    #     return payments_2020.layout
    # elif pathname == '/apps/payments_2019':
    #     return payments_2019.layout
    # else:
    #     return payments_2020.layout




if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    #app.server.run(host='0.0.0.0', port=8080, debug=True)