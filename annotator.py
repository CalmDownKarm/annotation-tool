import os
import glob
import gramex.data
import gramex.cache
from sqlalchemy import create_engine
C_ = {
    'T_NAME' : '_data_rows',
    'CONFIG': 'config.yaml'
}
def create_tables():
    directory = os.path.dirname(os.path.abspath(__file__))
    datasets = os.path.join(directory, 'datasets')
    int_db_url = os.path.join(directory, 'datasets.db')
    for directory in glob.glob(datasets+'/*/'):
        config = gramex.cache.open(os.path.join(datasets, directory, C_['CONFIG']), 'config')
        dataset_name = config.conf.name
        dataset_url = config.conf.url
        dataset_query = config.conf.get('query', None)
        engine = create_engine('sqlite:///{int_db_url}')
        datasets = gramex.cache.query('select * from datasets', engine, state=['datasets'])
        # if name in datasets, do nothing,
        if datasets[datasets['name'] == dataset_name].empty():
            # Load the dataset from the folder.
            if gramex.data.get_engine(dataset_url) == 'file':
                dataset_url = os.path.join(datasets, directory, dataset_url)
            data_rows = gramex.data.filter(url = dataset_url, query=dataset_query)
            

