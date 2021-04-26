import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Products = ({products}) => {
    const renderedProducts = products.sort((a, b) => {
      return parseFloat(b.cash_value_s) - parseFloat(a.cash_value_s);
    }).map((product, i) => {
        return (
            <React.Fragment key={product.id}>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{product.id.replace('-USD', '')}</span> 
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.price)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.balance)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.cash_value_s)}</span>
                <span style={{gridRow: i+2, textAlign: 'right'}}>{normalizeStringDecimal(product.mean_delta)}</span>
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
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(5, 12%)'}}>
            <span style={headerStyle}></span> 
            <span style={headerStyle}>price</span>
            <span style={headerStyle}>balance</span>
            <span style={headerStyle}>value</span>
            <span style={headerStyle}>diff</span>
            {renderedProducts}
        </div>
    );
};

export default Products;