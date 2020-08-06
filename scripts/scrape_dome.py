import requests
import pandas as pd
import time

def get_record(exh_id):
    url = f'https://exhibitions.univie.ac.at/search/export?entity=Person&filter[exhibition][exhibition][0]={exh_id}'
    return requests.get(url)

def read_record(data):
    return pd.read_excel(data)

exh_df = pd.read_excel('./Exhibition.xlsx')

artists_df = pd.DataFrame(columns=['ID', 'Name', 'Date of Birth', 'Place of Birth', 'Date of Death',
       'Place of Death', 'Gender', '(Primary) Nationality', 'ULAN', 'GND',
       'Wikidata', '# Exhibitions', '# Cat. Entries', 'Status', 'ExhibitionID'])

for id in exh_df['ID']:
    print(f'Processing record {id}')
    record = get_record(id)
    df = read_record(record.content)
    h, _w = df.shape
    if h == 0:
        continue
    df['ExhibitionID'] = pd.DataFrame([id] * h)
    artists_df = artists_df.append(df, ignore_index=True)
    artists_df.to_csv('./Artists.csv')
    time.sleep(0.5)
