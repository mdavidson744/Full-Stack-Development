from flask import Flask, make_response, jsonify, request
import uuid, random
import jwt
import datetime
from functools import wraps
import pymongo
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB #database
businesses = db.biz #collection

app.config['SECRET_KEY'] = 'mysecret'

@app.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode(
            {'user' : auth.username,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token' : token})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})


def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyayIsImV4cCI6MTYzODc0NzQwOX0.-uQz7SkGR3fDWulqmi_KI88qGHBSJDV-DHzqWWaqTk0'
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify( {'message' : 'Token is missing'} ), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify( {'message' : 'Token is invalid'}), 401
        
        return func(*args, **kwargs)
    
    return jwt_required_wrapper




@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get('pn'))
    if request.args.get("ps"):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    
    data_to_return = []
    for business in businesses.find().skip(page_start).limit(page_size):
        business["_id"] = str(business["_id"])
        for review in business["reviews"]:
            review["_id"] = str(review["_id"])
        data_to_return.append(business)
    
    return make_response(jsonify(data_to_return), 200)

@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
@jwt_required
def show_one_business(id):
    business = businesses.find_one({'_id': ObjectId(id)})
    if business is not None:
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review['_id'] = str(review['_id'])
        for tip in business['tips']:
            tip['_id'] = str(tip['_id'])
        return make_response(jsonify(business), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
# TODO validate rating is between 1 and 5 int
@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        next_id = str(uuid.uuid1())
        new_business = {
            "name": request.form["name"],
            "town": request.form["town"],
            "rating": request.form["rating"],
            "reviews": {},
        }
        businesses[next_id] = new_business
        return make_response(jsonify({next_id: new_business}), 201)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)


# TODO update the only fields that need changed, eg only change rating and not everything else
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response(jsonify({"error": "Invalid bussines ID"}), 404)
    else:
        if "name" in request.form and "town" in request.form and "rating" in request.form:
            businesses[id]["name"] = request.form["name"]
            businesses[id]["town"] = request.form["town"]
            businesses[id]["rating"] = request.form["rating"]

            return make_response(jsonify({businesses[id]}), 200)
        else:
            return make_response(jsonify({"error": "Missing form data"}), 404)


@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    if id in businesses:
        del businesses[id]
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid bussines ID"}), 404)


@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    if id in businesses:
        return make_response(jsonify(businesses[id]["reviews"]), 200)
    else:
        return make_response(jsonify({"error": "Invalid bussiness ID"}), 404)


@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["POST"])
def add_new_review(id):
    if "username" in request.form and "comment" in request.form and "stars" in request.form:
        next_id = str(uuid.uuid1())
        new_review = {
            "username": request.form["username"],
            "comment": request.form["comment"],
            "stars": request.form["stars"]
        }
        businesses[id]["reviews"][next_id] = new_review

        return make_response(jsonify({next_id: new_review}), 201)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)


@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    if b_id in businesses:
        if r_id in businesses[b_id]["reviews"]:
            return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid bussiness ID"}), 404)


@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    if b_id in businesses:
        if r_id in businesses[b_id]["reviews"]:
            if "username" in request.form and "comment" in request.form and "stars" in request.form:
                new_review = {
                    "username": request.form["username"],
                    "comment": request.form["comment"],
                    "stars": request.form["stars"]
                }
                businesses[b_id]["reviews"][r_id] = new_review

                return make_response(jsonify({r_id: new_review}), 200)
            else:
                return make_response(jsonify({"error": "Missing form data"}), 404)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid bussiness ID"}), 404)




@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    if b_id in businesses:
        if r_id in businesses[b_id]["reviews"]:
            del businesses[b_id]["reviews"][r_id]
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid bussiness ID"}), 404)


def generate_dummy_data():
    towns = ['colerain', 'Banbridge', 'Belfast', 'Lisburn', 'LondonDerry', 'Newry', 'Enniskillen', 'Omagh', 'Ballymena']
    businesses_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "biz " + str(i)
        town = towns[random.randint(0, len(towns) - 1)]
        rating = random.randint(1, 5)
        businesses_dict[id] = {
            "id" : id,
            "name": name,
            "town": town,
            "rating": rating,
            "reviews": {}
        }
    return businesses_dict



# [
#     {
#         "id": str(uuid.uuid1()),
#         "name": "piiza Mountain",
#         "town": "Colerain",
#         "rating": 5,
#         "reviews": []
#     },
#     {
#         "id": 2,
#         "name": "Wine Lake",
#         "town": "Ballymoney",
#         "rating": 3,
#         "reviews": []
#     },
#     {
#         "id": 3,
#         "name": "Sweet Desert",
#         "town": "Ballymena",
#         "rating": 4,
#         "reviews": []
#     }
# ]

if __name__ == "__main__":
    app.run(debug=True)