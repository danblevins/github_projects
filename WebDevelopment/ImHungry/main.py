from flask import Flask, redirect, url_for, render_template, request, json
import pandas as pd
import numpy as np
from yelpapi import YelpAPI
from bs4 import BeautifulSoup
import requests
import os
key = YelpAPI(os.environ.get('yelp_key'))

app=Flask(__name__)

### Web Pages ###
@app.route("/", methods=['POST', 'GET'])
def index():
    try:
        result=[]
        food = request.form.get("Food", False)
        location = request.form.get("Location", False)
        store = key.search_query(term=food, location=location, radius=40000, limit=10)
        for i in range(len(store['businesses'])):
            temp_dict={}
            temp_dict['name'] = store['businesses'][i]['name']
            try:
                temp_dict['price'] = store['businesses'][i]['price']
            except:
                temp_dict['price'] = 'Unavailable'
                continue
            try: 
                temp_dict['rating'] = store['businesses'][i]['rating']
            except:
                temp_dict['rating'] = 'Unavailable'
                continue
            try:
                temp_dict['num_rating'] = store['businesses'][i]['review_count']
            except:
                temp_dict['num_rating'] = 'Unavailable'
                continue
            try:
                temp_dict['address'] = ', '.join(store['businesses'][i]['location']['display_address'])
            except:
                temp_dict['address'] = 'Unavailable'
                continue

            temp_list=[]
            for j in range(len(store['businesses'][i]['categories'])):
                try:
                    temp_list.append(store['businesses'][i]['categories'][j]['title'])
                    temp_dict['category'] = ' / '.join(temp_list)
                except:
                    temp_dict['category'] = 'Unavailable'
                    continue
            result.append(temp_dict)
    except:
        pass
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=False)