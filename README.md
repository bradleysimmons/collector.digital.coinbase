# collector.digital.coinbase

this is a program to trade in the coinbase pro exchange using the api.

the program connects to the coinbase pro websocket for market data,
and also opens a websocket, which feeds a web client with real-time information.

the program uses a threshold balancing strategy, 
where the products in the portfolio are balanced evenly as the market changes.

the mean cash value is calculated, and the program buys or sells products
when their percent difference from the mean cash value is outside of the threshold.

this program is fun because there is no need to keep an order book or make predictions.
all of the events are triggered from the ticker websocket.  when a new price comes in, decisions are made.
