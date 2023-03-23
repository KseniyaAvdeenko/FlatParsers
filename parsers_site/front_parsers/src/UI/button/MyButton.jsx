import React from "react";

const MyButton = ({children, ...props}) => {
    return (
        <button {...props} className="btn btn_position">
            {children}
        </button>
    );
};

export default MyButton