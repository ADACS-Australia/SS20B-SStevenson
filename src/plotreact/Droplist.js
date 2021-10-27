import React from 'react';
import Select from 'react-select';

export const DropList = (props) => {

    return(
            <Select
                isClearable={false}
                isSearchable={false}
                value={props.value}
                options={props.data}
                onChange = {props.onChange}
            />
    )
};