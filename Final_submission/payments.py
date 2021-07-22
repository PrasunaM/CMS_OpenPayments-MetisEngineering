import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import pathlib
from app import app
import data_loader

PATH = pathlib.Path(__file__).parent.parent

total_amount_2020 = '9.12 Billion'
total_amount_2019 = '10.86 Billion'

data = {}
data[2020] = data_loader.load_cms_data(2020)
data[2019] = data_loader.load_cms_data(2019)

def get_df_speciality(year):

    cms_by_year = data[year].copy()
    #cms_by_year = data_loader.load_cms_data(year)
    #cms_by_year = pd.read_csv(PATH.joinpath(f'cms_new_{year}.csv'))

    df_speciality_by_year = cms_by_year[['physician_specialty', 'Total_payment']]
    df_speciality_by_year['physician_specialty'] = df_speciality_by_year['physician_specialty'].str.replace('Allopathic & Osteopathic Physicians|','')
    df_speciality_by_year['physician_specialty'] = df_speciality_by_year['physician_specialty'].str.strip('|')
    df_speciality_by_year['physician_specialty'] = df_speciality_by_year['physician_specialty'].str.lstrip()
    df_speciality_grp = df_speciality_by_year.groupby(['physician_specialty']).sum()
    df_speciality_grp = df_speciality_grp.sort_values(by = ['Total_payment'],ascending=False )
    
    df_speciality_top_20= df_speciality_grp.iloc[:20,:].reset_index()

    if year == 2019:
        speciality = {'Podiatric Medicine & Surgery Service Providers|Podiatrist|Foot & Ankle Surgery': 'Foot & Ankle Surgery','Internal Medicine|Hematology & Oncology': 'Hematology & Oncology', 'Internal Medicine|Cardiovascular Disease': 'Cardiovascular Disease', 'Orthopaedic Surgery|Orthopaedic Surgery of the Spine': 'Spine Surgery', 'Orthopaedic Surgery|Adult Reconstructive Orthopaedic Surgery' : 'Adult Reconstructive','Internal Medicine|Endocrinology, Diabetes & Metabolism': 'Endocrinology', 'Eye and Vision Services Providers|Optometrist': 'Optometrist', 'Orthopaedic Surgery|Orthopaedic Trauma': 'Orthopaedic Trauma' ,'Orthopaedic Surgery|Hand Surgery' : 'Hand Surgery', 'Internal Medicine|Pulmonary Disease': 'Pulmonary Disease', 'Orthopaedic Surgery|Sports Medicine': 'Sports Medicine'}
        df_speciality_top_20.replace({"physician_specialty": speciality}, inplace = True)
    else:
        speciality = {'Internal Medicine|Hematology & Oncology': 'Hematology & Oncology', 'Internal Medicine|Cardiovascular Disease': 'Cardiovascular Disease', 'Orthopaedic Surgery|Orthopaedic Surgery of the Spine': 'Spine Surgery', 'Orthopaedic Surgery|Adult Reconstructive Orthopaedic Surgery' : 'Adult Reconstructive','Internal Medicine|Endocrinology, Diabetes & Metabolism': 'Endocrinology', 'Internal Medicine|Gastroenterology': 'Gastroenterology', 'Internal Medicine|Rheumatology': 'Rheumatology' ,'Orthopaedic Surgery|Hand Surgery' : 'Hand Surgery', 'Internal Medicine|Pulmonary Disease': 'Pulmonary Disease', 'Radiology|Vascular & Interventional Radiology': 'Radiology'}
        df_speciality_top_20.replace({"physician_specialty": speciality}, inplace = True)

    df_speciality_top_20 = df_speciality_top_20.set_index('physician_specialty')

    return df_speciality_top_20

def get_df_month(year):
    cms_by_year = data[year].copy()
    #cms_by_year = data_loader.load_cms_data(year)
    #cms_by_year = pd.read_csv(PATH.joinpath(f'cms_new_{year}.csv'))
    df_month = cms_by_year[['Payment_month', 'Total_payment']].groupby(['Payment_month']).sum()
    months = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    df_month.index = pd.CategoricalIndex(df_month.index, categories=months, ordered=True)
    df_month = df_month.sort_index()
    return df_month

def get_df_drug(year):
    cms_by_drug = data[year].copy()
    #cms_by_drug = data_loader.load_cms_data(year)
    #cms_by_drug = pd.read_csv(PATH.joinpath(f'cms_new_{year}.csv'))
    drug_name = cms_by_drug[['DrugName', 'Total_payment']].groupby(['DrugName']).sum().sort_values(by=['Total_payment'], ascending = False)
    drug_name = drug_name.iloc[:10,:]
    return drug_name


def get_df_payment_type(year):
    cms_by_year = data[year].copy()
    #cms_by_year = data_loader.load_cms_data(year)
    payment_type_year = cms_by_year[['nature_of_payment_or_transfer_of_value', 'Total_payment']]
    payment_types = {'Compensation for services other than consulting, including serving as faculty or as a speaker at a venue other than a continuing education program': 'Compensation_Other', 'Compensation for serving as faculty or as a speaker for a non-accredited and noncertified continuing education program':'Faculty/speaker at NonAcc', 'Space rental or facility fees (teaching hospital only)' : 'Space Rental','Compensation for serving as faculty or as a speaker for an accredited or certified continuing education program': 'Faculty/speaker at Acc', 'Current or prospective ownership or investment interest' : 'Investment Interest'}
    payment_type_year.replace({"nature_of_payment_or_transfer_of_value": payment_types}, inplace = True)
    return payment_type_year


def get_drug_device_entity_names(year):
    df = data[year].copy()
    df['Paying_Entity'] = df['Paying_Entity'].str.lower()
    paying_entities = df.Paying_Entity.unique()
    paying_entities.sort()
    return paying_entities

top_entity_names = {}
top_entity_names[2020] = get_drug_device_entity_names(2020)
top_entity_names[2019] = get_drug_device_entity_names(2019)

def get_fig_drug_device(year, entity_name):
    PayingEntity = data[year].copy()
    #PayingEntity = data_loader.load_cms_data(year)
    PayingEntity['physician_specialty'] = PayingEntity['physician_specialty'].str.replace('Allopathic & Osteopathic Physicians|','')
    PayingEntity['physician_specialty'] = PayingEntity['physician_specialty'].str.strip('|')
    PayingEntity['physician_specialty'] = PayingEntity['physician_specialty'].str.lstrip()
    PayingEntity['Paying_Entity'] = PayingEntity['Paying_Entity'].str.lower()

    PayingEntity_grpd = PayingEntity.groupby(['Paying_Entity', 'DrugName']).sum().reset_index()
    fig = go.Figure()
    default_comp = entity_name
    # default_comp = top_entity_names[2020][0]
    # if year == 2019:
    #     default_comp = top_entity_names[2019][0]

    payment = PayingEntity_grpd[(PayingEntity_grpd['Paying_Entity'] == entity_name)]
        # We have to add traces

    fig.add_trace(go.Bar(x = payment['DrugName'] , y = payment['Total_payment'], visible = (entity_name == default_comp),text = payment["Total_payment"],texttemplate='%{text:.2s}', textposition='outside'))
    fig.update_layout(height = 800)# title_text= 'Drug/Device by Pharma/medical device entity in 2020' , title_x=0.5, yanchor='bottom')
    fig.update_layout(title={
        'text': f"Drug/Device by entity in {year}",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'bottom'})
    
    return fig


layout = html.Div([
    html.Div([
        html.H4('Open Payments Overview')
    ], style={'textAlign':'center','marginTop':'-15px'},id='subheader', className='subheader'),

    html.Div([
        html.Div([
            html.H5('2020 Summary')
        ], style={'textAlign':'center'},id='smallheader1',className='six columns smallheader'),
        html.Div([
            html.H5('2019 Summary')
        ], style={'textAlign':'center'},id='smallheader2',className='six columns smallheader')
    ],className='row flex-display'),

    # row of cards (row 2)
    html.Div([
        # 2020 amount
        html.Div([
            html.H6(children='Total Amount',
                    style={'textAlign': 'center'}),
            html.P(f"{total_amount_2020}",
                    style={'textAlign': 'center', 'fontSize': 30}),
        ], className='card_container two columns'), # 2020 amount ends

        # blank card
        html.Div([
             html.H6(style={'textAlign': 'center'}),
        ], className='card_container two columns'), # blank card ends

        # blank card
        html.Div([
             html.H6(style={'textAlign': 'center'}),
        ], className='card_container two columns'), # blank card ends


        # 2019 amount
        html.Div([
            html.H6(children='Total Amount',
                    style={'textAlign': 'center'}),
            html.P(f"{total_amount_2019}",
                    style={'textAlign': 'center', 'fontSize': 30}),
        ], className='card_container two columns'), # 2019 amount ends

        # blank card
        html.Div([
             html.H6(style={'textAlign': 'center'}),
        ], className='card_container two columns'), # blank card ends

        # blank card
        html.Div([
             html.H6(style={'textAlign': 'center'}),
        ], className='card_container two columns'), # blank card ends
        
    ], className='row flex display'), #row 2 ends

    #figures
    html.Div([
        #2020 plot
        html.Div([
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id='option_2020',
                        options=[
                                {'value':'1','label':'Speciality'},
                                {'value':'2','label':'Month'},
                                {'value':'3','label':'Drug'},
                                {'value':'4','label':'PaymentType'},

                                ],
                        value="1",
                        labelStyle={'display':'inline-block'}
                    ),
                ],className='eight columns'),
            ],className='row flex display'),
            dcc.Graph(id='plot_2020')
        ],className='card_container six columns'),


        #2019 plot
        html.Div([
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id='option_2019',
                        options=[
                                {'value':'1','label':'Speciality'},
                                {'value':'2','label':'Month'},
                                {'value':'3','label':'Drug'},
                                {'value':'4','label':'PaymentType'},
                                
                                ],
                        value="1",
                        labelStyle={'display':'inline-block'}
                    ),
                ],className='eight columns'),
            ],className='row flex display'),
            dcc.Graph(id='plot_2019')
        ],className='card_container six columns'),

    ], className='row flex display'),

    #Drug device by entity
    html.Div([

        #2020 plot
        html.Div([
            dcc.Dropdown(id="entity_names_2020",
                        options = [ { "value": entity, "label": entity } for entity in top_entity_names[2020] ],
                        multi=False,
                        value=top_entity_names[2020][0]
                        ),
            dcc.Graph(id='drug_device_2020', config={'displayModeBar':'hover'})
        ],className='card_container six columns'),

        #2019 plot
        html.Div([
            dcc.Dropdown(id="entity_names_2019",
                        options = [ { "value": entity, "label": entity } for entity in top_entity_names[2019] ],
                        multi=False,
                        value=top_entity_names[2019][0]
                        ),
            dcc.Graph(id='drug_device_2019', config={'displayModeBar':'hover'})
        ],className='card_container six columns'),

    ], className='row flex display')

], id='paymentsContainer', style={'display': 'flex','flex-direction':'column'})#last line don't touch


#plot_2020
@app.callback(
    Output('plot_2020', 'figure'),
    [Input("option_2020", "value")])
def display_plot_2020(option_2020):

    if option_2020 == '1':
        title = 'Payments in 2020 by Speciality'
        df_speciality = get_df_speciality(2020)
        fig = px.bar(df_speciality, x=df_speciality.index, y="Total_payment", text = "Total_payment",
                height=650
                #color='Total_payment', #barmode='group',
                )
        fig.update_layout(title_text=title, title_x=0.5,margin={"r":0,"l":0,"b":0}, xaxis={'categoryorder':'total descending'})
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside', marker_color='lightsalmon')
        fig.update_yaxes(range=[0, 55000000])
    elif option_2020 == '2':
        title = 'Payments in 2020 by Month'
        df_month = get_df_month(2020)
        fig = px.line(df_month, x=df_month.index, y="Total_payment", text = "Total_payment",
             #color='smoker', barmode='group',
             height=600)
        fig.update_layout(title_text=title, title_x=0.5)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='top center',marker_color='lightsalmon')
        fig.update_yaxes(range=[1000000, 18500000])
    elif option_2020 == '3':
        title = 'Payments in 2020 by Drug/Device'
        df_drug = get_df_drug(2020)
        fig = px.bar(df_drug, x=df_drug.index, y="Total_payment", text = 'Total_payment',
             #color='smoker', barmode='group',
             height=650)
        fig.update_layout(title_text=title, title_x=0.5,xaxis={'categoryorder':'total descending'})
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside',marker_color='lightsalmon')
        fig.update_yaxes(range=[0, 20000000])
    elif option_2020 == '4':
        title = 'Total Payments by Nature of Payments in 2020'
        df_payment_type = get_df_payment_type(2020)
        fig = px.pie(df_payment_type, values='Total_payment', names='nature_of_payment_or_transfer_of_value')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', title = title, title_x=0.5)
        fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


# #plot_2019
@app.callback(
    Output('plot_2019', 'figure'),
    [Input("option_2019", "value")])
def display_plot_2019(option_2019):

    if option_2019 == '1':
        df_speciality = get_df_speciality(2019)
        title = 'Payments in 2019 by Speciality'

        fig = px.bar(df_speciality, x=df_speciality.index, y="Total_payment", text = "Total_payment",
                height=600
                #color='Total_payment', #barmode='group',
                )
        fig.update_layout(title_text=title, title_x=0.5,margin={"r":0,"l":0,"b":0}, xaxis={'categoryorder':'total descending'})
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_yaxes(range=[0, 55000000])
    
    elif option_2019 == '2':
        title = 'Payments in 2019 by Month'
        df_month = get_df_month(2019)
        fig = px.line(df_month, x=df_month.index, y="Total_payment", text = 'Total_payment',
             #color='smoker', barmode='group',
             height=600)
        fig.update_layout(title_text=title, title_x=0.5)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='top center',marker_color='lightsalmon')
    elif option_2019 == '3':
        title = 'Payments in 2019 by Drug/Device'
        df_drug = get_df_drug(2019)
        fig = px.bar(df_drug, x=df_drug.index, y="Total_payment", text = "Total_payment",
             ##color='smoker', barmode='group',
             height=600)
        fig.update_layout(title_text=title, title_x=0.5,xaxis={'categoryorder':'total descending'})
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    elif option_2019 == '4':
        title = 'Total Payments by Nature of Payments in 2019'
        df_payment_type = get_df_payment_type(2019)
        fig = px.pie(df_payment_type, values='Total_payment', names='nature_of_payment_or_transfer_of_value')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', title = title, title_x=0.5)
        fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig




@app.callback(
    Output('drug_device_2020', 'figure'),
    [Input("entity_names_2020", "value")])
def display_drug_device_2020(entity_names_2020):
    fig = get_fig_drug_device(2020, entity_names_2020 )
    return fig

@app.callback(
    Output('drug_device_2019', 'figure'),
    [Input("entity_names_2019", "value")])
def display_drug_device_2019(entity_names_2019):
    fig = get_fig_drug_device(2019, entity_names_2019 )
    return fig


