import React from "react";
import sort_icon from "../img/sort.png";
import MySelect from "../UI/select/MySelect";
import search_icon from "../img/search.png";
import MyInput from "../UI/input/MyInput";


const FlatFilter = ({filter, setFilter}) => {
    return (
        <div>
            <div className="sorting sorting_border">
                <div className="side-bar__items-container">
                    <div className="sorting-icon">
                        <img src={sort_icon} alt="" className="sorting-icon__img"/>
                    </div>
                    <div className="sorting-selection">
                        <MySelect
                            value={filter.sort}
                            className="selection sort-selection"
                            onChange={selectedSort => setFilter({...filter, sort: selectedSort})}
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
                            value={filter.search}
                            onChange={e => setFilter({...filter, search: e.target.value})}
                            type="text"
                            className="search"
                            placeholder='Поиск'/>
                    </div>
                </div>
            </div>
            {/*<div className="filter">*/}
            {/*    <div className="filtered-search">*/}
            {/*        <div className="side-bar__items-container">*/}
            {/*            <div className="filter-icon">*/}
            {/*                <img src={filter_icon} alt="" className="filter-icon__img"/>*/}
            {/*            </div>*/}
            {/*            <p className="filter-params">Поиск по параметрам</p>*/}
            {/*        </div>*/}
            {/*        <div className="filter-search__form">*/}
            {/*            <div className="side-bar__items-container">*/}
            {/*                <div className="form">*/}
            {/*                    <MySelect*/}
            {/*                        value={filter.sort}*/}
            {/*                        className="selection selection__item"*/}
            {/*                        onChange={selectedSort => setFilter({...filter, sort: selectedSort})}*/}
            {/*                        defaultValue="Выберите город"*/}
            {/*                        options={[*/}
            {/*                            {value: 'city', name: 'г.Минск'},*/}
            {/*                            {value: 'city', name: 'г.Брест'},*/}
            {/*                            {value: 'city', name: "г.Могилев"},*/}
            {/*                            {value: 'city', name: "г.Гродно"},*/}
            {/*                            {value: 'update_date', name: "г.Гомель"},*/}
            {/*                            {value: 'update_date', name: "г.Витебск"}*/}
            {/*                        ]}*/}
            {/*                    />*/}
            {/*                    /!*<select name="" id="" className="selection selection__item">*!/*/}
            {/*                    /!*    <option value="">Выберите город</option>*!/*/}
            {/*                    /!*</select>*!/*/}
            {/*                    <select name="" id="" className="selection selection__item">*/}
            {/*                        <option value="">Выберите район</option>*/}
            {/*                    </select>*/}
            {/*                    <select name="" id="" className="selection selection__item">*/}
            {/*                        <option value="">Выберите микрорайон</option>*/}
            {/*                    </select>*/}
            {/*                    <div className="input">*/}
            {/*                        <label htmlFor="rooms">Количество комнат</label>*/}
            {/*                        <MyInput id="rooms" type="number" className="input__select"/>*/}
            {/*                    </div>*/}
            {/*                </div>*/}
            {/*            </div>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*</div>*/}
        </div>
    )
        ;
};

export default FlatFilter