CREATE KEYSPACE IF NOT EXISTS stocktracker
WITH replication = {
    'class': 'SimpleStrategy', 
    'replication_factor': 1  -- Adjust based on your cluster setup
};

USE stocktracker;

CREATE TABLE IF NOT EXISTS tracker ( 
    tickerName text, 
    openPrice float, 
    high float, 
    low float, 
    closePrice float, 
    volume text, 
    recommendationKey text, 
    fiftyDayAverage float, 
    trackTime timestamp, 
    PRIMARY KEY ((tickerName),trackTime) 
    ) WITH CLUSTERING ORDER BY (trackTime DESC);
