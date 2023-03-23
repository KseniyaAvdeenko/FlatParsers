import React from "react";
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";

const Form = () => {
    return (
        <form className="form">
            <select name="" id="" className="selection selection__item">
                <option value="">Выберите город</option>
            </select>
            <select name="" id="" className="selection selection__item">
                <option value="">Выберите район</option>
            </select>
            <select name="" id="" className="selection selection__item">
                <option value="">Выберите микрорайон</option>
            </select>
            <div className="input">
                <label htmlFor="rooms">Количество комнат</label>
                <MyInput id="rooms" type="number" className="input__select"/>
            </div>
            <MyButton>Найти</MyButton>
        </form>
    );
};

export default Form