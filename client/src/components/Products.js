import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Products = ({products}) => {
    const renderedProducts = products.sort((a, b) => {
      return parseFloat(b.cash_value) - parseFloat(a.cash_value);
    }).map((product, i) => {
        return (
            <React.Fragment key={product.product_id}>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{product.base_currency}</span> 
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.price)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.balance)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.cash_value)}</span>
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
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(6, 15%)'}}>
            <span style={headerStyle}></span> 
            <span style={headerStyle}>price</span>
            <span style={headerStyle}>balance</span>
            <span style={headerStyle}>value</span>
            <span style={headerStyle}>difference %</span>
            {renderedProducts}
        </div>
    );
};

export default Products;