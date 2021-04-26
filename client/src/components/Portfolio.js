import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Portfolio = ({portfolio}) => {
    return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
            <span style={{marginLeft: 'auto'}}>portfolio balance: {normalizeStringDecimal(portfolio.portfolio_balance)}</span>
            <span style={{marginLeft: 'auto'}}>cash value: {normalizeStringDecimal(portfolio.cash_value)}</span>
            <span style={{marginLeft: 'auto'}}>cash balance: {normalizeStringDecimal(portfolio.cash_balance)}</span>
        </div>
    );
};

export default Portfolio;