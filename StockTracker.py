import yfinance as yf 
import json
from confluent_kafka import Producer
from MySQLConnection import Connection
from datetime import datetime
import time
import threading
from StockString import MakeStockList
        
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)), "\n")
    else:
        print("Message produced: %s" % (str(msg)), "\n")


def TrackStockPrice():
    conf = {
            'bootstrap.servers': "localhost:9093",  # Change this to your Kafka server configuration
        }
        # Create Producer instance
    producer = Producer(**conf)

    c = Connection()
    conn, cursor = c.ConnectToMySQL('StockTracker') , c.MakeCursor()

    stockTickers = MakeStockList()
    
    terminated = False

    while not terminated:

        """ Get Ticker object from yfinance API, get stock price history, and latest value in price history"""
        """ Try: see if stock is still listed, if not then catch error Except: continue"""
        
        time.sleep(1)
        try:
            s = yf.Tickers(stockTickers)
            cur_time = datetime.now()
            hist = s.history('1d').iloc[0]
            info = s.info


            data = (
                stockTickers,
                hist['Open'],
                hist['High'],
                hist['Low'],
                hist['Close'],
                hist['Volume'],
                info['recommendationKey'],
                info['fiftyDayAverage'],
                cur_time)

            """Insert into MySQL db and send to Kafka"""
            sql = """
                INSERT INTO Tracker (tickerName, openPrice, high, low, closePrice, volume, recommendationKey, fiftyDayAverage, trackTime) 
                stockTickersUES (%s, %s, %s, %s,%s, %s, %s, %s, %s);
            """
            event = {
                'tickerName': stockTickers,
                'Open': data[1],
                'High': data[2],
                'Low': data[3],
                'Close': data[4],
                'Volume': data[5],
                'recommendationStrategy': data[6],
                'fiftyDayAverage': data[7],
                'timestamp': cur_time.isoformat()
            }
            print(event)
            cursor.execute(sql, data)
            conn.commit()
            producer.produce('stockevent', json.dumps(event).encode('utf-8'), callback= acked)
            producer.flush()
        except Exception as e:
            print("E: ", e)
            continue
                
    cursor.close()



TrackStockPrice()
