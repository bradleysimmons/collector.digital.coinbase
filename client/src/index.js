import React, {useEffect, useState, useRef} from 'react';
import ReactDOM from 'react-dom';
import './App.css'
import Portfolio from './components/Portfolio';


const App = () => {
    const [products, setProducts] = useState([]);
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
            setProducts(JSON.parse(e.data));
        };
    }, []);

    return (
        <div>
            <Portfolio products={products} />
        </div>
    )
};

ReactDOM.render(
    <App />, 
    document.querySelector('#root')
);