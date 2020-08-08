#!/usr/bin/env python3
"""
The purpose of schev_scrape.py is to scrape the schev website for fall enrollment, graduation headcount, and demographics for the Economics programs of 
most 4 year public school universities (excluding ODU, VSU, VMI, and Norfolk) and returns the final dataframe.

:: Functions ::
    make_univs_df()

Author(s): Dan Blevins
"""

#import libraries
import os
import pandas as pd
import numpy
from bs4 import BeautifulSoup
import requests

#make_univs_df pulls the fall enrollment and graduation headcount of Economics degrees for 4 year public universities. Excluding: ODU, VSU, VMI, and Norfolk
def make_univs_df():

    univs_dict = {
      'JMU': []
      , 'CNU': 'https://research.schev.edu/programbasics/231712/current/40/450601'
      , 'GMU': 'https://research.schev.edu/programbasics/232186/current/40/450601'
      , 'LONG': 'https://research.schev.edu/programbasics/232566/current/40/450601'
      , 'RAD': 'https://research.schev.edu/programbasics/233277/current/40/450601'
      , 'TECH': 'https://research.schev.edu/programbasics/233921/current/40/450601' #Need to include number 52.0601 as well
      , 'UMW': 'https://research.schev.edu/programbasics/232681/current/40/450601'
      , 'UVA': 'https://research.schev.edu/programbasics/234076/current/40/450601'
      , 'VCU': 'https://research.schev.edu/programbasics/234030/current/40/520601'
      , 'W&M': 'https://research.schev.edu/programbasics/231624/current/40/450601'
      }

    for univ,url in univs_dict.items():
        if 'JMU' in univ:
            final = pd.DataFrame()
            majors_dict = {'Accounting': [520301], 'CIS': [110401], 'Econ': [450601, 520601], 'Finance': [520801], 'Intl_Bus': [521101], 'Bus_Mgmt': [520201], 'Marketing': [521401]}
            for major,codes in majors_dict.items():
                count=0
                df = pd.DataFrame()
                for num in codes:
                    if len(codes) >= 2:
                        count += 1
                    page = requests.get("https://research.schev.edu/programbasics/232423/current/40/"+str(num))
                    soup = BeautifulSoup(page.content, 'html.parser')

                    cols = ['colACADYEAR-TH','colTTL_HC-TH', 'colTTL_DEGREES-TH']
                    dict_data = {}
                    for col in cols:
                        list_col = [] 
                        for data in soup.find_all('td', headers=col):
                            list_col.append(data.text)
                        dict_data[col] = list_col
                            
                    if count < 1:        
                        df = pd.DataFrame(dict_data)
                    else:
                        df_temp = pd.DataFrame(dict_data)
                        df = pd.concat([df,df_temp])
                        df['colTTL_HC-TH'] = df['colTTL_HC-TH'].astype(str).astype(int)
                        df['colTTL_DEGREES-TH'] = df['colTTL_DEGREES-TH'].astype(str).astype(int)
                        df = df.groupby(['colACADYEAR-TH']).agg({'colTTL_HC-TH':'sum','colTTL_DEGREES-TH':'sum'}).reset_index()
                        
                df.rename(columns={'colACADYEAR-TH': 'year', 'colTTL_HC-TH': 'fall_count', 'colTTL_DEGREES-TH': 'grad_count'}, inplace=True)
                df['major'] = major
                df['year'] = pd.to_datetime(df['year'].str.split('-').str[0]).dt.year
                df['fall_count'] = df['fall_count'].astype(str).astype(str).str.replace(',','').astype(int)
                df['grad_count'] = df['grad_count'].astype(str).astype(str).str.replace(',','').astype(int)
                final = pd.concat([final,df])

            final['cob_fall_count'] = final['fall_count'].groupby(final['year']).transform('sum')
            final['cob_grad_count'] = final['grad_count'].groupby(final['year']).transform('sum')
            final = final.sort_values(by=['major', 'year']).reset_index(drop=True)
            final['fall_perc'] = round(final['fall_count']/final['cob_fall_count']*100,1)
            final['grad_perc'] = round(final['grad_count']/final['cob_grad_count']*100,1)
            final = final.fillna(0)
            final['univ'] = str(univ).lower()
            final["univ"] = final["univ"].astype('category')
            
        else:
            final = pd.DataFrame()
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            cols = ['colACADYEAR-TH','colTTL_HC-TH', 'colTTL_DEGREES-TH']
            dict_data = {}
            for col in cols:
                list_col = [] 
                for data in soup.find_all('td', headers=col):
                    list_col.append(data.text)
                dict_data[col] = list_col

            df = pd.DataFrame(dict_data)     
            df.rename(columns={'colACADYEAR-TH': 'year', 
                                'colTTL_HC-TH': 'fall_count', 
                                'colTTL_DEGREES-TH': 'grad_count'
                              }, inplace=True)
            df['major'] = 'Econ'
            df['year'] = pd.to_datetime(df['year'].str.split('-').str[0]).dt.year
            df['fall_count'] = df['fall_count'].astype(str).astype(str).str.replace(',','').astype(int)
            df['grad_count'] = df['grad_count'].astype(str).astype(str).str.replace(',','').astype(int)
            final = df.sort_values(by=['major', 'year']).reset_index(drop=True)
            final['univ'] = str(univ).lower()
            final["univ"] = final["univ"].astype('category')

    return final

if __name__ == "__main__":
    make_univs_df()