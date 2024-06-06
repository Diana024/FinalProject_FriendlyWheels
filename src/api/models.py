from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorites_vehicles = db.relationship('FavoriteVehicle', backref='user', lazy=True)
    vehicle = db.relationship('Vehicle', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "email_stripe": self.email_stripe
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    marca_modelo = db.Column(db.String(50), nullable=False)
    matricula = db.Column(db.String(50), nullable=False)
    motor = db.Column(db.String(50), nullable=False)
    tipo_cambio = db.Column(db.String(50), nullable=False)
    asientos = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False)   
    precio_id_stripe = db.Column(db.String(50), nullable=False)
    producto_id_stripe = db.Column(db.String(50), nullable=False)   
    favorites_vehicles = db.relationship('FavoriteVehicle', backref='vehicle', lazy=True)
    url_img1 = db.Column(db.String(300), nullable=True)
    url_img2 = db.Column(db.String(300), nullable=True)
    url_img3 = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f'<Vehicle {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "marca_modelo": self.marca_modelo,
            "matricula": self.matricula,
            "motor": self.motor,
            "tipo_cambio": self.tipo_cambio,
            "asientos": self.asientos,
            "precio": self.precio,
            "user_id": self.user_id,
            "precio_id_stripe": self.precio_id_stripe,
            "producto_id_stripe": self.producto_id_stripe,
            "url_img1" : self.url_img1,
            "url_img2" : self.url_img2,
            "url_img3" : self.url_img3
        }

class FavoriteVehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return f'<FavoriteVehicle {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }
