import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

save = "/Users/danblevins/Desktop/the_office_quotes/data/data.csv"

#Scrape the office seasons
def scrape_seasons(season_min = 1, season_max = 7):
    base_url = 'http://officequotes.net/no'
    office_lines = pd.DataFrame()

    episode_number_overall = 1
    for season in range(season_min,season_max+1):
        url = base_url + str(season) + '-'
        num_errors = 0

        for episode in range(1,27):
            if num_errors == 0:
                if episode in {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                    temp_url = url + str(0) + str(episode) + '.php'
                else:
                    temp_url = url + str(episode) + '.php'

                error = '\n<p align="center"><img src="img/dwight_ahh.jpg" /></p>\n<p align="center"><font size="8">404 Page Not Found</font></p>\n<p align="center">(Did you ask yourself "Would an idiot do that?" before you typed in the URL?)</p>\n'
                response = requests.get(temp_url).content.decode(errors='ignore')

                if error in response:
                    pass
                else:
                  try:
                      soup = BeautifulSoup(response, 'html.parser')

                      results = []
                      for b_tag in soup.find_all('b')[13:]:
                          temp_dict = {'Character': None,
                          'Line' : None,
                          'Season' : None,
                          'Episode_Number' : None,
                          'Episode_Number_Overall': None}

                          temp_dict['Character'] = b_tag.text
                          temp_dict['Line'] = b_tag.next_sibling
                          temp_dict['Season'] = season
                          temp_dict['Episode_Number'] = episode
                          temp_dict['Episode_Number_Overall'] = episode_number_overall
                          results.append(temp_dict)
                      episode_number_overall += 1

                      df_results=pd.DataFrame(results)

                      index = (df_results[df_results['Character'] == 'Deleted Scene 1'].index.values)
                      if index.size > 0:
                          df_results = df_results.head(index[0])

                      office_lines = office_lines.append(df_results, ignore_index = True)
                  except:
                      num_errors += 1

    #Clean dataframe
    #office_lines.dropna(subset=['Line'], inplace=True)
    mask = (office_lines['Line'].str.len() == 40)
    office_lines = office_lines.loc[mask]
    #Fix the "Character" column for misspellings.
    office_lines['Character'] = office_lines['Character'].str.title()
    office_lines['Character'] = [character.strip() for character in office_lines['Character']]
    office_lines['Character'] = [character.strip('"') for character in office_lines['Character']]
    office_lines['Character'] = [character.strip(':') for character in office_lines['Character']]
    office_lines.replace({'Character':{'Michel:':'Michael:', 'Darry:' : 'Darryl:'}}, inplace=True)

    #Only include characters that have 1,000+ lines.
    data = office_lines.groupby(['Character']).Line.agg('count').reset_index().sort_values(by=['Line'], ascending=False)
    data = data[data['Line'] >= 10].sort_values(by=['Line'], ascending=False).reset_index(drop=True)

    df = pd.DataFrame()
    for character in data['Character']:
        char_data = office_lines[office_lines['Character'].isin([character])]
        df = df.append(char_data)

    df.to_csv(save, index=False, header=True)
    return df

scrape_seasons()