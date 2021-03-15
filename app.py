"""Flask app for Cupcakes"""
from flask import Flask, redirect, request, jsonify, render_template
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

@app.route("/api/cupcakes")
def get_cupcake_data():
  """Get data about cupcakes."""
  cupcakes = Cupcake.query.all()
  serialized = [c.serialize() for c in cupcakes]

  return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size, rating, image, ingredients:{}}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # ingredients = cupcake.ingredients
    # cupcake['ingredients'] = ingredients
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake from form data & return it.

    Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """
    # data = request.json["cupcake"]
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
  """Update cupcake from form data & return it."""

  cupcake = Cupcake.query.get_or_404(cupcake_id)

  flavor = request.json["flavor"]
  size = request.json["size"]
  rating = request.json["rating"]
  image = request.json["image"] or None

  cupcake.flavor = flavor
  cupcake.size = size
  cupcake.rating = rating
  cupcake.image = image

  db.session.commit()

  serialized = cupcake.serialize()

  return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
  """Delete cupcake."""

  cupcake = Cupcake.query.get_or_404(cupcake_id)
  db.session.delete(cupcake)
  db.session.commit()

  return (jsonify(message = "Deleted"), 200)


@app.route("/")
def display_home():
    """Display homepage with list of cupcakes and form to add new cupcake"""

    return render_template("homepage.html")

#/api/cupcakes/search
#cupcakes = Cupcake.query.filter(Cupcake.flavor.like(search_flavor)).all()
