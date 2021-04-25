import React from 'react';
import {normalizeStringDecimal} from '../helpers.js'

const Portfolio = ({products}) => {
    const renderedProducts = products.map((product, i) => {
        return (
            <React.Fragment>
                <span key={product.id + '1'} style={{gridRow: i, textAlign: 'right'}}>{product.id.replace('-USD', '')}</span> 
                <span key={product.id + '2'} style={{gridRow: i, textAlign: 'right'}}>{normalizeStringDecimal(product.price)}</span>
            </React.Fragment>
        );
    });

    return <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 7%)'}}>{renderedProducts}</div>;
};

export default Portfolio;