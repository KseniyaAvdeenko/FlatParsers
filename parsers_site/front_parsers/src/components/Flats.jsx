import FlatService from "./FlatService";
import React, {useEffect, useMemo, useState} from "react";
import sort_icon from "../img/sort.png";
import filter_icon from "../img/filter.png";
import search_icon from "../img/search.png"
import MyInput from "../UI/input/MyInput";
import Form from "./Form";
import FlatsList from "./FlatsList";
import MySelect from "../UI/select/MySelect";


const flatService = new FlatService()

export default function Flats() {

    const [flats, setFlats] = useState([])

    useEffect(() => {
        flatService.getFlats().then(function (result) {
            setFlats(result);
        })
    },);
    const [search, setSearch] = useState('')
    const [selectedSort, setSelectedSort] = useState('')

    const sortedFlats = useMemo(() => {
        if (selectedSort) {
            return [...flats].sort((a, b) => b[selectedSort] - a[selectedSort])
        };
        return flats;
    }, [selectedSort, flats])

     const sortedAndSearchedFlats = useMemo(() => {
        return sortedFlats.filter(flat => flat.title.toLowerCase().includes(search))
    }, [search, sortedFlats])

    const sortFlats = (sort) => {
        setSelectedSort(sort);
    }



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
                        <div className="sorting sorting_border">
                            <div className="side-bar__items-container">
                                <div className="sorting-icon">
                                    <img src={sort_icon} alt="" className="sorting-icon__img"/>
                                </div>
                                <div className="sorting-selection">
                                    <MySelect
                                        value={selectedSort}
                                        onChange={sortFlats}
                                        defaultValue="Сортировка по:"
                                        options={[
                                            {value: 'price', name: 'По цене (сначала дешевые)'},
                                            // {value: 'price', name: 'По цене (сначала дорогие)'},
                                            {value: 'square', name: "По площади(сначала маленькие)"},
                                            // {value: 'square', name: "По площади(сначала большие)"},
                                            {value: 'update_date', name: "По дате обновления(сначала новые)"},
                                            // {value: 'update_date', name: "По дате обновления(сначала старые)"}
                                        ]}
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="searching sorting_border">
                            <div className="side-bar__items-container">
                                <div className="sorting-icon">
                                    <img src={search_icon} alt="" className="sorting-icon__img"/>
                                </div>
                                <div className="search-input">
                                    <MyInput
                                        value={search}
                                        onChange={e => setSearch(e.target.value)}
                                        type="text"
                                        className="search"
                                        placeholder='Поиск'/>
                                </div>
                            </div>
                        </div>
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
                                        <Form/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </aside>
                    <main className="main-content">
                        {sortedAndSearchedFlats.length > 0
                            ? <div>{sortedAndSearchedFlats.map((flat) => <FlatsList key={flat.id} flat={flat}/>)}</div>
                            :<h4 className="subtitle subtitle_font-style">Квартиры не найдены</h4>
                        }
                    </main>
                </div>
            </section>
        </div>

    );
};

