__version__ = '1.0.2'

import pkgutil
import pandas as pd # type: ignore
from io import StringIO  # noqa: F401

def load_dataset(country, file_name):
    data = pkgutil.get_data('phenofect', f'Data/{country}/{file_name}')
    if data is None:
        raise FileNotFoundError(f"File '{file_name}' does not exist in the Data/{country} directory.")
    return pd.read_csv(StringIO(data.decode('utf-8')))

