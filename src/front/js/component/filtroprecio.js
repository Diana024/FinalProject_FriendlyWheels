import React, { useState } from "react";

export const FiltroPrecio = (props) => {

    return (
        <div className="dropdown">
            <button className="btn btn-outline-success border-2 dropdown-toggle bg-white text-secondary" type="button" data-bs-toggle="dropdown" aria-expanded="false">
            Precio por día
            </button>
            <ul className="dropdown-menu ">
                <div className="form-check ms-2">
                    <input onChange={() => props.setFiltroPrecio(null)}  className="form-check-input" type="radio" name="flexRadioDefault1" id="flexRadioDefault5"/>
                    <label className="form-check-label" htmlFor="flexRadioDefault5">
                        Sin Filtro
                    </label>
                </div>
                <div className="form-check ms-2">
                    <input onChange={() => props.setFiltroPrecio({ min: 1, max: 50 })} className="form-check-input" type="radio" name="flexRadioDefault1" id="flexRadioDefault6" />
                    <label className="form-check-label" htmlFor="flexRadioDefault6">
                    1 € - 50 €
                    </label>
                </div>
                <div className="form-check ms-2">
                    <input onChange={() => props.setFiltroPrecio({ min: 50, max: 100 })} className="form-check-input" type="radio" name="flexRadioDefault1" id="flexRadioDefault7"/>
                    <label className="form-check-label" htmlFor="flexRadioDefault7">
                    50 € - 100 €
                    </label>
                </div>
                <div className="form-check ms-2">
                    <input onChange={() => props.setFiltroPrecio({ min: 100, max: Infinity })}  className="form-check-input" type="radio" name="flexRadioDefault1" id="flexRadioDefault8"/>
                    <label className="form-check-label" htmlFor="flexRadioDefault8">
                        Más de 100 €
                    </label>
                </div>
            </ul>
        </div>
    );
};