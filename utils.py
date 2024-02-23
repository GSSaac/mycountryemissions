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
# ---this is an utitily files containing relevant functions are variables that will be called by the main.py

# Datasource:
# ---
# Global Carbon Budget (2023) – with major processing by Our World in Data. “Annual CO₂ emissions – GCB” [dataset]. 
# Global Carbon Project, “Global Carbon Budget” [original data].
# https://ourworldindata.org/co2-emissions


# import libraries and functions
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy import Text, MetaData, Table, insert, select, func
import pandas as pd

# Connect to the database
database_name = "./data/countries_views.db"
DATABASE_URL = f"sqlite:///{database_name}"

engine_views = create_engine(DATABASE_URL)

def create_db_and_tables():
    metadata = MetaData()
    countries_table = Table(
                'views',
                metadata,
                Column('Entity', String, nullable=False),
                Column('Date', Date, nullable=False),
    )

    metadata.create_all(engine_views)


    # # Insert data into the 'countries' table
    # with engine_views.connect() as connection:
    #     # Check if table is present in database
    #     table = Table('views', metadata, autoload=True)
    #     # check if the table countries is empty
    #     stmt = select([func.count()]).select_from(table)
    #     count = connection.execute(stmt).scalar()

    #     if count == 0: # if the table countries is empty then add data inside
    #         print('views is empty')
    #         # insert_stmt = insert(countries_table)
    #         # connection.execute(insert_stmt, countries_data)
            


def get_countries_emissions():
    database_name = "./data/countries_emissions.db"
    DATABASE_URL = f"sqlite:///{database_name}"
    # connect to database
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    metadata.create_all(engine)

    metadata.reflect(bind=engine)
    
    # get tables from database
    stmt = select(metadata.tables.values())
    with engine.connect() as conn:
        countries_df = conn.execute(stmt).all()
    countries_df = pd.DataFrame(countries_df)

    # isolate some data to use for plotting
    world_df = countries_df[countries_df['Entity']=='World']
    low_df = countries_df[countries_df['Entity']=='Lower-middle-income countries']
    middle_df = countries_df[countries_df['Entity']=='Upper-middle-income countries']
    high_df = countries_df[countries_df['Entity']=='High-income countries']
    # clean up data of interest
    # drop codes with nan
    countries_df = countries_df[~countries_df['Code'].isna()]
    # drop codes with underscore
    countries_df = countries_df[~countries_df['Code'].str.contains('_')]
    # get unique list of entities
    countries_list = countries_df['Entity'].unique()
    countries_list.sort()
    countries_df = countries_df.sort_values(by='Year')

    return countries_df,countries_list,high_df,middle_df,low_df, world_df
