import hashlib, secrets
from configparser import ConfigParser
import os
import logging
import datetime as dt
import pyodbc, sqlalchemy, urllib
import pandas as pd
import numpy as np
import polars as pl
import holidays
from pathlib import Path
import os
import shutil

BASE_DIR = Path(__file__).parent.parent
BASE_DIR = './builtin'

#--------------------------------------------------------------------------------
# Set up Logger
#--------------------------------------------------------------------------------
today_dt = dt.datetime.strftime(dt.date.today(), format='%y%m%d')

# Check if log folder is available, if not create one
os.makedirs(f'{BASE_DIR}/log', exist_ok=True)

# Set up logger
logger = logging.getLogger('ETL_log')
logger.setLevel(logging.DEBUG)

# Create file handler for logging to a file
file_handler = logging.FileHandler(f'{BASE_DIR}/log/etlLog_{today_dt}.log')

# Create log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s = %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)

#--------------------------------------------------------------------------
# Read in config file
#--------------------------------------------------------------------------
def read_config_file(section): 
    """  
    Read the configuration file to obtain connection credential to data
    section: the name of credentials
        For example: [MYSQLCREDS]
    config_path: Path of the configuration file
    """
    config = ConfigParser()
    config.read(os.path.join(BASE_DIR, 'conf', 'credentials.conf'))
   
    if config.has_section(section):
        config_dict = dict(config.items(section))
        
        return config_dict 
    else:
        print('Section provided is INVALID')
        return None 

config = read_config_file('DATABASE')

#--------------------------------------------------------------------------
# Functions to generate API Keys and Hash Keys
#--------------------------------------------------------------------------
def generate_api_key(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def generate_api_hash(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def create_same_val_df(df, col_name, val):
    """
    Function to create a new column with the same value throughout
    """
    df = df.with_columns(
        pl.Series([val] * len(df)).alias(col_name)
    )

    return df

#--------------------------------------------------------------------------------
# Create holiday dataframe function
#--------------------------------------------------------------------------------
def create_holiday_list(start_year: int, end_year) -> pl.DataFrame:
    """  
    Function to create a list of federal holidays
    """

    years = []
    holiday_master = pl.DataFrame()
    for year in range(start_year, end_year + 1):

        years.append(year)
        datelist = list(holidays.US(years=year).keys())
        holidaylist = list(holidays.US(years=year).values())

        tmp = pl.DataFrame(data={'HolidayDate': datelist,
                            'HolidayYear': pl.Series([year] * len(datelist)),
                            'HolidayName': holidaylist})
        
        holiday_master = holiday_master.vstack(tmp)
    return holiday_master

#---------------------------------------------------------------------
# Library that create database interaction
#---------------------------------------------------------------------   
class Database:

    def __init__(self, cred_config: dict):

        self.cred_config = cred_config
        self.connection = None
        self.cred_config = cred_config
        self.conn_str = (
            'Driver={ODBC Driver 18 for SQL Server};'
            f'server=tcp:{self.cred_config["server"]};'
            f'database={self.cred_config["database"]};'
            f'uid={self.cred_config["user"]};'
            f'pwd={self.cred_config["password"]};'
            # f'trustservercertificate=yes;'
            # f'encrypt=yes;'
            f'authentication=ActiveDirectoryPassword'
        )

        self.param = urllib.parse.quote_plus(self.conn_str)
        self.engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect={}'.format(self.param), fast_executemany=True)

    def connectDB(self):
        try:
            self.connection = pyodbc.connect(self.conn_str)
            logger.info('Load: Successfully connected to the database!')
            return self.connection
        except Exception as error:
            logger.debug(f'Load: Error occured: {error}')

    def select(self, select_query, param=tuple()):

        if not self.connection:
            conn = self.connectDB()
            cursor = conn.cursor()
        else:
            cursor = self.connection.cursor()

        try:
            result = cursor.execute(select_query, param).fetchall()
            
            if len(result) == 0:
                df = pd.DataFrame()
                logger.info('Select: No data returned from database')
            else:
                df = pd.DataFrame(np.array(result), columns=[desc[0] for desc in cursor.description]) 
        except pyodbc.Error as error:
            print(error)
            df = pd.DataFrame()

        return df

    def execute_query(self, query, params=tuple()):
        """
        Function that insert data into db
        """
        conn = self.connectDB()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)
            conn.commit()
        except Exception as error:
            logger.debug(f'Execute SQL Error: {error}')
            conn.rollback()


    def df_to_sql_truncate_and_append(self, df, table_name, schema):
        """ 
        Function that insert dataframe to database using sqlalchemy ORM
        """
    
        if df is None:
            logger.debug(f'Load: Unable to load data to {schema}.{table_name} due to empty data. Please check previous steps')
            return None
        
        df_pandas = df.to_pandas()

        if sqlalchemy.inspect(self.engine).has_table(table_name, schema=schema):  # Check if the table exist, if not, throw an error
            try:
                # Truncate the table to remove all data
                self.execute_query(f'TRUNCATE TABLE {schema}.{table_name}')
                logger.info(f'Load: Successfully truncated table {schema}.{table_name}')
            
                df_pandas.to_sql(table_name, 
                        self.engine, 
                        index=False, 
                        if_exists="append", 
                        schema=schema,
                        chunksize=5000)
                logger.info(f'Load: Successfully load data to {schema}.{table_name}')
            except Exception as error:
                logger.debug(f'Error occured: {error}')
        else:
            logger.debug(f'Load: Error: {table_name} does not exists!')

    def df_to_sql_append(self, df, table_name, schema):
        """ 
        Function that insert dataframe to database using sqlalchemy ORM
        """

        if df is None:
            logger.debug(f'Load: Unable to load data to {schema}.{table_name} due to empty data. Please check previous steps')
            return None
        
        df_pandas = df.to_pandas()
        
        if sqlalchemy.inspect(self.engine).has_table(table_name, schema=schema): 
            try:
                df_pandas.to_sql(table_name, 
                        self.engine, 
                        index=False, 
                        if_exists="append", 
                        schema=schema,
                        chunksize=5000)
                logger.info(f'Load: Successfully load data to {schema}.{table_name}')
            except pyodbc.DataError as error:
                logger.debug(f'Error occured: {error}')
        else:
            logger.debug(f'Load: Error: {table_name} does not exists!')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        try:
            if self.connection:
                self.connection.close()
                print('Successfully closed connection')
        except Exception as error:
            print(error)
        finally:
            if 'connection' in locals():
                self.connection.close()

#---------------------------------------------------------------------
# ETL Functions Section
#--------------------------------------------------------------------- 
def create_sqlTable_from_df(df, schema, tableName):
    """
    Function to build a create statement to create table in SQL Server
        from polar dataframe that map its datatype to SQL server table
    Input:
        df: Polar dataframe that has defined data type
        schema: schema of the table to create
        tableName: name of the table to create
    Output: CREATE statement string
    NOTE: You can adjust the type in SQL to whatever matches -> type_map_to_sql
    """
    type_map_to_sql = {
        pl.String: 'VARCHAR(MAX)',
        pl.Date: 'DATETIME2(6)',
        pl.Datetime(time_unit='us', time_zone=None): 'DATETIME2(6)',
        pl.Datetime: 'DATETIME2(6)',
        pl.Float64: 'FLOAT',
        pl.Float32: 'FLOAT',
        pl.Int64: 'BIGINT',
        pl.Int32: 'INT',
        pl.Boolean: 'BIT'
    }
    create_table_sql = f'\n\nCREATE TABLE {schema}.{tableName} (\n\t'
    
    columns = [f'{column} {type_map_to_sql.get(data_type)}' for column, data_type in df.schema.items()] 
    create_table_sql += ',\n\t'.join(columns) + '\n)'   
    
    return create_table_sql

def TheLabStandardMapping(mapping_template, df, sheet_name, labtable_name=None):
    """
    Function to map Client's Data to The Lab Standard column name
    Input: 
        mapping_template: Mapping template (in Excel)
        df: Client's DataFrame
    """

    if df is None:
        logger.debug('Standardization: DataFrame is empty. Check previous steps')
        return None

    # Read in template file    
    template = pl.read_excel(f'{BASE_DIR}/put_std_mapping_here/{mapping_template}', sheet_name=sheet_name)
    template = (
        template
            .filter(
                (pl.col('TheLab_TableName') == labtable_name)
            )
    )
   
    if len(template) == 0:
        logger.debug('Standardization: DataFrame is empty after filtering. Please check table_name parameter')
        return None
    
    # Create Mapping dictionary to map Client's column name to The Lab Standard column name
    column_map = dict(zip(template['TheLab_ColumnName'], template['Client_ColumnName']))
    
    column_map_by_df = {val: key for key, val in column_map.items() if val in df.columns}
    
    df_standard = df.select(
        pl.col(list(column_map_by_df.keys()))
    )

    df_standard = df_standard.rename(column_map_by_df)
    
    logger.info('Standardization: Successfully transform the data to The Lab data model')
    
    return df_standard

# Move Processed File to processed_data folder
def MoveFile(file_loc,
             file_name,
             processed_folder='processed_data'):

    # Move data file into processed_data folder
    source_file = os.path.join(file_loc, file_name)
    
    try:
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        destination_file = os.path.join(processed_folder, file_name)

        shutil.move(source_file, destination_file)
        logger.info(f'Move: {file_name} has been moved to {processed_folder} folder!')

    except Exception as error:
        logger.debug(f'Move: Error occured: {error}')

file_handler.close()