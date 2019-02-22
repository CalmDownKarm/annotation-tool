import os
import glob
import gramex.data
import gramex.cache
import pandas as pd

C_ = {
    'T_NAME': '_data_rows',
    'CONFIG': 'config.yaml',
    'UT_NAME': '_annotators',
    'A_NAME': '_annotations',
    'UT_CONFIG': {'user': pd.np.dtype('object'),
                  'github': pd.np.dtype('object'),
                  'test': pd.np.dtype('int64')},
    'A_CONFIG': {'user': pd.np.dtype('object'),
                 'annotation': pd.np.dtype('object'),
                 'timestamp': pd.np.dtype('<M8[ns]'),
                 'rowid': pd.np.dtype('int64')
                 }
}


def create_tables():
    directory = os.path.dirname(os.path.abspath(__file__))
    datasets = os.path.join(directory, 'datasets')
    int_db_url = os.path.join(directory, 'datasets.db')
    datasets_url = f'sqlite:///{int_db_url}'
    for directory in glob.glob(datasets+'/*/'):
        config = gramex.cache.open(os.path.join(
            datasets, directory, C_['CONFIG']), 'config')
        dataset_name = config.conf.name
        dataset_url = config.conf.url
        dataset_query = config.conf.get('query', None)
        engine = gramex.data.create_engine(datasets_url)
        datasets = gramex.cache.query(
            'select * from datasets', engine, state=['datasets'])
        # if name in datasets, do nothing,
        if datasets[datasets['name'] == dataset_name].empty():
            # Load the dataset from the folder.
            if gramex.data.get_engine(dataset_url) == 'file':
                dataset_url = os.path.join(datasets, directory, dataset_url)
            data_rows = gramex.data.filter(url=dataset_url, query=dataset_query)
            primary_keys = [config.conf.get('primary_key', None), None, None]
            columns = [data_rows.dtype.to_dict(), C_['UT_CONFIG'], C_['A_CONFIG']]
            tablenames = [dataset_name + C_[c] for c in ['T_NAME', 'UT_NAME', 'A_NAME']]
            for pk, cols, tablename in zip(primary_keys, columns, tablenames):
                create_table_query(tablename, engine, cols, pk)
            # Insert data rows
            gramex.data.insert(dataset_url, args=data_rows.to_dict(orient='list'),
                               table=dataset_name+C_['T_NAME'])
            # Insert row into datasets table
            columns = {key: [value] for key, value in config.conf.items()
                       if not isinstance(value, list)}
            gramex.data.insert(url=datasets_url, args=columns,
                               engine=engine, table='datasets')


def create_table_query(tablename, engine, columns, primary_key=None):
    ''' Executes sql statments to create tables.
    @param tablename:
    @param engine: sql alchemy engine object
    @param primary_key: name of primary key column
    '''
    pandas_to_SQLITE = {
        pd.np.dtype('int64'): 'BIGINT',
        pd.np.dtype('float64'): 'REAL',
        pd.np.dtype('object'): 'TEXT',
        pd.np.dtype('<M8[ns]'): 'DATETIME'
    }
    if primary_key:
        cols = [(f'{key} {pandas_to_SQLITE[val]}' + (' PRIMARY KEY' if key == primary_key else ''))
                for key, val in columns.items()]
    else:
        cols += ['index INTEGER PRIMARY KEY AUTOINCREMENT']
    query = f'CREATE TABLE {tablename}({", ".join(cols)});'
    print(query)
    engine.execute(query)
