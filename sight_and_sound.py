import json
import pandas
import pathlib
import pydash
import requests
import time
import tqdm
import uuid

data_path = pathlib.Path.cwd() / 'sight_and_sound.parquet'

if not data_path.exists():

    index = requests.get('https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time/all-voters').text
    index = index.split('<script type="text/javascript">var initialPageState = ')[1].split('</script>')[0]
    dataframe = pandas.DataFrame(pydash.get(json.loads(index), 'componentState.allVoters'))
    dataframe = dataframe[['firstname', 'surname', 'type', 'country', 'url']]

    votes = pandas.DataFrame()
    for x in tqdm.tqdm(dataframe.url.unique()):

        time.sleep(4)

        vote_page = pandas.read_html('https://www.bfi.org.uk'+x, encoding='utf8')[0]
        vote_page['url'] = x
        votes = pandas.concat([votes, vote_page])

    dataframe = pandas.merge(dataframe, votes, on='url', how='left')
    dataframe = dataframe.astype(str)
    dataframe.to_parquet(data_path)
else:
    dataframe = pandas.read_parquet(data_path)

print(len(dataframe))
dataframe.head()