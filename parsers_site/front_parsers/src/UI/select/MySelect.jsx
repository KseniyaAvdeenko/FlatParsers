import React from "react";

const MySelect = ({options, defaultValue, value, onChange}) => {
    return (
        <select
            name="sorting"
            className="selection sort-selection"
            value={value}
            onChange={event => onChange(event.target.value)}
        >
            <option disabled selected value="sorting" className="selection__item">{defaultValue}</option>
            {options.map(option =>
                <option className="selection__item" value={option.value} key={option.value}>
                    {option.name}
                </option>
            )}
        </select>
    );
};

export default MySelect