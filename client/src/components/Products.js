import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Products = ({products}) => {
    const renderedProducts = products.sort((a, b) => {
      return parseFloat(b.cash_value_s) - parseFloat(a.cash_value_s);
    }).map((product, i) => {
        return (
            <React.Fragment key={product.id}>
                <span style={{gridRow: i+1, textAlign: 'right'}}>{product.id.replace('-USD', '')}</span> 
                <span style={{gridRow: i+1, textAlign: 'right'}}>{normalizeStringDecimal(product.price)}</span>
                <span style={{gridRow: i+1, textAlign: 'right'}}>{normalizeStringDecimal(product.balance)}</span>
                <span style={{gridRow: i+1, textAlign: 'right'}}>{normalizeStringDecimal(product.cash_value_s)}</span>
                <span style={{gridRow: i+1, textAlign: 'right'}}>{normalizeStringDecimal(product.mean_delta)}</span>
            </React.Fragment>
        );
    });

    return <div style={{display: 'grid', gridTemplateColumns: 'repeat(5, 12%)'}}>{renderedProducts}</div>;
};

export default Products;