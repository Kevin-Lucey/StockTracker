Kevin Lucey
Southern Connecticut State University | CSC545
Project - Stock tracker

Project Description
=======
Implement CQRS design pattern for more efficient read and writes to SQL and NoSQL databases 
in a use case where accurate and timely data is important as well as a high throughput of data.


Necessary Libraries
=======
    -yfinance
    -cassandra-driver
    -pandas

Installation & Setup
==========
1. Run Stock-Schema.sql file in MySQL
2. Change connection configuration (password) in MySQLConnection.py 
3. Create or Change a cassandra instance 
        Use cassandra-schema.cql to create the keyspace and table 
4. Run SaveStockSymbols.py file to load all of the stock ticker symbols into the DB
5. Create a topic in Kafka named 'stockevent'

Running the application
==========
1. Run KafkaToCassandra.py in a terminal
2. Run StockTracker.py in a seperate terminal
3. Run AlgorithmicTrader.py in a serperate terminal 
