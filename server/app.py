# server/app.py

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

# -------------------------------
# /plants  → GET (all), POST (create)
# -------------------------------
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [p.to_dict() for p in plants], 200

    def post(self):
        data = request.get_json()
        try:
            plant = Plant(
                name=data.get('name'),
                image=data.get('image'),
                price=data.get('price')
            )
            db.session.add(plant)
            db.session.commit()
            return plant.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

# -------------------------------
# /plants/<id>  → GET single plant
# -------------------------------
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
