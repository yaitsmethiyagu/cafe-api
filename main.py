from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    all_cafe = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafe)

    return jsonify(random_cafe.to_dict()), 200

    # return jsonify(
    #     id= random_cafe.id,
    #     name = random_cafe.name,
    #     map_url = random_cafe.map_url,
    #     img_url = random_cafe.img_url,
    #     location = random_cafe.location,
    #     seats = random_cafe.seats,
    #     has_toilet = random_cafe.has_toilet,
    #     has_wifi = random_cafe.has_wifi,
    #     has_sockets = random_cafe.has_sockets,
    #     can_take_calls = random_cafe.can_take_calls,
    #     coffee_price = random_cafe.coffee_price
    # )


@app.route("/all")
def get_all():
    all_cafe = db.session.query(Cafe).all()

    return jsonify([item.to_dict() for item in all_cafe])


@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets= bool(request.form.get("has_sockets")),
        can_take_calls= bool(request.form.get("can_take_calls")),
        coffee_price= request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(
        success="New cafe added to database"
    ), 200


@app.route("/search")
def search():
    if request.args:
        location_query = request.args.get("loc")

        result_cafe = db.session.query(Cafe).filter(Cafe.location == location_query.title()).all()

        if result_cafe:
            return jsonify([item.to_dict() for item in result_cafe]), 200

        else:
            return jsonify(
                error="Sorry we dont have records for this area"
            ), 404

    return jsonify( response = "Bad request"), 404


@app.route("/update_price/<id>", methods=["PATCH"])
def update_price(id):
    if request.args:
        price = request.args.get("price")
        result = db.session.query(Cafe).filter(Cafe.id == id).all()[0]

        result.coffee_price = price
        db.session.commit()

        return jsonify(
            sucess="Price updated in data base"
        ), 200
    else:
        return jsonify(response = "Invalid Cafe ID"), 404


@app.route("/delete/<id>", methods=["DELETE"])
def delete_cafe(id):
    if request.args.get("apikey") == "top_secrete":
        selected_cafe = db.session.query(Cafe).filter(Cafe.id == id).all()

        if selected_cafe:
            db.session.delete(selected_cafe[0])
            db.session.commit()
            return jsonify(response = "Cafe record deleted"), 200
        else:
            return jsonify(response= "Sorry Cafe not found with your ID"), 404

    else:
        return jsonify(response = "Invalid API key"), 403


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
