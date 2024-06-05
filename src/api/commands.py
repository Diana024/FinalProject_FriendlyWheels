import click
from api.models import db, User, Vehicle, FavoriteVehicle
"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("fill-db")
    def fill_db():
        """ Este comando rellenará la base de datos con datos de ejemplo. """
        
        db.drop_all()
        db.create_all()

        try:
            users = [
                User(email="cadimain@gmail.com", password="111111"),
                User(email="marta@gmail.com", password="222222"),
                User(email="ines@gmail.com", password="333333"),
                User(email="carmelo@gmail.com", password="444444"),
                User(email="diana@gmail.com", password="555555"),
            ]
            db.session.add_all(users)
            db.session.commit()
            
            vehicles = [
                Vehicle(marca_modelo="AUDI A3",
                        matricula="1234HPW", 
                        motor="Hibrido", 
                        tipo_cambio= "Automatico", 
                        asientos=5, 
                        precio= 50,
                        user_id= users[0].id, 
                        precio_id_stripe= "price_1POJpyBy1Y4Nz1On2xEWPeTL",
                        producto_id_stripe = "0",
                        url_img1= "https://prod.pictures.autoscout24.net/listing-images/ecade580-ca4e-44ca-bf97-22060506b48a_dd9be07f-a887-4b28-aded-f07a5acb5159.jpg/720x540.webp",
                        url_img2= "https://prod.pictures.autoscout24.net/listing-images/ecade580-ca4e-44ca-bf97-22060506b48a_837ede51-3651-4ea4-bebb-81c531534541.jpg/720x540.webp",
                        url_img3= "https://prod.pictures.autoscout24.net/listing-images/ecade580-ca4e-44ca-bf97-22060506b48a_7aa273df-b678-41dd-8aa6-55766095f6b4.jpg/720x540.webp"
                    ),

                Vehicle(marca_modelo="TOYOTA AURIS",
                        matricula="1834ABC", 
                        motor="Gasolina", 
                        tipo_cambio= "Manual", 
                        asientos=5, 
                        precio= 55,
                        user_id= users[0].id, 
                        precio_id_stripe= "price_1POJqsBy1Y4Nz1OndJu7dcEn",
                        producto_id_stripe = "0",
                        url_img1= "https://prod.pictures.autoscout24.net/listing-images/7649d4fe-2bc9-4709-bb74-9a67af815cf0_f8c352b2-f659-4b26-b101-abe4c8079440.jpg/720x540.webp",
                        url_img2= "https://prod.pictures.autoscout24.net/listing-images/7649d4fe-2bc9-4709-bb74-9a67af815cf0_9c14e1f4-6da7-418f-9fbb-f488330c70db.jpg/720x540.webp",
                        url_img3= "https://prod.pictures.autoscout24.net/listing-images/7649d4fe-2bc9-4709-bb74-9a67af815cf0_5a7ac744-18d1-4844-8d64-4e7bfc5569f2.jpg/720x540.webp"
                    ),

                Vehicle(marca_modelo="FIAT 500",
                        matricula="1234ABC", 
                        motor="Diesel", 
                        tipo_cambio= "Manual", 
                        asientos=2, 
                        precio= 30,
                        user_id= users[0].id, 
                        precio_id_stripe= "price_1POJrBBy1Y4Nz1OnuRySxxsK",
                        producto_id_stripe = "0",
                        url_img1= "https://prod.pictures.autoscout24.net/listing-images/9bdef8ca-9258-4522-96c0-5fbaca49e4e4_d9d89502-07c1-466d-a303-cb919f5a06db.jpg/720x540.webp",
                        url_img2= "https://prod.pictures.autoscout24.net/listing-images/9bdef8ca-9258-4522-96c0-5fbaca49e4e4_0e6b3cd2-d095-4e18-93bd-723152911bf7.jpg/720x540.webp",
                        url_img3= "https://prod.pictures.autoscout24.net/listing-images/9bdef8ca-9258-4522-96c0-5fbaca49e4e4_3aa18080-7fce-45f9-93d9-548474ea2904.jpg/720x540.webp"
                    ),

                Vehicle(marca_modelo="TESLA S",
                        matricula="6666DIA", 
                        motor="Electrico", 
                        tipo_cambio= "Automatico", 
                        asientos=4, 
                        precio= 105,
                        user_id= users[0].id, 
                        precio_id_stripe= "price_1POJrTBy1Y4Nz1On4rDgwpmh",
                        producto_id_stripe = "0",
                        url_img1= "https://prod.pictures.autoscout24.net/listing-images/4d108279-6d01-4841-bc62-3c4fbf53ad18_25ad9d38-5565-448b-8513-ce840ad7b042.jpg/720x540.webp",
                        url_img2= "https://prod.pictures.autoscout24.net/listing-images/4d108279-6d01-4841-bc62-3c4fbf53ad18_8daf0b4a-c267-45a6-8365-df49787e3286.jpg/720x540.webp",
                        url_img3= "https://prod.pictures.autoscout24.net/listing-images/4d108279-6d01-4841-bc62-3c4fbf53ad18_76df16ca-deed-453b-a9ad-909f78a34555.jpg/720x540.webp"
                    ),
                
                Vehicle(marca_modelo="CITROEN C5",
                        matricula="4561MAR", 
                        motor="Hibrido", 
                        tipo_cambio= "Manual", 
                        asientos=5, 
                        precio= 60,
                        user_id= users[0].id, 
                        precio_id_stripe= "price_1POJroBy1Y4Nz1OnWMApJmjf",
                        producto_id_stripe = "0", 
                        url_img1= "https://prod.pictures.autoscout24.net/listing-images/ddf48611-f142-4bf8-b89d-5332dad87ab8_4edb25e6-c691-4f9d-9e47-46f12dba100c.jpg/720x540.webp",
                        url_img2= "https://prod.pictures.autoscout24.net/listing-images/ddf48611-f142-4bf8-b89d-5332dad87ab8_1931e889-0bd6-49ef-9f01-64c13eabe809.jpg/720x540.webp",
                        url_img3= "https://prod.pictures.autoscout24.net/listing-images/ddf48611-f142-4bf8-b89d-5332dad87ab8_0f22a46e-b069-41fb-92f4-220e12a88e17.jpg/720x540.webp"
                    ),

                Vehicle(marca_modelo="MERCEDES VITO",
                        matricula="1818MLK", 
                        motor="Gasolina", 
                        tipo_cambio= "Automatico", 
                        asientos=9, 
                        precio= 120,
                        user_id= users[0].id, 
                        precio_id_stripe= "price_1POJt8By1Y4Nz1OnhWopXgFu",
                        producto_id_stripe = "0", 
                        url_img1= "https://prod.pictures.autoscout24.net/listing-images/4eb68efd-9ed1-407c-b2c5-6df67e95fc60_895fbe2d-bd13-4a92-af56-57d2acba41bb.jpg/720x540.webp",
                        url_img2= "https://prod.pictures.autoscout24.net/listing-images/4eb68efd-9ed1-407c-b2c5-6df67e95fc60_0bfb4e0d-9719-4379-9cd4-fc16f5acac27.jpg/720x540.webp",
                        url_img3= "https://prod.pictures.autoscout24.net/listing-images/4eb68efd-9ed1-407c-b2c5-6df67e95fc60_217b4232-b470-49dc-9a62-10359f3eaa0e.jpg/720x540.webp"
                    ) 
            ]
            db.session.add_all(vehicles)
            db.session.commit()
            
            favoriteVehicle = [
                FavoriteVehicle(user_id=users[0].id, vehicle_id=vehicles[0].id ),
                FavoriteVehicle(user_id=users[0].id, vehicle_id=vehicles[1].id ),
                FavoriteVehicle(user_id=users[0].id, vehicle_id=vehicles[2].id ),
                FavoriteVehicle(user_id=users[0].id, vehicle_id=vehicles[3].id ),
                FavoriteVehicle(user_id=users[0].id, vehicle_id=vehicles[4].id ),
                FavoriteVehicle(user_id=users[0].id, vehicle_id=vehicles[5].id )
                ]
            db.session.add_all(favoriteVehicle)
            db.session.commit()

            print("La base de datos ha sido poblada con datos de ejemplo.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al llenar la base de datos: {e}")