import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Portfolio = ({portfolio}) => {
    console.log(portfolio)
    return (
        <div>
            <span style={{alignText: 'right'}}>cash value: {normalizeStringDecimal(portfolio.cash_value)}</span><br/>
            <span style={{alignText: 'right'}}>cash balance: {normalizeStringDecimal(portfolio.cash_balance)}</span>
        </div>
    );
};

export default Portfolio;