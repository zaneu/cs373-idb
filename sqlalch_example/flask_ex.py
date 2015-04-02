from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

data = [
  {
    "id": 1,
    "name": "Caribou Lou",
    "description": "Referenced in the song \"Caribou Lou\" by rapper Tech N9ne where he sings about it - \"...151 rum, pineapple juice, and malibu, caribou, get them all numb...\". The directions are included in the song also but are scaled to a unknown jug quantity. Therefore mix as you please but remember it's the 151 that will hit you. Originated in Kansas City, MO.",
    "recipe": "1 1/2 parts 151 proof rum, 1 part Malibu coconut rum, 5 parts pineapple juice",
    "ingredients": "151 proof rum, Malibu coconut rum, pineapple juice"
  },
  {
    "id": 2,
    "name": "Jager Bomb",
    "description": "The Jager Bomb is originally a mixture of Red Bull and Jagermeister, both being popular products, although it's increasingly common for other energy drinks to be substituted for the RB. The caffeine-alcohol combination creates a unique \"high\" or at the very least, a counteract to the depressant of alcohol - making you more aware, more energetic, and more active.",
    "recipe": "1/2 can Red Bull energy drink, 1 - 2 oz Jagermeister herbal liqueur",
    "ingredients": "Red Bull energy drink, Jagermeister herbal liqueur"
  }
]


@app.route("/drinks", methods=['GET'])
def get_drinks():
    print ("Getting drinks.")
    return jsonify ({'data': data})

#@app.route("/users", methods=['GET'])
#def get_users():
	#print ("Getting users.")
	#return database stuff from SQLAlchemy 


if __name__ == "__main__":
    app.run()



