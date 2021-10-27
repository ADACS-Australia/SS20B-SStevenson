import React from 'react';

export const ShowcaseButton = (props) => {
    const {onClick, buttonContent} = props;

    return (
        <button onClick={onClick}>
            {buttonContent}
        </button>
    )
};