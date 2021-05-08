import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Products = ({products}) => {
    const renderedProducts = products.sort((a, b) => {
      return parseFloat(b.cash_value) - parseFloat(a.cash_value);
    }).map((product, i) => {
        console.log(product.base_currency + ': ' + product.trade_minimum)
        return (
            <React.Fragment key={product.product_id}>

                <span style={{gridRow: i+2, textAlign: 'right'}}>{product.base_currency}</span> 
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.price)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.balance)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.cash_value)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.delta_24h)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.market_delta)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.balance_delta)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.mean_diff)}</span>
            </React.Fragment>
        );
    });

    const headerStyle = {
        gridRow: 1, 
        textAlign: 'right',
        textDecoration: 'underline',
        paddingBottom: '10px'
    }

    return (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(9, 11%)'}}>
            <span style={headerStyle}></span> 
            <span style={headerStyle}>price</span>
            <span style={headerStyle}>balance</span>
            <span style={headerStyle}>value</span>
            <span style={headerStyle}>24h</span>
            <span style={headerStyle}>run %</span>
            <span style={headerStyle}>run bal</span>
            <span style={headerStyle}>relative</span>
            {renderedProducts}
        </div>
    );
};

export default Products;