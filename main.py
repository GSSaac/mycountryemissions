# Author: 
# --- Giuseppina Schiavone
# Organization: 
# --- Sustainability Advanced Analytics Consultancy
# Date: 
# --- February 2024
# Project:
# ---
#   Build and Deploy A Python Web App In One Evening
#   Online Working Session
#   26th February 2024, 6:00-8:00 PM, CET

# Description of this file:
# ---this is the main file of the application called by uvicorn main:app

# Datasource:
# ---
# Global Carbon Budget (2023) – with major processing by Our World in Data. “Annual CO₂ emissions – GCB” [dataset]. 
# Global Carbon Project, “Global Carbon Budget” [original data].
# https://ourworldindata.org/co2-emissions


# import libraries and functions

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import MetaData
from datetime import datetime

import uvicorn
import sys

from utils import create_db_and_tables, engine_views, get_countries_emissions
import plotly.express as px


sys.path.append("./")


# open application
app = FastAPI()
# mount the folders static and data
app.mount("/static", StaticFiles(directory="./static"), name = "static")
app.mount("/data", StaticFiles(directory="./data"), name = "data")
templates = Jinja2Templates(directory="./templates")

# get current date
now = datetime.now().date()

# get dataset of countries' emissions
countries_df,countries_list,high_df,middle_df,low_df, world_df = get_countries_emissions()


########## figure start: ANIMATED EMISSIONS MAP
fig = px.choropleth(countries_df,
                    locations='Code',
                    color='Annual CO₂ emissions',
                    animation_frame='Year',
                    animation_group='Entity',
                    #title='Choropleth Map of Countries Annual Emissions',
                    color_continuous_scale='YlOrRd')
fig.frames = list(reversed(fig.frames))
fig["layout"].pop("updatemenus") # optional, drop animation buttons
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Annual CO₂ emissions in tonnes",
    ),
)
fig.update_geos(projection_type="natural earth", visible=False, scope="world")#,projection_scale=1, center={"lat": 29.5, "lon": 42.5})
plot_config = {'displayModeBar': False}
plot_map = fig.to_html(full_html=False,config=plot_config)
########## figure end


# at startup create table of countries views from users
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    now = datetime.now().date()
    return now


# connect to main mycountryemissions.html
@app.get('/', response_class = HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        'mycountryemissions.html', {"request": request,
        "my_country": [],
        "countries_list" : countries_list,
        "plot_html": plot_map}
    )



# get selected country from dropdownmenu and produce visualizations
@app.get('/getmycountry/')
def read_mycountry(request: Request, my_country: str):

    # get selected data and produce a script that prints the emissions of the selected country in the last available year
    selected_data = countries_df[countries_df['Entity']==my_country]
    E = str(selected_data[selected_data['Year']==selected_data['Year'].max()]['Annual CO₂ emissions'].values[0])
    Y = selected_data['Year'].max()

    script_emissions = f"""
        <div class="hidden-text" id="hiddenText">
            <strong>{E} tonnes of CO₂ </strong> in {Y} in {my_country}
        </div>
        """
    
    # append data of selected country to database of countries views
    countries_views_table = [my_country,now]
    countries_views_table = pd.DataFrame(countries_views_table).T
    countries_views_table.columns = ['Entity','Date']
    countries_views_table.to_sql(name='views', con=engine_views,if_exists='append', index=False)


    # get countries views from database of countries views
    countries_views_df = pd.read_sql_table(table_name="views", con=engine_views)
    # select only the views of the current day
    countries_views_df = countries_views_df.loc[countries_views_df['Date']==str(now),:]
    # count views per country and connect countries to emissions in the last available year
    view_count_df = countries_views_df['Entity'].value_counts().reset_index(name='# views')
    select_countries_last_year = countries_df.loc[countries_df['Year']==countries_df['Year'].max(),:].reset_index(drop = True)
    emissions_selectd_countries = select_countries_last_year[['Annual CO₂ emissions','Entity']].loc[select_countries_last_year['Entity'].isin(view_count_df['Entity'].tolist()),:].set_index(['Entity'])
    view_count_df.set_index(['Entity'],inplace = True)
    view_count_df['Annual CO₂ emissions'] = 0.0
    view_count_df['Annual CO₂ emissions'].loc[emissions_selectd_countries.index] = emissions_selectd_countries['Annual CO₂ emissions']
    view_count_df.reset_index(inplace = True)

    
    ########### figure start: COUNTRIES VISITED DURING THE SESSION
    fig = px.bar(view_count_df, x='Entity', y='# views',color = 'Annual CO₂ emissions',color_continuous_scale='YlOrRd')
    fig.update_layout({ 'xaxis_title':" ",
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    fig.update_coloraxes(colorbar={'orientation':'h', 'thickness':10})
    fig.update_layout(
    coloraxis_colorbar=dict(
        title="CO₂ emissions in tonnes in "+str(countries_df['Year'].max()),
        lenmode='fraction', len=0.5,
        y = 1,
        # yanchor='top',
        titleside = 'top'
    ),
    )
    plot_config = {'displayModeBar': False}
    plot_views = fig.to_html(full_html=False,config=plot_config)
    ########### figure end




    ########### figure start: SELECTED COUNTRY'S EMISSION OVER TIME
    df = pd.concat([world_df,low_df,middle_df,high_df,selected_data], axis = 0)
    fig = px.line(df, x='Year', y='Annual CO₂ emissions', color='Entity', markers=True)
    fig['data'][0]['line']['color']='rgb(0, 0, 0)'
    fig['data'][1]['line']['color']='rgb(240,240,240)'
    fig['data'][2]['line']['color']='rgb(204, 204,204)'
    fig['data'][3]['line']['color']='rgb(128,128,128)'
    fig['data'][4]['line']['color']='rgb(255,0,0)'
    fig['data'][4]['line']['width']=5
    fig.update_layout({'yaxis_title':"CO₂ emissions in tonnes",
    'xaxis_title':" ",
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))
    # fig.update_layout(yaxis_range=[0,500000000])
    fig.update_layout(legend={"title":""})
    # fig.update_layout(modebar_remove=['zoom', 'pan'])
    plot_config = {'displayModeBar': True}
    plot_overtime = fig.to_html(full_html=False,config=plot_config)
    ########### figure end

    # combine the visualizations in a script where they are set into 2 columns


    script_visuals = f"""
        <div class="row">
            <div class="column">
            <h3>{my_country} 's emissions over time</h3>
            {plot_overtime}
            </div>
            <div class="column">
            <h3>Countries most viewed</h3>
            {plot_views}
            </div>
        </div>"""

    
    return templates.TemplateResponse(
        'mycountryemissions.html',
         {"request": request,
         "my_country": my_country, 
         "countries_list" : countries_list, 
         "script": script_emissions,
         "plot_html": script_visuals}
    )
