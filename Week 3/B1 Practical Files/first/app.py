from flask import Flask, make_response, jsonify, request
import uuid, random

app = Flask(__name__)


@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    businesses_list = [ { k : v } for k, v in businesses.items() ]
    data_to_return = businesses_list[ page_start:page_start + page_size]
    return make_response(jsonify(data_to_return), 200)


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


@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    if id in businesses:
        return make_response(jsonify(businesses[id]), 200)
    else:
        return make_response(jsonify({"error": "Invalid bussiness ID"}), 404)


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


businesses = {}
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
    businesses = generate_dummy_data()
    app.run(debug=True)