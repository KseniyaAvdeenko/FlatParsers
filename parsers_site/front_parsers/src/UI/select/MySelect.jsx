import React from "react";

const MySelect = ({options, defaultValue, value, onChange, className}) => {
    return (
        <select
            className={className}
            name="sorting"
            value={value}
            onChange={event => onChange(event.target.value)}
        >
            <option disabled selected value="sorting" className="selection__item">{defaultValue}</option>
            {options.map(option =>
                <option
                    className="selection__item"
                    value={option.value}
                    key={option.name}
                >
                    {option.name}
                </option>
            )}
        </select>
    );
};

export default MySelect