import re
import os
import glob
import gramex.data
import gramex.cache
import pandas as pd
from gramex import variables as C_


def create_tables():
    directory = os.path.dirname(os.path.abspath(__file__))
    datasets_path = os.path.join(directory, 'datasets')
    int_db_url = os.path.join(directory, 'datasets.db')
    datasets_url = f'sqlite:///{int_db_url}'
    for directory in glob.glob(datasets_path+'/*/'):
        config = gramex.cache.open(os.path.join(datasets_path, directory, C_['CONFIG']), 'config')
        dataset_name = config.conf.name
        dataset_url = config.conf.url
        dataset_query = config.conf.get('query', None)
        engine = gramex.data.create_engine(datasets_url)
        datasets = gramex.cache.query('select * from datasets', engine, state=['datasets'])
        # if name in datasets, do nothing,
        if datasets[datasets['name'] == dataset_name].empty:
            # Load the dataset from the folder.
            if gramex.data.get_engine(dataset_url) == 'file':
                dataset_url = os.path.join(datasets_path, directory, dataset_url)
            data_rows = gramex.data.filter(url=dataset_url, query=dataset_query)
            primary_keys = [config.conf.get('primary_key', None), None, None]
            columns = [data_rows.dtypes.to_dict(), C_['UT_CONFIG'], C_['A_CONFIG']]
            tablenames = [dataset_name + C_[c] for c in ['T_NAME', 'UT_NAME', 'A_NAME']]
            for pk, cols, tablename in zip(primary_keys, columns, tablenames):
                create_table_query(tablename, engine, cols, pk)
            # Insert data rows
            count = gramex.data.insert(datasets_url, args=data_rows.to_dict(orient='list'),
                               table=dataset_name+C_['T_NAME'])
            print(f'{count} rows inserted')
            # Insert row into datasets table
            columns = {key: [value] for key, value in config.conf.items()
                       if not isinstance(value, list)}
            gramex.data.insert(url=datasets_url, args=columns, table='datasets')


def create_table_query(tablename, engine, columns, primary_key=None):
    '''
    Executes sql statments to create tables.
    @param tablename:
    @param engine: sql alchemy engine object
    @param primary_key: name of primary key column
    '''
    pandas_to_SQLITE = {
        "pd.np.dtype('int64')": 'BIGINT',
        "pd.np.dtype('float64')": 'REAL',
        "pd.np.dtype('object')": 'TEXT',
        "pd.np.dtype('<M8[ns]')": 'DATETIME'
    }
    slug = re.compile('[^A-Za-z0-9s-]')
    [print(key, val) for key, val in columns.items()]
    # cols = [(f'{slug.sub("", key)} {pandas_to_SQLITE[val]}' +
    #          (' PRIMARY KEY' if key == primary_key else ''))
    #         for key, val in columns.items()]
    # if not primary_key:
    #     cols += ['prikey INTEGER PRIMARY KEY AUTOINCREMENT']
    # query = f'CREATE TABLE IF NOT EXISTS {tablename}({", ".join(cols)});'
    engine.execute(query)
