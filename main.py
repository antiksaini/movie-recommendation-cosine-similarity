from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

from recommender import getSuggestions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/get": {"origins": "http://localhost:5000"}})


@app.route('/get')
@cross_origin()
def getRecommendation():
  given_name = request.args.get('title')
  suggestions = getSuggestions(given_name)
#  suggestions.headers.add('Access-Control-Allow-Origin', '*')
  return suggestions

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")

if __name__ == '__main__':
  app.run(debug=True)