import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Portfolio = ({portfolio}) => {
    console.log(portfolio)
    return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
            <span style={{marginLeft: 'auto'}}>portfolio balance: {normalizeStringDecimal(portfolio.portfolio_balance)}</span>
            <span style={{marginLeft: 'auto'}}>cash balance: {normalizeStringDecimal(portfolio.cash_balance)}</span>
            <span style={{marginLeft: 'auto'}}>market %: {normalizeStringDecimal(portfolio.market_delta)}</span>
            <span style={{marginLeft: 'auto'}}>portfolio %: {normalizeStringDecimal(portfolio.balance_delta)}</span>
            <span style={{marginLeft: 'auto', 'color': 'green'}}>{portfolio.balancing === true ? 'balancing' : ''}</span>
        </div>
    );
};

export default Portfolio;