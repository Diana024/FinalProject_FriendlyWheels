from flask import Flask, request, jsonify, url_for, Blueprint, redirect
from api.models import db, User, Vehicle, FavoriteVehicle
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager  # type: ignore
import stripe
import os


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_exist = User.query.filter_by(email=email).first()
    if email == "" or password == "":
        return jsonify({"msg": "El email y password son obligatorios"}), 400
    if user_exist is None:
        new_user = User(
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 201
    else:
        return jsonify({"msg": "El usuario ya existe"}), 409
    
@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_exist = User.query.filter_by(email=email).first()
    if email == "" or password == "":
        return jsonify({"msg": "Todos los campos son obligatorios"}), 400
    if email != user_exist.email or password != user_exist.password:
        return jsonify({"msg": "El email o password no son correctos"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token),200

@api.route('/vehicle', methods=['POST'])
@jwt_required()
def add_vehicle():
    email = get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    marca_modelo = request.json.get("marca_modelo")
    matricula = request.json.get("matricula")
    motor = request.json.get("motor")
    tipo_cambio = request.json.get("tipo_cambio")
    asientos = request.json.get("asientos")
    precio = request.json.get("precio")
    if (marca_modelo == "" or matricula == "" or motor == "" or tipo_cambio == "" or asientos == "" or precio == ""):
        return jsonify({"msg": "Todos los campos son obligatorios."}), 400
    existing_vehicle = Vehicle.query.filter_by(matricula=matricula).first()
    if existing_vehicle:
        return jsonify({"msg": "El vehículo con esta matrícula ya existe"}), 409
    new_vehicle = Vehicle(
        marca_modelo=marca_modelo,
        matricula=matricula,
        motor=motor,
        tipo_cambio=tipo_cambio,
        asientos=asientos,
        precio=precio,
        user_id= user_id
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"msg": "El vehículo ha sido creado correctamente"}), 200

@api.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    all_vehicles_list = list(map(lambda item:item.serialize(), all_vehicles))
    if all_vehicles_list == []:
        return jsonify({"msg":"No se han encontrado vehículos"}), 404
    response_body = {
        "msg": "ok",
        "results": all_vehicles_list
    }
    return jsonify(response_body), 200

@api.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg":"El vehículo no existe"}), 404
    return jsonify(vehicle.serialize()), 200

@api.route('vehicle/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    email = get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    vehicle_exist = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_exist is None:
        return jsonify({"msg": "El vehículo no existe"}), 400
    else:
        vehicle_to_delete = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        if vehicle_to_delete:
            db.session.delete(vehicle_to_delete)
            db.session.commit()
            return jsonify({"msg": "Vehículo eliminado correctamente"}), 200
        else:
            return ({"msg": "No puedes eliminar este vehículo, ya que no es un vehiculo propio"}), 400
        
@api.route("/favorite/vehicle/<int:vehicle_id>", methods=["POST"])
@jwt_required()
def create_favorite_vehicle(vehicle_id):
    email = get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    vehicle_exist = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_exist is None:
        return ({"msg": "Este vehículo no existe"}), 400
    else:
        exist_favorite_vehicle = FavoriteVehicle.query.filter_by(vehicle_id=vehicle_id, user_id=user_id).first()
        if exist_favorite_vehicle is None:
            new_favorite_vehicle = FavoriteVehicle(vehicle_id= vehicle_id, user_id=user_id)
            db.session.add(new_favorite_vehicle)
            db.session.commit()
            return jsonify({"msg": "El vehículo se añadió a favoritos"}), 201
        else:
            return jsonify({'msg': 'El vehículo ya lo tienes en favoritos.'}), 400
        
@api.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_all_favorites():
    email =  get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    all_favorites = FavoriteVehicle.query.filter_by(user_id=user_id).all()
    all_favorites_list = list(map(lambda item: item.serialize(), all_favorites))
    if all_favorites_list == []:
        return jsonify({"msg":"No tienes favoritos hasta el momento"}), 404
    response_body = {
        "msg": "ok",
        "results":
            all_favorites_list,
    }
    return jsonify(response_body), 200

@api.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_vehicle(vehicle_id):
    email = get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    vehicle_exist = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_exist is None:
        return jsonify({"msg": "El vehículo no existe"}), 400
    else:
        favorite_vehicle_to_delete = FavoriteVehicle.query.filter_by(vehicle_id=vehicle_id, user_id=user_id).first()
        if favorite_vehicle_to_delete:
            db.session.delete(favorite_vehicle_to_delete)
            db.session.commit()
            return jsonify({"msg": "Vehículo eliminado correctamente de favoritos"}), 200
        else:
            return ({"msg": "El vehículo no existe en favoritos"}), 400
        
@api.route('/user/rent', methods=['GET'])
@jwt_required()
def get_all_rents():
    email =  get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    all_rents = Vehicle.query.filter_by(user_id=user_id).all()
    all_rents_list = list(map(lambda item: item.serialize(), all_rents))
    if all_rents_list == []:
        return jsonify({"msg":"You don't have vehicles in rent"}), 404
    response_body = {
        "msg": "ok",
        "results":
            all_rents_list,
    }
    return jsonify(response_body), 200

#Ruta de pago de stripe

@api.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    price = request.json.get("price", None)
    quantity = request.json.get("quantity", None)
    print(price)
    print(quantity)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': "price_1PHNr401WUGKqP0MAXCQIuq7",
                    'quantity': quantity,
                },

            ],
            mode='payment',
            success_url= os.getenv('BACKEND_URL')+ '?success=true',
            cancel_url= os.getenv('BACKEND_URL') + '?canceled=true',
        )
        # return jsonify("ok"),200
    except Exception as e:
        return str(e)
    # return jsonify("ok"),200
    return redirect(checkout_session.url, code=303)
    # return jsonify(checkout_session.url, code=303)
   
