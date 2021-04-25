import React, {useEffect, useState, useRef} from 'react';
import ReactDOM from 'react-dom';
import './App.css'
import Products from './components/Products';
import Portfolio from './components/Portfolio';


const App = () => {
    const [products, setProducts] = useState([]);
    const [portfolio, setPortfolio] = useState([]);
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new WebSocket("ws://127.0.0.1:8888/");
        ws.current.onopen = () => console.log("ws opened");
        ws.current.onclose = () => console.log("ws closed");

        return () => {
            ws.current.close();
        };
    }, []);

    useEffect(() => {
        if (!ws.current) return;
        ws.current.onmessage = e => {
            setPortfolio(JSON.parse(e.data)['portfolio']);
            setProducts(JSON.parse(e.data)['products']);
        };
    }, []);

    return (
        <div style={{display: 'grid', gridTemplateColumns: '75% 25%'}}>
            <Products products={products} />
            <Portfolio portfolio={portfolio} />
        </div>
    )
};

ReactDOM.render(
    <App />, 
    document.querySelector('#root')
);