import flask 
from flask import request, jsonify, redirect
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
  return redirect("https://www.freaksmind.me", code=302)

@app.errorhandler(404)
def page_not_found(e):
  return jsonify("Not Found"), 404

@app.route('/v1/games/recommended/', methods = ['GET'])
def api_id():

  if 'game' in request.args:
      id = request.args['game']
  else:
      return "Error: No game field provided. Please specify a game."

  df = pd.read_csv("https://raw.githubusercontent.com/FreaksMind/recommendation-api/master/games.csv")
  def data_c(row):
    return row['genres'] + " " + row['publisher'] + " " + row['year']
  
  df["data_co"] = df.apply(data_c, axis = 1)
  matrice = CountVectorizer().fit_transform(df["data_co"])
  cosine_s = cosine_similarity(matrice)
  
  def get_title(index):
    return df[df.index == index]["title"].values[0]

  def get_index(title):
  	return df[df.title == title]["index"].values[0]
  
  test_game = id
  game_index = get_index(test_game)
  
  similar_games = list(enumerate(cosine_s[game_index]))
  sortedz = sorted(similar_games, key = lambda x: x[1], reverse = True)[1: ]
  thislist = []
  i = 0
  for element in sortedz:
    thislist.append(get_title(element[0]))
    i = i + 1
    if i >= 3:
        break
  
  return jsonify(thislist)


app.run()
