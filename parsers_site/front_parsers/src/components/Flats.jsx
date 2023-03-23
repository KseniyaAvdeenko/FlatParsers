import FlatService from "./FlatService";
import React, {useEffect, useMemo, useState} from "react";
import sort_icon from "../img/sort.png";
import filter_icon from "../img/filter.png";
import search_icon from "../img/search.png"
import MyInput from "../UI/input/MyInput";
import Form from "./Form";
import FlatsList from "./FlatsList";
import MySelect from "../UI/select/MySelect";
import FlatFilter from "./FlatFilter";
import MyButton from "../UI/button/MyButton";


const flatService = new FlatService()

export default function Flats() {

    const [flats, setFlats] = useState([])

    useEffect(() => {
        flatService.getFlats().then(function (result) {
            setFlats(result);
        })
    },);
    const [filter, setFilter] = useState({sort: '', search: ''})

    const sortedFlats = useMemo(() => {
        if (filter.sort) {
            function Sorting(fl) {
                if (fl.find(x => [filter.sort] !== 'number'))
                    return [...flats].sort((a, b) => a[filter.sort].localeCompare(b[filter.sort]))
                else
                    return [...flats].sort((a, b) => a[filter.sort] - b[filter.sort])
            };
            return Sorting(flats)
        }
        ;
        return flats;
    }, [filter.sort, flats])


    const sortedAndSearchedFlats = useMemo(() => {
        return sortedFlats.filter(flat => flat.title.toLowerCase().includes(filter.search))
    }, [filter.search, sortedFlats])


    return (
        <div className="content">
            <div className="intro intro_size intro_color ">
                <div className="flex-container">
                    <h1 className="title title_font-style">Добро пожаловать в инфоцентр</h1>
                    <h4 className="subtitle subtitle_font-style">Мы собрали квартиры с 2х самых популяных
                        источников <b>realt.by</b> и <b>gohome.by</b> по поиску квартир</h4>
                </div>
            </div>
            <section className="main-container">
                <div className="flex-container">
                    <aside className="side-bar side-bar_bg-color">
                        <FlatFilter filter={filter} setFilter={setFilter}/>
                        <div className="filter">
                            <div className="filtered-search">
                                <div className="side-bar__items-container">
                                    <div className="filter-icon">
                                        <img src={filter_icon} alt="" className="filter-icon__img"/>
                                    </div>
                                    <p className="filter-params">Поиск по параметрам</p>
                                </div>
                                <div className="filter-search__form">
                                    <div className="side-bar__items-container">
                                        <div className="form">

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
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </aside>
                    <main className="main-content">
                        {sortedAndSearchedFlats.length > 0
                            ? <div>{sortedAndSearchedFlats.map((flat) => <FlatsList key={flat.id} flat={flat}/>)}</div>
                            : <h4 className="subtitle subtitle_font-style">Квартиры не найдены</h4>
                        }
                    </main>
                </div>
            </section>
        </div>

    );
};

