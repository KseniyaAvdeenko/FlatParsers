import React, {useEffect, useState} from "react";
import FlatService from "./FlatService";
import {Link, useParams} from "react-router-dom";

const flatService = new FlatService()

export default function Flat() {
    const [flat, setFlat] = useState([])
    const {flat_id} = useParams();


    useEffect(() => {
        flatService.getFlat(flat_id).then(function (result) {
            setFlat(result);
        })
    }, [flat_id]);


    const date = flat.update_date || "";
    const editDate = date?.slice(8, 10) + '.' + date?.slice(5, 7) + '.' + date?.slice(0,4)

    const photos = flat.photo_links || ""
    const splitedPhotos = photos?.split(",")
    // const readyPhotos = splitedPhotos?.slice(0,4)
    const readyPhotos = splitedPhotos



    // console.log(photos)
    return(
        <main className="main-content">
            <div className="flex-container"><Link className="back-link" to="/" >&#8656; Вернуться на главную страницу</Link></div>
            <div className="flex-container">
                <div className="flat-container">
                <div className="flat-title subtitle_font-style">{flat.title}</div>
                <hr color='#261F18' size="1" width="100%" align="left"/>
                <div className="flat-info__items">
                    <a href={flat.link} className="flat-link flat-info__item">Ссылка на источник: {flat.reference}</a>
                    <div className="flat-info__item">Дата обновления: {editDate}</div>
                    <div className="flat-info__item">Цена: {flat.price} BYN</div>
                    <div className="flat-info__item">Цена за метр: {flat.price_for_meter} BYN</div>
                    <div className="flat-info__item">Общая площадь: {flat.square} кв. м.</div>
                    <div className="flat-info__item">Общая площадь: {flat.house_year}</div>
                    <div className="flat-info__item">Количество комнат: {flat.rooms_quantity}</div>
                </div>
                <hr color='#261F18' size="1" width="100%" align="left"/>
                <div className="flat-info__items">
                    <div className="flat-info__item">Город: {flat.city}</div>
                    <div className="flat-info__item">Район: {flat.district}</div>
                    <div className="flat-info__item">Микрорайон: {flat.micro_district}</div>
                    <div className="flat-info__item">Адрес: {flat.street} {flat.house_number}</div>
                    <div className="flat-info__item">Номер продавца: {flat.seller_phone}</div>
                </div>
                <hr color='#261F18' size="1" width="100%" align="left"/>
                <div className="flat-photo__items ">
                    {readyPhotos.map((photo) => <img src={photo} alt="" width="290" height="300" className='flat-photo__item'/>)}
                </div>
                <hr color='#261F18' size="1" width="100%" align="left"/>
                <p className="flat-description">
                    <span className="flat-description flat-info__item">
                        Описание: </span>
                    {flat.description}
                </p>
            </div>
            </div>
        </main>
    )
};


