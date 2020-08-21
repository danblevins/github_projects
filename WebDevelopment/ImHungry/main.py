from flask import Flask, redirect, url_for, render_template, request, json
import pandas as pd
import numpy as np
from yelpapi import YelpAPI
#from flask_graphql import GraphQLView
#from schema import schema
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from bs4 import BeautifulSoup
import requests
import os
#

app=Flask(__name__)

### Web Pages ###
@app.route("/", methods=['POST', 'GET'])
def index():
    result=[]
    food = request.form.get("Food", 'Food')
    location = request.form.get("Location", 'City, State or Zipcode')

    if food in ['Food',''] and location in ['City, State or Zipcode','']:
        result=''
        message=''
    else:
        try:
            message = 'View your results below! (Results loaded using GraphQL)'
            api_key = os.environ.get('yelp_key')
            header = {'Authorization': 'bearer {}'.format(api_key),
                    'Content-Type':"application/json"}
            transport = RequestsHTTPTransport(url='https://api.yelp.com/v3/graphql', headers=header, use_json=True)
            client = Client(transport=transport, fetch_schema_from_transport=True)

            gql_str = ("""{{search(term: "{}",
                            location: "{}",
                            radius: 40000,
                            limit: 10,
                            sort_by: "best_match",
                            open_now: true) {{
                        business {{
                            name
                            price
                            rating
                            review_count
                            location {{
                                address1
                                city
                                state
                                country
                            }}
                            categories {{
                                alias
                            }}
                        }}
                    }}
                }}
            """).format(food, location)
            query_dict = client.execute(gql(gql_str))

            for i in range(len(query_dict['search']['business'])):
                temp_dict={}
                temp_dict['name'] = query_dict['search']['business'][i]['name']
                temp_dict['price'] = query_dict['search']['business'][i]['price']
                temp_dict['rating'] = query_dict['search']['business'][i]['rating']
                temp_dict['num_rating'] = query_dict['search']['business'][i]['review_count']
                temp_dict['address'] = (
                    query_dict['search']['business'][i]['location']['address1'] + ', ' 
                    + query_dict['search']['business'][i]['location']['city'] + ', ' 
                    + query_dict['search']['business'][i]['location']['state'] + ', ' 
                    + query_dict['search']['business'][i]['location']['country']
                )
                temp_list=[]
                for j in range(len(query_dict['search']['business'][i]['categories'])):
                    try:
                        temp_list.append(query_dict['search']['business'][i]['categories'][j]['alias'])
                        temp_dict['category'] = ' / '.join(temp_list)
                    except:
                        temp_dict['category'] = 'N/A'
                result.append(temp_dict)

        except:
            key = YelpAPI(os.environ.get('yelp_key'))
            store = key.search_query(term=food, location=location, radius=40000, limit=10, sort_by='best_match', open_now=True)
            for i in range(len(store['businesses'])):
                temp_dict={}
                temp_dict['name'] = store['businesses'][i]['name']
                temp_dict['price'] = store['businesses'][i]['price']
                temp_dict['rating'] = store['businesses'][i]['rating']
                temp_dict['num_rating'] = store['businesses'][i]['review_count']
                temp_dict['address'] = ', '.join(store['businesses'][i]['location']['display_address'])

                temp_list=[]
                for j in range(len(store['businesses'][i]['categories'])):
                    try:
                        temp_list.append(store['businesses'][i]['categories'][j]['title'])
                        temp_dict['category'] = ' / '.join(temp_list)
                    except:
                        temp_dict['category'] = 'N/A'
                        continue
                result.append(temp_dict)

            message = message = 'View your results below! (Results loaded using REST API)'

    return render_template("index.html", result=result, food=food, location=location, message=message)

if __name__ == '__main__':
    app.run(debug=False)