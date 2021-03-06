from flask import Flask, json, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId
import string

app = Flask(__name__)

#make connection
client = MongoClient( "mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

# ------- main functions of the api ------- 

#BUSINESSES
#all
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

#one
@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    if len(id) != 24 or not all(c in string.hexdigits for c in id): #checking if hexdigit as mongo used 24 character id's
        return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch
    
    business = businesses.find_one({'_id':ObjectId(id)})
    if business is not None:
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review['_id'] = str(review['_id'])
        return make_response(jsonify(business), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch

#add
@app.route("/api/v1.0/businesses", methods=["POST"])
def add_businesses():
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        new_business = {
            "name": request.form["name"],
            "town": request.form["town"],
            "rating": request.form["rating"],
            "reviews": [],
        }
        new_business_id = businesses.insert_one(new_business) #insertion
        new_business_link = "http://localhost:5000/api/v1.0/businesses/" + str(new_business_id.inserted_id)
        return make_response(jsonify({"url": new_business_link}), 201)
    else:
        return make_response(jsonify({"error": "Missing form data"}, 404)) #catch

#update
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if "name" in request.form and "town" in request.form and "rating" in request.form: #check
        result = businesses.update_one( \
            { "_id": ObjectId(id)},{
            "$set": { "name": request.form["name"],
                     "town": request.form["town"],
                     "rating": request.form["rating"]
                     } #update where
            })
        if result.matched_count == 1: #if true
            edited_business_link = "http://localhost:5000/api/v1.0/businesses/" + id
            return make_response(jsonify(
                { "url": edited_business_link } ), 200) 
        else:
            return make_response(jsonify(
                { "error": "Invalid business ID" } ), 404) #catch
    else:
        return make_response(jsonify(
            { "error": "Missing form data"} ), 404) #catch
        
#delete
@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    result = businesses.delete_one( { "_id" : ObjectId(id) } )
    if result.deleted_count == 1:
        return make_response(jsonify( {} ), 204)
    else:
        return make_response(jsonify( { "error": "Invalid business ID"} ), 404)
    

#REVIEWS
#add
@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["POST"])
def add_new_review(id):
    if len(id) != 24 or not all(c in string.hexdigits for c in id): #checking if hexdigit as mongo used 24 character id's
        return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch
    
    new_review = {
        "_id": ObjectId(),
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"]
    }
    businesses.update_one( { "_id": ObjectId(id) }, \
        {"$push": {"reviews": new_review } } )
    new_review_link = "http://localhost:5000/api/v1.0/businesses/" + id + "/reviews/" + str(new_review['_id'])
    return make_response(jsonify( { "url" : new_review_link } ), 201)

#get all
@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    
    if len(id) != 24 or not all(c in string.hexdigits for c in id): #checking if hexdigit as mongo used 24 character id's
       return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch
    
    data_to_return = []
    business = businesses.find_one( \
        { "_id": ObjectId(id) },
        { "reviews": 1, "_id" : 0 } )
    for review in business["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)
    return make_response(jsonify( data_to_return ), 200)

#one review
@app.route("/api/v1.0/businesses/<bid>/reviews/<rid>", methods=["GET"])
def fetch_one_review(bid, rid):
    if len(bid) != 24 or not all(c in string.hexdigits for c in bid): #checking if bid is appropriate
       return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch
    if len(rid) != 24 or not all(c in string.hexdigits for c in rid): #checking if bid is appropriate
       return make_response(jsonify({"error": "Invalid review ID"}), 404) #catch
    
    #check if the business part exists
    business = businesses.find_one({'_id':ObjectId(bid)}) #check for business id
    if business is None:
        return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch. 404 used to signify missing resource. Rest not needed
    
    #check if the review part exists
    review = businesses.find_one( 
        { "reviews._id" : ObjectId(rid) }, #ccheck for review id
        { "_id" : 0, "reviews.$": 1 } )
    if review is None:
        return make_response( jsonify( {"error": "Invalid review ID"}), 404) #backup catch
    
    review['reviews'][0]['_id'] = str(review['reviews'][0]['_id'])
    
    return make_response(jsonify(review['reviews'][0]), 200)

#edit review
@app.route("/api/v1.0/businesses/<bid>/reviews/<rid>", methods=["PUT"])
def edit_review(bid, rid):
    if len(bid) != 24 or not all(c in string.hexdigits for c in bid): #checking if bid is appropriate
       return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch
    if len(rid) != 24 or not all(c in string.hexdigits for c in rid): #checking if bid is appropriate
       return make_response(jsonify({"error": "Invalid review ID"}), 404) #catch
   
    #check if the business part exists
    business = businesses.find_one({'_id':ObjectId(bid)}) #check for business id
    if business is None:
        return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch. 404 used to signify missing resource. Rest not needed
   
   #check if the review part exists
    review = businesses.find_one( 
        { "reviews._id" : ObjectId(rid) }, #check for review id
        { "_id" : 0, "reviews.$": 1 } )
    if review is None:
        return make_response( jsonify( {"error": "Invalid review ID"}), 404) #backup catch
    
    if "username" in request.form and "comment" in request.form and "stars" in request.form: #check
        edited_review = {
            "reviews.$.username" : request.form["username"],
            "reviews.$.comment" : request.form["comment"],
            "reviews.$.stars" : request.form["stars"]
        }
        businesses.update_one(
            { "reviews._id" : ObjectId(rid) },
            { "$set" : edited_review }
        )
        edited_review_url = "http://localhost:5000/api/v1.0/businesses/" + bid + "/reviews/" + rid
        return make_response(jsonify( {"url": edited_review_url } ), 200) #success
    else: 
        return make_response(jsonify(
            { "error": "Missing form data"} ), 404) #catch


#delete review
@app.route("/api/v1.0/businesses/<bid>/reviews/<rid>", methods=["DELETE"])
def delete_review(bid, rid):
    if len(bid) != 24 or not all(c in string.hexdigits for c in bid): #checking if bid is appropriate
       return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch
    if len(rid) != 24 or not all(c in string.hexdigits for c in rid): #checking if bid is appropriate
       return make_response(jsonify({"error": "Invalid review ID"}), 404) #catch
   
   #check if the business part exists
    business = businesses.find_one({'_id':ObjectId(bid)}) #check for business id
    if business is None:
        return make_response(jsonify({"error": "Invalid business ID"}), 404) #catch. 404 used to signify missing resource. Rest not needed
   
    #check if the review part exists
    review = businesses.find_one( 
        { "reviews._id" : ObjectId(rid) }, #check for review id
        { "_id" : 0, "reviews.$": 1 } )
    if review is None:
        return make_response( jsonify( {"error": "Invalid review ID"}), 404) #backup catch
   
    businesses.update_one(
        { "_id" : ObjectId(bid) },
        { "$pull" : { "reviews" : { "_id" : ObjectId(rid) } } }  
    )
    return make_response(jsonify( {} ), 204)#delete

if __name__ == "__main__":
    app.run( debug = True) #run as python default