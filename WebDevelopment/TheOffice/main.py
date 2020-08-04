from flask import Flask, redirect, url_for, render_template, request, json
import pandas as pd
import random
import re

app=Flask(__name__)

def get_quote():
    data = pd.read_csv("/Users/danblevins/Desktop/office_game/data/data.csv")
    correct = random.choice(data['Character'].unique().tolist())
    char_data = data[data['Character'] == correct].sample(n=1).reset_index(drop=True)
    quote = str(" '"+char_data['Line'][0]+"' ")

    char_list=[correct]
    while len(char_list) < 4:
        add_char = random.choice(data['Character'].unique().tolist())
        if add_char not in char_list:
            char_list.append(add_char)
        else:
            pass
    random.shuffle(char_list)

    return quote, correct, char_list

### Web Pages ###
@app.route("/", methods=['POST', 'GET'])
def home():
    quote, correct, char_list = get_quote()

    return render_template('index.html', quote=quote, correct=correct, char_list=char_list)

@app.route("/answer")
def answer():
    correct = request.args.get("correct")

    #quote = str(home())
    #char1 = '<h3 type="submit" name="quote"> &#39; '
    #char2 = '&#39; </h3>'
    #quote = (quote[quote.find(char1)+1 : quote.find(char2)])
    #print(quote)
    #print(str(home()))


    return render_template('answer.html', correct=correct)

if __name__ == '__main__':
    app.run(debug=True)
