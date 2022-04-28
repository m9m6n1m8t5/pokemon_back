from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource
import requests
import random

app = Flask(__name__, static_folder="../frontend/dist/static", template_folder="../frontend/dist")
app.config['JSON_AS_ASCII'] = False 
api = Api(app)


class Quiz(Resource):
  ALL_MOVES = 826
  
  def _getNameJa(self,names):
    name_ja = [d["name"] for d in names if d["language"]["name"]=="ja-Hrkt"]
    if len(name_ja)==0:
      return False
    else:
      return name_ja[0]

  def get(self):
    idx = random.randrange(1,Quiz.ALL_MOVES+1)
    r_move = requests.get("https://pokeapi.co/api/v2/move/" + str(idx)).json()
    
    move_name_en = r_move["name"]
    move_name_ja = self._getNameJa(r_move["names"])
    
    r_type = requests.get(r_move["type"]["url"]).json()
    move_type_ja = self._getNameJa(r_type["names"])
    
    r_class = requests.get(r_move["damage_class"]["url"]).json()
    move_class_ja = self._getNameJa(r_class["names"])
    
    learning_pokemon_url = random.choice(r_move["learned_by_pokemon"])["url"]
    r_learning_pokemon = requests.get(learning_pokemon_url).json()
    r_species = requests.get(r_learning_pokemon["species"]["url"]).json()
    learning_pokemon_ja = self._getNameJa(r_species["names"])

    rtn = {
      "englishName": move_name_en,
      "japaneseName": move_name_ja,
      "hintText": [
        f"{learning_pokemon_ja}がおぼえるよ",
        f"{move_class_ja}わざだよ", 
        f"{move_type_ja}タイプだよ"
        ],
    }
    return jsonify(rtn)

api.add_resource(Quiz, "/api/quiz")

# CORSエラー対策
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route("/", defaults={"path":""})
@app.route("/<path:path>")
def index(path):
  return render_template("index.html")

if __name__=="__main__":
  app.run(debug=True)