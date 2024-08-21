/* 
CSC545 project
Database Schema
*/
#drop database StockTracker;
CREATE DATABASE StockTracker;
CREATE DATABASE Portfolio;
use StockTracker;

CREATE TABLE TickerSymbol (
	tickerId INT AUTO_INCREMENT PRIMARY KEY,
	tickerName	VARCHAR(5) NOT NULL
);
CREATE TABLE Tracker (
	trackId int auto_increment primary key,
	tickerName varchar(5) NOT NULL,
    openPrice float(7,2) NOT NULL,
    high float(7,2) NOT NULL,
    low float(7,2) NOT NULL,
    closePrice float(7,2) NOT NULL,
    volume varchar(25) NOT NULL,
    recommendationKey varchar(4) NOT NULL,
    fiftyDayAverage float(7,2) NOT NULL,
    trackTime timestamp NOT NULL
);

select * from Tracker;

#drop database Portfolio;
CREATE DATABASE Portfolio;
use Portfolio;
CREATE TABLE ClientPortfolio (
	portId int auto_increment primary key,
    tickerName varchar(5) NOT NULL,
    price float(7,2) NOT NULL,
    buyTime timestamp NOT NULL
);
select * from ClientPortfolio;

