import React, {useContext, useEffect} from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";

export const MisCoches = () => {
    const { store, actions } = useContext(Context);

    async function eliminarVehiculo(vehicle_id) {
        let respuesta = await actions.removeVehicle(vehicle_id)
        if (respuesta === "success") {
            swal("Vehículo eliminado correctamente", "", "success")
        }
    }

    useEffect(() => {
		actions.myVehiclesInRent();
	}, []);

    return (
        <>
            <div className="footer-view vehicles mb-5 mt-2 justify-content-center bg-light">
				<div className="container">
                    {store.myVehicles.length === 0 
                        ? (
                            <>
                                <h2 className="mt-3 mb-2 text-success"><strong>MIS COCHES EN ALQUILER</strong></h2>
                                <div className="fs-4 mt-4 mb-3"><strong>Añade tu primer coche a Friendly Wheels</strong></div>
                                <div className="texto-favoritos">Pulsa en el botón añadir que se muestra a continuación para añadir tu primer coche</div>
                                <Link to={`/agregarvehiculo`}>
                                    <div className="mt-3">
                                        <button className="rounded btn-lg btn-success">Añadir mi primer coche</button>
                                    </div>
                                </Link>
                            </>
                        )
                        : (
                            <>
                                <h2 className="mt-3 mb-4 text-success text-center"><strong>MIS COCHES EN ALQUILER</strong></h2>
                                <div className="row text-dark d-flex gap-4 justify-content-center">
                                    {store.myVehicles.map((vehicle) => (
                                        <div key={vehicle.id} className="vehiculo card" style={{ width: "22rem", height: "27rem"}}>
                                                <img className="imagen1" src={vehicle.url_img1} style={{width: "100%", objectFit: "cover", height: "12rem"}} />
                                            <div className="card-body ms-2 p-2">
                                                <h3 className="card-title mb-3 text-success mt-3 mb-3"><strong>{vehicle.marca_modelo.toUpperCase()}</strong></h3>
                                                <p className="card-text fs-5"><strong>Matrícula:</strong> {vehicle.matricula.toUpperCase()}</p>
                                            </div>
                                            <div className="d-flex justify-content-end mt-auto pb-3">
                                                <button onClick={() => eliminarVehiculo(vehicle.id)} className="btn-danger btn-lg border-2 rounded me-3">
                                                    Eliminar
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </>
                        )                           
                    }
                </div>
            </div>     
        </>
    );
};