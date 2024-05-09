"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Vehicle, FavoriteVehicle, MyVehicleInRent
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager 

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_exist = User.query.filter_by(email=email).first()
    if email is "" or password is "":
        return jsonify({"msg": "Email and password are required"}), 400
    if user_exist is None: 
        new_user = User(
            email=email, 
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "User has already exist"}), 400
      
@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_exist = User.query.filter_by(email=email).first()
    if user_exist is None:
        return jsonify({"msg": "Email doesn't exist"}), 404
    if email != user_exist.email or password != user_exist.password:
        return jsonify({"msg": "Bad email or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token),200
  
@api.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    all_vehicles_list = list(map(lambda item:item.serialize(), all_vehicles))
    if all_vehicles_list == []:
        return jsonify({"msg":"Vehicles not found"}), 404
    response_body = {
        "msg": "ok",
        "results": all_vehicles_list
    }
    return jsonify(response_body), 200  
  
@api.route('/rent/vehicle/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle_in_rent(vehicle_id):
    email = get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    vehicle_exist = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_exist is None:
        return jsonify({"msg": "This vehicle doesn't exist"}), 400
    else:
        rent_vehicle_to_delete = MyVehicleInRent.query.filter_by(vehicle_id=vehicle_id, user_id=user_id).first()
        if rent_vehicle_to_delete:
            db.session.delete(rent_vehicle_to_delete)
            db.session.commit()
            return jsonify({"msg": "Vehicle deleted to rent"}), 200
        else:  
            return ({"msg": "This vehicle doesn't exist in rent"}), 400
 