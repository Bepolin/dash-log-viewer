import pathlib
import glob

import pandas as pd

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
df_device = pd.read_csv('data/device_info.csv', encoding='utf-8-sig')
df_do_capture = pd.read_csv('data/usage_count/do_capture.csv', encoding='utf-8-sig')
date_list = list(df_device.columns)
date_list.remove('user_id')

dataset_list = [i for i in glob.glob('data/usage_count/*.csv')]


def _get_drop_reten(row):
    first_pet = row[0]
    last_pet = row[1]
    if first_pet == last_pet:
        return '機種変なし'
    else:
        if last_pet != '他社':
            return 'リテンション'
        elif last_pet == '他社':
            return '離脱'
        else:
            return 'その他'

def generate_device_change_table(date1, date2):
    df_device_change = df_device[['user_id', date1, date2]]
    first_last_pet = df_device[[date1, date2]]
    df_device_change['drop_reten'] = first_last_pet.apply(_get_drop_reten, axis=1)

    return df_device_change

def generate_usage_count_table(dataset, date1, date2):
    df_usage_count = pd.read_csv(f'data/usage_count/{dataset}.csv', encoding='utf-8-sig')
    date_list = pd.date_range(start=date1, end=date2, freq='D')
    return date_list, df_usage_count
