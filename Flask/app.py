from flask import Flask, jsonify, request
#from joblib import dump, load
from map import *

# d = app.data['traffic_gdf'] = traffic_gdf

app = Flask(__name__)
#load("model.joblib")

# Selects the page for which a function is to be defined. Right now there will only be one page in your website.

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]

@app.route('/')

def hello():
    # return "hello"
    # d = app.data['traffic_gdf'] = traffic_gdf
    return m._repr_html_()

# The above function returns the HTML code to be displayed on the page

@app.route('/incomes')
def get_incomes():
  return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return '', 204

if __name__ == '__main__':

   app.run()
