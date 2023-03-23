import React from "react";

const FlatsList = (props) => {
    // console.log(props)
    return (
        <a href={`/${props.flat.id}`} className="flat-container">
            <div className="flat-title subtitle_font-style">{props.flat.title}</div>
            <a href={props.flat.link} className="flat-link subtitle_font-style">{props.flat.reference}</a>
            <div className="flat-info__items">
                <div className="flat-info__item">Цена: {props.flat.price} BYN</div>
                <div className="flat-info__item">Город: {props.flat.city}</div>
                <div className="flat-info__item">Район: {props.flat.district}</div>
                <div className="flat-info__item">Микрорайон: {props.flat.micro_district}</div>
                <div className="flat-info__item">Количество комнат: {props.flat.rooms_quantity}</div>
                <div className="flat-info__item">Общая площадь: {props.flat.square}</div>

            </div>
        </a>
    );
};

export default FlatsList